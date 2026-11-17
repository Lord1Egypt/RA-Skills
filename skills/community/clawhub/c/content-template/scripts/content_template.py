#!/usr/bin/env python3
"""
content_template.py - 内容模板管理 exec 脚本
功能: 模板增删改查、变量替换(Jinja2引擎)、A/B测试、模板继承
输入: JSON (action/template_id/variables)
输出: JSON (template/result/suggestions)
v2.0: Jinja2模板引擎升级，支持条件渲染/循环/继承，向后兼容旧{var}格式
"""
import json

import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

import logging

try:
    from jinja2 import Environment, BaseLoader, TemplateSyntaxError, UndefinedError
except ImportError:
    # Jinja2不可用时降级为纯字符串替换
    Environment = None
    BaseLoader = None
    TemplateSyntaxError = None
    UndefinedError = None

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("content-template", source="skills/_lazy/content-template/scripts/content_template.py")
from mcps.shared.atomic_write import atomic_read_json, atomic_write_json
from mcps.shared.constants import DISTILL_TONE_TO_MARKETING_MAP

TEMPLATE_DIR = Path(__file__).resolve().parents[3] / "data" / "content" / "templates"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)

# Jinja2环境配置
_jinja_env = None
if Environment is not None:
    _jinja_env = Environment(
        loader=BaseLoader(),
        keep_trailing_newline=True,
        undefined=__import__('jinja2').StrictUndefined,
    )

def _is_jinja_template(content: str) -> bool:
    """检测内容是否为Jinja2模板格式(含{{ }}/{% %}/{# #})"""
    return bool(re.search(r'\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\}', content))

def _convert_legacy_to_jinja(content: str) -> str:
    """将旧格式{variable_name}转换为Jinja2格式{{ variable_name }}

    仅转换{word}模式，不转换{{ }}/{% %}等已有Jinja2语法
    """
    # 先保护已有的Jinja2语法，避免误转换
    # 匹配{word}但不匹配{{ word }}/{% %}/{# #}
    def _replace_single_brace(match: re.Match) -> str:
        var_name = match.group(1)
        return f"{{{{ {var_name} }}}}"

    # 匹配{word}但不紧跟{或}（排除{{和}}）
    result = re.sub(r'(?<!\{)\{(\w+)\}(?!\})', _replace_single_brace, content)
    return result

def _render_jinja(content: str, variables: dict) -> tuple:
    """使用Jinja2渲染模板

    返回: (rendered_content, warnings_list)
    """
    warnings = []

    if _jinja_env is None:
        # Jinja2不可用，降级为简单字符串替换
        rendered = content
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
            rendered = rendered.replace(f"{{{key}}}", str(value))
        warnings.append("Jinja2不可用，已降级为简单字符串替换")
        return rendered, warnings

    # 自动检测并转换旧格式
    if not _is_jinja_template(content):
        content = _convert_legacy_to_jinja(content)

    try:
        template = _jinja_env.from_string(content)
        rendered = template.render(**variables)
        return rendered, warnings
    except TemplateSyntaxError as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        warnings.append(f"Jinja2模板语法错误: {e}")
        # 降级为简单替换
        rendered = content
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
            rendered = rendered.replace(f"{{{key}}}", str(value))
        return rendered, warnings
    except UndefinedError as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        warnings.append(f"Jinja2变量未定义: {e}")
        # 使用默认值重新渲染
        try:
            env_fallback = Environment(
                loader=BaseLoader(),
                keep_trailing_newline=True,
                undefined=__import__('jinja2').Undefined,
            )
            template = env_fallback.from_string(content)
            rendered = template.render(**variables)
            return rendered, warnings
        except Exception as e:
            logger.warning(f"Unexpected error: {e}", exc_info=True)
            rendered = content
            for key, value in variables.items():
                rendered = rendered.replace(f"{{{{ {key} }}}}", str(value))
                rendered = rendered.replace(f"{{{key}}}", str(value))
            return rendered, warnings

def _extract_jinja_variables(content: str) -> list:
    """提取Jinja2模板中的变量名"""
    # 提取{{ var }}中的变量
    vars_found = re.findall(r'\{\{\s*(\w+)\s*\}\}', content)
    # 提取{% if var %} / {% for x in var %}中的变量
    vars_found.extend(re.findall(r'\{%\s*if\s+(\w+)', content))
    vars_found.extend(re.findall(r'\{%\s*for\s+\w+\s+in\s+(\w+)', content))
    return list(set(vars_found))

def get_templates() -> Any:
    """获取所有模板

    Returns:
        Any: 返回值说明
    """
    templates = []
    for f in TEMPLATE_DIR.glob("*.json"):
        templates.append(atomic_read_json(f, {}))
    return templates

def get_template(template_id: str) -> dict[str, Any]:
    """获取单个模板

    Args:
        template_id (str): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    fpath = TEMPLATE_DIR / f"{template_id}.json"
    if not fpath.exists():
        return {}
    return atomic_read_json(fpath, {})

def create_template(template_id: str, name: str, content: str, platform: str, tags: Optional[list] = None, template_type: str = "generic", category: str = "default", variables: Optional[dict] = None, extends: Optional[str] = None) -> dict[str, Any]:
    """创建模板

    extends: 父模板ID，用于模板继承({% extends %})

    Args:
        template_id (str): 参数说明
        name (str): 参数说明
        content (str): 参数说明
        platform (str): 参数说明
        tags (Optional[list]): 参数说明
        template_type (str): 参数说明
        category (str): 参数说明
        variables (Optional[dict]): 参数说明
        extends (Optional[str]): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    # v53.0修复(BUG-WAVE20-004): content为None时返回结构化错误,避免re.findall(None)崩溃
    if not content:
        return {"success": False, "data": {}, "error": "content参数必填,create action用于注册模板而非生成内容. 如需生成内容请使用action=generate", "code": "CT-ERR-CONTENT-REQUIRED"}

    fpath = TEMPLATE_DIR / f"{template_id}.json"
    if fpath.exists():
        return {"success": False, "error": f"模板已存在: {template_id}", "code": "CT-ERR-01"}

    defined_vars = variables or {}
    if not defined_vars:
        # 同时提取旧格式和新格式变量
        legacy_vars = re.findall(r'(?<!\{)\{(\w+)\}(?!\})', content)
        jinja_vars = _extract_jinja_variables(content)
        all_vars = list(set(legacy_vars + jinja_vars))
        defined_vars = {v: f"<{v}的值>" for v in all_vars}

    template = {
        "template_id": template_id,
        "name": name,
        "type": template_type,
        "category": category,
        "variables": defined_vars,
        "content": content,
        "platform": platform,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "usage_count": 0
    }
    if extends:
        template["extends"] = extends
    atomic_write_json(fpath, template, indent=2, ensure_ascii=False)
    return {"success": True, "data": template, "error": None, "code": "CT-SUCCESS-01"}

def replace_variables(template_id: str, variables: dict) -> dict[str, Any]:
    """变量替换生成内容(Jinja2引擎，向后兼容旧{var}格式)

    Args:
        template_id (str): 参数说明
        variables (dict): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    template = get_template(template_id)
    if not template:
        return {"success": False, "error": f"模板不存在: {template_id}", "code": "CT-ERR-02"}

    content = template["content"]
    defined_vars = template.get("variables", {})
    required_vars = [k for k, v in defined_vars.items() if not str(v).startswith("<")]

    # 检测模板格式
    is_jinja = _is_jinja_template(content)
    engine_used = "jinja2" if is_jinja or _jinja_env is not None else "legacy"

    # 检查必填变量
    missing_required = []
    if is_jinja:
        jinja_vars = _extract_jinja_variables(content)
        missing_required = [v for v in required_vars if v not in variables and v in jinja_vars]
    else:
        missing_required = [v for v in required_vars if v not in variables and f"{{{v}}}" in content]

    # 使用Jinja2渲染
    rendered, render_warnings = _render_jinja(content, variables)

    # 检测未替换变量
    unreplaced_legacy = re.findall(r'(?<!\{)\{(\w+)\}(?!\})', rendered)
    unreplaced_jinja = re.findall(r'\{\{\s*(\w+)\s*\}\}', rendered)
    unreplaced = list(set(unreplaced_legacy + unreplaced_jinja))

    warnings = list(render_warnings)
    if unreplaced:
        warnings.append(f"内容中仍有{len(unreplaced)}个未替换变量: {unreplaced}")
    if missing_required:
        warnings.append(f"缺少必填变量: {missing_required}")

    # 更新使用次数
    fpath = TEMPLATE_DIR / f"{template_id}.json"
    template["usage_count"] = template.get("usage_count", 0) + 1
    template["updated_at"] = datetime.now().isoformat()
    atomic_write_json(fpath, template, indent=2, ensure_ascii=False)

    result_data = {
        "content": rendered,
        "template_id": template_id,
        "variables_used": list(variables.keys()),
        "engine": engine_used,
    }
    if warnings:
        result_data["warnings"] = warnings
        result_data["unreplaced_variables"] = unreplaced
        result_data["missing_required_variables"] = missing_required
    return {"success": True, "data": result_data, "error": None, "code": "CT-SUCCESS-02"}

def render_with_inheritance(template_id: str, variables: dict) -> dict[str, Any]:
    """模板继承渲染: 子模板{% extends "parent_id" %} + {% block name %}

    1. 读取子模板，检测{% extends "parent_id" %}
    2. 加载父模板
    3. 使用Jinja2的继承机制渲染

    Args:
        template_id (str): 参数说明
        variables (dict): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    template = get_template(template_id)
    if not template:
        return {"success": False, "error": f"模板不存在: {template_id}", "code": "CT-ERR-04"}

    content = template["content"]
    extends_match = re.search(r'\{%\s*extends\s+["\'](\w+)["\']\s*%\}', content)

    if not extends_match:
        # 无继承，直接渲染
        return replace_variables(template_id, variables)

    parent_id = extends_match.group(1)
    parent_template = get_template(parent_id)
    if not parent_template:
        return {"success": False, "error": f"父模板不存在: {parent_id}", "code": "CT-ERR-05"}

    if _jinja_env is None:
        return {"success": False, "error": "Jinja2不可用，模板继承需要Jinja2引擎", "code": "CT-ERR-06"}

    # 构建继承渲染环境
    class _InheritanceLoader(BaseLoader):
        def __init__(self, templates_dict: dict):
            self.templates = templates_dict

        def get_source(self, env: Any, name: Any) -> Any:
            """获取 source

            Args:
                env (Any): 参数说明
                name (Any): 参数说明

            Returns:
                Any: 返回值说明
            
            Raises:
                TemplateNotFound: 异常说明
            """
            if name in self.templates:
                source = self.templates[name]
                return source, name, lambda: True
            raise __import__('jinja2').TemplateNotFound(name)

    templates_map = {
        parent_id: parent_template["content"],
        template_id: content,
    }
    env = Environment(
        loader=_InheritanceLoader(templates_map),
        keep_trailing_newline=True,
        undefined=__import__('jinja2').Undefined,
    )

    try:
        tmpl = env.get_template(template_id)
        rendered = tmpl.render(**variables)
    except TemplateSyntaxError as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        return {"success": False, "error": f"模板继承语法错误: {e}", "code": "CT-ERR-07"}
    except Exception as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        return {"success": False, "error": f"模板继承渲染失败: {e}", "code": "CT-ERR-UNKNOWN"}

    # 更新使用次数
    fpath = TEMPLATE_DIR / f"{template_id}.json"
    template["usage_count"] = template.get("usage_count", 0) + 1
    template["updated_at"] = datetime.now().isoformat()
    atomic_write_json(fpath, template, indent=2, ensure_ascii=False)

    return {
        "success": True,
        "data": {
            "content": rendered,
            "template_id": template_id,
            "parent_id": parent_id,
            "variables_used": list(variables.keys()),
            "engine": "jinja2-inheritance",
        },
        "error": None,
        "code": "CT-SUCCESS-04"
    }

def ab_test(template_a: str, template_b: str, metrics_a: dict, metrics_b: dict) -> dict[str, Any]:
    """A/B测试对比

    Args:
        template_a (str): 参数说明
        template_b (str): 参数说明
        metrics_a (dict): 参数说明
        metrics_b (dict): 参数说明

    Returns:
        dict[str, Any]: 返回值说明
    """
    score_a = metrics_a.get("views", 0) * 0.25 + metrics_a.get("likes", 0) * 0.3 + metrics_a.get("comments", 0) * 0.2 + metrics_a.get("shares", 0) * 0.25
    score_b = metrics_b.get("views", 0) * 0.25 + metrics_b.get("likes", 0) * 0.3 + metrics_b.get("comments", 0) * 0.2 + metrics_b.get("shares", 0) * 0.25

    winner = "A" if score_a > score_b else "B"
    diff = abs(score_a - score_b) / max(score_a, score_b, 1) * 100

    return {
        "success": True,
        "data": {
            "winner": winner,
            "scores": {"A": round(score_a, 1), "B": round(score_b, 1)},
            "difference_percent": round(diff, 1),
            "recommendation": f"模板{winner}表现更优，建议使用模板{winner}"
        },
        "error": None,
        "code": "CT-SUCCESS-03"
    }

def generate_content(topic: str, template_type: str = "article", suggestions: list = None, content_angles: str = "", tenant_id: str = "",
                      brand_profile: dict = None, style_fingerprint: dict = None, persona_profile: dict = None,
                      brand_keywords: list = None, kb_content: str = "", content_guidelines: dict = None,
                      recent_lessons: list = None) -> dict[str, Any]:
    """根据选题调用LLM生成文章内容(BUG-WAVE20-004修复)

    根因: pipeline"文案生成"步骤原用create action(注册模板),语义错配导致content=None崩溃
    修复: 新增generate action,调用LLM基于选题生成真实文章内容

    V58.0修复(BUG-WAVE24-001): 改用unified_llm.llm_chat()统一入口替代直接调用9Router
    根因: 9Router上游provider(SiliconFlow/DeepSeek)余额不足(402 Payment Required),导致超时
    修复: 通过unified_llm的fallback chain自动切换到sensenova/zhipu等可用provider
    (R75.2连接统一化: 禁止独立API调用,使用unified_llm统一入口)

    架构修复: 生成prompt增强,注入品牌/风格/IP/SEO/KB上下文(当参数存在时才添加)

    Args:
        topic: 选题(来自"选题决策"步骤输出的topic/suggestions)
        template_type: 内容类型(article/product_intro/short_post等)
        suggestions: 选题建议列表(来自content-research-mcp)
        content_angles: 内容角度(来自content-research-mcp)
        tenant_id: 租户ID(用于品牌关键词注入)
        brand_profile: 品牌信息(brand_name/brand_tone/slogan等)
        style_fingerprint: 写作风格指纹(tone_tendency/vocabulary_preference等)
        persona_profile: 人设特质(summary等)
        brand_keywords: 品牌关键词列表(需在正文中自然出现)
        kb_content: 知识库参考内容(供LLM参考但不直接复制)

    Returns:
        {success: bool, data: {content, title, word_count, topic}, error: str|null, code: str|null}
    """
    import os as _os

    # 构建LLM提示词
    topic_text = topic or (suggestions[0] if suggestions else "热门话题")
    # FIX-V55-003: content_angles类型保护,可能是list/str/None
    # content-research-mcp返回的content_angles是list[str],直接传入会触发格式异常
    if isinstance(content_angles, list):
        angles_text = "\n".join(f"- {a}" for a in content_angles) if content_angles else ""
    elif content_angles:
        angles_text = str(content_angles)
    else:
        angles_text = ""

    type_prompts = {
        "article": "请写一篇800-1200字的深度文章，包含引人入胜的标题、开头引入、正文论述和结尾总结",
        "product_intro": "请写一段300-500字的产品介绍文案，突出产品卖点和使用场景",
        "short_post": "请写一篇200-300字的短文/动态，适合社交媒体发布，语言轻松活泼",
    }
    format_prompt = type_prompts.get(template_type, type_prompts["article"])

    # 架构修复: 构建可选的上下文信息(当参数存在时才添加)
    context_parts = []
    if brand_profile:
        context_parts.append(f"品牌信息: 品牌名={brand_profile.get('brand_name','')}, 品牌调性={brand_profile.get('brand_tone','')}, Slogan={brand_profile.get('slogan','')}")
    if style_fingerprint:
        context_parts.append(f"写作风格: 语气={style_fingerprint.get('tone_tendency','')}, 词汇偏好={style_fingerprint.get('vocabulary_preference','')}")
        # 消费表现反馈数据(从raw_analysis中提取各维度优化建议)
        _raw = style_fingerprint.get("raw_analysis") or {}
        if isinstance(_raw, str):
            try:
                _raw = json.loads(_raw)
            except (json.JSONDecodeError, TypeError):
                _raw = {}
        for _dim_key, _dim_label in [
            ("performance_adjustments", "综合表现"),
            ("performance_seo", "SEO表现"),
            ("performance_geo", "GEO表现"),
            ("performance_brand", "品牌表现"),
            ("performance_marketing", "营销表现"),
        ]:
            _dim_data = _raw.get(_dim_key)
            if _dim_data and isinstance(_dim_data, dict):
                _parts = []
                for _field in ("title_pattern", "content_structure", "topic_preference", "tone_adjustment"):
                    _val = _dim_data.get(_field)
                    if _val:
                        _parts.append(f"{_field}={_val}")
                _avoid = _dim_data.get("avoid_patterns")
                if _avoid and isinstance(_avoid, list) and _avoid:
                    _parts.append(f"避免={','.join(_avoid[:3])}")
                if _parts:
                    context_parts.append(f"{_dim_label}优化建议: {', '.join(_parts)}")
    if persona_profile:
        context_parts.append(f"人设特质: {persona_profile.get('summary','')}")
    if brand_keywords:
        context_parts.append(f"品牌关键词(需在正文中自然出现): {', '.join(brand_keywords)}")
    if content_guidelines:
        tone = content_guidelines.get("tone", "")
        target_audience = content_guidelines.get("target_audience", "")
        forbidden_words = content_guidelines.get("forbidden_words", [])
        required_mentions = content_guidelines.get("required_mentions", [])
        key_points = content_guidelines.get("key_points", [])
        parts = []
        if tone:
            parts.append(f"语气={tone}")
        if target_audience:
            parts.append(f"目标受众={target_audience}")
        if forbidden_words:
            parts.append(f"禁用词={forbidden_words}")
        if required_mentions:
            parts.append(f"必须提及={required_mentions}")
        if key_points:
            parts.append(f"关键要点={key_points}")
        if parts:
            context_parts.append(f"内容指南: {', '.join(parts)}")
    if kb_content:
        context_parts.append(f"知识库参考(请参考但不直接复制): {kb_content[:500]}")
    if recent_lessons:
        lessons_text = "; ".join(recent_lessons[:5])
        context_parts.append(f"近期发布经验(请在创作时参考): {lessons_text}")

    context_str = "\n".join(context_parts) if context_parts else ""

    prompt = f"""请根据以下选题创作内容。

选题: {topic_text}
内容角度: {angles_text}
{context_str}
要求: {format_prompt}
请确保品牌信息和关键词自然融入内容。请直接输出文章内容，不要添加额外的说明或标记。"""

    # V58.0修复: 使用unified_llm统一入口替代直接调用9Router(R75.2连接统一化)
    # BUG-FIX(2026-08-05): 原fallback_chain跳过9router是错误的,
    # 9Router容器正常运行(juejin-9router:20128),free-first路由可用。
    # sensenova/zhipu的API Key为空,dashscope返回403未购买模型,
    # 导致整个fallback链全部失败。修复: 将9router加入fallback链首位。
    from mcps.shared.unified_llm import llm_chat

    try:
        result = llm_chat(
            prompt=prompt,
            system_prompt="你是一位专业的内容创作者，擅长根据选题创作高质量、有深度的内容。",
            caller="content-template",
            max_tokens=2048,
            temperature=0.7,
            fallback_chain=["9router", "sensenova", "zhipu", "dashscope"],
            max_retries=1,  # R10修复: 9Router超时192s×1次=192s,加fallback约282s<orchestrator 290s
        )

        if not result.get("success"):
            error_msg = result.get("error", "unknown error")
            logger.error(f"[content-template] generate_content LLM调用失败: {error_msg}")
            return {"success": False, "data": {}, "error": f"LLM调用失败: {error_msg}", "code": "CT-GEN-LLM-ERROR"}

        content = result.get("raw_text", "")
        if not content or not content.strip():
            return {"success": False, "data": {}, "error": "LLM返回空内容", "code": "CT-GEN-EMPTY"}

        # 提取标题(第一行或前50字)
        lines = content.strip().split("\n")
        title = lines[0].strip("#").strip() if lines else content[:50]

        return {
            "success": True,
            "data": {
                "content": content,
                "title": title,
                "word_count": len(content),
                "topic": topic_text,
                "template_type": template_type,
                "model": "unified_llm",
            },
            "error": None,
            "code": "CT-GEN-SUCCESS",
        }
    except Exception as e:
        logger.error(f"[content-template] generate_content LLM调用失败: {e}")
        return {"success": False, "data": {}, "error": f"LLM调用失败: {e}", "code": "CT-GEN-LLM-ERROR"}

def main():
    """主函数: 读取输入 → 执行操作 → 输出结果"""
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            print(json.dumps({"success": False, "data": {}, "error": "无输入数据", "code": "CT-ERR-00"}))
            sys.exit(1)

        try:
            data = json.loads(raw_input)
        except json.JSONDecodeError as e:
            logger.warning(f"[content_template] 输入JSON解析失败: {e}")
            logger.error(json.dumps({"success": False, "data": {}, "error": "输入JSON格式错误", "code": "CT-ERR-01"}))
            sys.exit(1)

        action = data.get("action", "list")

        if action == "list":
            result = {"success": True, "data": {"templates": get_templates()}, "error": None, "code": "CT-SUCCESS-00"}
        elif action == "get":
            result = {"success": True, "data": {"template": get_template(data.get("template_id"))}, "error": None, "code": "CT-SUCCESS-00"}
        elif action == "generate":
            # v53.0修复(BUG-WAVE20-004): 新增generate action,调用LLM生成文章内容
            # 前序步骤(选题决策)输出通过step_params.update(previous_output)传入:
            # - topic: 选题标题
            # - suggestions: 选题建议列表
            # - content_angles: 内容角度
            # 架构修复: 额外提取品牌/风格/IP/KB上下文(由content-orchestrator预注入)
            topic = data.get("topic") or data.get("title", "")
            suggestions = data.get("suggestions", [])
            content_angles = data.get("content_angles", "")
            if not topic and suggestions:
                # 从suggestions提取topic(可能是字符串列表或字典列表)
                first = suggestions[0]
                topic = first if isinstance(first, str) else first.get("title", first.get("topic", ""))
            # FIX-V55-003: content_angles可能嵌套在suggestions[0]中(content-research-mcp返回格式)
            if not content_angles and suggestions:
                first = suggestions[0]
                if isinstance(first, dict):
                    content_angles = first.get("content_angles", "")
            template_type = data.get("template_type", data.get("type", "article"))
            tenant_id = data.get("tenant_id", "")
            # 架构修复: 提取上下文参数(由content-orchestrator预注入到step_params)
            brand_profile = data.get("brand_profile") or None
            style_fingerprint = data.get("style_fingerprint") or None
            persona_profile = data.get("persona_profile") or None
            brand_keywords = data.get("brand_keywords") or None
            kb_content = data.get("kb_content", "")
            content_guidelines = data.get("content_guidelines") or None
            recent_lessons = data.get("recent_lessons") or None
            result = generate_content(topic, template_type, suggestions, content_angles, tenant_id,
                                        brand_profile=brand_profile, style_fingerprint=style_fingerprint,
                                        persona_profile=persona_profile, brand_keywords=brand_keywords,
                                        kb_content=kb_content, content_guidelines=content_guidelines,
                                        recent_lessons=recent_lessons)
        elif action == "create":
            result = create_template(
                data.get("template_id"), data.get("name"), data.get("content"),
                data.get("platform"), data.get("tags"), data.get("type", "generic"),
                data.get("category", "default"), data.get("variables"),
                data.get("extends")
            )
        elif action == "replace":
            result = replace_variables(data.get("template_id"), data.get("variables", {}))
        elif action == "render_inheritance":
            result = render_with_inheritance(data.get("template_id"), data.get("variables", {}))
        elif action == "ab_test":
            result = ab_test(data.get("template_a"), data.get("template_b"), data.get("metrics_a", {}), data.get("metrics_b", {}))
        elif action == "polish":
            # BUG-359真修复: 去AI味 — 路由到marketing_polish.py polish_four_steps
            # 来源: 34号文档§4 "集成到portal_generate_content后处理链"
            # DEF-U49 P2: 消耗蒸馏style_fingerprint智能调整tone(示范下游消费)
            import subprocess as _subproc
            polish_script = str(Path(__file__).parent / "marketing_polish.py")
            content = data.get("content", "")
            title = data.get("title", "")
            tone = data.get("tone", "enthusiastic")
            product = data.get("product", "")
            # BUG-FIX(2026-08-05): 添加调试日志,确认管道执行时content是否正确传递
            print(f"[content_template] polish: content_len={len(content)}, title={title[:30]}, data_keys={list(data.keys())}", file=sys.stderr, flush=True)
            benefit = data.get("benefit", "")
            # DEF-U49 P2: 从蒸馏style_fingerprint提取tone_tendency智能调整tone
            # 来源: 60号文档v2.0 §2.4 + DEF-U49 P1-4(蒸馏数据下游消费示范)
            style_fp = data.get("style_fingerprint", {})
            if isinstance(style_fp, dict) and style_fp.get("tone_tendency"):
                distill_tone = str(style_fp.get("tone_tendency", "")).lower()
                # R8修复: "persuasive"应为"conversion"(与TONE_TEMPLATES定义一致)
                # R9统一化: tone_map从constants.py导入DISTILL_TONE_TO_MARKETING_MAP(R75.5消除碎片化)
                tone_map = DISTILL_TONE_TO_MARKETING_MAP
                if distill_tone in tone_map:
                    tone = tone_map[distill_tone]
                    logger.info(f"[content-template] DEF-U49 P2: 蒸馏tone_tendency={distill_tone} → tone={tone}")
            cmd_args = [
                sys.executable, polish_script,
                "--action", "polish",
                "--content", content,
                "--title", title,
                "--tone", tone,
            ]
            if product:
                cmd_args.extend(["--product", product])
            if benefit:
                cmd_args.extend(["--benefit", benefit])
            try:
                proc = _subproc.run(cmd_args, capture_output=True, text=True, timeout=120, encoding="utf-8")
                if proc.returncode == 0:
                    polish_result = json.loads(proc.stdout)
                    result = polish_result
                else:
                    result = {"success": False, "data": {}, "error": f"polish脚本失败: {proc.stderr[:500]}", "code": "CT-POLISH-ERR"}
            except Exception as e:
                logger.error(f"content template polish异常: {e}", exc_info=True)
                result = {"success": False, "data": {}, "error": f"polish执行异常: {e}", "code": "CT-POLISH-EXC"}
        else:
            result = {"success": False, "data": {}, "error": f"未知操作: {action}", "code": "CT-ERR-03"}

        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result.get("success") else 1)

    except ValueError as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "CT-ERR-VAL"}))
        sys.exit(1)
    except Exception as e:
        logger.error(f"content template异常: {e}", exc_info=True)
        logger.error(json.dumps({"success": False, "data": {}, "error": str(e), "code": "CT-ERR-UNKNOWN"}))
        sys.exit(2)

if __name__ == "__main__":
    main()
