#!/usr/bin/env python3
"""内容编排器 - 统一入口脚本
根据管道类型编排内容生成+发布流程
"""
import sys

import json
import os
import argparse
import subprocess
from datetime import datetime
from typing import Any

# R14-R7统一入口: db_logger替代logging(规则18)
sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts")))
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
from mcps.shared.atomic_write import atomic_read_json
logger = get_logger("content-orchestrator", source="skills/content-orchestrator/scripts/content_orchestrator.py")

# v2.6修复(BUG-E2E-020): Windows GBK编码stderr无法输出\ufffd等字符
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception as e:

        logger.error(f"content_orchestrator: {e}")
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception as e:

        logger.error(f"content_orchestrator: {e}")

sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "..", "..", "mcps", "shared")))
try:
    from mcp_caller import call_mcp
    _MCP_AVAILABLE = True
except ImportError:
    _MCP_AVAILABLE = False

# P0-33修复: 平台知识库加载器(来源:P1-17修复S-30 + 02手册§二28平台)
try:
    from platform_knowledge_loader import load_multi_platform_knowledge as _load_platform_kb
    _PLATFORM_KB_AVAILABLE = True
except ImportError:
    _PLATFORM_KB_AVAILABLE = False
    _load_platform_kb = None

# Token优化: 内容生成缓存(见30白皮书§十一+修复提示词R14+R33)
try:
    from content_cache import ContentCache
    _CACHE_AVAILABLE = True
except ImportError:
    _CACHE_AVAILABLE = False
    logger.error("[content-orchestrator] ContentCache不可用，草稿缓存功能降级")

# RC-1/RC-2修复: 引擎占位符解析器(按租户套餐动态选择TTS/视频/图像/唇形同步MCP)
# BUG-V4A-002修复: pipeline_engine_resolver.py已创建(5轮审核确认原文件不存在,注释"已实现"为虚假信息R74.1 F7)
try:
    from pipeline_engine_resolver import resolve_pipeline_steps as _resolve_engine_steps
    _ENGINE_RESOLVER_AVAILABLE = True
except ImportError:
    _ENGINE_RESOLVER_AVAILABLE = False
    logger.error("[content-orchestrator] pipeline_engine_resolver不可用,${engine.*}占位符将无法解析")

# P2-1: 导入统一编排器模块(pipeline_state状态机 + hotspot_engine热点选题)
# 来源: 31文档P2-1(合并3个内容编排器) + 18_统一入口规则(编排→content-orchestrator)
sys.path.insert(0, str(os.path.dirname(__file__)))
try:
    import pipeline_state
    _STATE_AVAILABLE = True
except ImportError:
    _STATE_AVAILABLE = False
    logger.error("[content-orchestrator] pipeline_state不可用，状态追踪降级")

try:
    import hotspot_engine
    _HOTSPOT_AVAILABLE = True
except ImportError:
    _HOTSPOT_AVAILABLE = False
    logger.error("[content-orchestrator] hotspot_engine不可用，热点选题降级")

# P1-4管线补全: 营销注入/SEO/GEO/审核/AI声明5步(来源:content-orchestrator SKILL.md门控声明)
# 顺序: 生成→IP特质→写作风格→去AI味→营销注入→SEO→GEO→审核→AI声明→发布

# BUG-189修复: AI声明注入内联实现(原依赖risk-detector MCP但该MCP未注册)
# 各平台AI生成内容声明要求(来源:02手册§五5.1 + 01手册§五5.1)
_AI_DECLARATION_TEMPLATES = {
    "xianyu": "【AI辅助生成】本商品文案由AI辅助生成，仅供参考。",
    "douyin": "该内容包含AI生成素材",
    "xiaohongshu": "笔记含AI生成内容",
    "shipinhao": "本内容包含AI生成素材",
    "csdn": "> 本文由AI辅助生成，如有不当之处欢迎指正。",
    "zhihu": "【AI辅助创作】",
    "bilibili": "本视频/文章包含AI生成内容",
    "default": "【AI辅助生成】",
}

def _inject_ai_declaration(content: str, platform: str = "default") -> dict:
    """内联AI声明注入(BUG-189修复)

    各平台要求AI生成内容标注声明,未声明可能被平台处罚/删除。

    Args:
        content: 原始内容
        platform: 目标平台

    Returns:
        {success: bool, data: {content, declaration, platform}, error: str|null}
    """
    declaration = _AI_DECLARATION_TEMPLATES.get(platform, _AI_DECLARATION_TEMPLATES["default"])
    # 避免重复注入
    if declaration in content:
        return {"success": True, "data": {"content": content, "declaration": declaration, "platform": platform, "already_injected": True}, "error": None}
    # 注入到内容末尾
    injected_content = f"{content}\n\n{declaration}"
    return {"success": True, "data": {"content": injected_content, "declaration": declaration, "platform": platform, "already_injected": False}, "error": None}

# BUG-190修复: 租户风格配置查询(原未传递给下游)
def _read_tenant_styles_file(tenant_id: str) -> dict:
    """从文件读取租户风格配置(降级方案: Cron任务无token时使用)

    读取 data/tenant_styles/{tenant_id}.json，返回解析后的dict。
    用于_token为空时降级获取brand_keywords/content_guidelines等配置。

    Returns:
        解析后的tenant_styles dict或空dict
    """
    if not tenant_id:
        return {}
    try:
        # V43修复(BUG-14): 使用_PROJECT_ROOT替代硬编码路径,支持Docker等非d:\JueJin部署环境
        styles_path = _PROJECT_ROOT / "data" / "tenant_styles" / f"{tenant_id}.json"
        if styles_path.exists():
            return atomic_read_json(styles_path)
    except Exception as e:
        logger.error(f"[content-orchestrator] 读取tenant_styles文件失败(tenant_id={tenant_id}): {e}")
    return {}

def _query_tenant_style_config(tenant_id: str, token: str = "") -> dict:
    """查询租户风格配置(BUG-190修复 + V43 Cron降级)

    优先通过agency-portal-mcp获取; token为空时(Cron任务场景)降级读文件。

    Args:
        tenant_id: 租户ID
        token: 租户JWT token(BUG-FIX 2026-08-05: portal_get_tenant_style需要token参数,
               原代码传tenant_id导致inspect.signature过滤后无参数,触发熔断器)

    Returns:
        {content_guidelines, brand_keywords, video_brand_overlay} 或空dict
    """
    if not tenant_id:
        return {}
    # V43: token为空时降级读文件(Cron任务无session token)
    if not token or not _MCP_AVAILABLE:
        file_data = _read_tenant_styles_file(tenant_id)
        if file_data:
            logger.info(f"[content-orchestrator] _query_tenant_style_config: token为空,降级读取文件(brand_keywords={len(file_data.get('brand_keywords', []))}个)")
            return {
                "content_guidelines": file_data.get("content_guidelines", ""),
                "brand_keywords": file_data.get("brand_keywords", []),
                "video_brand_overlay": file_data.get("video_brand_overlay", {}),
                # V43修复: 读取AI生成的SEO/GEO配置(小白用户通过AI生成→保存→管道消费)
                "ai_seo_config": file_data.get("ai_seo_config", {}),
                "ai_geo_config": file_data.get("ai_geo_config", {}),
            }
        if not token:
            logger.warning(f"[content-orchestrator] _query_tenant_style_config: token为空且文件不存在,跳过租户风格查询(tenant_id={tenant_id})")
        return {}
    try:
        result = call_mcp("agency-portal-mcp", "portal_get_tenant_style", {"token": token})
        if result.get("success"):
            data = result.get("data", {})
            # V43修复: MCP返回的data可能含style_config嵌套层,需兼容两种结构
            _cfg = data.get("style_config", data) if isinstance(data, dict) else {}
            return {
                "content_guidelines": _cfg.get("content_guidelines", data.get("content_guidelines", "")),
                "brand_keywords": _cfg.get("brand_keywords", data.get("brand_keywords", [])),
                "video_brand_overlay": _cfg.get("video_brand_overlay", data.get("video_brand_overlay", {})),
                # V43修复: 读取AI生成的SEO/GEO配置(MCP返回完整style_data,含ai_*_config)
                "ai_seo_config": data.get("ai_seo_config", _cfg.get("ai_seo_config", {})),
                "ai_geo_config": data.get("ai_geo_config", _cfg.get("ai_geo_config", {})),
            }
    except Exception as e:
        logger.error(f"[content-orchestrator] 租户风格配置查询失败(非关键): {e}")
    return {}

# 架构修复: 租户品牌Profile查询(预获取,确保生成步骤前可用)
def _query_tenant_brand_profile(tenant_id: str, token: str = "") -> dict:
    """查询租户品牌Profile(架构修复 + V43 Cron降级)

    优先通过agency-portal-mcp获取; token为空时(Cron任务场景)降级读文件。

    Args:
        tenant_id: 租户ID
        token: 租户JWT token(portal_get_tenant_brand_profile需要token参数)

    Returns:
        品牌Profile dict或空dict(非致命,失败时降级)
    """
    if not tenant_id:
        return {}
    # V43: token为空时降级读文件(Cron任务无session token)
    if not token or not _MCP_AVAILABLE:
        file_data = _read_tenant_styles_file(tenant_id)
        if file_data:
            logger.info(f"[content-orchestrator] _query_tenant_brand_profile: token为空,降级读取文件(brand_name={file_data.get('brand_name', 'N/A')})")
            return {
                "brand_name": file_data.get("brand_name", ""),
                "brand_slogan": file_data.get("brand_slogan", ""),
                "brand_keywords": file_data.get("brand_keywords", []),
                "content_guidelines": file_data.get("content_guidelines", {}),
                "cover_style": file_data.get("cover_style", {}),
                # V43修复: 读取AI生成的品牌/营销配置(小白用户通过AI生成→保存→管道消费)
                "ai_brand_config": file_data.get("ai_brand_config", {}),
                "ai_marketing_config": file_data.get("ai_marketing_config", {}),
            }
        if not token:
            logger.warning(f"[content-orchestrator] _query_tenant_brand_profile: token为空且文件不存在,跳过品牌Profile查询(tenant_id={tenant_id})")
        return {}
    try:
        result = call_mcp("agency-portal-mcp", "portal_get_tenant_brand_profile", {"token": token})
        if result.get("success"):
            data = result.get("data", {})
            if not isinstance(data, dict):
                return {}
            # V43修复: MCP handler不返回ai_brand_config/ai_marketing_config,从文件补充
            _file_data = _read_tenant_styles_file(tenant_id)
            if _file_data:
                if not data.get("ai_brand_config") and _file_data.get("ai_brand_config"):
                    data["ai_brand_config"] = _file_data["ai_brand_config"]
                if not data.get("ai_marketing_config") and _file_data.get("ai_marketing_config"):
                    data["ai_marketing_config"] = _file_data["ai_marketing_config"]
            return data
    except Exception as e:
        logger.error(f"[content-orchestrator] 品牌Profile查询失败(非关键,降级为空): {e}")
    return {}

# DEF-U49 P2: 蒸馏21维指纹查询(激活pps-mcp.get_distill_fingerprint桥接工具)
# 来源: 60号文档v2.0 §2.4 + DEF-U49 P1-4(孤儿工具激活)
# 职责: 通过pps-mcp.get_distill_fingerprint获取21维蒸馏数据,注入下游步骤
# 注: get_persona_profile(步骤1)保留,负责获取人设档案(照片/配音/外观);本函数负责蒸馏指纹
def _query_tenant_distill_fingerprint(tenant_id: str) -> dict:
    """查询租户蒸馏21维指纹(DEF-U49 P2: 激活跨MCP桥接)

    通过pps-mcp.get_distill_fingerprint获取蒸馏数据:
    - persona_profile(4维人物IP)
    - style_fingerprint(6维写作风格)
    - video_style_fingerprint(6维视频风格)
    - longform_structure(5维长文结构)
    - brand_analysis(品牌分析缓存)

    Args:
        tenant_id: 租户标识(在多租户体系中作为tenant_slug使用)

    Returns:
        蒸馏数据dict或空dict(非致命,失败时降级)
    """
    if not tenant_id or not _MCP_AVAILABLE:
        return {}
    try:
        result = call_mcp("pps-mcp", "get_distill_fingerprint", {"tenant_slug": tenant_id})
        if result.get("success"):
            data = result.get("data", {})
            # 仅提取蒸馏字段(不包含_warning等元数据)
            return {
                "persona_profile": data.get("persona_profile", {}),
                "style_fingerprint": data.get("style_fingerprint", {}),
                "video_style_fingerprint": data.get("video_style_fingerprint", {}),
                "longform_structure": data.get("longform_structure", {}),
                "brand_analysis": data.get("brand_analysis", {}),
            }
        else:
            logger.info(f"[content-orchestrator] 蒸馏指纹无数据(非关键): {result.get('error', '空')}")
    except Exception as e:
        logger.error(f"[content-orchestrator] 蒸馏指纹查询失败(非关键,降级为空): {e}")
    return {}

# 问题2修复: agent_memory自学习经验消费
# 职责: 查询agent_memory表中最近7天category='publish_feedback'的经验记录
# 注入到内容生成步骤的LLM提示词中,使内容生成能参考历史发布反馈
# 降级: 查询失败时返回空列表(非致命,不阻塞内容生成)
def _query_agent_memory_lessons(tenant_id: str) -> list:
    """查询agent_memory表中的自学习经验(发布反馈类)

    从agent_memory表查询最近7天category='publish_feedback'的经验记录,
    按importance_score降序取前10条,返回summary文本列表,供内容生成时参考。

    Args:
        tenant_id: 租户标识(用于日志记录)

    Returns:
        经验文本列表,查询失败时返回空列表(非致命,不阻塞内容生成)
    """
    if not tenant_id:
        return []
    try:
        from mcps.shared.db_pool import get_connection, return_connection
        import psycopg2.extras

        # R4修复: 添加owner LIKE过滤实现租户隔离
        # agent_memory.owner格式为'{tenant_id}:{agent_id}',按tenant_id前缀过滤
        # 修复前: WHERE category='publish_feedback' (无租户过滤,跨租户数据泄露)
        # 修复后: AND owner LIKE %s (仅查询当前租户的经验)
        tenant_owner_pattern = f"{tenant_id}:%"
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # R8修复(P1): 设置RLS上下文(agent_memory表已启用RLS+FORCED)
                # 不设置app.current_tenant时查询返回0行,导致自生长经验无法被消费
                cur.execute("SET app.current_tenant = %s", (tenant_id,))
                cur.execute("""
                    SELECT summary, content, importance_score
                    FROM agent_memory
                    WHERE category = 'publish_feedback'
                      AND is_active = TRUE
                      AND owner LIKE %s
                      AND created_at >= NOW() - INTERVAL '7 days'
                    ORDER BY importance_score DESC
                    LIMIT 10
                """, (tenant_owner_pattern,))
                rows = cur.fetchall()
        finally:
            return_connection(conn)

        if not rows:
            logger.info(f"[content-orchestrator] agent_memory: 近7天无publish_feedback经验 tenant={tenant_id}")
            return []

        lessons = []
        for row in rows:
            summary = row.get("summary", "")
            if summary and summary.strip():
                lessons.append(summary.strip())
            else:
                content = row.get("content", {})
                if isinstance(content, dict):
                    lesson_text = content.get("lesson", content.get("summary", ""))
                    if lesson_text:
                        lessons.append(str(lesson_text))

        logger.info(f"[content-orchestrator] agent_memory: 加载{len(lessons)}条publish_feedback经验 tenant={tenant_id}")
        return lessons
    except Exception as e:
        logger.error(f"[content-orchestrator] agent_memory查询失败(非关键,降级为空): {e}")
        return []

# P0-C修复: 租户知识库查询改为通过postgres-mcp(R53三层隔离)
# A2修复: tenant_knowledge_* → unified_knowledge_*(R75.7统一知识库)
# 职责: 通过postgres-mcp查询unified_knowledge_docs+unified_knowledge_chunks
# 降级: PG不可用时返回空dict(非致命)
# 注: pgvector深度语义检索仍由portal_generate_content中F-03逻辑处理(不变)
def _query_tenant_knowledge(tenant_id: str) -> dict:
    """查询租户知识库(P0-C修复: 通过postgres-mcp查询PG)

    PG唯一路径(R75.1存储统一化: JSON降级路径已移除,旧JSON fallback deprecated,不考虑向后兼容)。

    Args:
        tenant_id: 租户ID

    Returns:
        {products, faq, policies, kb_content} 或空dict(非致命,失败时返回空)
    """
    if not tenant_id:
        return {}

    # PG唯一路径: 通过postgres-mcp查询PG(R53三层隔离)
    # A2修复: 使用unified_knowledge_*表(替代tenant_knowledge_*)
    # DEF-KB-08修复: 扩展查询JOIN unified_knowledge_chunks获取chunk_text内容(限制5条,控制Token)
    try:
        from mcps.shared.mcp_caller import call_mcp
        _pg_result = call_mcp(
            "postgres-mcp", "pg_query",
            {"sql": "SELECT d.file_name, d.file_type, c.chunk_text "
                    "FROM unified_knowledge_docs d "
                    "JOIN unified_knowledge_chunks c ON d.doc_id = c.doc_id "
                    "WHERE d.tenant_id = $1 AND d.status = 'active' AND c.status = 'active' "
                    "ORDER BY c.created_at DESC "
                    "LIMIT 5",
             "params": [tenant_id]}
        )
        if _pg_result and _pg_result.get("success"):
            _rows = _pg_result.get("data", {}).get("rows", [])
            if _rows:
                # 从PG查询结果提取结构化信息
                _products = []
                _faq = []
                _policies = []
                _kb_content_parts = []
                for _row in _rows:
                    _file_name = _row.get("file_name", "")
                    _file_type = _row.get("file_type", "")
                    _chunk_text = _row.get("chunk_text", "")
                    if _file_type in (".pdf", ".docx", ".txt", ".md"):
                        _products.append({"name": _file_name, "type": _file_type})
                    elif "faq" in _file_name.lower():
                        _faq.append({"name": _file_name})
                    elif "policy" in _file_name.lower() or "polic" in _file_name.lower():
                        _policies.append({"name": _file_name})
                    # DEF-KB-08: 收集chunk_text内容拼接为kb_content,供下游Skill消费
                    if _chunk_text:
                        _kb_content_parts.append(_chunk_text)
                _kb_content = "\n---\n".join(_kb_content_parts) if _kb_content_parts else ""
                logger.info(f"[content-orchestrator] DEF-KB-08: PG知识库查询成功(含chunk_text): products={len(_products)}, faq={len(_faq)}, policies={len(_policies)}, kb_content_len={len(_kb_content)}")
                return {"products": _products, "faq": _faq, "policies": _policies, "kb_content": _kb_content}
            else:
                logger.info(f"[content-orchestrator] DEF-KB-10: PG知识库无数据 tenant={tenant_id}")
                return {}
        else:
            logger.warning(f"[content-orchestrator] DEF-KB-10: PG查询返回失败 tenant={tenant_id}")
    except ImportError:
        logger.error("[content-orchestrator] DEF-KB-10: mcp_caller未安装(R75.6 shared模块准入违规)")
    except Exception as _pg_err:
        logger.error(f"[content-orchestrator] DEF-KB-10: PG查询失败 tenant={tenant_id}: {_pg_err}")
    return {}

# P0-33修复: 平台知识库查询(来源:P1-17修复S-30 + 02手册§二28平台)
# 职责: 通过platform_knowledge_loader加载目标平台运营知识,注入下游步骤
def _query_platform_knowledge(platforms: str) -> str:
    """查询平台知识库(P0-33修复: 4库协同)

    通过platform_knowledge_loader加载目标平台运营知识库SKILL.md核心内容。

    Args:
        platforms: 逗号分隔的平台标识("douyin,xiaohongshu"或"抖音,小红书")

    Returns:
        平台知识库文本(≤2000字/平台),无匹配返回空字符串
    """
    if not platforms or not _PLATFORM_KB_AVAILABLE:
        return ""
    try:
        kb_text = _load_platform_kb(platforms)
        if kb_text:
            logger.info(f"[content-orchestrator] P0-33: 平台知识库已加载({len(kb_text)}字), platforms={platforms}")
        return kb_text or ""
    except Exception as e:
        logger.error(f"[content-orchestrator] 平台知识库查询失败(非关键,降级为空): {e}")
    return ""

# BUG-359真修复: 添加3个关键步骤(来源:33号文档§3 + 34号文档§4 + 02手册§五5.1)
# 步骤1: 个人IP特质注入 — 通过pps-mcp.get_persona_profile获取人设档案(照片/配音/外观)并注入内容
# 步骤2: 写作风格特质注入 — 通过agency-portal-mcp.portal_get_tenant_style获取基础风格配置
# 步骤3: 去AI味 — 通过content-template polish action调用marketing_polish.py polish_four_steps
# 注: 21维蒸馏指纹通过_query_tenant_distill_fingerprint预查询注入(DEF-U49 P2)
_IP_STYLE_DEAI_STEPS = [
    {"name": "品牌特质注入", "tool": "agency-portal-mcp", "action": "portal_get_tenant_brand_profile", "params": {}},
    {"name": "个人IP特质注入", "tool": "pps-mcp", "action": "get_persona_profile", "params": {}},
    {"name": "写作风格特质注入", "tool": "agency-portal-mcp", "action": "portal_get_tenant_style", "params": {}},
    {"name": "去AI味", "tool": "content-template", "action": "polish", "params": {}},
]

_MARKETING_SEO_GEO_REVIEW_STEPS = _IP_STYLE_DEAI_STEPS + [
    {"name": "营销注入", "tool": "market-copywriter", "action": "adapt_platform", "params": {"platform": "${platform}"}},
    {"name": "SEO优化", "tool": "seo-optimizer", "action": "optimize", "params": {"content": "${prev_output.content}"}},
    {"name": "GEO优化", "tool": "geo-content-optimizer", "action": "optimize", "params": {"content": "${prev_output.content}"}},
    # V43修复: 补充防查重检测和内容质量评分步骤(与外部JSON管道对齐)
    {"name": "防查重检测", "tool": "content-rewriter", "action": "detect", "params": {"content": "${prev_output.content}", "platform": "${platform}"}},
    # DEF-95 T05: 质量门控(4维: length/keyword/format/sensitive) — 在内容评分前做格式检查
    {"name": "质量门控", "tool": "quality-gate", "action": "check", "params": {"content": "${prev_output.content}", "platform": "${platform}"}},
    # 内容质量评分(7维,已由V43修复移到营销注入之后)
    {"name": "内容质量评分", "tool": "content-calibrator", "action": "score", "params": {"content": "${prev_output.content}", "platform": "${platform}"}},
    # DEF-95 T06: 内容质量补充评分(3维: coherence/consistency/quality) — 在7维评分后补充语义评分
    {"name": "内容质量补充评分", "tool": "content-quality-scorer", "action": "score", "params": {"content": "${prev_output.content}", "platform": "${platform}"}},
    {"name": "内容审核", "tool": "sensitive-word-mcp", "action": "check_sensitive_words", "params": {"text": "${prev_output.content}"}},
    # RC-5修复(2026-07-12): 移除inject_ai_declaration步骤
    # 原因: risk-detector无risk_detector.py入口脚本,call_skill会SKILL_NOT_FOUND
    # AI声明注入由portal_generate_content统一处理(buglist v2.0 RC-5建议方案)
]

# BUG-184修复: 3个强制门控实现(来源:content-orchestrator SKILL.md门控声明)
# 门控1: MARKETING_GATE_FAILED - 营销注入失败+降级也失败时拦截
# 门控2: ATTRACTIVENESS_SCORE_LOW - 内容吸引力评分<60分时拦截
# 门控3: DIFFERENTIATION_FAILED - 内容差异化相似度>70%时拦截
# PL-NOVEL/PL-DRAMA也含"营销注入"步骤,需门控检查(来源:实施计划v3 Step C/D)
_GATE_PIPELINE_TYPES = {"PL-VIDEO", "PL-IMAGE", "PL-AUDIO", "PL-LIPSYNC", "PL-COMIC", "PL-NOVEL", "PL-DRAMA",
                        "E2E-VIDEO", "E2E-IMAGE", "E2E-DAILY", "PL-ARTICLE-BATCH", "PL-COMIC-BATCH",
                        "PL-NOVEL-BATCH", "PL-VIDEO-BATCH", "PL-NEWPROD", "PL-HOTSPOT", "PL-PRODUCT"}

# ── call_skill: 通过subprocess调用SKILL exec脚本(来源:实施计划v3 Step A) ──
import re as _re_module
from pathlib import Path as _Path

_SKILL_NAME_RE = _re_module.compile(r'^[a-zA-Z0-9_-]+$')
_PROJECT_ROOT = _Path(os.environ.get("PORTAL_PROJECT_ROOT", "d:/JueJin")).resolve()
if not (_PROJECT_ROOT / "skills").exists():
    _docker_root = _Path("/app")
    if _docker_root.exists() and (_docker_root / "skills").exists():
        _PROJECT_ROOT = _docker_root

# 非MCP工具(需通过call_skill调用的SKILL exec脚本)
# Phase2: _SKILL_TOOLS保留为fallback，实际路由由_is_skill_tool()运行时推断
# R33防还原: 移除xianyu-publisher(管道已改用fishclaw-mcp),移除fortune-teller和novel_bridge(不存在)
# geo-content-optimizer: exec文件名为geo_optimizer.py(非标准geo_content_optimizer.py),需fallback
_SKILL_TOOLS = {"novel-to-script", "series-manager", "title-generator", "geo-content-optimizer"}

# Phase2: MCP server列表缓存(进程级，openclaw.json不常变)
_MCP_SERVERS_CACHE: set | None = None

def _is_skill_tool(tool_name: str) -> bool:
    """Phase2: 运行时推断tool是Skill还是MCP

    启发式规则(与call_skill()的3候选路径一致):
    1. 是MCP server → False (走call_mcp)
    2. 有exec脚本(skills/{tool}/scripts/或_lazy/或content-orchestrator本地) → True (走call_skill)
    3. 无exec脚本 → False (走call_mcp,可能是MCP tool或不存在)

    这消除了_SKILL_TOOLS硬编码集合的需求：
    - 新增Skill无需修改代码(自动检测exec脚本)
    - 删除Skill时自动失效(文件不存在→返回False→走MCP路径→MCP_NOT_CONFIGURED)
    """
    global _MCP_SERVERS_CACHE
    skills_dir = _Path(__file__).parent.parent.parent  # d:\JueJin\skills

    # Phase2fix: 先填充MCP缓存(无论后续判断如何,都需要MCP缓存)
    if _MCP_SERVERS_CACHE is None:
        try:
            openclaw_path = skills_dir.parent / "openclaw.json"
            config = atomic_read_json(openclaw_path)
            _MCP_SERVERS_CACHE = set(config.get("mcp", {}).get("servers", {}).keys())
        except Exception as e:
            logger.warning(f"Unexpected error: {e}", exc_info=True)
            _MCP_SERVERS_CACHE = set()

    # 规则1: 是MCP server → 走call_mcp
    if tool_name in _MCP_SERVERS_CACHE:
        return False

    # 规则2: 检查exec脚本是否存在(4个位置,与call_skill()一致)
    # BUG-V3-004修复(2026-07-14): 添加scripts/目录作为fallback路径
    # 基础设施审计修复: self_growth_activator已更名为self-growth,使用标准Skill路径
    script_name = tool_name.replace('-', '_')
    has_exec = (skills_dir / tool_name / "scripts" / f"{script_name}.py").exists() or \
               (skills_dir / "_lazy" / tool_name / "scripts" / f"{script_name}.py").exists() or \
               (skills_dir / "content-orchestrator" / "scripts" / f"{script_name}.py").exists() or \
               (skills_dir.parent / "scripts" / f"{script_name}.py").exists()
    if has_exec:
        return True

    # 规则3: _SKILL_TOOLS fallback(保留为fallback,Phase2设计)
    # 运行时推断未找到exec脚本时,检查硬编码集合(声明式Skill或exec在非标准路径)
    if tool_name in _SKILL_TOOLS:
        return True

    # 规则4: 无exec脚本且不在_SKILL_TOOLS → 走call_mcp(可能是MCP tool或不存在)
    return False

# BUG-FIX(2026-08-05): 管道步骤间content字段保持
# 根因: previous_output被每步的data完全替换,当中间步骤(品牌Profile/IP特质/写作风格)的
# 输出不包含content字段时,步骤1生成的内容丢失,导致步骤9"去AI味"收到空content。
# 修复: 每步输出后,从旧previous_output继承缺失的关键字段(content/title/topic/platform)。
# BUG-FIX R3-L2.4(2026-08-06): 添加content_id到保持字段,确保发布步骤能获取内容ID
_PRESERVE_FIELDS = {"content", "title", "topic", "platform", "platforms", "text", "markdown", "content_id", "audio_url", "video_url", "image_urls", "script_text", "characters", "storyboard", "video_path", "audio_path", "images", "asset_id", "keywords", "tenant_id", "task_id"}

# 内容覆盖字段: 当步骤返回这些字段时,用它们覆盖content(修复数据流断裂)
# 根因: SEO/GEO/营销/去AI味/排版等步骤修改内容后以不同字段名返回,导致修改被静默丢弃
_CONTENT_OVERRIDE_FIELDS = ("polished_content", "adapted_content", "geo_optimized_content", "optimized_content", "formatted_content", "script_text")

def _merge_step_output(prev_output: dict, step_data: dict) -> dict:
    """合并步骤输出,保持关键内容字段不断链(微创修复)

    当步骤输出不含content等字段时,从前一步输出继承,确保内容生成→去AI味→营销注入→SEO的content链路完整。
    新增: 当步骤返回内容覆盖字段(polished_content/adapted_content等)时,自动覆盖content字段。
    """
    if not isinstance(step_data, dict):
        return {"raw_output": step_data}
    merged = dict(step_data)
    # 内容覆盖: 当步骤返回优化后的内容字段时,用它覆盖content(修复数据流断裂P0)
    for _override_field in _CONTENT_OVERRIDE_FIELDS:
        if _override_field in merged and merged[_override_field]:
            merged["content"] = merged[_override_field]
            break
    for field in _PRESERVE_FIELDS:
        if field not in merged and field in prev_output:
            merged[field] = prev_output[field]
    return merged

def call_skill(skill_name: str, action: str, params: dict) -> dict[str, Any]:
    """通过subprocess调用SKILL的exec脚本(安全版,来源:实施计划v3 Step A)

    Args:
        skill_name: SKILL名称(kebab-case)
        action: 操作类型
        params: 参数字典

    Returns:
        {success: bool, data: dict, error: str|null, code: str|null}
    """
    # 1. 白名单校验(防路径遍历,来源:R2-安全审查R9.2)
    if not _SKILL_NAME_RE.match(skill_name):
        return {"success": False, "data": {}, "error": f"skill_name格式非法: {skill_name}", "code": "SKILL_NAME_INVALID"}

    # 2. 定位exec脚本(先skills/后_lazy/后content-orchestrator本地后scripts/)
    # BUG-V3-004修复(2026-07-14): 添加scripts/目录作为fallback路径
    script_name = skill_name.replace('-', '_')
    candidates = [
        _PROJECT_ROOT / "skills" / skill_name / "scripts" / f"{script_name}.py",
        _PROJECT_ROOT / "skills" / "_lazy" / skill_name / "scripts" / f"{script_name}.py",
        _PROJECT_ROOT / "skills" / "content-orchestrator" / "scripts" / f"{script_name}.py",
        _PROJECT_ROOT / "scripts" / f"{script_name}.py",
    ]
    script_path = None
    for c in candidates:
        if c.exists():
            script_path = c
            break
    if not script_path:
        return {"success": False, "data": {}, "error": f"SKILL脚本不存在: {skill_name}", "code": "SKILL_NOT_FOUND"}

    # 3. Path.relative_to安全校验(防路径穿越,来源:R2-安全审查路径安全)
    try:
        script_path.resolve().relative_to(_PROJECT_ROOT)
    except ValueError:
        return {"success": False, "data": {}, "error": "路径穿越检测", "code": "PATH_TRAVERSAL"}

    # 4. subprocess调用(列表形式,无shell=True)
    cmd = [sys.executable, str(script_path), "--action", action, "--params", json.dumps(params, ensure_ascii=False)]
    # BUG-AUDIT-015修复: 同时通过stdin传递数据(40个Skill使用stdin模式而非--params)
    # stdin payload格式: {"action": action, **params} - 兼容content_template/video_generator等stdin Skills
    stdin_payload = json.dumps({"action": action, **params}, ensure_ascii=False)
    try:
        # v2.6修复(BUG-E2E-020): 添加PYTHONUTF8=1环境变量+errors=replace
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=300,
            encoding="utf-8", errors="replace", cwd=str(_PROJECT_ROOT),
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
            input=stdin_payload,
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout.strip())
            except json.JSONDecodeError:
                return {"success": False, "data": {}, "error": f"JSON解析失败: {result.stdout[:200]}", "code": "JSON_PARSE_ERROR"}
        else:
            # v2.7修复(BUG-E2E-024): SKILL exec脚本在success=false时exit(1),但错误JSON已打印到stdout
            # 必须先尝试解析stdout获取真实错误信息,仅当stdout无有效JSON时才回退到stderr
            stdout_text = result.stdout.strip() if result.stdout else ""
            if stdout_text:
                try:
                    parsed = json.loads(stdout_text)
                    if isinstance(parsed, dict) and "success" in parsed:
                        return parsed
                except json.JSONDecodeError as e:
                    # P1-15修复: JSON解析失败需记录(原except:pass)
                    logger.error(f"_call_skill stdout JSON解析失败: {e}")
            return {"success": False, "data": {}, "error": result.stderr[:500] if result.stderr else "SKILL执行失败(无输出)", "code": "SKILL_EXEC_FAILED"}
    except subprocess.TimeoutExpired:
        return {"success": False, "data": {}, "error": f"SKILL执行超时(300秒): {skill_name}", "code": "SKILL_TIMEOUT"}
    except FileNotFoundError:
        return {"success": False, "data": {}, "error": f"SKILL脚本未找到: {script_path}", "code": "SKILL_NOT_FOUND"}

def _check_marketing_gate(step_result: dict, step_params: dict) -> dict:
    """门控1: 营销注入门控检查(来源:SKILL.md§营销注入门控)

    检查market-copywriter是否成功注入营销元素,失败时尝试降级模板重试1次。

    Returns:
        {passed: bool, error: str|null, code: str|null, data: dict}
    """
    if step_result.get("success", False):
        return {"passed": True, "error": None, "code": None, "data": step_result.get("data", {})}

    # 降级策略: 使用品类差异化基础营销模板(来源:SKILL.md§降级策略)
    # 此处仅记录降级意图,实际降级由market-copywriter Skill内部处理
    logger.warning("[content-orchestrator] 营销注入失败,尝试降级模板重试")
    # 注意: 降级重试逻辑由execute_pipeline在门控失败时触发1次重试
    return {
        "passed": False,
        "error": f"营销注入门控失败: {step_result.get('error', 'market-copywriter调用失败')}",
        "code": "MARKETING_GATE_FAILED",
        "data": {},
    }

def _check_attractiveness_score(step_result: dict, step_params: dict) -> dict:
    """门控2: 内容吸引力评分门控(来源:SKILL.md§内容吸引力评分门控)

    调用LLM对生成内容进行0-100分评分,<60分则拦截。

    Returns:
        {passed: bool, error: str|null, code: str|null, data: dict}
    """
    try:
        # llm_chat统一入口(内部处理API Key,无需手动检查SILICONFLOW_API_KEY)
        from mcps.shared.unified_llm import llm_chat

        content_data = step_result.get("data", {})
        title = content_data.get("title", step_params.get("topic", ""))
        summary = content_data.get("summary", content_data.get("content", ""))[:500]
        platform = step_params.get("platform", "通用")

        prompt = f"""你是一位内容营销评分专家。请对以下内容进行吸引力评分(0-100分)。

目标平台: {platform}
内容标题: {title}
内容摘要: {summary}

评分维度:
1. 标题吸引力(权重30%): 是否包含数字/疑问/对比/悬念等钩子元素
2. 开头3秒钩子(权重25%): 前50字是否能抓住注意力
3. 内容深度(权重20%): 是否有独特见解/数据支撑/实操步骤
4. CTA清晰度(权重15%): 行动号召是否明确可执行
5. SEO适配度(权重10%): 关键词布局是否合理

严格输出JSON:
{{"title_score": N, "hook_score": N, "depth_score": N, "cta_score": N, "seo_score": N, "total_score": N, "suggestion": "优化建议"}}"""

        # BUG-FIX(2026-08-05): 原代码硬编码provider="siliconflow",余额不足时403直接失败。
        # 移除provider和model参数,让llm_chat使用默认fallback链(9router→siliconflow→zhipu→sensenova→dashscope)
        resp = llm_chat(
            prompt=prompt,
            system_prompt="",
            caller="content-orchestrator",
            temperature=0.3,
        )

        if not resp.get("success"):
            logger.warning(f"[content-orchestrator] 吸引力评分LLM调用失败: {resp.get('error', '')},跳过门控")
            return {"passed": True, "error": None, "code": None, "data": {"score_skipped": True}}

        # 解析LLM返回的JSON评分
        content_text = resp.get("raw_text", "")
        # 提取JSON部分
        import re
        json_match = re.search(r'\{[^{}]*"total_score"[^{}]*\}', content_text, re.DOTALL)
        if not json_match:
            logger.warning("[content-orchestrator] 吸引力评分LLM返回格式异常,跳过门控")
            return {"passed": True, "error": None, "code": None, "data": {"score_skipped": True}}

        score_data = json.loads(json_match.group())
        total_score = score_data.get("total_score", 0)

        logger.info(f"[content-orchestrator] 吸引力评分: {total_score}/100 (标题{score_data.get('title_score')}/钩子{score_data.get('hook_score')}/深度{score_data.get('depth_score')}/CTA{score_data.get('cta_score')}/SEO{score_data.get('seo_score')})")

        if total_score < 60:
            return {
                "passed": False,
                "error": f"内容吸引力评分不达标: {total_score}/100 (需≥60), 优化建议: {score_data.get('suggestion', '无')}",
                "code": "ATTRACTIVENESS_SCORE_LOW",
                "data": {"score": total_score, "suggestion": score_data.get("suggestion")},
            }

        return {"passed": True, "error": None, "code": None, "data": {"score": total_score}}

    except Exception as e:
        logger.error(f"[content-orchestrator] 吸引力评分LLM调用失败,跳过门控(非安全红线): {e}")
        return {"passed": True, "error": None, "code": None, "data": {"score_skipped": True, "error": str(e)}}

def _check_differentiation(step_params: dict, tenant_id: str) -> dict:
    """门控3: 内容差异化检查(来源:SKILL.md§内容差异化检查)

    检查24小时内同主题内容的相似度,>70%则拦截。

    Returns:
        {passed: bool, error: str|null, code: str|null, data: dict}
    """
    try:
        topic = step_params.get("topic", "")
        if not topic:
            return {"passed": True, "error": None, "code": None, "data": {"diff_skipped": True}}

        # 查询24小时内同主题已发布内容的差异化维度
        # 延迟导入避免循环依赖
        sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts")))
        from mcps.shared.atomic_write import atomic_read_json

        # 读取24小时内已发布内容记录(简化实现: 检查content_pipelines目录)
        pipelines_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "content_pipelines")
        if not os.path.exists(pipelines_dir):
            return {"passed": True, "error": None, "code": None, "data": {"diff_skipped": True, "reason": "no_history"}}

        # 简化相似度检查: 检查同主题内容数量
        similar_count = 0
        now = datetime.now()
        for fname in os.listdir(pipelines_dir):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(pipelines_dir, fname)
            try:
                data = atomic_read_json(fpath)
                if not data:
                    continue
                # 检查是否24小时内
                created_at = data.get("created_at", "")
                if created_at:
                    try:
                        created_time = datetime.fromisoformat(created_at.replace("Z", ""))
                        if (now - created_time).total_seconds() > 86400:  # 24小时
                            continue
                    except Exception as e:
                        logger.warning(f"Unexpected error: {e}", exc_info=True)
                        continue
                # 检查主题相似性(简化: 标题包含相同关键词)
                record_topic = data.get("topic", data.get("title", ""))
                if topic and record_topic and (topic in record_topic or record_topic in topic):
                    similar_count += 1
            except Exception as e:
                logger.warning(f"Unexpected error: {e}", exc_info=True)
                continue

        # 简化规则: 同主题内容>2条则认为相似度>70%(实际应调用LLM计算)
        if similar_count > 2:
            return {
                "passed": False,
                "error": f"内容差异化检查未通过: 24小时内已有{similar_count}条同主题内容,相似度>70%",
                "code": "DIFFERENTIATION_FAILED",
                "data": {"similar_count": similar_count, "suggestion": "调整至少1个差异化维度(切入角度/情绪基调/内容深度/表现形式)"},
            }

        return {"passed": True, "error": None, "code": None, "data": {"similar_count": similar_count}}

    except Exception as e:
        logger.error(f"[content-orchestrator] 差异化检查异常,跳过门控: {e}")
        return {"passed": True, "error": None, "code": None, "data": {"diff_skipped": True, "error": str(e)}}

# P0-5修复: 门控4 GEO评分≥60门控(来源:02手册§12.7 GEO优化规则)
GEO_PASS_THRESHOLD = 60
# S-01优化: GEO降级连续失败计数器,连续3次降级后转为硬拦截(防止无限降级放行)
_geo_fail_count = 0
_GEO_MAX_DEGRADE_COUNT = 3

def _check_geo_score(step_result: dict, step_params: dict) -> dict:
    """门控4: GEO评分门控检查(来源:02手册§12.7 + geo-content-optimizer SKILL.md)

    检查geo-content-optimizer返回的geo_score是否≥60,<60则拦截发布。
    geo-content-optimizer不可用时降级放行(记录warning)。
    S-01优化: 连续3次降级后转为硬拦截(passed=False),成功时重置计数器。

    Returns:
        {passed: bool, error: str|null, code: str|null, data: dict}
    """
    global _geo_fail_count
    try:
        if not step_result.get("success", False):
            # GEO优化步骤本身失败,降级放行(不阻塞发布链路)
            # S-01优化: 连续3次降级后转为硬拦截
            if _geo_fail_count >= _GEO_MAX_DEGRADE_COUNT:
                logger.error(f"[content-orchestrator] GEO优化连续降级{_geo_fail_count}次,转为硬拦截: {step_result.get('error', '')}")
                return {"passed": False, "error": f"GEO优化连续降级{_geo_fail_count}次,转为硬拦截(来源:S-01优化)", "code": "GEO_DEGRADE_LIMIT", "data": {"geo_skipped": True, "reason": "geo_optimize_failed", "degrade_count": _geo_fail_count}}
            _geo_fail_count += 1
            logger.warning(f"[content-orchestrator] GEO优化步骤失败,降级放行(第{_geo_fail_count}次): {step_result.get('error', '')}")
            return {"passed": True, "error": None, "code": None, "data": {"geo_skipped": True, "reason": "geo_optimize_failed", "degrade_count": _geo_fail_count}}

        geo_data = step_result.get("data", {})
        geo_score = geo_data.get("geo_score", 0)

        # geo_score不存在时降级放行(兼容旧版geo-content-optimizer)
        if geo_score == 0 and "geo_score" not in geo_data:
            # S-01优化: 连续3次降级后转为硬拦截
            if _geo_fail_count >= _GEO_MAX_DEGRADE_COUNT:
                logger.error(f"[content-orchestrator] GEO评分连续降级{_geo_fail_count}次,转为硬拦截")
                return {"passed": False, "error": f"GEO评分连续降级{_geo_fail_count}次,转为硬拦截(来源:S-01优化)", "code": "GEO_DEGRADE_LIMIT", "data": {"geo_skipped": True, "reason": "no_geo_score", "degrade_count": _geo_fail_count}}
            _geo_fail_count += 1
            logger.warning(f"[content-orchestrator] GEO评分未返回,降级放行(第{_geo_fail_count}次)")
            return {"passed": True, "error": None, "code": None, "data": {"geo_skipped": True, "reason": "no_geo_score", "degrade_count": _geo_fail_count}}

        if geo_score < GEO_PASS_THRESHOLD:
            return {
                "passed": False,
                "error": f"GEO评分门控失败: geo_score={geo_score} < {GEO_PASS_THRESHOLD}(来源:02手册§12.7)",
                "code": "GEO_SCORE_LOW",
                "data": {"geo_score": geo_score, "threshold": GEO_PASS_THRESHOLD, "suggestion": "增加结构化数据/FAQ Schema/AI引用潜力"},
            }

        # S-01优化: 成功通过时重置降级计数器
        _geo_fail_count = 0
        return {"passed": True, "error": None, "code": None, "data": {"geo_score": geo_score}}

    except Exception as e:
        # S-01优化: 连续3次降级后转为硬拦截
        if _geo_fail_count >= _GEO_MAX_DEGRADE_COUNT:
            logger.error(f"[content-orchestrator] GEO评分检查连续降级{_geo_fail_count}次,转为硬拦截: {e}")
            return {"passed": False, "error": f"GEO评分检查连续降级{_geo_fail_count}次,转为硬拦截(来源:S-01优化): {e}", "code": "GEO_DEGRADE_LIMIT", "data": {"geo_skipped": True, "error": str(e), "degrade_count": _geo_fail_count}}
        _geo_fail_count += 1
        logger.warning(f"[content-orchestrator] GEO评分检查异常,降级放行(第{_geo_fail_count}次): {e}")
        return {"passed": True, "error": None, "code": None, "data": {"geo_skipped": True, "error": str(e), "degrade_count": _geo_fail_count}}

# DEF-95 T07: 低分重试机制(评分<0.7时触发content-rewriter,最多2次)
_quality_retry_count: dict[str, int] = {}  # pipeline_id → retry count

def _check_quality_score_with_retry(step_result: dict, step_params: dict, pipeline_id: str = "") -> dict:
    """门控5: 内容质量评分低分重试(DEF-95 T07)

    检查content-calibrator评分, <0.7时触发content-rewriter重写+重评, 最多2次。
    重试2次后仍<0.7则降级放行(标记quality_warning),不阻塞管道。

    Returns:
        {passed: bool, error: str|null, code: str|null, data: dict}
    """
    try:
        score_data = step_result.get("data", {})
        score = float(score_data.get("score", 0)) if score_data.get("score") else 0

        if score >= 0.7:
            return {"passed": True, "error": None, "code": None, "data": score_data}

        # 低分触发重试
        retry_key = pipeline_id or step_params.get("topic", "default")
        current_retries = _quality_retry_count.get(retry_key, 0)

        if current_retries >= 2:
            logger.warning(f"[content-orchestrator] 质量评分{score}<0.7, 已重试{current_retries}次, 降级放行")
            _quality_retry_count[retry_key] = 0  # 重置
            score_data["quality_warning"] = True
            score_data["retry_count"] = current_retries
            return {"passed": True, "error": f"质量评分{score}低于0.7, 已重试{current_retries}次仍不达标, 降级放行", "code": "QUALITY_LOW_DEGRADED", "data": score_data}

        # 触发content-rewriter重写
        logger.info(f"[content-orchestrator] 质量评分{score}<0.7, 第{current_retries+1}次重试: 调用content-rewriter改进内容")
        content = step_params.get("content", score_data.get("content", ""))
        platform = step_params.get("platform", "")
        rewrite_result = call_skill("content-rewriter", "rewrite", {"content": content, "platform": platform, "reason": f"质量评分{score}低于0.7"})

        if rewrite_result.get("success"):
            improved_content = rewrite_result.get("data", {}).get("content", content)
            # 重新评分
            rescore_result = call_skill("content-calibrator", "score", {"content": improved_content, "platform": platform})
            if rescore_result.get("success"):
                new_score = float(rescore_result.get("data", {}).get("score", 0))
                logger.info(f"[content-orchestrator] 重试{current_retries+1}次后评分: {score}→{new_score}")
                _quality_retry_count[retry_key] = current_retries + 1
                if new_score >= 0.7:
                    _quality_retry_count[retry_key] = 0
                    return {"passed": True, "error": None, "code": None, "data": rescore_result.get("data", {})}
                # 递归重试
                return _check_quality_score_with_retry(rescore_result, {**step_params, "content": improved_content}, pipeline_id)

        _quality_retry_count[retry_key] = current_retries + 1
        return {"passed": True, "error": f"质量评分{score}低于0.7, 重试{current_retries+1}次未改善, 继续执行", "code": "QUALITY_RETRY_EXHAUSTED", "data": score_data}

    except Exception as e:
        logger.error(f"[content-orchestrator] 质量评分重试检查异常(降级放行): {e}")
        return {"passed": True, "error": str(e), "code": "QUALITY_CHECK_ERROR", "data": {}}

def _validate_pipeline_json(data: dict, filename: str) -> bool:
    """验证pipeline.json的Schema格式

    P1修复: 防止格式错误的pipeline.json静默失败
    必须包含: pipeline_type(str), steps(list, 非空), 每步有name和tool字段

    Returns:
        True=验证通过, False=验证失败(已记录日志)
    """
    if not isinstance(data, dict):
        logger.error(f"[content-orchestrator] pipeline.json {filename} 根节点不是dict, 跳过")
        return False

    pt = data.get("pipeline_type", "")
    if not pt or not isinstance(pt, str):
        logger.error(f"[content-orchestrator] pipeline.json {filename} 缺少pipeline_type字段或类型错误, 跳过")
        return False

    steps = data.get("steps", [])
    if not isinstance(steps, list) or len(steps) == 0:
        logger.error(f"[content-orchestrator] pipeline.json {filename} steps字段不是非空list, 跳过")
        return False

    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            logger.error(f"[content-orchestrator] pipeline.json {filename} step[{i}] 不是dict, 跳过")
            return False
        if "name" not in step or "tool" not in step:
            logger.error(f"[content-orchestrator] pipeline.json {filename} step[{i}] 缺少name或tool字段, 跳过")
            return False

    # Phase4: 版本字段检查(可选,缺失时默认1.0.0)
    if "version" not in data:
        data["version"] = "1.0.0"
        logger.info(f"[content-orchestrator] pipeline.json {filename} 无version字段, 默认1.0.0")
    elif not isinstance(data["version"], str):
        logger.warning(f"[content-orchestrator] pipeline.json {filename} version字段不是str, 使用默认1.0.0")
        data["version"] = "1.0.0"

    return True

def _load_external_pipelines() -> dict:
    """扫描 skills/*/pipeline.json 和 plugins/*/pipeline.json 文件，加载外部管道定义

    Gap1修复: Pipeline配置化注册
    P1修复: 增加Schema验证，防止格式错误的JSON静默失败
    PLUGIN-MIGRATE-001: 扩展扫描 plugins/ 目录(插件物理存储),通过inode去重避免Junction重复

    Returns:
        外部管道字典 {pipeline_type: steps_list}，加载失败返回空字典
    """
    external = {}
    skills_dir = _Path(__file__).parent.parent.parent  # d:\JueJin\skills
    plugins_dir = skills_dir.parent / "plugins"  # d:\JueJin\plugins (PLUGIN-MIGRATE-001)
    try:
        # Phase2: 扫描 skills/*/pipeline.json 和 skills/*/pipelines/*.json
        pipeline_files = list(skills_dir.glob("*/pipeline.json")) + list(skills_dir.glob("*/pipelines/*.json"))
        # PLUGIN-MIGRATE-001: 同时扫描 plugins/*/pipeline.json 和 plugins/*/pipelines/*.json
        if plugins_dir.exists():
            pipeline_files += list(plugins_dir.glob("*/pipeline.json")) + list(plugins_dir.glob("*/pipelines/*.json"))
        # 去重: 通过inode避免Junction链接导致的重复扫描
        seen_inodes = set()
        unique_files = []
        for pf in pipeline_files:
            try:
                st = pf.stat()
                inode_key = (st.st_dev, st.st_ino)
                if inode_key not in seen_inodes:
                    seen_inodes.add(inode_key)
                    unique_files.append(pf)
            except OSError:
                unique_files.append(pf)
        for pipeline_file in unique_files:
            try:
                data = atomic_read_json(pipeline_file)
                # P1修复: Schema验证
                if not _validate_pipeline_json(data, pipeline_file.name):
                    continue
                pt = data["pipeline_type"]
                steps = data["steps"]
                external[pt] = steps
                logger.info(f"[content-orchestrator] 加载外部管道 {pt} from {pipeline_file.name} ({len(steps)}步)")
            except (json.JSONDecodeError, OSError) as e:
                logger.warning(f"[content-orchestrator] 外部管道文件加载失败 {pipeline_file}: {e}")
    except Exception as e:
        logger.error(f"[content-orchestrator] 外部管道扫描异常: {e}")
    return external

# 外部管道缓存(进程级，避免每次调用都扫描文件系统)
_EXTERNAL_PIPELINES_CACHE: dict | None = None
_EXTERNAL_PIPELINES_MTIME: float = 0.0  # P2修复: 记录上次扫描时间

def _get_all_pipelines() -> dict:
    """获取全部管道(内置+外部)，带进程级缓存

    Gap1修复: Pipeline配置化注册
    P2修复: 增加mtime检查，pipeline.json变更后自动刷新缓存

    Phase2: 外部管道优先(管道定义已外置化到pipelines/*.json)。
    保留内置定义作为fallback。
    """
    global _EXTERNAL_PIPELINES_CACHE, _EXTERNAL_PIPELINES_MTIME
    import time
    # P2修复: 检查skills目录的最新mtime，变更则刷新缓存
    # Phase2: 同时检查 pipelines/*.json 的mtime
    skills_dir = _Path(__file__).parent.parent.parent
    try:
        all_pipelines = list(skills_dir.glob("*/pipeline.json")) + list(skills_dir.glob("*/pipelines/*.json"))
        current_mtime = max(f.stat().st_mtime for f in all_pipelines) if all_pipelines else 0
    except Exception as e:
        logger.warning(f"Unexpected error: {e}", exc_info=True)
        current_mtime = 0

    if _EXTERNAL_PIPELINES_CACHE is None or current_mtime > _EXTERNAL_PIPELINES_MTIME:
        _EXTERNAL_PIPELINES_CACHE = _load_external_pipelines()
        _EXTERNAL_PIPELINES_MTIME = current_mtime
    return _EXTERNAL_PIPELINES_CACHE

# 删除影响修复: Pipeline步骤工具覆盖机制
# 问题: PL-DRAMA硬编码"novel-to-script"，删除该Skill会导致管道断裂
# 修复: 通过data/pipeline_overrides.json可重定向到替代工具，无需改代码
_PIPELINE_OVERRIDES_CACHE: dict | None = None

def _load_pipeline_overrides() -> dict:
    """加载pipeline步骤工具覆盖配置

    从data/pipeline_overrides.json加载，允许在不修改代码的情况下
    将pipeline步骤中的tool字段重定向到替代Skill/MCP。
    格式: {pipeline_name: {step_name: {tool: new_tool}}}

    Returns:
        覆盖配置字典
    """
    global _PIPELINE_OVERRIDES_CACHE
    if _PIPELINE_OVERRIDES_CACHE is not None:
        return _PIPELINE_OVERRIDES_CACHE

    overrides_path = _PROJECT_ROOT / "data" / "pipeline_overrides.json"
    try:
        data = atomic_read_json(overrides_path)
        # 过滤掉以_开头的元数据键
        _PIPELINE_OVERRIDES_CACHE = {
            k: v for k, v in data.items()
            if not k.startswith("_") and isinstance(v, dict)
        }
        logger.info(f"[content-orchestrator] 加载pipeline覆盖配置: {len(_PIPELINE_OVERRIDES_CACHE)}个管道")
    except FileNotFoundError:
        _PIPELINE_OVERRIDES_CACHE = {}
    except Exception as e:
        logger.error(f"[content-orchestrator] 加载pipeline_overrides.json失败: {e}")
        _PIPELINE_OVERRIDES_CACHE = {}

    return _PIPELINE_OVERRIDES_CACHE

def _apply_pipeline_overrides(pipeline_type: str, steps: list) -> list:
    """应用pipeline步骤工具覆盖

    Args:
        pipeline_type: 管道类型
        steps: 原始步骤列表

    Returns:
        应用覆盖后的步骤列表(深拷贝)
    """
    overrides = _load_pipeline_overrides()
    if pipeline_type not in overrides:
        return steps

    pipeline_override = overrides[pipeline_type]
    result = []
    for step in steps:
        step_copy = dict(step)
        step_name = step_copy.get("name", "")
        if step_name in pipeline_override:
            new_tool = pipeline_override[step_name].get("tool")
            if new_tool and new_tool != step_copy.get("tool"):
                old_tool = step_copy.get("tool", "")
                step_copy["tool"] = new_tool
                step_copy["_overridden_from"] = old_tool
                logger.info(f"[content-orchestrator] 管道{pipeline_type}步骤'{step_name}'工具覆盖: {old_tool}→{new_tool}")
                # Phase2: 不再需要手动更新_SKILL_TOOLS，_is_skill_tool()运行时自动推断
        result.append(step_copy)

    return result

def _check_skill_exists(skill_name: str) -> bool:
    """检查Skill的exec脚本是否存在

    删除影响修复: 在执行pipeline前预检所有Skill是否存在，
    避免执行到中途才发现Skill不存在。

    Args:
        skill_name: Skill名称(kebab-case)

    Returns:
        True如果Skill脚本存在
    """
    script_name = skill_name.replace('-', '_')
    candidates = [
        _PROJECT_ROOT / "skills" / skill_name / "scripts" / f"{script_name}.py",
        _PROJECT_ROOT / "skills" / "_lazy" / skill_name / "scripts" / f"{script_name}.py",
        _PROJECT_ROOT / "skills" / "content-orchestrator" / "scripts" / f"{script_name}.py",
    ]
    return any(c.exists() for c in candidates)

def _check_mcp_tools_availability(mcp_tools: list[dict[str, Any]]) -> dict[str, Any]:
    """检查MCP工具在openclaw.json中的配置状态

    读取openclaw.json的mcp.servers配置,检查每个MCP是否已配置且未disabled。
    仅记录warning,不阻断执行(步骤可能是optional的)。

    Args:
        mcp_tools: MCP工具列表 [{step, tool, optional}]

    Returns:
        {total_mcp_steps: int, unavailable: [{step, tool, reason, optional}], all_configured: bool}
    """
    unavailable: list[dict[str, Any]] = []

    try:
        openclaw_path = _PROJECT_ROOT / "openclaw.json"
        config = atomic_read_json(openclaw_path)
        servers_config = config.get("mcp", {}).get("servers", {})
    except Exception as e:
        logger.warning(f"[content-orchestrator] 读取openclaw.json失败,MCP可用性预检降级: {e}")
        for mcp in mcp_tools:
            unavailable.append({
                "step": mcp["step"],
                "tool": mcp["tool"],
                "reason": "CONFIG_READ_FAILED",
                "optional": mcp["optional"],
            })
        return {
            "total_mcp_steps": len(mcp_tools),
            "unavailable": unavailable,
            "all_configured": False,
        }

    for mcp in mcp_tools:
        tool_name = mcp["tool"]
        if tool_name not in servers_config:
            logger.warning(f"[content-orchestrator] MCP '{tool_name}'(步骤:{mcp['step']})未在openclaw.json中配置")
            unavailable.append({
                "step": mcp["step"],
                "tool": tool_name,
                "reason": "NOT_CONFIGURED",
                "optional": mcp["optional"],
            })
        else:
            server_entry = servers_config.get(tool_name)
            if isinstance(server_entry, dict) and server_entry.get("disabled", False):
                logger.warning(f"[content-orchestrator] MCP '{tool_name}'(步骤:{mcp['step']})已disabled")
                unavailable.append({
                    "step": mcp["step"],
                    "tool": tool_name,
                    "reason": "DISABLED",
                    "optional": mcp["optional"],
                })

    return {
        "total_mcp_steps": len(mcp_tools),
        "unavailable": unavailable,
        "all_configured": len(unavailable) == 0,
    }


def check_pipeline_skill_availability(pipeline_type: str) -> dict[str, Any]:
    """预检pipeline中所有Skill工具和MCP工具的可用性

    Skill可用性: 检查exec脚本文件是否存在
    MCP可用性: 检查openclaw.json中是否已配置且未disabled(仅warning,不阻断)

    Args:
        pipeline_type: 管道类型

    Returns:
        {all_available: bool, missing_skills: [{step, skill_name, optional}],
         total_skill_steps: int,
         mcp_availability: {total_mcp_steps: int, unavailable: [{step, tool, reason, optional}], all_configured: bool}}
    """
    try:
        steps = get_pipeline_steps(pipeline_type)
    except ValueError:
        return {
            "all_available": False,
            "missing_skills": [],
            "total_skill_steps": 0,
            "mcp_availability": {"total_mcp_steps": 0, "unavailable": [], "all_configured": True},
            "error": "管道不存在",
        }

    missing = []
    skill_count = 0
    mcp_tools: list[dict[str, Any]] = []
    for step in steps:
        tool = step.get("tool", "")
        # Phase2: 运行时推断替代硬编码_SKILL_TOOLS检查
        if _is_skill_tool(tool):
            skill_count += 1
            if not _check_skill_exists(tool):
                missing.append({
                    "step": step.get("name", ""),
                    "skill_name": tool,
                    "optional": step.get("optional", False),
                })
        else:
            # 非Skill工具即为MCP工具,收集用于可用性预检
            if tool:
                mcp_tools.append({
                    "step": step.get("name", ""),
                    "tool": tool,
                    "optional": step.get("optional", False),
                })

    # MCP可用性预检: 检查openclaw.json中是否已配置且未disabled(仅warning,不阻断执行)
    mcp_availability = _check_mcp_tools_availability(mcp_tools)

    return {
        "all_available": len(missing) == 0,
        "missing_skills": missing,
        "total_skill_steps": skill_count,
        "mcp_availability": mcp_availability,
    }

def get_pipeline_steps(pipeline_type: str) -> list[Any]:
    """返回指定管道的执行步骤列表

    Args:
        pipeline_type: 管道类型

    Returns:
        步骤列表，每步包含 name/tool/action/params

    Raises:
        ValueError: 管道类型不存在
    """
    pipelines = {
        # ── 5条内容管道 ──
        # BUG-233修复: PL-VIDEO步骤顺序与02手册§五5.2对齐
        # 02手册§五5.2正确顺序: 热点监控→选题策划→文案生成→视频生成→AI配图(可选)→口型同步(可选)→多平台发布
        # 旧实现缺失: 热点监控/选题策划/文案生成/AI配图/口型同步/多平台发布 6个步骤
        # 新实现: 在保留原有步骤基础上,按§5.2顺序补全缺失步骤
        "PL-VIDEO": [
            # §5.2前置阶段: 热点监控→选题策划→文案生成
            {"name": "热点监控", "tool": "dailyhot-mcp", "action": "get_multi_hot", "params": {"platforms": "bilibili,ithome,36kr"}},
            {"name": "选题策划", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {}},
            {"name": "文案生成", "tool": "content-template", "action": "generate", "params": {"template_type": "article"}},
            # §5.2视频生成阶段: 脚本→配音→画面→合成→字幕(保留原有步骤)
            {"name": "脚本生成", "tool": "narrato-mcp", "action": "generate_narration_script", "params": {}},
            {"name": "配音生成", "tool": "tts-adapter-mcp", "action": "synthesize", "params": {}},
            {"name": "画面生成", "tool": "kling-mcp", "action": "kling_text_to_video", "params": {}},
            {"name": "视频合成", "tool": "video-generator", "action": "compose_video", "params": {}},
            # BUG-231修复: 添加字幕生成步骤(来源:02手册§五5.2视频内容必须有字幕)
            {"name": "字幕生成", "tool": "video-generator", "action": "generate_subtitle", "params": {"subtitle_style": "default", "font_size": 24}},
            # R5修复: 移除optional标记，默认全部步骤齐备(来源:用户要求"不存在可选步骤")
            {"name": "AI配图", "tool": "flux-mcp", "action": "generate_image", "params": {}},
            {"name": "口型同步", "tool": "liveportrait-mcp", "action": "generate_lip_sync", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            # §5.2发布阶段: 多平台发布
            {"name": "多平台发布", "tool": "content-publisher", "action": "publish_now", "params": {}},
        ],
        "PL-IMAGE": [
            {"name": "文案生成", "tool": "content-template", "action": "generate", "params": {"template_type": "article"}},
            {"name": "配图生成", "tool": "flux-mcp", "action": "generate_image", "params": {"prompt": "${prev_output.content}"}},
            # V43修复: visual-content-generator→content-formatter(与外部JSON管道对齐,排版用format_engine)
            {"name": "图文排版", "tool": "content-formatter", "action": "format", "params": {"content": "${prev_output.content}", "platform": "${platform}", "format_level": "auto"}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS,
        "PL-AUDIO": [
            {"name": "文案生成", "tool": "content-template", "action": "generate", "params": {"template_type": "article"}},
            {"name": "语音合成", "tool": "tts-adapter-mcp", "action": "synthesize", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS,
        "PL-LIPSYNC": [
            {"name": "语音生成", "tool": "tts-adapter-mcp", "action": "synthesize", "params": {}},
            {"name": "口型同步", "tool": "liveportrait-mcp", "action": "generate_lip_sync", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS,
        "PL-COMIC": [
            {"name": "角色画面生成", "tool": "character-consistency-mcp", "action": "generate_comic_panel", "params": {}},
            {"name": "分镜脚本生成", "tool": "narrato-mcp", "action": "generate_narration_script", "params": {}},
            {"name": "分镜转视频", "tool": "kling-mcp", "action": "kling_image_to_video", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS,
        # ── 2条小说/短剧管道(来源:实施计划v3 Step C/D) ──
        # P0-I修复: 删除内置PL-NOVEL定义,统一从pipelines/PL-NOVEL.json(v1.2.0)加载
        # 原因: 内置定义含"AI声明注入"(risk-detector.inject_ai_declaration),与外部JSON不一致
        #       外部JSON已移除此步骤改为"发布状态回写"(novel_bridge.publish_chapter)
        #       (P0-022新增发布状态回写,P2-010移除AI声明注入由content-publisher统一处理)
        # 外部JSON覆盖机制见L953-955(_get_all_pipelines→pipelines[ext_type]=ext_steps)
        # PL-NOVEL定义见: skills/content-orchestrator/pipelines/PL-NOVEL.json
        # P0-031修复(NEW-DEF-04): 删除内置PL-DRAMA定义,统一从pipelines/PL-DRAMA.json加载
        # 原因: 内置定义与外部JSON双定义,修改时易遗漏同步,导致fallback到旧定义
        # PL-DRAMA定义见: skills/content-orchestrator/pipelines/PL-DRAMA.json
        # ── 3条端到端管道 ──
        "E2E-VIDEO": [
            {"name": "选题", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {}},
            {"name": "脚本生成", "tool": "narrato-mcp", "action": "generate_narration_script", "params": {}},
            # R45同根因修复+BUG-V6-015: cosyvoice→tts-adapter-mcp(4层降级), text_to_video→kling_text_to_video
            {"name": "配音生成", "tool": "tts-adapter-mcp", "action": "synthesize", "params": {}},
            {"name": "画面生成", "tool": "kling-mcp", "action": "kling_text_to_video", "params": {}},
            {"name": "视频合成", "tool": "video-generator", "action": "compose_video", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            {"name": "视频发布", "tool": "sau-mcp", "action": "upload_video", "params": {}},
        ],
        "E2E-IMAGE": [
            {"name": "选题", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {}},
            {"name": "文案生成", "tool": "content-template", "action": "generate", "params": {"template_type": "article"}},
            {"name": "配图生成", "tool": "flux-mcp", "action": "generate_image", "params": {"prompt": "${prev_output.content}"}},
            # V43修复: visual-content-generator→content-formatter(与外部JSON管道对齐,排版用format_engine)
            {"name": "图文排版", "tool": "content-formatter", "action": "format", "params": {"content": "${prev_output.content}", "platform": "${platform}", "format_level": "auto"}},
            # R6-4修复: 移除重复的"内容审核"(sensitive-word-mcp)步骤
            # 原因: _MARKETING_SEO_GEO_REVIEW_STEPS末尾已包含sensitive-word-mcp检查(发布前最终审核)
            #       content-qa-guard的15维风险检测也覆盖敏感词维度,无需在此重复调用
            {"name": "合规风控(U19)", "tool": "content-qa-guard", "action": "check", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            {"name": "图文发布", "tool": "content-publisher", "action": "publish_now", "params": {}},
        ],
        "E2E-DAILY": [
            {"name": "热点获取", "tool": "dailyhot-mcp", "action": "get_multi_hot", "params": {"platforms": "bilibili,ithome,36kr"}},
            {"name": "选题决策", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {}},
            {"name": "文案生成", "tool": "content-template", "action": "generate", "params": {"template_type": "article"}},
            {"name": "配图生成", "tool": "flux-mcp", "action": "generate_image", "params": {"prompt": "${prev_output.content}"}},
            # V43修复: visual-content-generator→content-formatter(与外部JSON管道对齐,排版用format_engine)
            {"name": "图文排版", "tool": "content-formatter", "action": "format", "params": {"content": "${prev_output.content}", "platform": "${platform}", "format_level": "auto"}},
            # R6-4修复: 移除重复的"内容审核"(sensitive-word-mcp)步骤
            # 原因: _MARKETING_SEO_GEO_REVIEW_STEPS末尾已包含sensitive-word-mcp检查(发布前最终审核)
            #       content-qa-guard的15维风险检测也覆盖敏感词维度,无需在此重复调用
            {"name": "合规风控(U19)", "tool": "content-qa-guard", "action": "check", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            {"name": "多平台发布", "tool": "content-publisher", "action": "publish_now", "params": {}},
            {"name": "排期调度", "tool": "content-publisher", "action": "schedule_smart", "params": {"preferred_time": "auto"}, "description": "智能排期发布(DEF-07修复): 调用content-publisher的schedule_smart，根据平台活跃时段自动排期"},
        ],
        # ── v1.1 新增: 9商品内容生产专属管道(2026-06-03) ──
        # 复用PL-VIDEO/PL-IMAGE/PL-LIPSYNC能力,商品级编排
        # 来源: xianyu-publisher/SKILL.md v1.1 NEW-PROD-01~09 + 2026年6月全网搜索内容矩阵规划
        "PL-NEWPROD": [
            {"name": "商品信息拉取", "tool": "fishclaw-mcp", "action": "get_item_stats", "params": {"product_id": "all"}},
            {"name": "热点监控", "tool": "dailyhot-mcp", "action": "get_multi_hot", "params": {"platforms": "bilibili,ithome,36kr"}},
            {"name": "选题决策", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {"focus": "new_product_promotion"}},
            {"name": "文案生成(商品介绍)", "tool": "content-template", "action": "generate", "params": {"template_type": "product_intro"}},
            # R10修复(管道断点Problem 3): 原步骤使用不存在的content-orchestrator-router/route_by_product
            # 替换为实际MCP调用: flux-mcp生成配图 + ${engine.video}按套餐生成视频
            {"name": "商品配图生成", "tool": "flux-mcp", "action": "generate_image", "params": {"prompt": "${prev_output.content}"}},
            {"name": "商品视频生成", "tool": "kling-mcp", "action": "kling_text_to_video", "params": {"script": "${prev_output.content}"}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            # DEF-01修复: 调用fishclaw-mcp.publish_item实际发布闲鱼商品(与PL-HOTSPOT/PL-PRODUCT一致)
            {"name": "闲鱼商品发布", "tool": "fishclaw-mcp", "action": "publish_item", "params": {"title": "", "account_id": "default"}},
            {"name": "多平台发布(抖音+小红书+视频号)", "tool": "content-publisher", "action": "publish_now", "params": {"platforms": ["douyin", "xiaohongshu", "shipinhao"]}},
            {"name": "排期调度", "tool": "content-publisher", "action": "schedule_smart", "params": {"preferred_time": "auto"}},
            # R10修复(管道断点): track_performance action不存在于content_analytics.py(仅支持analyze/batch)
            # 改为batch(批量分析最近3天内容表现,72h≈3天)
            {"name": "效果分析(72h后)", "tool": "content-analytics", "action": "batch", "params": {"days": "3"}},
        ],
        # ── v1.2 新增: 热点驱动+素材驱动管道(来源:09设计文档U7) ──
        # PL-HOTSPOT: 热点→选品→竞品→分析→闲鱼商品发布+多平台内容分发
        # DEF-01修复(TECH-DEBT-032): 闲鱼商品发布改用fishclaw-mcp.publish_item(实际MCP工具)
        # 原xianyu-publisher是SKILL(梯度SKU生成)非MCP,调用会MCP_NOT_CONFIGURED断裂
        "PL-HOTSPOT": [
            {"name": "热点获取", "tool": "dailyhot-mcp", "action": "get_multi_hot", "params": {"platforms": "bilibili,ithome,36kr"}},
            {"name": "选品方向", "tool": "content-research-mcp", "action": "generate_topic_suggestions", "params": {"focus": "hot_trend"}},
            {"name": "竞品采集", "tool": "media-crawler-mcp", "action": "search_posts", "params": {}},
            {"name": "选品分析", "tool": "content-research-mcp", "action": "search_wechat_articles", "params": {}},
            {"name": "商品参数生成", "tool": "content-template", "action": "generate", "params": {"template_type": "product_hot"}},
            {"name": "合规风控(U19)", "tool": "content-qa-guard", "action": "check", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            # DEF-01修复: 调用fishclaw-mcp.publish_item(title, account_id)实际发布闲鱼商品
            {"name": "闲鱼商品发布", "tool": "fishclaw-mcp", "action": "publish_item", "params": {"title": "", "account_id": "default"}},
            {"name": "多平台内容分发", "tool": "content-publisher", "action": "publish_now", "params": {}},
            {"name": "发布反馈(U13)", "tool": "self-growth", "action": "learn", "params": {"category": "publish_feedback", "importance": 5}},
        ],
        # PL-PRODUCT: 素材检索→素材匹配→规格转换→风格转换→5要素注入→合规→[品牌+营销+SEO+GEO+防查重+评分+审核]→闲鱼商品发布+多平台分发
        # V43修复: 移除重复品牌Profile注入(已由_MARKETING_SEO_GEO_REVIEW_STEPS中的_IP_STYLE_DEAI_STEPS统一提供)
        # DEF-01修复(TECH-DEBT-032): 闲鱼商品发布改用fishclaw-mcp.publish_item(实际MCP工具)
        "PL-PRODUCT": [
            {"name": "素材检索", "tool": "agency-portal-mcp", "action": "portal_list_assets", "params": {}},
            {"name": "素材匹配评分", "tool": "content-orchestrator", "action": "match_materials", "params": {}},
            {"name": "图片规格转换", "tool": "flux-mcp", "action": "generate_image", "params": {"prompt": "${prev_output.content}"}},
            {"name": "文案风格转换", "tool": "content-template", "action": "generate", "params": {"template_type": "product_brand"}},
            # R10修复(管道断点): inject_marketing_elements action不存在于content_template.py
            # 改为market-copywriter.full_copywriting(涵盖卖点/痛点/信任/稀缺/行动5要素)
            {"name": "5要素注入(卖点/痛点/信任/稀缺/行动)", "tool": "market-copywriter", "action": "full_copywriting", "params": {}},
            {"name": "合规风控(U19)", "tool": "content-qa-guard", "action": "check", "params": {}},
        ] + _MARKETING_SEO_GEO_REVIEW_STEPS + [
            # DEF-01修复: 调用fishclaw-mcp.publish_item(title, account_id)实际发布闲鱼商品
            {"name": "闲鱼商品发布", "tool": "fishclaw-mcp", "action": "publish_item", "params": {"title": "", "account_id": "default"}},
            {"name": "多平台内容分发", "tool": "content-publisher", "action": "publish_now", "params": {}},
            {"name": "发布反馈(U13)", "tool": "self-growth", "action": "learn", "params": {"category": "publish_feedback", "importance": 5}},
        ],
    }

    # Phase2: 外部管道优先(管道定义已外置化到pipelines/*.json)
    # 保留内置定义作为fallback(当pipeline.json被删除时仍可用)
    external = _get_all_pipelines()
    for ext_type, ext_steps in external.items():
        pipelines[ext_type] = ext_steps  # 外部覆盖内置

    if pipeline_type not in pipelines:
        raise ValueError(f"未知管道类型: {pipeline_type}，支持: {list(pipelines.keys())}")

    # 删除影响修复: 应用pipeline步骤工具覆盖(从data/pipeline_overrides.json加载)
    return _apply_pipeline_overrides(pipeline_type, pipelines[pipeline_type])

def _query_tenant_assets(tenant_id: str) -> list:
    """查询租户素材库，通过agency-portal-mcp的portal_list_assets获取租户上传的素材

    Args:
        tenant_id: 租户ID

    Returns:
        素材列表，每个元素包含 url/file_path/asset_type/description 等字段。
        查询失败时返回空列表（降级到AI生成）。
    """
    try:
        import subprocess
        # R10修复: 原硬编码skills/agency-asset-manager/路径,实际文件在skills/_lazy/下
        # 尝试两个路径: skills/ (核心) 和 skills/_lazy/ (懒加载)
        script_path = None
        for _candidate in [
            "skills/agency-asset-manager/scripts/asset_manager.py",
            "skills/_lazy/agency-asset-manager/scripts/asset_manager.py",
        ]:
            if os.path.exists(_candidate):
                script_path = _candidate
                break
        if not script_path:
            logger.warning("[_query_tenant_assets] asset_manager.py not found in skills/ or skills/_lazy/")
            return []
        result = subprocess.run(
            [sys.executable, script_path, "--action", "list", "--tenant_id", tenant_id],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=15, cwd=os.getcwd(),
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if data.get("success"):
                assets = data.get("data", {}).get("assets", [])
                if assets:
                    return assets
    except Exception as e:
        logger.error(f"content orchestrator异常: {e}", exc_info=True)
        logger.warning(f"[content-orchestrator] 素材查询降级(非关键): {type(e).__name__}: {e}")
    return []

def orchestrate_pipeline(pipeline_type: str, params: dict) -> dict[str, Any]:
    """编排指定管道的内容生成+发布流程

    Args:
        pipeline_type: 管道类型 (PL-VIDEO/PL-IMAGE/PL-AUDIO/PL-LIPSYNC/PL-COMIC/E2E-VIDEO/E2E-IMAGE/E2E-DAILY)
        params: 管道参数 (topic/direction/tenant_id/platforms等)

    Returns:
        {success: bool, data: {pipeline_type, steps_completed, results}, error: str|null, code: str|null}
    """
    try:
        # 租户隔离校验：代运营场景必须传入tenant_id
        tenant_id = params.get("tenant_id", "")
        if tenant_id:
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+$', tenant_id):
                return {"success": False, "data": {}, "error": f"tenant_id格式非法: {tenant_id}", "code": "TENANT_ID_INVALID"}

        # 查询租户素材库：代运营场景下优先使用租户上传的素材
        tenant_assets = []
        if tenant_id:
            tenant_assets = _query_tenant_assets(tenant_id)

        steps = get_pipeline_steps(pipeline_type)
        results = []

        for i, step in enumerate(steps):
            step_params = dict(step.get("params", {}))
            # BUG-FIX(2026-08-05): agency-portal-mcp工具需要token参数进行身份验证。
            # 管道步骤params中通常不包含token,从pipeline_params的_session_token注入。
            # 只对agency-portal-mcp的工具注入,避免影响其他MCP工具。
            if step.get("tool") == "agency-portal-mcp" and "token" not in step_params:
                _session_token = params.get("_session_token", "")
                if _session_token:
                    step_params["token"] = _session_token
                    logger.info(f"[content-orchestrator] BUG-FIX: 为步骤'{step.get('name')}'注入token(params._session_token存在)")
                else:
                    logger.warning(f"[content-orchestrator] BUG-FIX: 步骤'{step.get('name')}'需要token但params中无_session_token, params keys={list(params.keys())}")
            # 租户隔离：将tenant_id注入每个步骤的参数中
            # BUG-FIX(2026-08-05): pps-mcp.get_persona_profile需要agent_id参数,
            # 当用户无人设档案时agent_id缺失,导致TypeError。
            # 修复: agent_id缺失时跳过此步骤,返回空数据(不影响内容生成主流程)。
            if step.get("tool") == "pps-mcp" and step.get("action") == "get_persona_profile":
                if not step_params.get("agent_id"):
                    logger.info(f"[content-orchestrator] 步骤'{step.get('name')}': agent_id缺失,跳过人设档案获取")
                    step_result = {
                        "step": i + 1,
                        "name": step.get("name", ""),
                        "tool": step.get("tool", ""),
                        "success": True,
                        "data": {"persona_profile": {}, "skipped": True, "reason": "agent_id未设置"},
                        "error": None,
                    }
                    results.append(step_result)
                    # V43修复(BUG-6): 移除previous_output引用——orchestrate_pipeline仅构建步骤列表,
                    # 不执行步骤,previous_output在execute_pipeline(L1851)中才定义。
                    # 原代码会导致NameError崩溃整个orchestrate_pipeline函数。
                    continue

            if tenant_id:
                step_params["tenant_id"] = tenant_id
            # 素材注入：将租户素材注入到需要图片/参考资料的步骤中
            if tenant_assets:
                asset_urls = [a.get("url", a.get("file_path", "")) for a in tenant_assets if a.get("url") or a.get("file_path")]
                if asset_urls:
                    step_params.setdefault("image_urls", [])
                    step_params["image_urls"] = asset_urls + step_params["image_urls"]
                    step_params["reference_materials"] = [a.get("description", a.get("asset_type", "")) for a in tenant_assets]
            step_result = {
                "step": i + 1,
                "name": step["name"],
                "tool": step["tool"],
                "action": step["action"],
                "status": "ready",
                "params": step_params,
            }
            results.append(step_result)

        return {
            "success": True,
            "data": {
                "pipeline_type": pipeline_type,
                "total_steps": len(steps),
                "steps": results,
                "tenant_assets_count": len(tenant_assets),
                "tenant_assets_source": "asset_manager" if tenant_assets else ("ai_fallback" if tenant_id else "none"),
                "instruction": "按顺序执行每个步骤的tool+action，将上一步输出作为下一步输入",
            },
            "error": None,
            "code": None,
        }
    except ValueError as e:
        logger.error(f"content orchestrator异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "PIPELINE_NOT_FOUND"}
    except Exception as e:
        logger.error(f"content orchestrator异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "ORCHESTRATE_ERROR"}

def list_pipelines() -> dict[str, Any]:
    """列出所有可用管道及其步骤

    Returns:
        dict[str, Any]: 返回值说明
    """
    all_pipelines = {}
    # Gap1修复: 包含外部管道
    external = _get_all_pipelines()
    all_types = [
        "PL-VIDEO", "PL-IMAGE", "PL-AUDIO", "PL-LIPSYNC", "PL-COMIC",
        "PL-NOVEL", "PL-DRAMA",
        "E2E-VIDEO", "E2E-IMAGE", "E2E-DAILY", "PL-NEWPROD",
        "PL-HOTSPOT", "PL-PRODUCT",
    ] + list(external.keys())
    # 去重(防止外部管道与内置同名)
    seen = set()
    unique_types = []
    for pt in all_types:
        if pt not in seen:
            seen.add(pt)
            unique_types.append(pt)

    for pt in unique_types:
        steps = get_pipeline_steps(pt)
        all_pipelines[pt] = {
            "total_steps": len(steps),
            "steps": [s["name"] for s in steps],
            "tools": list(set(s["tool"] for s in steps)),
        }
    return {"success": True, "data": all_pipelines, "error": None, "code": None}

def _step_content_type(step_name: str) -> str:
    """从步骤名称推断内容类型，用于缓存Key"""
    name_lower = step_name.lower()
    if "脚本" in step_name or "script" in name_lower:
        return "script"
    if "文案" in step_name or "标题" in step_name or "copy" in name_lower:
        return "description"
    if "选题" in step_name or "topic" in name_lower:
        return "topic"
    if "配音" in step_name or "speech" in name_lower or "tts" in name_lower:
        return "audio"
    if "画面" in step_name or "视频" in step_name or "video" in name_lower:
        return "video"
    if "配图" in step_name or "图片" in step_name or "image" in name_lower or "生图" in step_name:
        return "image"
    if "排版" in step_name or "visual" in name_lower:
        return "layout"
    if "发布" in step_name or "publish" in name_lower:
        return "publish"
    if "审核" in step_name or "check" in name_lower:
        return "review"
    return "other"

def _cache_step_result(cache: ContentCache, product_id: str, step_name: str,
                       step_index: int, result: dict, params: dict) -> None:
    """将步骤结果写入缓存

    Token优化: 缓存LLM生成结果，失败重试时跳过(见30白皮书§十一+修复提示词R33)
    """
    content_type = _step_content_type(step_name)
    value = {
        "step_index": step_index,
        "step_name": step_name,
        "content_type": content_type,
        "result": result,
    }
    input_params = {k: v for k, v in params.items() if k in ("topic", "direction", "template_type", "product_id", "focus")}

    if content_type in ("description", "script", "topic"):
        cache.save_text(product_id, content_type, value, input_params=input_params)
    elif content_type == "image":
        cache.save_image(product_id, content_type, value, input_params=input_params)
    elif content_type == "video":
        cache.save_video(product_id, content_type, value, input_params=input_params)
    elif content_type == "audio":
        cache.save_text(product_id, content_type, value, input_params=input_params)

def _check_step_cache(cache: ContentCache, product_id: str, step_name: str,
                      params: dict) -> dict | None:
    """检查步骤结果是否已缓存

    Returns:
        缓存的结果字典，未命中返回None
    """
    content_type = _step_content_type(step_name)
    input_params = {k: v for k, v in params.items() if k in ("topic", "direction", "template_type", "product_id", "focus")}

    if content_type in ("description", "script", "topic", "audio"):
        cached = cache.get_text(product_id, content_type, input_params=input_params)
    elif content_type == "image":
        cached = cache.get_image(product_id, content_type, input_params=input_params)
    elif content_type == "video":
        cached = cache.get_video(product_id, content_type, input_params=input_params)
    else:
        return None

    if cached and isinstance(cached, dict) and "result" in cached:
        return cached["result"]
    return None

def _parse_multi_role_dialogues(script_text: str) -> list:
    """P0-011修复: 解析剧本中的多角色对白
    支持格式:
      - "角色A:台词内容" (中文冒号)
      - "角色A：台词内容" (全角冒号)
      - "角色A: 台词内容" (冒号后有空格)
      - "角色A（旁白）：台词内容" (带角色说明)
    返回: [{role: str, text: str, voice_id: str}, ...]
    voice_id初始为空,由tts-adapter-mcp根据novel_characters.voice_id填充
    """
    import re as _re
    if not script_text or not isinstance(script_text, str):
        return []
    # 匹配: 行首角色名 + 冒号(中/英/全角) + 台词内容
    # 角色名: 2-20个字符(中文/英文/数字),可含括号说明
    pattern = _re.compile(
        r'^([^:\n：]{2,20})\s*[:：]\s*(.+)$',
        _re.MULTILINE
    )
    dialogues = []
    for match in pattern.finditer(script_text):
        role = match.group(1).strip()
        text = match.group(2).strip()
        # 过滤明显非对白的行(如"场景:"、"旁白:"保留)
        if not role or not text or len(text) < 2:
            continue
        # 移除角色名中的括号说明
        role_clean = _re.sub(r'[（(].*?[）)]', '', role).strip()
        if not role_clean:
            role_clean = role
        dialogues.append({
            "role": role_clean,
            "text": text,
            "voice_id": "",  # 由tts-adapter-mcp填充
        })
    return dialogues

def _resolve_template_vars(step_params: dict, previous_output: dict, initial_params: dict) -> dict:
    """解析pipeline步骤参数中的模板变量

    FIX-V57-001: pipeline JSON中${platform}和${prev_output.content}模板变量
    在execute_pipeline中无替换逻辑,导致content-calibrator收到字面字符串
    触发INVALID_PLATFORM验证失败。

    支持的模板格式(与pipeline JSON约定一致):
      ${prev_output.KEY} → previous_output.get(KEY, "")
      ${params.KEY}      → initial_params.get(KEY, "")
      ${platform}        → initial_params.get("platform")或initial_params.get("platforms")[0], 默认"weibo"

    单点修复,不新增碎片化功能,仅补全缺失的变量替换逻辑。
    全链思考:
      - 数据库: 无变更,模板变量在运行时解析
      - MCP: content-calibrator收到正确platform参数,无MCP代码变更
      - Skill: content-calibrator SKILL.md无变更,验证逻辑已正确
      - 配置: pipeline JSON无变更,模板语法已定义
      - UI: 无变更,后端修复自动生效
    """
    import re as _re
    _template_re = _re.compile(r'\$\{([^}]+)\}')

    def _replace_match(m):
        expr = m.group(1).strip()
        # ${prev_output.KEY} → previous_output[KEY]
        if expr.startswith("prev_output."):
            key = expr[len("prev_output."):]
            val = previous_output.get(key, "")
            return str(val) if val is not None else ""
        # ${params.KEY} → initial_params[KEY]
        if expr.startswith("params."):
            key = expr[len("params."):]
            val = initial_params.get(key, "")
            return str(val) if val is not None else ""
        # ${platform} → 从initial_params获取,默认weibo(有效平台)
        if expr == "platform":
            val = initial_params.get("platform", initial_params.get("platforms", "weibo"))
            if isinstance(val, list):
                val = val[0] if val else "weibo"
            return str(val) if val else "weibo"
        # 未知变量 → 空字符串(不破坏原有逻辑)
        return ""

    resolved = {}
    for k, v in step_params.items():
        if isinstance(v, str) and "${" in v:
            resolved[k] = _template_re.sub(_replace_match, v)
        else:
            resolved[k] = v
    return resolved

def execute_pipeline(pipeline_name: str, params: dict) -> dict[str, Any]:
    """确定性编排执行: 按步骤顺序执行MCP调用，每步验证上一步结果

    Token优化: 每步执行前检查缓存，命中则跳过LLM调用(见30白皮书§十一+修复提示词R14+R33)

    Args:
        pipeline_name: 管道类型 (PL-VIDEO/PL-IMAGE/PL-AUDIO/PL-LIPSYNC/PL-COMIC/E2E-VIDEO/E2E-IMAGE/E2E-DAILY)
        params: 管道参数 (topic/direction/tenant_id/platforms等)

    Returns:
        {success: bool, data: {pipeline_name, total_steps, steps_completed, results, failed_step}, error: str|null, code: str|null}
    """
    try:
        if not _MCP_AVAILABLE:
            return {"success": False, "data": {}, "error": "mcp_caller不可用，无法执行管道", "code": "MCP_CALLER_UNAVAILABLE"}

        steps = get_pipeline_steps(pipeline_name)

        # 删除影响修复: 预检pipeline中Skill可用性，提前发现缺失Skill
        availability = check_pipeline_skill_availability(pipeline_name)
        if not availability["all_available"]:
            missing_required = [m for m in availability["missing_skills"] if not m["optional"]]
            if missing_required:
                missing_names = ", ".join(f"{m['step']}({m['skill_name']})" for m in missing_required)
                logger.warning(f"[content-orchestrator] 管道{pipeline_name}缺少必需Skill: {missing_names}")
                # 不阻断执行: Skill可能在_lazy目录或通过pipeline_overrides.json重定向
                # 实际执行到该步骤时call_skill会返回SKILL_NOT_FOUND错误
            missing_optional = [m for m in availability["missing_skills"] if m["optional"]]
            if missing_optional:
                logger.info(f"[content-orchestrator] 管道{pipeline_name}可选Skill缺失(将跳过): {missing_optional}")

        tenant_id = params.get("tenant_id", "")
        if tenant_id:
            import re
            if not re.match(r'^[a-zA-Z0-9_-]+$', tenant_id):
                return {"success": False, "data": {}, "error": f"tenant_id格式非法: {tenant_id}", "code": "TENANT_ID_INVALID"}

        # RC-1/RC-2修复: 解析${engine.*}占位符(按租户套餐动态选择MCP工具)
        # 根因: pipeline JSON中TTS/视频/图像/唇形同步工具名用${engine.xxx}占位符,
        #        但执行器从未调用pipeline_engine_resolver,导致21处占位符全部失效
        # 修复: 在pipeline执行前调用resolve_pipeline_steps替换占位符为实际MCP工具名
        if _ENGINE_RESOLVER_AVAILABLE and tenant_id:
            placeholder_count = sum(1 for s in steps if isinstance(s.get("tool", ""), str) and "${engine." in s.get("tool", ""))
            if placeholder_count > 0:
                steps = _resolve_engine_steps(steps, tenant_id)
                logger.info(f"[content-orchestrator] RC-1/RC-2修复: 已解析{placeholder_count}个引擎占位符 tenant={tenant_id} pipeline={pipeline_name}")
        else:
            # 无tenant_id或引擎解析器不可用时,使用默认引擎映射替换占位符
            _DEFAULT_ENGINE_MAP = {
                "${engine.tts}": "tts-adapter-mcp",
                "${engine.image_video}": "kling-mcp",
                "${engine.lipsync}": "liveportrait-mcp",
                "${engine.image}": "flux-mcp",
                "${engine.video}": "kling-mcp",
                "${engine.digital_human}": "character-workshop-mcp",
            }
            _default_resolved = 0
            for _s in steps:
                _tool = _s.get("tool", "")
                if isinstance(_tool, str) and _tool in _DEFAULT_ENGINE_MAP:
                    _s["tool"] = _DEFAULT_ENGINE_MAP[_tool]
                    _default_resolved += 1
            if _default_resolved > 0:
                logger.info(f"[content-orchestrator] 默认引擎解析: 已解析{_default_resolved}个引擎占位符(无tenant_id,使用默认映射) pipeline={pipeline_name}")

        # RC-3修复: 统一注入"去AI味"步骤(来源:33号文档§3 + 02手册§五5.1)
        # 根因: 外部pipeline JSON覆盖内置定义时丢失了"去AI味"步骤
        # 修复: 执行器在加载pipeline步骤后,自动检查并注入"去AI味"步骤
        # 位置: "写作风格特质注入"之后、"营销注入"之前
        _HAS_DEAI_STEP = any(s.get("name") == "去AI味" for s in steps)
        if not _HAS_DEAI_STEP:
            _style_idx = next((i for i, s in enumerate(steps) if s.get("name") == "写作风格特质注入"), -1)
            if _style_idx >= 0:
                _deai_step = {"name": "去AI味", "tool": "content-template", "action": "polish", "params": {}}
                steps.insert(_style_idx + 1, _deai_step)
                logger.info(f"[content-orchestrator] RC-3修复: 已在'写作风格特质注入'后注入'去AI味'步骤 pipeline={pipeline_name}")
            else:
                _marketing_idx = next((i for i, s in enumerate(steps) if s.get("name") == "营销注入"), -1)
                if _marketing_idx >= 0:
                    _deai_step = {"name": "去AI味", "tool": "content-template", "action": "polish", "params": {}}
                    steps.insert(_marketing_idx, _deai_step)
                    logger.info(f"[content-orchestrator] RC-3修复: 已在'营销注入'前注入'去AI味'步骤 pipeline={pipeline_name}")

        tenant_assets = []
        if tenant_id:
            tenant_assets = _query_tenant_assets(tenant_id)

        # BUG-190修复: 查询租户风格配置并传递给下游步骤
        # BUG-FIX(2026-08-05): 传递_session_token,避免portal_get_tenant_style无token调用触发熔断器
        tenant_style_config = {}
        _session_token = params.get("_session_token", "")
        if tenant_id:
            tenant_style_config = _query_tenant_style_config(tenant_id, _session_token)
            if tenant_style_config:
                logger.info(f"[content-orchestrator] 租户风格配置已加载: guidelines={bool(tenant_style_config.get('content_guidelines'))}, brand_keywords={len(tenant_style_config.get('brand_keywords', []))}个")

        # 架构修复: 预获取租户品牌Profile,确保生成步骤(步骤3)在品牌注入步骤(步骤9-11)之前执行时仍有品牌上下文
        tenant_brand_profile = {}
        if tenant_id:
            tenant_brand_profile = _query_tenant_brand_profile(tenant_id, _session_token)
            if tenant_brand_profile:
                logger.info(f"[content-orchestrator] 品牌Profile已预加载: brand_name={tenant_brand_profile.get('brand_name','')}")

        # DEF-U49 P2: 查询蒸馏21维指纹并传递给下游步骤(激活pps-mcp.get_distill_fingerprint)
        distill_fingerprint = {}
        if tenant_id:
            distill_fingerprint = _query_tenant_distill_fingerprint(tenant_id)
            if distill_fingerprint:
                dims_loaded = sum(1 for v in distill_fingerprint.values() if v)
                logger.info(f"[content-orchestrator] 蒸馏指纹已加载: {dims_loaded}/5类(persona/style/video/longform/brand)")

        # 问题2修复: 查询agent_memory自学习经验(publish_feedback类),注入到内容生成提示词
        recent_lessons = _query_agent_memory_lessons(tenant_id) if tenant_id else []

        # P0-32修复: 查询租户知识库并传递给下游步骤(4库协同: 知识库/素材库/蒸馏库/平台知识库)
        tenant_knowledge = {}
        if tenant_id:
            tenant_knowledge = _query_tenant_knowledge(tenant_id)

        # P0-33修复: 查询平台知识库并传递给下游步骤
        platforms_str = params.get("platforms", params.get("platform", ""))
        if isinstance(platforms_str, list):
            platforms_str = ",".join(str(p) for p in platforms_str)
        platform_kb_text = _query_platform_knowledge(str(platforms_str)) if platforms_str else ""

        # Token优化: 初始化内容缓存
        cache = ContentCache() if _CACHE_AVAILABLE else None
        product_id = params.get("product_id", params.get("topic", pipeline_name))

        # P2-1: 创建管线状态记录(来源:31文档P2-1统一编排器)
        pipeline_state_record = None
        if _STATE_AVAILABLE:
            try:
                custom_steps = [s["name"] for s in steps]
                pipeline_state_record = pipeline_state.create_pipeline(
                    title=params.get("topic", pipeline_name),
                    pipeline_type=pipeline_name,
                    tenant_id=tenant_id,
                    items_count=1,
                    source="content-orchestrator",
                    custom_steps=custom_steps,
                )
            except Exception as e:
                logger.error(f"[content-orchestrator] 管线状态创建失败(非关键): {e}")

        # Token优化: 检查草稿缓存，恢复已完成的步骤(见30白皮书§十一+修复提示词R14+R33)
        draft_data = None
        if cache and product_id:
            try:
                draft_data = cache.get_draft(product_id)
                if draft_data and draft_data.get("completed_steps"):
                    logger.info(f"[content-orchestrator] 草稿缓存命中: {product_id}, 已完成{len(draft_data['completed_steps'])}步")
            except Exception as e:
                logger.error(f"content orchestrator异常: {e}", exc_info=True)
                logger.warning(f"[content-orchestrator] 草稿缓存读取失败(非关键): {e}")

        results = []
        previous_output = dict(params)
        cached_steps = 0
        # V43修复(BUG-9): 每次execute_pipeline调用时重置GEO降级计数器,避免多租户场景下互相影响
        global _geo_fail_count
        _geo_fail_count = 0
        # DEF-KB-14: 用于保存PL-PRODUCT步骤1(素材检索)的assets结果,透传到步骤3(素材匹配评分)
        step1_assets = []

        for i, step in enumerate(steps):
            # Token优化: 如果草稿缓存中有该步骤的结果，跳过执行
            if draft_data and draft_data.get("completed_steps") and str(i + 1) in draft_data["completed_steps"]:
                step_result = draft_data["completed_steps"][str(i + 1)]
                step_result["from_draft"] = True
                results.append(step_result)
                cached_steps += 1
                # DEF-KB-14: 捕获PL-PRODUCT步骤1(素材检索)的assets结果(草稿缓存路径)
                if step.get("name") == "素材检索" and step_result.get("success"):
                    _step1_data = step_result.get("data", {})
                    if isinstance(_step1_data, dict) and "assets" in _step1_data:
                        step1_assets = _step1_data["assets"]
                        logger.info(f"[content-orchestrator] DEF-KB-14: 捕获步骤1素材检索assets(草稿): {len(step1_assets)}个")
                prev_data = step_result.get("data", {})
                previous_output = _merge_step_output(previous_output, prev_data)
                # BUG-AUDIT-015修复: 缓存命中时也更新状态文件(否则状态显示pending造成"从未启动"假象)
                if pipeline_state_record and _STATE_AVAILABLE:
                    try:
                        pipeline_state.update_step(pipeline_state_record["id"], step["name"], "completed")
                    except Exception as e:
                        logger.error(f"[content-orchestrator] 缓存命中update_step失败(非关键): {e}")
                continue
            step_params = dict(step.get("params", {}))
            # BUG-FIX(2026-08-05): agency-portal-mcp工具需要token参数进行身份验证。
            # 管道步骤params中通常不包含token,从pipeline_params的_session_token注入。
            # 只对agency-portal-mcp的工具注入,避免影响其他MCP工具。
            if step.get("tool") == "agency-portal-mcp" and "token" not in step_params:
                _session_token = params.get("_session_token", "")
                if _session_token:
                    step_params["token"] = _session_token
            # FIX-V57-001: 解析模板变量(${platform}/${prev_output.KEY})在update之前
            # 根因: pipeline JSON中"platform":"${platform}"在orchestrator中无替换逻辑
            # 修复: 添加_resolve_template_vars函数解析模板变量为实际值
            step_params = _resolve_template_vars(step_params, previous_output, params)
            # FIX-V58-002: previous_output不得覆盖pipeline步骤显式声明的参数
            # 根因: step_params.update(previous_output)会用上一步输出覆盖${platform}解析结果
            #        导致content-calibrator收到dict(热点数据)而非string(平台名)
            # 修复: 只合并非显式声明的key,保留模板解析的显式参数值
            _explicit_step_keys = set(step.get("params", {}).keys())
            for _k, _v in previous_output.items():
                if _k not in _explicit_step_keys:
                    step_params[_k] = _v

            # P0-018修复(NEW-DEF-07): PL-DRAMA步骤间字段映射
            # 根因: 各步骤输出字段名与下一步期望输入字段名不匹配,导致数据传递静默失败
            # 修复: 在step_params.update后添加字段别名映射,确保跨步骤数据流通
            _FIELD_MAPPING = {
                "content_full": "novel_text",
                "chapter_number": "chapter_num",
                "script_text": "drama_script",
                "scenes": "scene_list",
                "characters": "character_list",
                "storyboard": "storyboards",
                "audio_files": "voice_files",
                "video_files": "shot_videos",
                "merged_video_path": "composed_video",
                "subtitle_path": "subtitle_file",
                "marketing_copy": "marketing_text",
                "ai_declaration": "declaration_text",
                # BE-03: 管道步骤persona_id映射到pps-mcp.get_persona_profile的agent_id参数,
                # 确保PL-NEWS/PL-FORTUNE/PL-DRAMA的persona_id参数能正确透传
                "persona_id": "agent_id",
            }
            for _old_key, _new_key in _FIELD_MAPPING.items():
                if _old_key in step_params and _new_key not in step_params:
                    step_params[_new_key] = step_params[_old_key]

            # P0-011修复: 多角色对白分离(漫剧配音步骤)
            # 当步骤为"配音生成"且multi_role=true时,解析剧本中的角色对白
            # 格式: "角色A:台词" → [{role: "角色A", text: "台词", voice_id: "xxx"}, ...]
            # voice_id从novel_characters.voice_id读取(需content-orchestrator无法直接查PG,
            # 由tts-adapter-mcp根据voice_id_source=novel_characters自行查询)
            if step.get("name") == "配音生成" and step_params.get("multi_role"):
                drama_script = step_params.get("drama_script") or step_params.get("script_text") or ""
                if drama_script:
                    dialogues = _parse_multi_role_dialogues(drama_script)
                    if dialogues:
                        step_params["dialogues"] = dialogues
                        step_params["dialogue_count"] = len(dialogues)
                        logger.info(f"[PL-DRAMA] P0-011: 解析{len(dialogues)}条角色对白")

            # P0-010修复: 角色画面生成步骤注入character_list
            # 从前序步骤输出中提取角色列表,传递给character-consistency-mcp
            if step.get("name") == "角色画面生成":
                char_list = step_params.get("character_list") or step_params.get("characters") or []
                if char_list:
                    step_params["characters"] = char_list
                    step_params["face_refs"] = [c.get("face_ref", "") for c in char_list if isinstance(c, dict)]

            # BUG-FIX(2026-08-05): pps-mcp.get_persona_profile需要agent_id参数,
            # 当用户无人设档案时agent_id缺失,导致TypeError。
            # 修复: agent_id缺失时跳过此步骤,返回空数据(不影响内容生成主流程)。
            if step.get("tool") == "pps-mcp" and step.get("action") == "get_persona_profile":
                if not step_params.get("agent_id"):
                    logger.info(f"[content-orchestrator] execute_pipeline步骤'{step.get('name')}': agent_id缺失,跳过人设档案获取")
                    step_result = {
                        "step": i + 1,
                        "name": step.get("name", ""),
                        "tool": step.get("tool", ""),
                        "success": True,
                        "data": {"persona_profile": {}, "skipped": True, "reason": "agent_id未设置"},
                        "error": None,
                    }
                    results.append(step_result)
                    prev_data = step_result["data"]
                    previous_output = _merge_step_output(previous_output, prev_data)
                    continue

            if tenant_id:
                step_params["tenant_id"] = tenant_id
            if tenant_assets:
                asset_urls = [a.get("url", a.get("file_path", "")) for a in tenant_assets if a.get("url") or a.get("file_path")]
                if asset_urls:
                    step_params.setdefault("image_urls", [])
                    step_params["image_urls"] = asset_urls + step_params["image_urls"]
                    step_params["reference_materials"] = [a.get("description", a.get("asset_type", "")) for a in tenant_assets]

            # DEF-KB-14: 将PL-PRODUCT步骤1(素材检索)的assets结果透传到步骤3(素材匹配评分)
            # 根因: 步骤2(品牌Profile注入)输出会覆盖previous_output,导致步骤3无法获取步骤1的assets
            # 修复: 使用持久变量step1_assets跨步骤透传,步骤3 match_materials可通过step_params["step1_assets"]获取
            if step1_assets:
                step_params.setdefault("step1_assets", step1_assets)

            # BUG-190修复: 将租户风格配置传递给下游步骤
            if tenant_style_config:
                step_params.setdefault("content_guidelines", tenant_style_config.get("content_guidelines", ""))
                step_params.setdefault("brand_keywords", tenant_style_config.get("brand_keywords", []))
                step_params.setdefault("video_brand_overlay", tenant_style_config.get("video_brand_overlay", {}))

            # 架构修复: 将预获取的品牌Profile传递给下游步骤(确保生成步骤前有品牌上下文)
            if tenant_brand_profile:
                step_params.setdefault("brand_profile", tenant_brand_profile)
                # V43修复: 注入AI生成的品牌/营销配置(小白用户AI生成→保存→管道消费)
                if tenant_brand_profile.get("ai_brand_config"):
                    step_params.setdefault("ai_brand_config", tenant_brand_profile["ai_brand_config"])
                if tenant_brand_profile.get("ai_marketing_config"):
                    step_params.setdefault("ai_marketing_config", tenant_brand_profile["ai_marketing_config"])

            # V43修复: 注入AI生成的SEO/GEO配置(小白用户AI生成→保存→管道消费)
            if tenant_style_config:
                if tenant_style_config.get("ai_seo_config"):
                    step_params.setdefault("ai_seo_config", tenant_style_config["ai_seo_config"])
                if tenant_style_config.get("ai_geo_config"):
                    step_params.setdefault("ai_geo_config", tenant_style_config["ai_geo_config"])

            # DEF-U49 P2: 将蒸馏21维指纹传递给下游步骤(激活跨MCP蒸馏消费链路)
            # 来源: 60号文档v2.0 §2.4 + DEF-U49 P1-4(孤儿工具激活)
            # 下游Skill(content-template/seo-optimizer/market-copywriter等)按需消费
            if distill_fingerprint:
                step_params.setdefault("persona_profile", distill_fingerprint.get("persona_profile", {}))
                step_params.setdefault("style_fingerprint", distill_fingerprint.get("style_fingerprint", {}))
                step_params.setdefault("video_style_fingerprint", distill_fingerprint.get("video_style_fingerprint", {}))
                step_params.setdefault("longform_structure", distill_fingerprint.get("longform_structure", {}))
                step_params.setdefault("brand_analysis", distill_fingerprint.get("brand_analysis", {}))

            # 问题2修复: 将agent_memory自学习经验注入到步骤参数(供content-template generate消费)
            if recent_lessons:
                step_params.setdefault("recent_lessons", recent_lessons)

            # P0-32修复: 将租户知识库传递给下游步骤(4库协同)
            if tenant_knowledge:
                step_params.setdefault("kb_products", tenant_knowledge.get("products", []))
                step_params.setdefault("kb_faq", tenant_knowledge.get("faq", []))
                step_params.setdefault("kb_policies", tenant_knowledge.get("policies", []))
                # DEF-KB-08: 将chunk_text拼接的kb_content传递给下游步骤(供SEO/GEO/Copywriter消费)
                step_params.setdefault("kb_content", tenant_knowledge.get("kb_content", ""))

            # P0-33修复: 将平台知识库传递给下游步骤
            if platform_kb_text:
                step_params.setdefault("platform_knowledge", platform_kb_text)

            # V42-LOG: 全局预取注入埋点 — 每步记录注入的上下文
            if step.get("tool") in ("content-template", "seo-optimizer", "geo-content-optimizer", "market-copywriter"):
                logger.info(
                    f"[INJECT] step={i+1} tool={step.get('tool','')} | "
                    f"brand_profile={'Y' if tenant_brand_profile else 'N'} | "
                    f"distill_fp={'Y' if distill_fingerprint else 'N'} | "
                    f"persona={'Y' if distill_fingerprint and distill_fingerprint.get('persona_profile') else 'N'} | "
                    f"style_fp={'Y' if distill_fingerprint and distill_fingerprint.get('style_fingerprint') else 'N'} | "
                    f"style_fp_raw_analysis={'Y' if distill_fingerprint and isinstance(distill_fingerprint.get('style_fingerprint'), dict) and distill_fingerprint['style_fingerprint'].get('raw_analysis') else 'N'} | "
                    f"tenant_style_cfg={'Y' if tenant_style_config else 'N'} | "
                    f"ai_brand={'Y' if tenant_brand_profile and tenant_brand_profile.get('ai_brand_config') else 'N'} | "
                    f"ai_marketing={'Y' if tenant_brand_profile and tenant_brand_profile.get('ai_marketing_config') else 'N'} | "
                    f"ai_seo={'Y' if tenant_style_config and tenant_style_config.get('ai_seo_config') else 'N'} | "
                    f"ai_geo={'Y' if tenant_style_config and tenant_style_config.get('ai_geo_config') else 'N'} | "
                    f"tenant_kb={'Y' if tenant_knowledge else 'N'} | "
                    f"platform_kb={'Y' if platform_kb_text else 'N'} | "
                    f"recent_lessons={'Y' if recent_lessons else 'N'}"
                )

            # 架构修复: 在生成步骤(content-template+generate)执行前,确保品牌/风格/IP上下文已注入
            # 根因: 部分管道的生成步骤(步骤3)在品牌/IP/风格获取步骤(步骤9-11)之前执行,导致生成时无上下文
            # 修复: 全局预获取已注入brand_profile/style_fingerprint/persona_profile/brand_keywords/kb_content,
            #        此处作为安全网,确保生成步骤参数完整(若全局注入失败则按需补充)
            _step_tool = step.get("tool", "")
            _step_action = step.get("action", "")
            if _step_tool == "content-template" and _step_action == "generate" and tenant_id:
                if "brand_profile" not in step_params:
                    try:
                        _bp = _query_tenant_brand_profile(tenant_id, _session_token)
                        if _bp:
                            step_params.setdefault("brand_profile", _bp)
                    except Exception as _e:
                        logger.warning(f"[content-orchestrator] 生成步骤前品牌Profile按需补充失败(非关键): {_e}")
                if "style_fingerprint" not in step_params:
                    try:
                        _sc = _query_tenant_style_config(tenant_id, _session_token)
                        if _sc:
                            step_params.setdefault("brand_keywords", _sc.get("brand_keywords", []))
                    except Exception as _e:
                        logger.warning(f"[content-orchestrator] 生成步骤前风格配置按需补充失败(非关键): {_e}")
                # 安全网补充: persona_profile fallback(若全局distill_fingerprint预获取失败,此处重试)
                if "persona_profile" not in step_params:
                    try:
                        _df = _query_tenant_distill_fingerprint(tenant_id)
                        if _df and _df.get("persona_profile"):
                            step_params.setdefault("persona_profile", _df["persona_profile"])
                            # 顺带补充其他蒸馏维度(若也缺失)
                            for _dk in ("style_fingerprint", "video_style_fingerprint", "longform_structure", "brand_analysis"):
                                if _dk not in step_params and _df.get(_dk):
                                    step_params.setdefault(_dk, _df[_dk])
                    except Exception as _e:
                        logger.warning(f"[content-orchestrator] 生成步骤前人设Profile按需补充失败(非关键): {_e}")

            # BUG-189修复: AI声明注入步骤使用内联函数(原risk-detector MCP未注册)
            if step["name"] == "AI声明注入":
                content_to_inject = previous_output.get("content", previous_output.get("text", previous_output.get("markdown", "")))
                platform = params.get("platform", step_params.get("platform", "default"))
                # V42-LOG: AI声明注入前
                logger.info(
                    f"[STEP-PRE] step={i+1} tool=inline action=inject_ai_declaration | "
                    f"content_len={len(str(content_to_inject)) if content_to_inject else 0} | "
                    f"platform={platform}"
                )
                inject_result = _inject_ai_declaration(content_to_inject, platform)
                # V42-LOG: AI声明注入后
                _inject_content = inject_result.get("data", {}).get("content", "") if isinstance(inject_result.get("data"), dict) else ""
                logger.info(
                    f"[STEP-POST] step={i+1} tool=inline action=inject_ai_declaration | "
                    f"success={inject_result.get('success', False)} | "
                    f"result_content_len={len(str(_inject_content)) if _inject_content else 0} | "
                    f"delta={len(str(_inject_content)) - len(str(content_to_inject)) if _inject_content and content_to_inject else 0:+d} | "
                    f"error={inject_result.get('error', 'N/A')}"
                )
                step_result = {
                    "step": i + 1,
                    "name": step["name"],
                    "tool": "inline(ai_declaration)",
                    "action": "inject_ai_declaration",
                    "success": inject_result.get("success", True),
                    "data": inject_result.get("data", {}),
                    "error": inject_result.get("error"),
                    "from_cache": False,
                }
                results.append(step_result)
                prev_data = step_result.get("data", {})
                previous_output = _merge_step_output(previous_output, prev_data)
                if pipeline_state_record and _STATE_AVAILABLE:
                    try:
                        pipeline_state.update_step(pipeline_state_record["id"], step["name"], "completed")
                    except Exception as e:
                        logger.error(f"管道状态更新失败(非关键),继续执行: {e}")
                continue

            # P2-1: 热点选题引擎集成(PL-HOTSPOT/E2E-DAILY管道,来源:31文档P2-1)
            if _HOTSPOT_AVAILABLE and pipeline_name in ("PL-HOTSPOT", "E2E-DAILY"):
                if step["name"] == "热点获取":
                    try:
                        hotspot_result = hotspot_engine.load_hotspots(tenant_id)
                        if hotspot_result.get("success"):
                            step_params["hotspot_data"] = hotspot_result["data"]
                    except Exception as e:
                        logger.error(f"[content-orchestrator] 热点加载失败(非关键): {e}")
                elif step["name"] == "选题决策":
                    try:
                        hotspot_data = previous_output.get("hotspot_data", {})
                        if hotspot_data:
                            topics = hotspot_engine.generate_topics(hotspot_data, tenant_id, count=10)
                            step_params["pre_generated_topics"] = topics
                    except Exception as e:
                        logger.error(f"[content-orchestrator] 选题预生成失败(非关键): {e}")

            # P2-1: 更新步骤状态为in_progress(来源:31文档P2-1统一编排器)
            if pipeline_state_record and _STATE_AVAILABLE:
                try:
                    pipeline_state.update_step(
                        pipeline_state_record["id"], step["name"], "in_progress"
                    )
                except Exception as e:

                    logger.error(f"content_orchestrator: {e}")

            # P0-27修复: condition条件执行支持
            # 格式: "condition": "previous_output.field_name" — 当previous_output中有该字段且为True时执行
            _step_condition = step.get("condition")
            if _step_condition and isinstance(_step_condition, str):
                _cond_field = _step_condition.replace("previous_output.", "")
                _cond_value = previous_output.get(_cond_field, False)
                if not _cond_value:
                    logger.info(f"[content-orchestrator] P0-27: 步骤'{step['name']}'条件不满足(condition={_step_condition}),跳过")
                    step_result = {
                        "step": i + 1, "name": step["name"], "tool": step["tool"], "action": step["action"],
                        "success": True, "data": {}, "error": None, "from_cache": False, "skipped": True,
                    }
                    results.append(step_result)
                    continue

            # Token优化: 检查缓存，命中则跳过MCP调用(见30白皮书§十一)
            # V43修复(BUG-11): 添加"detect"到排除列表——防查重检测结果依赖数据库状态(非确定性),缓存可能导致恢复时使用过时block结果
            cached_result = None
            if cache and step.get("action") not in ("publish", "upload_video", "schedule_smart", "track_performance", "detect"):
                cached_result = _check_step_cache(cache, product_id, step["name"], step_params)

            if cached_result is not None:
                step_result = {
                    "step": i + 1,
                    "name": step["name"],
                    "tool": step["tool"],
                    "action": step["action"],
                    "success": cached_result.get("success", True),
                    "data": cached_result.get("data", {}),
                    "error": cached_result.get("error"),
                    "from_cache": True,
                }
                cached_steps += 1
            else:
                # P0-B修复: 路由match_materials到既有scripts/material_matcher.py(R45复用)
                # 来源: 分析2 §5.3根因 + hotspot_engine.py:504 subprocess调用模式
                # R45: 同类bug批量修复,复用既有实现,禁止新写
                if step.get("tool") == "content-orchestrator" and step.get("action") == "match_materials":
                    import subprocess as _sp
                    _matcher_script = os.path.join(
                        os.path.dirname(__file__), "..", "..", "..",
                        "scripts", "material_matcher.py"
                    )
                    _kw_str = ",".join(step_params.get("keywords", []) or [step_params.get("topic", "")][:10])
                    try:
                        _proc = _sp.run(
                            [sys.executable, _matcher_script,
                             "--tenant-id", str(step_params.get("tenant_id", "")),
                             "--keywords", _kw_str,
                             "--top", "3"],
                            capture_output=True, text=True, timeout=30,
                            cwd=str(_PROJECT_ROOT),
                        )
                        if _proc.returncode == 0:
                            import json as _json
                            _match_result = _json.loads(_proc.stdout) if _proc.stdout.strip() else {"success": False}
                            mcp_result = _match_result
                        else:
                            mcp_result = {"success": False, "data": {}, "error": f"material_matcher退出码{_proc.returncode}: {_proc.stderr[:200]}", "code": "MATCHER_FAILED"}
                    except Exception as _match_err:
                        logger.error(f"[content-orchestrator] P0-B: match_materials调用失败(非阻断): {_match_err}")
                        mcp_result = {"success": False, "data": {}, "error": str(_match_err), "code": "MATCHER_EXCEPTION"}
                    step_result = {
                        "step": i + 1, "name": step["name"], "tool": step["tool"], "action": step["action"],
                        "success": mcp_result.get("success", False), "data": mcp_result.get("data", {}),
                        "error": mcp_result.get("error"), "from_cache": False,
                    }
                    results.append(step_result)
                    if cache and mcp_result.get("success", False):
                        _cache_step_result(cache, product_id, step["name"], i + 1, mcp_result, step_params)
                    continue

                # novel-bridge特殊处理: 路由到mcps/shared/novel_bridge.py脚本
                # 支持 action: init_novel, generate_chapters, get_latest_chapter 等
                if step.get("tool") == "novel-bridge":
                    import subprocess as _sp2
                    _bridge_script = os.path.join(str(_PROJECT_ROOT), "mcps", "shared", "novel_bridge.py")
                    if not os.path.isfile(_bridge_script):
                        mcp_result = {"success": False, "data": {}, "error": f"novel_bridge.py不存在: {_bridge_script}", "code": "BRIDGE_NOT_FOUND"}
                    else:
                        _bridge_action = step.get("action", "")
                        _bridge_params = dict(step_params)
                        _bridge_params.setdefault("tenant_id", str(step_params.get("tenant_id", "")))
                        try:
                            _bridge_proc = _sp2.run(
                                [sys.executable, _bridge_script,
                                 "--action", _bridge_action,
                                 "--params", json.dumps(_bridge_params, ensure_ascii=False)],
                                capture_output=True, text=True, timeout=120,
                                cwd=str(_PROJECT_ROOT),
                            )
                            if _bridge_proc.returncode == 0:
                                _bridge_result = json.loads(_bridge_proc.stdout) if _bridge_proc.stdout.strip() else {"success": False}
                                mcp_result = _bridge_result
                            else:
                                mcp_result = {"success": False, "data": {}, "error": f"novel_bridge退出码{_bridge_proc.returncode}: {_bridge_stderr[:200] if (_bridge_stderr := _bridge_proc.stderr) else ''}", "code": "BRIDGE_FAILED"}
                        except Exception as _bridge_err:
                            logger.error(f"[content-orchestrator] novel-bridge调用失败: {_bridge_err}")
                            mcp_result = {"success": False, "data": {}, "error": str(_bridge_err), "code": "BRIDGE_EXCEPTION"}
                    step_result = {
                        "step": i + 1, "name": step["name"], "tool": step["tool"], "action": step["action"],
                        "success": mcp_result.get("success", False), "data": mcp_result.get("data", {}),
                        "error": mcp_result.get("error"), "from_cache": False,
                    }
                    results.append(step_result)
                    if cache and mcp_result.get("success", False):
                        _cache_step_result(cache, product_id, step["name"], i + 1, mcp_result, step_params)
                    continue

                # V42-LOG: 关键数据流转埋点 — 步骤执行前(记录传入参数)
                _log_tool = step.get("tool", "")
                _log_action = step.get("action", "")
                _LOG_TOOLS = {"seo-optimizer", "geo-content-optimizer", "market-copywriter",
                              "content-formatter", "content-template", "content-qa-guard",
                              "content-rewriter", "content-publisher", "inline"}
                if _log_tool in _LOG_TOOLS:
                    _log_content = (step_params.get("content") or step_params.get("text")
                                    or step_params.get("script") or step_params.get("drama_script") or "")
                    _log_brand = step_params.get("brand_profile") or {}
                    _log_persona = step_params.get("persona_profile") or {}
                    _log_style = step_params.get("style_fingerprint") or {}
                    _log_raw = _log_style.get("raw_analysis") if isinstance(_log_style, dict) else None
                    if isinstance(_log_raw, str):
                        try:
                            import json as _json_log
                            _log_raw = _json_log.loads(_log_raw)
                        except Exception:
                            _log_raw = {}
                    _log_raw = _log_raw if isinstance(_log_raw, dict) else {}
                    logger.info(
                        f"[STEP-PRE] step={i+1} tool={_log_tool} action={_log_action} | "
                        f"content_len={len(str(_log_content)) if _log_content else 0} | "
                        f"platform={step_params.get('platform', 'N/A')} | "
                        f"brand_profile={'Y(' + str(len(_log_brand)) + ' keys)' if _log_brand else 'N'} | "
                        f"persona_profile={'Y(' + str(len(_log_persona)) + ' keys)' if _log_persona else 'N'} | "
                        f"style_fingerprint={'Y(' + str(len(_log_style)) + ' keys)' if _log_style else 'N'} | "
                        f"raw_analysis_dims={[k for k in _log_raw if k.startswith('performance_')] or 'N'} | "
                        f"kb_content={'Y(' + str(len(step_params.get('kb_content', ''))) + ' chars)' if step_params.get('kb_content') else 'N'} | "
                        f"recent_lessons={'Y(' + str(len(step_params.get('recent_lessons', []))) + ' items)' if step_params.get('recent_lessons') else 'N'} | "
                        f"param_keys={sorted(list(step_params.keys()))[:15]}"
                    )

                # Phase2: 运行时推断路由(_is_skill_tool检查SKILL.md+MCP注册)
                # 旧的_SKILL_TOOLS硬编码集合已废弃，改为运行时自动推断
                # P0-27修复: retry重试支持(来源:pipeline步骤retry字段)
                # 修复(2026-08-10): MCP_NOT_CONFIGURED不重试(R74反敷衍)
                _retry_max = step.get("retry", 0) if isinstance(step.get("retry"), int) else 0
                _retry_done = 0
                while True:
                    if _is_skill_tool(step["tool"]):
                        mcp_result = call_skill(step["tool"], step["action"], step_params)
                    else:
                        mcp_result = call_mcp(step["tool"], step["action"], step_params)
                    if mcp_result.get("success", False) or _retry_done >= _retry_max:
                        break
                    # MCP_NOT_CONFIGURED不重试(配置缺失,重试无意义)
                    if mcp_result.get("code") == "MCP_NOT_CONFIGURED":
                        logger.error(f"[content-orchestrator] 步骤'{step['name']}'工具'{step['tool']}'未配置,跳过重试")
                        break
                    _retry_done += 1
                    logger.warning(f"[content-orchestrator] P0-27: 步骤'{step['name']}'第{_retry_done}/{_retry_max}次重试")

                # V42-LOG: 关键数据流转埋点 — 步骤执行后(记录输出变化)
                if _log_tool in _LOG_TOOLS:
                    _result_data = mcp_result.get("data") if isinstance(mcp_result.get("data"), dict) else {}
                    _result_content = (_result_data.get("content") or _result_data.get("optimized_content")
                                        or _result_data.get("adapted_content") or _result_data.get("formatted_content")
                                        or _result_data.get("script") or _result_data.get("script_text") or "")
                    _delta = len(str(_result_content)) - len(str(step_params.get("content") or step_params.get("text") or step_params.get("script") or ""))
                    logger.info(
                        f"[STEP-POST] step={i+1} tool={_log_tool} action={_log_action} | "
                        f"success={mcp_result.get('success', False)} | "
                        f"result_content_len={len(str(_result_content)) if _result_content else 0} | "
                        f"delta={_delta:+d} | "
                        f"seo_score={_result_data.get('seo_score', 'N/A')} | "
                        f"geo_score={_result_data.get('geo_score', 'N/A')} | "
                        f"compliance_passed={_result_data.get('passed', _result_data.get('compliance_passed', 'N/A'))} | "
                        f"data_keys={sorted(list(_result_data.keys()))[:10]} | "
                        f"error={mcp_result.get('error', 'N/A')}"
                    )

                step_result = {
                    "step": i + 1,
                    "name": step["name"],
                    "tool": step["tool"],
                    "action": step["action"],
                    "success": mcp_result.get("success", False),
                    "data": mcp_result.get("data", {}),
                    "error": mcp_result.get("error"),
                    "from_cache": False,
                }

                # Token优化: 成功的LLM生成步骤写入缓存
                if cache and mcp_result.get("success", False):
                    _cache_step_result(cache, product_id, step["name"], i + 1, mcp_result, step_params)

            results.append(step_result)

            # 防查重检测: 检查content-rewriter detect返回的data.status
            # V43修复: block时自动改写+重新检测(30天无人值守要求自愈)
            # V43-LOG: 详细记录改写前后SimHash指纹值,便于排查改写失败原因
            if (step.get("tool") == "content-rewriter" and step.get("action") == "detect"
                    and step_result.get("success") and step_result.get("data", {}).get("status") == "block"):
                _block_reason = step_result.get("data", {}).get("message", "同平台内容重复(SimHash)")
                _current_content = step_params.get("content", previous_output.get("content", ""))
                _platform = step_params.get("platform", params.get("platform", "unknown"))
                _orig_fp = step_result.get("data", {}).get("fingerprint", "N/A")
                _orig_same_dist = step_result.get("data", {}).get("min_same_platform_distance", "N/A")
                _orig_cross_dist = step_result.get("data", {}).get("min_cross_platform_distance", "N/A")
                logger.info(
                    f"[DEDUP-AUTOHEAL] step={i+1} 防查重block触发自愈 | "
                    f"platform={_platform} | reason={_block_reason} | "
                    f"原指纹={_orig_fp} | 同平台距离={_orig_same_dist} | 跨平台距离={_orig_cross_dist} | "
                    f"内容长度={len(_current_content)}"
                )

                # 步骤1: 调用content-rewriter rewrite进行改写
                _rewrite_result = call_skill("content-rewriter", "rewrite", {
                    "content": _current_content,
                    "platform": _platform,
                    "use_llm": True,
                })
                if _rewrite_result.get("success") and _rewrite_result.get("data", {}).get("rewritten"):
                    _rewritten = _rewrite_result["data"]["rewritten"]
                    logger.info(
                        f"[DEDUP-AUTOHEAL] 改写完成 | "
                        f"原文长度={len(_current_content)} → 改写后长度={len(_rewritten)} | "
                        f"内容变化={len(_rewritten) != len(_current_content)}"
                    )
                    # 步骤2: 重新检测改写后的内容
                    _recheck_result = call_skill("content-rewriter", "detect", {
                        "content": _rewritten,
                        "platform": _platform,
                    })
                    if _recheck_result.get("success"):
                        _recheck_status = _recheck_result.get("data", {}).get("status", "unknown")
                        _recheck_fp = _recheck_result.get("data", {}).get("fingerprint", "N/A")
                        _recheck_same_dist = _recheck_result.get("data", {}).get("min_same_platform_distance", "N/A")
                        _recheck_cross_dist = _recheck_result.get("data", {}).get("min_cross_platform_distance", "N/A")
                        logger.info(
                            f"[DEDUP-AUTOHEAL] 重新检测结果 | "
                            f"status={_recheck_status} | 新指纹={_recheck_fp} | "
                            f"同平台距离={_recheck_same_dist} | 跨平台距离={_recheck_cross_dist} | "
                            f"指纹变化={'Y' if _recheck_fp != _orig_fp else 'N'}"
                        )
                    if _recheck_result.get("success") and _recheck_result.get("data", {}).get("status") != "block":
                        # 改写成功,更新内容
                        logger.info(f"[DEDUP-AUTOHEAL] 自愈成功: 改写后通过防查重检测,继续管道")
                        previous_output["content"] = _rewritten
                        step_result["data"]["status"] = "pass"
                        step_result["data"]["message"] = "改写后通过防查重检测"
                        step_result["data"]["rewritten"] = True
                        step_result["data"]["original_fingerprint"] = _orig_fp
                        step_result["data"]["new_fingerprint"] = _recheck_fp
                    elif not _recheck_result.get("success"):
                        # V43修复(BUG-12): 检测失败(技术错误)不应等同于查重失败,降级放行已改写内容
                        logger.warning(
                            f"[DEDUP-AUTOHEAL] 重新检测失败(技术错误),降级放行已改写内容 | "
                            f"error={_recheck_result.get('error', 'N/A')} | "
                            f"原指纹={_orig_fp} | 改写后内容已更新"
                        )
                        previous_output["content"] = _rewritten
                        step_result["data"]["status"] = "pass"
                        step_result["data"]["message"] = f"改写后检测失败(技术错误),降级放行: {_recheck_result.get('error', '')}"
                        step_result["data"]["rewritten"] = True
                        step_result["data"]["original_fingerprint"] = _orig_fp
                    else:
                        # 改写后仍block
                        logger.warning(
                            f"[DEDUP-AUTOHEAL] 自愈失败: 改写后仍block,阻断管道 | "
                            f"原指纹={_orig_fp} → 新指纹={_recheck_result.get('data', {}).get('fingerprint', 'N/A')} | "
                            f"改写未能产生足够差异"
                        )
                        step_result["success"] = False
                        step_result["error"] = f"防查重拦截: 改写后仍重复 - {_block_reason}"
                        step_result["code"] = "DEDUP_BLOCK_AFTER_REWRITE"
                else:
                    # 改写失败
                    _rw_error = _rewrite_result.get("error", "未知错误")
                    logger.warning(
                        f"[DEDUP-AUTOHEAL] 改写调用失败 | error={_rw_error} | "
                        f"原指纹={_orig_fp} | 内容长度={len(_current_content)}"
                    )
                    step_result["success"] = False
                    step_result["error"] = f"防查重拦截: {_block_reason} (改写失败: {_rw_error})"
                    step_result["code"] = "DEDUP_BLOCK_REWRITE_FAILED"

            # V43修复: warning(跨平台相似)也触发改写,但不阻断管道
            # 原因: 跨平台相似内容应在质量评分/审核前改写,而非等到publisher层改写(绕过质检)
            if (step.get("tool") == "content-rewriter" and step.get("action") == "detect"
                    and step_result.get("success") and step_result.get("data", {}).get("status") == "warning"):
                _warn_reason = step_result.get("data", {}).get("message", "跨平台内容相似(SimHash)")
                _warn_content = step_params.get("content", previous_output.get("content", ""))
                _warn_platform = step_params.get("platform", params.get("platform", "unknown"))
                _warn_fp = step_result.get("data", {}).get("fingerprint", "N/A")
                _warn_cross_dist = step_result.get("data", {}).get("min_cross_platform_distance", "N/A")
                logger.info(
                    f"[DEDUP-WARN-AUTOHEAL] step={i+1} 跨平台相似warning触发改写 | "
                    f"platform={_warn_platform} | reason={_warn_reason} | "
                    f"原指纹={_warn_fp} | 跨平台距离={_warn_cross_dist} | "
                    f"内容长度={len(_warn_content)}"
                )
                _warn_rewrite = call_skill("content-rewriter", "rewrite", {
                    "content": _warn_content,
                    "platform": _warn_platform,
                    "use_llm": True,
                })
                if _warn_rewrite.get("success") and _warn_rewrite.get("data", {}).get("rewritten"):
                    _warn_rewritten = _warn_rewrite["data"]["rewritten"]
                    logger.info(
                        f"[DEDUP-WARN-AUTOHEAL] 改写完成 | "
                        f"原文长度={len(_warn_content)} → 改写后长度={len(_warn_rewritten)}"
                    )
                    # V43修复(BUG-13): warning改写后也需重新检测,与block处理保持一致
                    _warn_recheck = call_skill("content-rewriter", "detect", {
                        "content": _warn_rewritten,
                        "platform": _warn_platform,
                    })
                    _warn_recheck_status = "unknown"
                    _warn_new_fp = "N/A"
                    if _warn_recheck.get("success"):
                        _warn_recheck_status = _warn_recheck.get("data", {}).get("status", "unknown")
                        _warn_new_fp = _warn_recheck.get("data", {}).get("fingerprint", "N/A")
                        logger.info(
                            f"[DEDUP-WARN-AUTOHEAL] 重新检测结果 | "
                            f"status={_warn_recheck_status} | 新指纹={_warn_new_fp} | "
                            f"指纹变化={'Y' if _warn_new_fp != _warn_fp else 'N'}"
                        )
                    previous_output["content"] = _warn_rewritten
                    step_result["data"]["status"] = "pass" if _warn_recheck_status != "block" else "warning"
                    step_result["data"]["message"] = f"跨平台相似已改写(重检:{_warn_recheck_status})"
                    step_result["data"]["rewritten"] = True
                    step_result["data"]["original_fingerprint"] = _warn_fp
                    step_result["data"]["new_fingerprint"] = _warn_new_fp
                else:
                    logger.warning(
                        f"[DEDUP-WARN-AUTOHEAL] 改写失败,使用原文继续(warning不阻断) | "
                        f"error={_warn_rewrite.get('error', '未知')}"
                    )

            if not step_result.get("success", False):
                # P2-1: 更新步骤状态为failed(来源:31文档P2-1统一编排器)
                if pipeline_state_record and _STATE_AVAILABLE:
                    try:
                        pipeline_state.update_step(
                            pipeline_state_record["id"], step["name"], "failed",
                            error=step_result.get("error"),
                        )
                    except Exception as e:

                        logger.error(f"content_orchestrator: {e}")
                # Token优化: 步骤失败时保存草稿(见30白皮书§十一+修复提示词R14+R33)
                if cache and product_id and results:
                    try:
                        completed_steps = {}
                        for r in results:
                            if r.get("success", False):
                                completed_steps[str(r["step"])] = r
                        if completed_steps:
                            cache.save_draft(product_id, {
                                "completed_steps": completed_steps,
                                "failed_step": i + 1,
                                "failed_step_name": step["name"],
                                "pipeline_name": pipeline_name,
                                "saved_at": datetime.now().isoformat(),
                                "reason": "pipeline_step_failed",
                            })
                            logger.info(f"[content-orchestrator] 步骤失败，草稿已缓存: {product_id}, 已完成{len(completed_steps)}步")
                    except Exception as e:
                        logger.error(f"content orchestrator异常: {e}", exc_info=True)
                        logger.warning(f"[content-orchestrator] 草稿缓存保存失败(非关键): {e}")
                # v2.6修复(BUG-E2E-022): PL-DRAMA管道容错 - 核心步骤(1-3)失败才中断
                # MCP依赖步骤(4-12: 分镜/配音/画面/视频/字幕等)失败时继续执行,记录失败但不中断
                # 这样E2E测试可以验证核心流程(章节获取→剧本转换→系列管理)的完整性
                # P0-27修复: optional/on_error容错支持(来源:pipeline步骤optional/on_error字段)
                _is_optional = step.get("optional", False)
                _on_error = step.get("on_error", "")
                if _is_optional or _on_error in ("skip", "continue"):
                    logger.warning(f"[content-orchestrator] P0-27: 步骤'{step['name']}'失败,optional={_is_optional}/on_error={_on_error},跳过继续: {step_result.get('error', '')[:200]}")
                    continue
                _PL_DRAMA_CORE_STEPS = 3
                if pipeline_name == "PL-DRAMA" and (i + 1) > _PL_DRAMA_CORE_STEPS:
                    _drama_step_name = step['name']
                    _drama_error = step_result.get('error', '')[:200]
                    logger.warning(f"PL-DRAMA步骤{_drama_step_name}失败但管道继续: {_drama_error}")
                    continue
                return {
                    "success": False,
                    "data": {
                        "pipeline_name": pipeline_name,
                        "total_steps": len(steps),
                        "steps_completed": i,
                        "failed_step": i + 1,
                        "failed_step_name": step["name"],
                        "results": results,
                        "cached_steps": cached_steps,
                        "pipeline_state_id": pipeline_state_record["id"] if pipeline_state_record else None,
                    },
                    "error": f"步骤{i+1} '{step['name']}' 失败: {step_result.get('error', '未知错误')}",
                    "code": "PIPELINE_STEP_FAILED",
                }

            # P2-1: 更新步骤状态为completed(来源:31文档P2-1统一编排器)
            if pipeline_state_record and _STATE_AVAILABLE:
                try:
                    pipeline_state.update_step(
                        pipeline_state_record["id"], step["name"], "completed",
                        output=step_result.get("data"),
                    )
                except Exception as e:

                    logger.error(f"content_orchestrator: {e}")

            # BUG-184修复: 3个强制门控检查(来源:SKILL.md§营销注入门控+§内容吸引力评分门控+§内容差异化检查)
            # 仅对5条内容管道(PL-VIDEO/PL-IMAGE/PL-AUDIO/PL-LIPSYNC/PL-COMIC)执行门控
            if pipeline_name in _GATE_PIPELINE_TYPES:
                gate_result = None

                # 门控1: 营销注入门控(步骤名="营销注入")
                if step["name"] == "营销注入":
                    gate_result = _check_marketing_gate(step_result, step_params)
                    if not gate_result["passed"]:
                        logger.warning(f"[content-orchestrator] 营销注入门控失败: {gate_result['error']}")

                # 门控2: 内容吸引力评分门控(步骤名="内容审核"后执行评分)
                elif step["name"] == "内容审核":
                    gate_result = _check_attractiveness_score(step_result, step_params)
                    if not gate_result["passed"]:
                        logger.warning(f"[content-orchestrator] 吸引力评分门控失败: {gate_result['error']}")

                # 门控3: 内容差异化检查(步骤名="多平台发布"前执行)
                elif step["name"] == "多平台发布":
                    gate_result = _check_differentiation(step_params, tenant_id)
                    if not gate_result["passed"]:
                        logger.warning(f"[content-orchestrator] 差异化检查门控失败: {gate_result['error']}")

                # P0-5修复: 门控4 GEO评分≥60门控(步骤名="GEO优化"后执行,来源:02手册§12.7)
                elif step["name"] == "GEO优化":
                    gate_result = _check_geo_score(step_result, step_params)
                    if not gate_result["passed"]:
                        logger.warning(f"[content-orchestrator] GEO评分门控失败: {gate_result['error']}")

                # DEF-95 T07: 门控5 质量评分低分重试(步骤名="内容质量评分"后执行)
                elif step["name"] == "内容质量评分":
                    gate_result = _check_quality_score_with_retry(step_result, step_params, pipeline_id)
                    if not gate_result["passed"]:
                        logger.warning(f"[content-orchestrator] 质量评分门控失败: {gate_result['error']}")
                    elif gate_result.get("code") == "QUALITY_LOW_DEGRADED":
                        logger.warning(f"[content-orchestrator] 质量评分降级放行: {gate_result['error']}")

                # 门控失败则拦截管道执行
                if gate_result and not gate_result["passed"]:
                    return {
                        "success": False,
                        "data": {
                            "pipeline_name": pipeline_name,
                            "total_steps": len(steps),
                            "steps_completed": i + 1,
                            "failed_step": i + 1,
                            "failed_step_name": step["name"],
                            "gate_failed": gate_result["code"],
                            "results": results,
                            "cached_steps": cached_steps,
                            "gate_data": gate_result.get("data", {}),
                            "pipeline_state_id": pipeline_state_record["id"] if pipeline_state_record else None,
                        },
                        "error": gate_result["error"],
                        "code": gate_result["code"],
                    }

            # DEF-KB-14: 捕获PL-PRODUCT步骤1(素材检索)的assets结果(正常执行路径)
            # 步骤1 portal_list_assets返回的assets保存到step1_assets,供步骤3 match_materials消费
            if step.get("name") == "素材检索" and step_result.get("success"):
                _step1_data = step_result.get("data", {})
                if isinstance(_step1_data, dict) and "assets" in _step1_data:
                    step1_assets = _step1_data["assets"]
                    logger.info(f"[content-orchestrator] DEF-KB-14: 捕获步骤1素材检索assets: {len(step1_assets)}个")

            prev_data = step_result.get("data", {})
            previous_output = _merge_step_output(previous_output, prev_data)

        # 发布成功后失效该商品缓存(避免过期内容被复用)
        if cache:
            cache.invalidate_product(product_id)

        # P2-1: 标记管线完成(来源:31文档P2-1统一编排器)
        if pipeline_state_record and _STATE_AVAILABLE:
            try:
                pipeline_state.complete(pipeline_state_record["id"])
            except Exception as e:

                logger.error(f"content_orchestrator: {e}")

        # v2.6修复(BUG-E2E-022): 统计失败的非核心步骤(PL-DRAMA容错模式)
        failed_non_core_steps = [r for r in results if not r.get("success", False)]
        successful_steps = [r for r in results if r.get("success", False)]

        # P0-024修复: PL-DRAMA产出物校验——视频关键步骤失败时标记video_available=false
        # 根因: 非核心步骤(4-12)失败仍返回success=true,前端显示"生成成功"但漫剧无视频/音频
        # 修复: 检查配音/画面/视频合成/字幕生成步骤,任一失败则标记video_available=false
        _VIDEO_CRITICAL_STEPS = {"配音生成", "画面生成", "视频合成", "字幕生成"}
        failed_step_names_set = {r.get("name", "") for r in failed_non_core_steps}
        video_available = not _VIDEO_CRITICAL_STEPS.intersection(failed_step_names_set)

        # BUG-FIX(2026-08-06 Bug20): 添加降级消息,告知用户哪些功能因外部API问题被跳过
        _degradation_messages = []
        _image_degraded = "配图生成" in failed_step_names_set
        if _image_degraded:
            _degradation_messages.append("图片生成因API余额不足已降级跳过，内容将以纯文本形式发布")
        if not video_available:
            _degradation_messages.append("视频关键步骤失败，生成的漫剧不包含视频/音频")

        return {
            "success": True,
            "data": {
                "pipeline_name": pipeline_name,
                "total_steps": len(steps),
                "steps_completed": len(successful_steps),
                "results": results,
                "final_output": previous_output,
                "tenant_assets_count": len(tenant_assets),
                "cached_steps": cached_steps,
                "pipeline_state_id": pipeline_state_record["id"] if pipeline_state_record else None,
                "failed_non_core_steps": len(failed_non_core_steps),
                "failed_step_names": [r.get("name", "") for r in failed_non_core_steps],
                "video_available": video_available,  # P0-024: 前端据此判断漫剧是否可用
                "image_degraded": _image_degraded,  # Bug20: 前端据此判断是否显示"无配图"提示
                "degradation_messages": _degradation_messages,  # Bug20: 用户可见的降级说明
                "partial": len(failed_non_core_steps) > 0,  # PL-DRAMA容错: 非核心步骤失败时标记为部分完成
            },
            "error": None,
            "code": None,
        }
    except ValueError as e:
        logger.error(f"content orchestrator异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "PIPELINE_NOT_FOUND"}
    except Exception as e:
        logger.error(f"content orchestrator异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "EXECUTE_PIPELINE_ERROR"}

def resume_pipeline(pipeline_id: str) -> dict[str, Any]:
    """恢复停滞的管线 - 读取PG中已完成步骤，利用草稿缓存跳过，从第一个未完成步骤继续执行

    FIX-V56-003: 增强recover能力，从诊断报告升级为实际恢复执行
    全链思考:
      - 数据库: 读取content_pipelines.steps JSONB获取已完成步骤输出
      - MCP: 复用execute_pipeline的call_skill/call_mcp调用链
      - Skill: 复用execute_pipeline的步骤执行逻辑，不新增执行路径
      - 配置: LLM端点已在v55.0修复(NINEROUTER_URL+smart-route)
      - UI: pipeline_state.update_step更新PG状态，前端自动感知

    Args:
        pipeline_id: 管线ID (CP-YYYYMMDD-xxxxxx)

    Returns:
        {success: bool, data: {pipeline_id, resumed_from_step, steps_completed, results}, error: str|null, code: str|null}
    """
    try:
        if not _STATE_AVAILABLE:
            return {"success": False, "data": {}, "error": "pipeline_state模块不可用", "code": "STATE_UNAVAILABLE"}

        p = pipeline_state._fetch(pipeline_id)
        if not p:
            return {"success": False, "data": {}, "error": f"管线 {pipeline_id} 不存在", "code": "PIPELINE_NOT_FOUND"}

        pipeline_type = p.get("pipeline_type", "E2E-DAILY")
        tenant_id = p.get("tenant_id", "")
        title = p.get("title", "")
        steps = p.get("steps", [])

        # 找到第一个非completed步骤
        first_non_completed_idx = None
        completed_steps_data = {}
        for i, s in enumerate(steps):
            if isinstance(s, dict):
                status = s.get("status", "pending")
                if status == "completed":
                    # 收集已完成步骤的输出作为草稿缓存
                    step_output = s.get("output")
                    if step_output:
                        completed_steps_data[str(i + 1)] = {
                            "step": i + 1,
                            "name": s.get("id", ""),
                            "tool": "",
                            "action": "",
                            "success": True,
                            "data": step_output if isinstance(step_output, dict) else {"raw_output": step_output},
                            "error": None,
                            "from_draft": True,
                        }
                elif status in ("failed", "pending", "in_progress"):
                    if first_non_completed_idx is None:
                        first_non_completed_idx = i
                        # 重置failed步骤为pending
                        if status == "failed":
                            pipeline_state.update_step(pipeline_id, s.get("id", ""), "pending", error=None)
                            logger.info(f"[content-orchestrator] resume: 重置步骤'{s.get('id','?')}' failed→pending")

        if first_non_completed_idx is None:
            return {"success": True, "data": {"pipeline_id": pipeline_id, "resumed_from_step": None,
                    "message": "所有步骤已完成，无需恢复"}, "error": None, "code": "ALREADY_COMPLETE"}

        resumed_step_name = steps[first_non_completed_idx].get("id", "?")
        logger.info(f"[content-orchestrator] resume: 管线{pipeline_id}从步骤'{resumed_step_name}'(idx={first_non_completed_idx})恢复, 已完成{len(completed_steps_data)}步")

        # 将已完成步骤写入草稿缓存，使execute_pipeline跳过这些步骤
        if _CACHE_AVAILABLE and completed_steps_data:
            try:
                cache = ContentCache()
                product_id = title or pipeline_id
                cache.save_draft(product_id, {"completed_steps": completed_steps_data})
                logger.info(f"[content-orchestrator] resume: 草稿缓存已写入{len(completed_steps_data)}步 product_id={product_id}")
            except Exception as e:
                logger.warning(f"[content-orchestrator] resume: 草稿缓存写入失败(非关键，将重新执行已完成步骤): {e}")

        # 构造执行参数
        params = {"topic": title or "热门话题"}
        if tenant_id:
            params["tenant_id"] = tenant_id
        # FIX-V57-001: 从已完成步骤输出中提取platform,确保resume时模板变量能正确解析
        for _idx, _sd in completed_steps_data.items():
            _sd_data = _sd.get("data", {})
            if isinstance(_sd_data, dict):
                _plat = _sd_data.get("platform", _sd_data.get("platforms", ""))
                if _plat:
                    if isinstance(_plat, list):
                        _plat = _plat[0] if _plat else ""
                    params["platform"] = str(_plat)
                    break
        if "platform" not in params:
            params["platform"] = "weibo"  # 默认有效平台,确保${platform}模板变量可解析

        # 调用execute_pipeline恢复执行
        result = execute_pipeline(pipeline_type, params)

        # 更新原管线状态(不是新创建的管线)
        if result.get("success"):
            logger.info(f"[content-orchestrator] resume: 管线{pipeline_id}恢复执行成功")
        else:
            logger.warning(f"[content-orchestrator] resume: 管线{pipeline_id}恢复执行失败: {result.get('error')}")

        return {
            "success": result.get("success", False),
            "data": {
                "pipeline_id": pipeline_id,
                "pipeline_type": pipeline_type,
                "resumed_from_step": resumed_step_name,
                "resumed_from_idx": first_non_completed_idx,
                "completed_steps_before_resume": len(completed_steps_data),
                "execute_result": result.get("data", {}),
            },
            "error": result.get("error"),
            "code": result.get("code"),
        }
    except Exception as e:
        logger.error(f"[content-orchestrator] resume异常: {e}", exc_info=True)
        return {"success": False, "data": {}, "error": str(e), "code": "RESUME_ERROR"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="内容编排器")
    parser.add_argument("--action", choices=["orchestrate", "execute", "list", "recover", "list-active", "hotspot-topics", "resume"], required=True)
    parser.add_argument("--pipeline", type=str, help="管道类型")
    parser.add_argument("--params", type=str, default="{}", help="管道参数(JSON)")
    # P2-1: 新增CLI子命令参数(来源:31文档P2-1统一编排器)
    parser.add_argument("--pipeline-id", type=str, help="管线ID(用于recover)")
    parser.add_argument("--tenant-id", type=str, help="租户ID")
    parser.add_argument("--count", type=int, default=10, help="选题数量(用于hotspot-topics)")

    args = parser.parse_args()

    if args.action == "list":
        print(json.dumps(list_pipelines(), ensure_ascii=False, indent=2))
    elif args.action == "execute":
        if not args.pipeline:
            print(json.dumps({
                "success": False, "data": {},
                "error": "缺少--pipeline参数", "code": "MISSING_PIPELINE",
            }, ensure_ascii=False))
            sys.exit(1)
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            logger.error(f"Exception in except block: {e}");
            logger.error(json.dumps({
                "success": False, "data": {},
                "error": f"params JSON解析失败: {e}", "code": "INVALID_PARAMS",
            }, ensure_ascii=False))
            sys.exit(1)
        result = execute_pipeline(args.pipeline, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.action == "orchestrate":
        if not args.pipeline:
            print(json.dumps({
                "success": False, "data": {},
                "error": "缺少--pipeline参数", "code": "MISSING_PIPELINE",
            }, ensure_ascii=False))
            sys.exit(1)
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError as e:
            logger.error(f"Exception in except block: {e}");
            logger.error(json.dumps({
                "success": False, "data": {},
                "error": f"params JSON解析失败: {e}", "code": "INVALID_PARAMS",
            }, ensure_ascii=False))
            sys.exit(1)
        result = orchestrate_pipeline(args.pipeline, params)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    # P2-1: 新增CLI子命令(来源:31文档P2-1统一编排器)
    elif args.action == "recover":
        pid = args.pipeline_id
        if not pid:
            print(json.dumps({
                "success": False, "data": {},
                "error": "缺少--pipeline-id参数", "code": "MISSING_PIPELINE_ID",
            }, ensure_ascii=False))
            sys.exit(1)
        if not _STATE_AVAILABLE:
            print(json.dumps({
                "success": False, "data": {},
                "error": "pipeline_state模块不可用", "code": "STATE_UNAVAILABLE",
            }, ensure_ascii=False))
            sys.exit(1)
        result = pipeline_state.recover(pid)
        if result:
            print(json.dumps({"success": True, "data": result, "error": None, "code": None}, ensure_ascii=False, indent=2, default=str))
        else:
            print(json.dumps({"success": False, "data": {}, "error": f"管线 {pid} 不存在", "code": "PIPELINE_NOT_FOUND"}, ensure_ascii=False))
            sys.exit(1)
    elif args.action == "list-active":
        if not _STATE_AVAILABLE:
            print(json.dumps({
                "success": False, "data": {},
                "error": "pipeline_state模块不可用", "code": "STATE_UNAVAILABLE",
            }, ensure_ascii=False))
            sys.exit(1)
        items = pipeline_state.list_active(args.tenant_id or "")
        print(json.dumps({
            "success": True,
            "data": {"active_count": len(items), "pipelines": items},
            "error": None, "code": None,
        }, ensure_ascii=False, indent=2, default=str))
    elif args.action == "hotspot-topics":
        if not _HOTSPOT_AVAILABLE:
            print(json.dumps({
                "success": False, "data": {},
                "error": "hotspot_engine模块不可用", "code": "HOTSPOT_UNAVAILABLE",
            }, ensure_ascii=False))
            sys.exit(1)
        tenant_id = args.tenant_id or ""
        if not tenant_id:
            print(json.dumps({
                "success": False, "data": {},
                "error": "缺少--tenant-id参数", "code": "MISSING_TENANT_ID",
            }, ensure_ascii=False))
            sys.exit(1)
        result = hotspot_engine.orchestrate(tenant_id, args.count)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.action == "resume":
        pid = args.pipeline_id
        if not pid:
            print(json.dumps({
                "success": False, "data": {},
                "error": "缺少--pipeline-id参数", "code": "MISSING_PIPELINE_ID",
            }, ensure_ascii=False))
            sys.exit(1)
        result = resume_pipeline(pid)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
