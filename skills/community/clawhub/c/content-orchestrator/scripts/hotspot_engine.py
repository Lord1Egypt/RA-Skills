#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热点选题引擎 v2.0 - 统一编排器热点模块(P2-1迁移)

从hotspot_topic_orchestrator.py迁移,LLM调用改用unified_llm统一入口。
流程: 热点加载→LLM选题→素材匹配→降级补充

降级策略(来源:09文档U12): LLM失败→模板选题,素材不足→Pexels/Pixabay补充
LLM统一入口(来源:18_统一入口规则): mcps.shared.unified_llm.llm_chat

来源: 31文档P2-1(合并3个内容编排器) + 09文档U12(热点→选题→素材匹配编排) + 05文档DEF-U30(dotenv自动加载)
"""
import argparse

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import logging

# 修复: 必须在mcps.shared导入前设置sys.path(非lazy文件parents[3]=d:\JueJin)
_PROJECT_ROOT_HE = Path(__file__).resolve().parent.parent.parent.parent
for _p in [str(_PROJECT_ROOT_HE), str(_PROJECT_ROOT_HE / "scripts"), str(_PROJECT_ROOT_HE / "mcps" / "shared")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

from mcps.shared.db_logger import get_logger
logger = get_logger("system", source="skills/content-orchestrator/scripts/hotspot_engine.py")

# 加载.env环境变量(来源:DEF-U30)
try:
    from dotenv import load_dotenv
    _env_path = _PROJECT_ROOT_HE / ".env"
    if _env_path.exists():
        load_dotenv(str(_env_path))
except ImportError as e:
    logger.error(f"[hotspot_engine] dotenv未安装,跳过.env加载: {e}", file=sys.stderr)

# 导入unified_llm(统一LLM入口,来源:18_统一入口规则)
try:
    from mcps.shared.unified_llm import llm_chat
    _LLM_AVAILABLE = True
except ImportError:
    _LLM_AVAILABLE = False
    logger.error("[hotspot-engine] unified_llm不可用,LLM选题将降级到模板")

from mcps.shared.atomic_write import atomic_read_json, atomic_write_text

JUEJIN_HOME = Path(os.environ.get("JUEJIN_HOME", str(_PROJECT_ROOT_HE)))
HOTSPOT_DIR = JUEJIN_HOME / "memory" / "hotspots"

# 通用选题模板(热点不足时补充)
GENERIC_TOPIC_TEMPLATES = [
    "{brand}{industry}领域最新趋势解读",
    "如何用AI提升{industry}效率",
    "{industry}从业者必知的5个技巧",
    "{industry}行业痛点与解决方案",
    "{industry}新手入门完全指南",
    "{industry}变现路径深度分析",
    "从0到1做{industry}实战分享",
    "{industry}避坑指南与经验总结",
    "{industry}工具推荐与对比评测",
    "{industry}未来3年发展方向预测",
]

# 行业关键词映射(根据租户ID推断行业)
INDUSTRY_KEYWORDS = {
    "default": "AI自动化",
    "ai": "AI技术",
    "design": "设计",
    "edu": "教育",
    "tech": "科技",
    "content": "内容创作",
    "ecommerce": "电商",
}

# ─── 辅助函数 ─────────────────────────────────────────────

def _get_industry(tenant_id: str) -> str:
    """根据租户ID推断行业关键词"""
    tid_lower = tenant_id.lower()
    for key, industry in INDUSTRY_KEYWORDS.items():
        if key in tid_lower:
            return industry
    return INDUSTRY_KEYWORDS["default"]

def _get_brand_info(tenant_id: str) -> Dict[str, str]:
    """获取租户品牌信息

    优先从data/account_profiles.json读取,回退到默认值。
    v2.2: 新增directions(运营方向)读取(来源:09文档U14)。
    """
    brand_info = {
        "brand": tenant_id,
        "industry": _get_industry(tenant_id),
        "directions": "",
    }
    # 尝试从租户配置读取品牌名
    profile_file = JUEJIN_HOME / "data" / "account_profiles.json"
    if profile_file.exists():
        profiles = atomic_read_json(profile_file)
        if profiles is not None:
            if isinstance(profiles, dict):
                tenant_profile = profiles.get(tenant_id, {})
                if isinstance(tenant_profile, dict):
                    brand_info["brand"] = tenant_profile.get("brand_name", tenant_id)
                    brand_info["industry"] = tenant_profile.get("industry", brand_info["industry"])
                    brand_info["directions"] = tenant_profile.get("directions", "")
        else:
            logger.warning("account_profiles.json读取失败")
    # 尝试从tenant_credentials.json读取directions(agency-portal-mcp数据源)
    cred_file = JUEJIN_HOME / "mcps" / "agency-portal-mcp" / "data" / "tenant_credentials.json"
    if cred_file.exists() and not brand_info["directions"]:
        creds = atomic_read_json(cred_file)
        if creds is not None:
            if isinstance(creds, dict):
                tenant_cred = creds.get(tenant_id, {})
                if isinstance(tenant_cred, dict):
                    brand_info["directions"] = tenant_cred.get("directions", "")
        else:
            logger.warning("tenant_credentials.json读取失败")
    return brand_info

def _repair_json_string(json_str: str) -> str:
    """修复LLM返回的常见JSON格式问题

    处理: 单引号→双引号/裸键名加引号/尾部逗号/注释
    """
    s = json_str
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
    s = re.sub(r"'([^']+)'(\s*:)", r'"\1"\2', s)
    s = re.sub(r":\s*'([^']*)'", r': "\1"', s)
    s = re.sub(r'([{,]\s*)([a-zA-Z_\u4e00-\u9fff][a-zA-Z0-9_\u4e00-\u9fff]*)(\s*:)', r'\1"\2"\3', s)
    s = re.sub(r',\s*([}\]])', r'\1', s)
    return s

def _try_parse_json(content: str) -> Optional[Any]:
    """健壮的JSON解析: 多策略尝试解析LLM返回的JSON

    策略: 标准解析→提取块→修复后重试→贪婪提取
    """
    # 策略1: 直接解析
    try:
        return json.loads(content)
    except Exception as e:

        logger.error(f"hotspot_engine: {e}")
    # 策略2: 提取所有{...}或[...]块逐个尝试
    for match in re.finditer(r'(\[[\s\S]*?\]|\{[\s\S]*?\})', content):
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            continue
    # 策略3: 修复常见问题后重试
    repaired = _repair_json_string(content)
    try:
        return json.loads(repaired)
    except Exception as e:

        logger.error(f"hotspot_engine: {e}")
    for match in re.finditer(r'(\[[\s\S]*?\]|\{[\s\S]*?\})', repaired):
        try:
            return json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            continue
    # 策略4: 贪婪匹配
    for match in re.finditer(r'(\[[\s\S]+\]|\{[\s\S]+\})', content):
        candidate = match.group(1)
        try:
            return json.loads(candidate)
        except Exception as e:

            logger.error(f"hotspot_engine: {e}")
        try:
            return json.loads(_repair_json_string(candidate))
        except (json.JSONDecodeError, ValueError):
            continue
    return None

# ─── 核心API函数 ──────────────────────────────────────────

def load_hotspots(tenant_id: str = "", count: int = 10) -> Dict[str, Any]:
    """加载热点数据

    从memory/hotspots/读取最新日期的热点文件(dailyhot-mcp采集后保存到此目录)。
    支持两种文件格式: YYYY-MM-DD.json 或 YYYY-MM-DD/index.json

    Args:
        tenant_id: 租户ID(预留,当前热点数据为全局共享)
        count: 需要的热点数量(预留,当前返回全部)

    Returns:
        {success, data: {platforms: {name: [titles]}, total_items, date}, error, code}
    """
    if not HOTSPOT_DIR.exists():
        return {
            "success": False, "data": {},
            "error": f"热点数据目录不存在: {HOTSPOT_DIR}",
            "code": "NO_HOTSPOT_DIR",
        }
    # 查找最新日期的热点文件
    json_files = sorted(HOTSPOT_DIR.glob("*.json"), reverse=True)
    day_dirs = sorted(HOTSPOT_DIR.iterdir(), reverse=True) if HOTSPOT_DIR.exists() else []
    latest_index = None
    latest_date = None
    for d in day_dirs:
        if not d.is_dir():
            continue
        index_file = d / "index.json"
        if index_file.exists():
            latest_index = index_file
            latest_date = d.name
            break
    if not latest_index:
        for jf in json_files:
            name = jf.stem
            if len(name) == 10 and name[4] == "-" and name[7] == "-":
                latest_index = jf
                latest_date = name
                break
    if not latest_index or not latest_index.exists():
        return {
            "success": False, "data": {},
            "error": "未找到热点数据文件",
            "code": "NO_HOTSPOT_DATA",
        }
    raw = atomic_read_json(latest_index)
    if raw is None:
        return {
            "success": False, "data": {},
            "error": "热点数据解析失败: safe_read_json返回None",
            "code": "BAD_HOTSPOT_DATA",
        }
    # 提取各平台热点标题
    platforms: Dict[str, List[str]] = {}
    total_items = 0
    if "platforms" in raw and isinstance(raw["platforms"], dict):
        for plat_name, plat_data in raw["platforms"].items():
            if not isinstance(plat_data, dict):
                continue
            top_items = plat_data.get("top3", [])
            titles = [item.get("title", "") for item in top_items if isinstance(item, dict) and item.get("title")]
            if titles:
                platforms[plat_name] = titles
                total_items += len(titles)
    else:
        for key, value in raw.items():
            if key.startswith("_") or not isinstance(value, list):
                continue
            titles = []
            for item in value:
                if isinstance(item, dict) and item.get("title"):
                    titles.append(item["title"])
            if titles:
                platforms[key] = titles
                total_items += len(titles)
    return {
        "success": True,
        "data": {
            "platforms": platforms,
            "total_items": total_items,
            "date": latest_date,
            "source_file": str(latest_index),
        },
        "error": None, "code": None,
    }

def _generate_topics_with_llm(
    hotspot_titles: List[str],
    brand_info: Dict[str, str],
    count: int,
) -> List[Dict[str, Any]]:
    """使用unified_llm基于热点标题+品牌信息动态生成选题

    调用unified_llm.llm_chat(统一入口,来源:18_统一入口规则)。
    失败时返回空列表,调用方降级到模板逻辑。

    Args:
        hotspot_titles: 热点标题列表
        brand_info: 品牌信息{brand, industry, directions}
        count: 选题数量

    Returns:
        [{topic, angle, target_audience, content_type, hotspot_source, priority}]
        失败时返回空列表
    """
    if not _LLM_AVAILABLE:
        logger.warning("unified_llm不可用,LLM选题生成跳过")
        return []

    brand = brand_info.get("brand", "")
    industry = brand_info.get("industry", "AI自动化")
    directions = brand_info.get("directions", "")
    titles_summary = "\n".join(f"- {t}" for t in hotspot_titles[:20])

    # 构建业务相关性约束(来源:09文档v2.2 强制选题与租户业务相关)
    business_constraint = ""
    if directions:
        business_constraint = (
            f"\n核心约束: 选题必须与以下业务方向强相关!\n"
            f"业务方向: {directions}\n"
            f"每个选题必须能自然融入上述业务方向中的产品/服务。\n\n"
        )
    elif industry:
        business_constraint = (
            f"\n核心约束: 选题必须与{industry}行业相关!\n\n"
        )

    prompt = (
        f"你是一位资深内容策划专家。请基于以下热点和品牌信息,生成{count}个差异化选题。\n\n"
        f"品牌: {brand}\n"
        f"行业: {industry}\n"
        f"{business_constraint}"
        f"当前热点标题:\n{titles_summary}\n\n"
        f"要求:\n"
        f"1. 每个选题必须与至少一个热点标题相关联,且必须与品牌业务方向强相关\n"
        f"2. 选题之间要有差异化:切入角度不同(教程/评测/故事/数据)、情绪基调不同(专业/轻松/煽情)\n"
        f"3. 每个选题包含4个字段:\n"
        f'   - topic: 选题标题(吸引眼球,≤30字)\n'
        f'   - angle: 切入角度(教程/评测/故事/数据/趋势/避坑/变现之一)\n'
        f'   - target_audience: 目标受众(如"AI新手"/"自媒体人"/"小商家")\n'
        f'   - content_type: 内容形式(图文/视频之一)\n'
        f"4. 严格输出JSON数组,不要输出其他内容\n\n"
        f'示例输出格式:\n'
        f'[{{"topic":"...", "angle":"...", "target_audience":"...", "content_type":"..."}}]'
    )

    try:
        # 使用unified_llm统一入口(来源:18_统一入口规则)
        # 不使用expect_json=True,因为LLM返回可能需要修复解析
        result = llm_chat(
            prompt=prompt,
            system_prompt="",
            caller="hotspot-engine",
            temperature=0.8,
            max_tokens=2048,
        )

        if not result.get("success"):
            logger.warning(f"LLM选题生成失败: {result.get('error', '未知错误')}")
            return []

        content = result.get("raw_text", "")
        if not content:
            logger.warning("LLM返回空内容")
            return []

        # 提取JSON(兼容markdown代码块包裹)
        json_str = content.strip()
        if "```" in json_str:
            parts = json_str.split("```")
            for part in parts:
                part = part.strip()
                if part.startswith("json"):
                    part = part[4:].strip()
                if part.startswith("[") or part.startswith("{"):
                    json_str = part
                    break

        # 健壮JSON解析(4策略)
        topics_raw = _try_parse_json(json_str)
        if topics_raw is None:
            logger.warning("LLM选题JSON解析失败(所有策略均失败), 原始内容前200字符: %s", json_str[:200])
            return []
        if isinstance(topics_raw, dict):
            topics_raw = [topics_raw]
        if not isinstance(topics_raw, list):
            logger.warning("LLM返回非数组/对象格式: %s", type(topics_raw).__name__)
            return []

        # 转换为标准选题格式
        topics: List[Dict[str, Any]] = []
        for i, item in enumerate(topics_raw[:count]):
            if not isinstance(item, dict):
                continue
            topic_text = str(item.get("topic", "")).strip()
            if not topic_text:
                continue
            topics.append({
                "topic": topic_text,
                "angle": str(item.get("angle", "综合")),
                "target_audience": str(item.get("target_audience", "通用")),
                "content_type": str(item.get("content_type", "图文")),
                "hotspot_source": "llm_generated",
                "priority": i + 1,
            })
        return topics

    except Exception as e:
        logger.error(f"LLM选题生成失败(将降级到模板): {e}")
        return []

def generate_topics(hotspots: Dict[str, Any], tenant_id: str, count: int = 10) -> List[Dict[str, Any]]:
    """根据热点+租户品牌生成选题

    优先使用LLM(unified_llm统一入口)基于热点标题+品牌信息动态生成差异化选题。
    LLM不可用或无热点数据时降级到通用模板。

    Args:
        hotspots: load_hotspots()返回的热点数据
        tenant_id: 租户ID
        count: 选题数量

    Returns:
        [{topic, angle, target_audience, content_type, hotspot_source, priority}]
    """
    brand_info = _get_brand_info(tenant_id)
    brand = brand_info["brand"]
    industry = brand_info["industry"]

    # 收集所有热点标题(按平台分组,保持多样性)
    all_titles: List[str] = []
    platforms_data = hotspots.get("platforms", {})
    for plat_name, titles in platforms_data.items():
        for title in titles:
            all_titles.append(title)

    # 有热点数据时优先使用LLM动态生成
    if all_titles:
        llm_topics = _generate_topics_with_llm(all_titles, brand_info, count)
        if llm_topics:
            # LLM生成成功,不足部分用模板补充
            if len(llm_topics) < count:
                shortage = count - len(llm_topics)
                for j in range(shortage):
                    template = GENERIC_TOPIC_TEMPLATES[j % len(GENERIC_TOPIC_TEMPLATES)]
                    topic_text = template.format(brand=brand, industry=industry)
                    llm_topics.append({
                        "topic": topic_text,
                        "angle": "通用选题",
                        "target_audience": "通用",
                        "content_type": "图文",
                        "hotspot_source": "generic_template",
                        "priority": len(llm_topics) + 1,
                    })
            return llm_topics[:count]
        # LLM失败,降级到模板逻辑
        logger.info("LLM选题生成失败,降级到模板逻辑")

    # 降级: 按平台轮询选取热点+模板拼接
    selected_hotspots: List[Dict[str, str]] = []
    platform_queues: Dict[str, List[str]] = {k: list(v) for k, v in platforms_data.items()}
    platform_names = list(platform_queues.keys())
    idx = 0
    while len(selected_hotspots) < count and any(platform_queues.values()):
        if not platform_names:
            break
        plat = platform_names[idx % len(platform_names)]
        queue = platform_queues[plat]
        if queue:
            title = queue.pop(0)
            selected_hotspots.append({"title": title, "platform": plat})
        idx += 1
        platform_names = [p for p in platform_names if platform_queues[p]]

    # 生成选题
    topics: List[Dict[str, Any]] = []
    angle_templates = [
        "深度解读", "实用指南", "行业影响分析", "趋势预测",
        "避坑提醒", "变现机会", "技术解析", "案例拆解",
        "对比评测", "入门科普",
    ]
    for i, hs in enumerate(selected_hotspots):
        title = hs["title"]
        platform = hs["platform"]
        angle = angle_templates[i % len(angle_templates)]
        topic = f"【{brand}】{title}的{angle}"
        topics.append({
            "topic": topic,
            "angle": angle,
            "target_audience": "通用",
            "content_type": "图文",
            "hotspot_source": f"{platform}:{title}",
            "priority": i + 1,
        })

    # 热点不足时用通用模板补充
    if len(topics) < count:
        shortage = count - len(topics)
        for j in range(shortage):
            template = GENERIC_TOPIC_TEMPLATES[j % len(GENERIC_TOPIC_TEMPLATES)]
            topic_text = template.format(brand=brand, industry=industry)
            topics.append({
                "topic": topic_text,
                "angle": "通用选题",
                "target_audience": "通用",
                "content_type": "图文",
                "hotspot_source": "generic_template",
                "priority": len(topics) + 1,
            })
    return topics[:count]

def match_materials_for_topics(topics: List[Dict[str, Any]], tenant_id: str) -> List[Dict[str, Any]]:
    """为每个选题匹配素材

    对每个选题调用material_matcher.py(subprocess),
    收集匹配结果,素材不足时标记降级建议。

    Args:
        topics: generate_topics()返回的选题列表
        tenant_id: 租户ID

    Returns:
        选题列表,每个增加materials和material_degradation字段
    """
    matcher_script = JUEJIN_HOME / "scripts" / "material_matcher.py"
    results: List[Dict[str, Any]] = []

    for topic in topics:
        topic_text = topic["topic"]
        # 从选题中提取关键词
        keywords_raw = topic_text
        for prefix in ["【", "】"]:
            keywords_raw = keywords_raw.replace(prefix, " ")
        core_part = keywords_raw.split("的")[0].strip() if "的" in keywords_raw else keywords_raw.strip()
        keywords = [k.strip() for k in core_part.split() if k.strip() and len(k.strip()) > 1]
        if not keywords:
            keywords = [topic_text[:10]]

        materials: Dict[str, Any] = {"matches": [], "degradation": None}
        if matcher_script.exists():
            try:
                kw_str = ",".join(keywords)
                proc = subprocess.run(
                    [sys.executable, str(matcher_script),
                     "--tenant-id", tenant_id,
                     "--keywords", kw_str,
                     "--top", "3"],
                    capture_output=True, text=True, timeout=30,
                    cwd=str(JUEJIN_HOME),
                )
                if proc.returncode == 0:
                    match_result = json.loads(proc.stdout)
                    if match_result.get("success"):
                        match_data = match_result.get("data", {})
                        materials["matches"] = match_data.get("matches", [])
                        materials["degradation"] = match_data.get("degradation")
                else:
                    logger.warning("material_matcher返回非0: %s", proc.stderr[:200] if proc.stderr else "")
                    materials["degradation"] = {"reason": "material_matcher执行失败", "suggestion": "使用Pexels/Pixabay素材补充"}
            except subprocess.TimeoutExpired:
                logger.warning("material_matcher超时: %s", topic_text[:30])
                materials["degradation"] = {"reason": "material_matcher超时", "suggestion": "使用Pexels/Pixabay素材补充"}
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("material_matcher结果解析失败: %s", e)
                materials["degradation"] = {"reason": f"素材匹配结果解析失败: {e}", "suggestion": "使用Pexels/Pixabay素材补充"}
        else:
            materials["degradation"] = {"reason": "material_matcher.py不存在", "suggestion": "安装素材匹配模块或使用Pexels/Pixabay"}

        enriched = dict(topic)
        enriched["materials"] = materials["matches"]
        enriched["material_degradation"] = materials["degradation"]
        enriched["material_count"] = len(materials["matches"])
        results.append(enriched)

    return results

def orchestrate(tenant_id: str, count: int = 10, output_dir: str = "data/output/topics/") -> Dict[str, Any]:
    """完整编排流程: 热点→选题→素材匹配→降级补充

    Args:
        tenant_id: 租户ID
        count: 选题数量
        output_dir: 输出目录

    Returns:
        {success, data, error, code}
    """
    # Step1: 加载热点
    hotspot_result = load_hotspots(tenant_id, count)
    if not hotspot_result.get("success"):
        return {
            "success": False, "data": {},
            "error": f"热点加载失败: {hotspot_result.get('error')}",
            "code": hotspot_result.get("code", "HOTSPOT_LOAD_FAIL"),
        }
    hotspot_data = hotspot_result["data"]

    # Step2: 生成选题
    try:
        topics = generate_topics(hotspot_data, tenant_id, count)
    except Exception as e:
        logger.error("选题生成失败: %s", e)
        return {
            "success": False, "data": {},
            "error": f"选题生成失败: {e}",
            "code": "TOPIC_GEN_FAIL",
        }
    if not topics:
        return {"success": False, "data": {}, "error": "未生成任何选题", "code": "NO_TOPICS"}

    # Step3: 素材匹配
    try:
        enriched_topics = match_materials_for_topics(topics, tenant_id)
    except Exception as e:
        logger.error("素材匹配失败: %s", e)
        enriched_topics = []
        for t in topics:
            enriched = dict(t)
            enriched["materials"] = []
            enriched["material_degradation"] = {"reason": f"素材匹配流程异常: {e}", "suggestion": "使用Pexels/Pixabay素材补充"}
            enriched["material_count"] = 0
            enriched_topics.append(enriched)

    # Step4: 统计降级情况
    degraded_count = sum(1 for t in enriched_topics if t.get("material_degradation"))
    total_materials = sum(t.get("material_count", 0) for t in enriched_topics)

    # Step5: 输出结果
    output = {
        "tenant_id": tenant_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "hotspot_source": hotspot_data.get("date", ""),
        "hotspot_items": hotspot_data.get("total_items", 0),
        "topic_count": len(enriched_topics),
        "total_materials": total_materials,
        "degraded_topics": degraded_count,
        "topics": enriched_topics,
        "generated_at": datetime.now().isoformat(),
    }

    # 保存到文件
    try:
        out_path = Path(output_dir) if Path(output_dir).is_absolute() else JUEJIN_HOME / output_dir
        out_path.mkdir(parents=True, exist_ok=True)
        out_file = out_path / f"{datetime.now().strftime('%Y-%m-%d')}_{tenant_id}.json"
        _content = json.dumps(output, ensure_ascii=False, indent=2, default=str)
        atomic_write_text(out_file, _content)
        output["output_file"] = str(out_file)
    except OSError as e:
        logger.error("结果保存失败(非致命): %s", e)
        output["output_file"] = None
        output["save_error"] = str(e)

    return {"success": True, "data": output, "error": None, "code": None}

def main():
    """CLI入口"""
    parser = argparse.ArgumentParser(description="热点选题引擎 - P2-1统一编排器模块")
    parser.add_argument("--tenant-id", required=True, help="租户ID")
    parser.add_argument("--count", type=int, default=10, help="选题数量(默认: 10)")
    parser.add_argument("--output", default="data/output/topics/", help="输出目录")
    args = parser.parse_args()

    try:
        result = orchestrate(args.tenant_id, args.count, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        sys.exit(0 if result.get("success") else 1)
    except ValueError as e:
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "INVALID_PARAMS"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as e:
        logger.exception("编排执行失败")
        logger.error(f"Exception in except block: {e}");
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "ORCHESTRATE_ERROR"}, ensure_ascii=False, indent=2))
        sys.exit(2)

if __name__ == "__main__":
    main()
