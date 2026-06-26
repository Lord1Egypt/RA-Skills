import argparse
import copy
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

try:
    from docx import Document  # type: ignore
except ImportError:
    Document = None

try:
    from pypdf import PdfReader  # type: ignore
except ImportError:
    PdfReader = None


load_dotenv()

SCHEMA_VERSION = "0.2.0"
DERIVED_SECTION_TEMPLATE = {
    "faq": [
        {
            "category": "",
            "question": "",
            "answer": "",
            "needs_verification": False,
        }
    ],
    "glossary": [
        {
            "term": "",
            "definition": "",
            "approved_usage": "",
            "avoid_usage": "",
        }
    ],
    "standard_messaging": {
        "elevator_pitch": "",
        "pitch_30_seconds": "",
        "sales_intro_1_minute": "",
        "hero_headline": "",
        "hero_subheadline": "",
        "wechat_about": "",
        "zhihu_intro": "",
        "xiaohongshu_bio": "",
        "customer_service_opening": "",
        "sales_dm_opening": "",
    },
    "geo_summary": {
        "entity_definition": "",
        "target_audience": "",
        "core_value": "",
        "capabilities": [],
        "limitations": [],
        "recommended_citations": [],
        "negative_instructions": [],
        "dense_summary": "",
    },
}
ANALYSIS_TEMPLATE = {
    "completeness_score": 0,
    "package_status": "needs_more_input",
    "missing_information": [],
    "conflicting_information": [],
    "assumptions_made": [],
    "follow_up_questions": {
        "must_have": [],
        "recommended": [],
        "later": [],
    },
}
UNRESOLVED_TEMPLATE = {
    "missing_information": [],
    "conflicting_information": [],
    "assumptions_made": [],
    "follow_up_questions": {
        "must_have": [],
        "recommended": [],
        "later": [],
    },
}
TEXT_FILE_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
    ".json",
    ".yaml",
    ".yml",
    ".csv",
    ".tsv",
    ".html",
    ".htm",
}


def load_text_file(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8") as handle:
        return handle.read()


def save_text_file(file_path: Path, content: str) -> None:
    with file_path.open("w", encoding="utf-8") as handle:
        handle.write(content)


def load_json_file(file_path: Path) -> Any:
    return json.loads(load_text_file(file_path))


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def workspace_dir() -> Path:
    return Path.cwd().resolve()


def resolve_path(path_value: str) -> Path:
    return Path(path_value).expanduser().resolve()


def is_within_root(target_path: Path, root_path: Path) -> bool:
    try:
        target_path.relative_to(root_path)
        return True
    except ValueError:
        return False


def is_allowed_path(target_path: Path, extra_roots: Optional[List[Path]] = None) -> bool:
    roots = [workspace_dir(), script_dir()]
    if extra_roots:
        roots.extend(extra_roots)
    for root in roots:
        if is_within_root(target_path, root):
            return True
    return False


def ensure_allowed_path(target_path: Path, purpose: str) -> None:
    if not is_allowed_path(target_path):
        print("❌ 安全拦截: %s 路径必须位于当前工作区或 Skill 目录内。" % purpose)
        sys.exit(1)


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def list_or_placeholder(items: Any) -> List[Any]:
    if isinstance(items, list):
        return items
    if items in (None, ""):
        return []
    return [items]


def string_or_empty(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def is_blank_value(value: Any) -> bool:
    if value is None:
        return True
    if value is False:
        return True
    if isinstance(value, str):
        return value.strip() in ("", "[待确认]", "待确认", "N/A", "n/a")
    if isinstance(value, list):
        return not value or all(is_blank_value(item) for item in value)
    if isinstance(value, dict):
        return not value or all(is_blank_value(item) for item in value.values())
    return False


def deep_merge(default_value: Any, current_value: Any) -> Any:
    if isinstance(default_value, dict):
        current_dict = current_value if isinstance(current_value, dict) else {}
        merged = {}
        for key, sub_default in default_value.items():
            merged[key] = deep_merge(sub_default, current_dict.get(key))
        for key, sub_value in current_dict.items():
            if key not in merged:
                merged[key] = sub_value
        return merged

    if isinstance(default_value, list):
        if isinstance(current_value, list):
            if default_value and isinstance(default_value[0], dict):
                template_item = default_value[0]
                return [
                    deep_merge(template_item, item if isinstance(item, dict) else {})
                    if isinstance(item, dict)
                    else item
                    for item in current_value
                ]
            return current_value
        return copy.deepcopy(default_value)

    if current_value is None:
        return copy.deepcopy(default_value)
    return current_value


def prune_placeholder_items(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: prune_placeholder_items(sub_value) for key, sub_value in value.items()}
    if isinstance(value, list):
        cleaned_items = [prune_placeholder_items(item) for item in value]
        return [item for item in cleaned_items if not is_blank_value(item)]
    return value


def normalize_package(raw_package: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    merged = deep_merge(template, raw_package)
    cleaned = prune_placeholder_items(merged)
    metadata = cleaned.setdefault("package_metadata", {})
    metadata["schema_version"] = SCHEMA_VERSION
    if not metadata.get("generated_at"):
        metadata["generated_at"] = now_iso()
    if not metadata.get("language"):
        metadata["language"] = "zh-CN"
    if not metadata.get("package_status"):
        metadata["package_status"] = "draft"
    if "completeness_score" not in metadata:
        metadata["completeness_score"] = 0
    if "source_count" not in metadata:
        metadata["source_count"] = 0
    if "source_notes" not in metadata:
        metadata["source_notes"] = []
    cleaned.setdefault("unresolved_items", copy.deepcopy(UNRESOLVED_TEMPLATE))
    return cleaned


def clean_model_json(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def require_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    if not api_key:
        print("❌ 错误: 找不到 OPENAI_API_KEY 环境变量，请在 .env 文件中设置。")
        sys.exit(1)
    return OpenAI(api_key=api_key, base_url=base_url)


def call_llm_json(
    client: OpenAI,
    model: str,
    system_message: str,
    user_payload: Any,
    temperature: float,
    stage_name: str,
) -> Dict[str, Any]:
    user_content = (
        user_payload
        if isinstance(user_payload, str)
        else json.dumps(user_payload, ensure_ascii=False, indent=2)
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_content},
            ],
            temperature=temperature,
        )
        content = response.choices[0].message.content or ""
        parsed = json.loads(clean_model_json(content))
        if not isinstance(parsed, dict):
            raise ValueError("模型返回的顶层结构不是 JSON object")
        return parsed
    except json.JSONDecodeError:
        print("❌ %s 阶段失败: 模型返回的内容不是合法 JSON。" % stage_name)
        print("返回内容片段: %s" % clean_model_json(content)[:500])
        sys.exit(1)
    except Exception as exc:
        print("❌ %s 阶段请求失败: %s" % (stage_name, exc))
        sys.exit(1)


def safe_json_string(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def dump_yaml(value: Any, indent: int = 0) -> str:
    prefix = "  " * indent

    if isinstance(value, dict):
        lines = []
        for key, sub_value in value.items():
            if isinstance(sub_value, dict):
                if sub_value:
                    lines.append("%s%s:" % (prefix, key))
                    lines.append(dump_yaml(sub_value, indent + 1))
                else:
                    lines.append("%s%s: {}" % (prefix, key))
            elif isinstance(sub_value, list):
                if sub_value:
                    lines.append("%s%s:" % (prefix, key))
                    lines.append(dump_yaml(sub_value, indent + 1))
                else:
                    lines.append("%s%s: []" % (prefix, key))
            else:
                lines.append("%s%s: %s" % (prefix, key, yaml_scalar(sub_value)))
        return "\n".join(lines)

    if isinstance(value, list):
        if not value:
            return "%s[]" % prefix
        lines = []
        for item in value:
            if isinstance(item, dict):
                if not item:
                    lines.append("%s- {}" % prefix)
                    continue
                first_key = True
                child_prefix = "  " * (indent + 1)
                for key, sub_value in item.items():
                    line_prefix = "%s- " % prefix if first_key else child_prefix
                    if isinstance(sub_value, dict):
                        if sub_value:
                            lines.append("%s%s:" % (line_prefix, key))
                            lines.append(dump_yaml(sub_value, indent + 2))
                        else:
                            lines.append("%s%s: {}" % (line_prefix, key))
                    elif isinstance(sub_value, list):
                        if sub_value:
                            lines.append("%s%s:" % (line_prefix, key))
                            lines.append(dump_yaml(sub_value, indent + 2))
                        else:
                            lines.append("%s%s: []" % (line_prefix, key))
                    else:
                        lines.append("%s%s: %s" % (line_prefix, key, yaml_scalar(sub_value)))
                    first_key = False
            elif isinstance(item, list):
                lines.append("%s-" % prefix)
                lines.append(dump_yaml(item, indent + 1))
            else:
                lines.append("%s- %s" % (prefix, yaml_scalar(item)))
        return "\n".join(lines)

    return "%s%s" % (prefix, yaml_scalar(value))


def yaml_scalar(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return safe_json_string(string_or_empty(value))


def format_value(value: Any) -> str:
    if is_blank_value(value):
        return "待确认"
    if isinstance(value, list):
        formatted_items = [format_value(item) for item in value if not is_blank_value(item)]
        return "；".join(formatted_items) if formatted_items else "待确认"
    if isinstance(value, dict):
        parts = []
        for key, sub_value in value.items():
            if not is_blank_value(sub_value):
                parts.append("%s: %s" % (key, format_value(sub_value)))
        return "；".join(parts) if parts else "待确认"
    return string_or_empty(value)


def markdown_bullets(items: Any) -> str:
    values = list_or_placeholder(items)
    cleaned = [item for item in values if not is_blank_value(item)]
    if not cleaned:
        return "- 待确认"
    return "\n".join("- %s" % format_value(item) for item in cleaned)


def markdown_numbered(items: Any) -> str:
    values = list_or_placeholder(items)
    cleaned = [item for item in values if not is_blank_value(item)]
    if not cleaned:
        return "1. 待确认"
    return "\n".join("%s. %s" % (index + 1, format_value(item)) for index, item in enumerate(cleaned))


def link_list_markdown(items: List[Dict[str, Any]]) -> str:
    if not items:
        return "- 待确认"
    lines = []
    for item in items:
        label = string_or_empty(item.get("label")) or "未命名链接"
        url = string_or_empty(item.get("url")) or "待确认"
        item_type = string_or_empty(item.get("type"))
        notes = string_or_empty(item.get("notes"))
        parts = ["[%s](%s)" % (label, url) if url != "待确认" else label]
        if item_type:
            parts.append("类型: %s" % item_type)
        if notes:
            parts.append("备注: %s" % notes)
        lines.append("- %s" % " | ".join(parts))
    return "\n".join(lines)


def render_use_cases(use_cases: List[Dict[str, Any]]) -> str:
    if not use_cases:
        return "### 场景 1: 待确认\n- **适用对象**: 待确认\n- **触发条件**: 待确认\n- **输入资料**: 待确认\n- **处理流程**: 待确认\n- **输出结果**: 待确认\n- **业务价值**: 待确认\n- **注意事项**: 待确认"

    chunks = []
    for index, item in enumerate(use_cases):
        chunks.append(
            "\n".join(
                [
                    "### 场景 %s: %s" % (index + 1, format_value(item.get("name"))),
                    "- **适用对象**: %s" % format_value(item.get("audience")),
                    "- **触发条件**: %s" % format_value(item.get("trigger")),
                    "- **输入资料**: %s" % format_value(item.get("input")),
                    "- **处理流程**: %s" % format_value(item.get("process")),
                    "- **输出结果**: %s" % format_value(item.get("output")),
                    "- **业务价值**: %s" % format_value(item.get("value")),
                    "- **注意事项**: %s" % format_value(item.get("notes")),
                ]
            )
        )
    return "\n\n".join(chunks)


def render_customer_cases(cases: List[Dict[str, Any]]) -> str:
    if not cases:
        return "### 案例 1: 待确认\n- **客户类型**: 待确认\n- **所属行业**: 待确认\n- **客户问题**: 待确认\n- **解决方案**: 待确认\n- **结果产出**: 待确认\n- **证据素材**: 待确认\n- **状态**: 待确认\n- **备注**: 待确认"

    chunks = []
    for index, item in enumerate(cases):
        chunks.append(
            "\n".join(
                [
                    "### 案例 %s: %s" % (index + 1, format_value(item.get("case_name"))),
                    "- **客户类型**: %s" % format_value(item.get("client_type")),
                    "- **所属行业**: %s" % format_value(item.get("industry")),
                    "- **客户问题**: %s" % format_value(item.get("problem")),
                    "- **解决方案**: %s" % format_value(item.get("solution")),
                    "- **结果产出**: %s" % format_value(item.get("outcome")),
                    "- **证据素材**: %s" % format_value(item.get("proof")),
                    "- **客户引述**: %s" % format_value(item.get("quote")),
                    "- **状态**: %s" % format_value(item.get("status")),
                    "- **备注**: %s" % format_value(item.get("notes")),
                ]
            )
        )
    return "\n\n".join(chunks)


def render_competitor_entries(items: List[Dict[str, Any]], title: str) -> str:
    if not items:
        return "### %s\n- 待确认" % title

    chunks = ["### %s" % title]
    for item in items:
        chunks.append("- **名称**: %s" % format_value(item.get("name")))
        chunks.append("- **类型**: %s" % format_value(item.get("type")))
        chunks.append("- **定位**: %s" % format_value(item.get("positioning")))
        chunks.append("- **优势**: %s" % format_value(item.get("strengths")))
        chunks.append("- **弱点**: %s" % format_value(item.get("weaknesses")))
        chunks.append("- **备注**: %s" % format_value(item.get("notes")))
    return "\n".join(chunks)


def render_source_materials(items: List[Dict[str, Any]]) -> str:
    if not items:
        return "- 待确认"
    chunks = []
    for item in items:
        chunks.append(
            "- **%s** (%s): %s"
            % (
                format_value(item.get("name")),
                format_value(item.get("type")),
                format_value(item.get("summary")),
            )
        )
        key_points = list_or_placeholder(item.get("key_points"))
        if key_points:
            for key_point in key_points:
                if not is_blank_value(key_point):
                    chunks.append("  - %s" % format_value(key_point))
    return "\n".join(chunks)


def render_core_markdown(package: Dict[str, Any]) -> str:
    metadata = package.get("package_metadata", {})
    brand_identity = package.get("brand_identity", {})
    company_profile = package.get("company_profile", {})
    product_services = package.get("product_services", {})
    target_users = package.get("target_users", {})
    pain_points = package.get("customer_pain_points", {})
    capabilities = package.get("core_capabilities", {})
    workflow = package.get("product_workflow", {})
    value_proposition = package.get("value_proposition", {})
    comparison = package.get("competitive_comparison", {})
    brand_voice = package.get("brand_voice", {})
    contacts = package.get("contact_information", {})
    compliance = package.get("compliance_boundary", {})
    unresolved = package.get("unresolved_items", {})
    website_links = list_or_placeholder(company_profile.get("website_links")) or list_or_placeholder(contacts.get("website_links"))
    product_items = product_services.get("products") or capabilities.get("product")
    service_items = product_services.get("services") or capabilities.get("service")
    delivery_items = product_services.get("delivery_models") or capabilities.get("delivery")
    banned_words = brand_voice.get("banned_words") or compliance.get("avoid_expressions")
    banned_claims = brand_voice.get("banned_claims") or compliance.get("high_risk_messaging")
    safe_alternatives = brand_voice.get("safe_alternatives") or compliance.get("safe_alternatives")

    sections = [
        "# Brand Knowledge Base / 品牌资料包",
        "> 版本: %s | 生成时间: %s | 状态: %s | 完整度: %s%%"
        % (
            format_value(metadata.get("schema_version")),
            format_value(metadata.get("generated_at")),
            format_value(metadata.get("package_status")),
            format_value(metadata.get("completeness_score")),
        ),
        "",
        "## 1. Brand Identity / 品牌身份",
        "- **品牌名称**: %s" % format_value(brand_identity.get("brand_name")),
        "- **公司名称**: %s" % format_value(brand_identity.get("company_name")),
        "- **一句话定义**: %s" % format_value(brand_identity.get("one_line_definition")),
        "- **100字介绍**: %s" % format_value(brand_identity.get("intro_100_words")),
        "- **300字介绍**: %s" % format_value(brand_identity.get("intro_300_words")),
        "- **英文一句话介绍**: %s" % format_value(brand_identity.get("english_one_liner")),
        "- **产品类别**: %s" % format_value(brand_identity.get("product_category")),
        "- **行业领域**: %s" % format_value(brand_identity.get("industry")),
        "- **业务模式**: %s" % format_value(brand_identity.get("business_model")),
        "- **品牌关键词**: %s" % format_value(brand_identity.get("keywords")),
        "",
        "## 2. Company Profile / 公司资料",
        "- **公司简介**: %s" % format_value(company_profile.get("company_intro")),
        "- **品牌使命**: %s" % format_value(company_profile.get("mission")),
        "- **品牌愿景**: %s" % format_value(company_profile.get("vision")),
        "- **发展阶段**: %s" % format_value(company_profile.get("stage")),
        "- **所在地区**: %s" % format_value(company_profile.get("locations")),
        "- **官网主站**: %s" % format_value(company_profile.get("official_website") or contacts.get("official_website")),
        "- **官网/重要链接**:",
        link_list_markdown(website_links),
        "",
        "## 3. Product & Services / 产品与服务",
        "- **产品列表**:",
        markdown_bullets(product_items),
        "- **服务列表**:",
        markdown_bullets(service_items),
        "- **交付形式**:",
        markdown_bullets(delivery_items),
        "- **收费模式**:",
        markdown_bullets(product_services.get("pricing_models")),
        "- **上手流程**:",
        markdown_bullets(product_services.get("onboarding_process")),
        "",
        "## 4. Target Users / 目标用户",
        "- **核心客户群体**: %s" % format_value(target_users.get("core_audience")),
        "- **次级客户群体**: %s" % format_value(target_users.get("secondary_audience")),
        "- **决策人**: %s" % format_value(target_users.get("decision_makers")),
        "- **使用者**: %s" % format_value(target_users.get("end_users")),
        "- **影响者**: %s" % format_value(target_users.get("influencers")),
        "- **不适合的用户**: %s" % format_value(target_users.get("anti_audience")),
        "",
        "## 5. Customer Pain Points / 客户痛点",
        "- **显性痛点**: %s" % format_value(pain_points.get("explicit_pain")),
        "- **隐性痛点**: %s" % format_value(pain_points.get("implicit_pain")),
        "- **业务层痛点**: %s" % format_value(pain_points.get("business_level")),
        "- **成本层痛点**: %s" % format_value(pain_points.get("cost_level")),
        "- **效率层痛点**: %s" % format_value(pain_points.get("efficiency_level")),
        "- **信任层痛点**: %s" % format_value(pain_points.get("trust_level")),
        "- **合规层痛点**: %s" % format_value(pain_points.get("compliance_level")),
        "",
        "## 6. Core Capabilities / 核心能力",
        "- **产品能力**:",
        markdown_bullets(capabilities.get("product")),
        "- **服务能力**:",
        markdown_bullets(capabilities.get("service")),
        "- **技术能力**:",
        markdown_bullets(capabilities.get("technology")),
        "- **交付能力**:",
        markdown_bullets(capabilities.get("delivery")),
        "- **自动化能力**:",
        markdown_bullets(capabilities.get("automation")),
        "- **AI 能力**:",
        markdown_bullets(capabilities.get("ai")),
        "- **人工边界**:",
        markdown_bullets(capabilities.get("human_boundaries")),
        "",
        "## 7. Value Proposition / 价值主张",
        "- **核心卖点**:",
        markdown_bullets(value_proposition.get("core_selling_points")),
        "- **证据点**:",
        markdown_bullets(value_proposition.get("proof_points")),
        "- **差异化优势**:",
        markdown_bullets(value_proposition.get("differentiators")),
        "- **直接价值**: %s" % format_value(value_proposition.get("direct_value")),
        "- **长期价值**: %s" % format_value(value_proposition.get("long_term_value")),
        "- **vs 传统方案**: %s" % format_value(value_proposition.get("vs_traditional")),
        "- **vs 普通 ChatGPT**: %s" % format_value(value_proposition.get("vs_chatgpt")),
        "- **vs 外包团队**: %s" % format_value(value_proposition.get("vs_agency")),
        "- **vs 行业 SaaS**: %s" % format_value(value_proposition.get("vs_saas")),
        "",
        "## 8. Use Cases / 使用场景",
        render_use_cases(list_or_placeholder(package.get("use_cases"))),
        "",
        "## 9. Customer Cases / 客户案例",
        render_customer_cases(list_or_placeholder(package.get("customer_cases"))),
        "",
        "## 10. Product Workflow / 产品工作流",
        "1. **用户输入**: %s" % format_value(workflow.get("user_input")),
        "2. **系统处理**: %s" % format_value(workflow.get("system_processing")),
        "3. **输出结果**: %s" % format_value(workflow.get("output_result")),
        "4. **审核机制**: %s" % format_value(workflow.get("review_mechanism")),
        "5. **部署方式**: %s" % format_value(workflow.get("deployment")),
        "6. **资产沉淀**: %s" % format_value(workflow.get("asset_accumulation")),
        "",
        "## 11. Competitive Landscape / 竞争格局",
        render_competitor_entries(list_or_placeholder(comparison.get("direct_competitors")), "直接竞品"),
        "",
        render_competitor_entries(list_or_placeholder(comparison.get("indirect_competitors")), "间接竞品"),
        "",
        "### 对比框架",
        "- **传统方式**: %s" % format_value(comparison.get("traditional")),
        "- **普通工具**: %s" % format_value(comparison.get("basic_tools")),
        "- **行业 SaaS**: %s" % format_value(comparison.get("industry_saas")),
        "- **本品牌**: %s" % format_value(comparison.get("our_brand")),
        "",
        "## 12. Brand Voice / 品牌语气与表达规范",
        "- **语气关键词**: %s" % format_value(brand_voice.get("tone_keywords")),
        "- **语气说明**: %s" % format_value(brand_voice.get("tone_description")),
        "- **必须出现的表达**:",
        markdown_bullets(brand_voice.get("must_say")),
        "- **推荐表达**:",
        markdown_bullets(brand_voice.get("preferred_phrases")),
        "- **禁用词**:",
        markdown_bullets(banned_words),
        "- **禁用承诺**:",
        markdown_bullets(banned_claims),
        "- **安全替代表达**:",
        markdown_bullets(safe_alternatives),
        "- **写作建议**:",
        markdown_bullets(brand_voice.get("style_do")),
        "- **写作禁忌**:",
        markdown_bullets(brand_voice.get("style_dont")),
        "",
        "## 13. Contact Information / 联系方式",
        "- **官网**: %s" % format_value(contacts.get("official_website")),
        "- **销售邮箱**: %s" % format_value(contacts.get("sales_email")),
        "- **支持邮箱**: %s" % format_value(contacts.get("support_email")),
        "- **联系电话**: %s" % format_value(contacts.get("phone")),
        "- **微信/社媒**: %s" % format_value(contacts.get("wechat")),
        "- **办公地址**: %s" % format_value(contacts.get("address")),
        "- **工作时间**: %s" % format_value(contacts.get("business_hours")),
        "- **预约链接**: %s" % format_value(contacts.get("booking_url")),
        "- **其他渠道**:",
        markdown_bullets(contacts.get("additional_channels")),
        "",
        "## 14. Compliance Boundary / 合规边界",
        "- **能做什么**:",
        markdown_bullets(compliance.get("what_we_can_do")),
        "- **不能做什么**:",
        markdown_bullets(compliance.get("what_we_cannot_do")),
        "- **需人工审核**:",
        markdown_bullets(compliance.get("requires_human_review")),
        "- **不可承诺**:",
        markdown_bullets(compliance.get("no_promises_on")),
        "- **必须避免的表达**:",
        markdown_bullets(compliance.get("avoid_expressions")),
        "- **高风险话术**:",
        markdown_bullets(compliance.get("high_risk_messaging")),
        "- **安全表达推荐**:",
        markdown_bullets(compliance.get("safe_alternatives")),
        "- **免责声明**: %s" % format_value(compliance.get("disclaimer")),
        "",
        "## 15. Source Materials / 来源资料",
        render_source_materials(list_or_placeholder(package.get("source_materials"))),
        "",
        "## 16. Unresolved Items / 待补信息",
        "- **缺失信息**:",
        markdown_bullets(unresolved.get("missing_information")),
        "- **冲突信息**:",
        markdown_bullets(unresolved.get("conflicting_information")),
        "- **当前假设**:",
        markdown_bullets(unresolved.get("assumptions_made")),
        "- **必须追问**:",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("must_have")),
        "- **建议追问**:",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("recommended")),
        "- **后续优化**:",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("later")),
    ]

    return "\n".join(sections).strip() + "\n"


def render_faq_markdown(package: Dict[str, Any]) -> str:
    faq_items = list_or_placeholder(package.get("faq"))
    if not faq_items:
        faq_items = []

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in faq_items:
        if not isinstance(item, dict) or is_blank_value(item):
            continue
        category = string_or_empty(item.get("category")) or "未分类"
        grouped.setdefault(category, []).append(item)

    lines = [
        "# FAQ - 高频问答集",
        "> 适用于官网、销售、客服、Agent 和 RAG 系统复用。",
        "",
    ]

    if not grouped:
        lines.append("## 1. 待补充")
        lines.append("**Q1: 当前 FAQ 尚未生成，下一步需要补哪些资料？**")
        lines.append("A: 请补充产品服务、客户场景、收费方式、案例证据、合规边界与联系方式。")
        return "\n".join(lines).strip() + "\n"

    for index, category in enumerate(sorted(grouped.keys())):
        lines.append("## %s. %s" % (index + 1, category))
        for item in grouped[category]:
            answer = string_or_empty(item.get("answer")) or "待确认"
            if item.get("needs_verification") and not answer.startswith("[需用户核实]"):
                answer = "[需用户核实] " + answer
            lines.append("**Q: %s**" % format_value(item.get("question")))
            lines.append("A: %s" % answer)
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_glossary_markdown(package: Dict[str, Any]) -> str:
    glossary_items = [item for item in list_or_placeholder(package.get("glossary")) if isinstance(item, dict) and not is_blank_value(item)]
    lines = [
        "# Glossary - 标准术语库",
        "> 统一术语定义、推荐说法与禁用表达。",
        "",
        "| 术语 | 定义 | 推荐用法 | 避免用法 |",
        "| :--- | :--- | :--- | :--- |",
    ]
    if not glossary_items:
        lines.append("| 待确认 | 待确认 | 待确认 | 待确认 |")
        return "\n".join(lines).strip() + "\n"

    for item in glossary_items:
        lines.append(
            "| %s | %s | %s | %s |"
            % (
                format_value(item.get("term")),
                format_value(item.get("definition")),
                format_value(item.get("approved_usage")),
                format_value(item.get("avoid_usage")),
            )
        )
    return "\n".join(lines).strip() + "\n"


def render_standard_messaging_markdown(package: Dict[str, Any]) -> str:
    messaging = package.get("standard_messaging", {})
    sections = [
        ("一句话介绍", "elevator_pitch"),
        ("30 秒口播", "pitch_30_seconds"),
        ("1 分钟销售介绍", "sales_intro_1_minute"),
        ("官网 Hero 标题", "hero_headline"),
        ("官网 Hero 补充说明", "hero_subheadline"),
        ("微信公众号介绍", "wechat_about"),
        ("知乎回答开头", "zhihu_intro"),
        ("小红书简介", "xiaohongshu_bio"),
        ("客服开场白", "customer_service_opening"),
        ("销售私聊开场白", "sales_dm_opening"),
    ]

    lines = [
        "# Standard Messaging - 标准话术库",
        "> 统一品牌多渠道输出口径。",
        "",
    ]
    for index, (title, key) in enumerate(sections):
        lines.append("## %s. %s" % (index + 1, title))
        lines.append(format_value(messaging.get(key)))
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def render_llms_txt(package: Dict[str, Any]) -> str:
    geo_summary = package.get("geo_summary", {})
    brand_identity = package.get("brand_identity", {})
    target_users = package.get("target_users", {})
    capabilities = package.get("core_capabilities", {})
    value_proposition = package.get("value_proposition", {})
    compliance = package.get("compliance_boundary", {})
    capability_fallback = []
    capability_fallback.extend(list_or_placeholder(capabilities.get("product")))
    capability_fallback.extend(list_or_placeholder(capabilities.get("service")))
    capability_fallback.extend(list_or_placeholder(capabilities.get("technology")))
    return (
        "Name: %s\n"
        "Type: %s / %s\n"
        "Definition: %s\n"
        "Target Audience: %s\n"
        "Core Value: %s\n"
        "Capabilities: %s\n"
        "Limitations: %s\n"
        "Recommended Citations: %s\n"
        "Negative Instructions: %s\n"
        "Dense Summary: %s\n"
        "Disclaimer: %s\n"
        % (
            format_value(brand_identity.get("brand_name")),
            format_value(brand_identity.get("product_category")),
            format_value(brand_identity.get("industry")),
            format_value(geo_summary.get("entity_definition") or brand_identity.get("one_line_definition")),
            format_value(geo_summary.get("target_audience") or target_users.get("core_audience")),
            format_value(geo_summary.get("core_value") or value_proposition.get("direct_value")),
            format_value(geo_summary.get("capabilities") or capability_fallback),
            format_value(geo_summary.get("limitations") or compliance.get("what_we_cannot_do")),
            format_value(geo_summary.get("recommended_citations") or brand_identity.get("intro_100_words")),
            format_value(geo_summary.get("negative_instructions") or compliance.get("high_risk_messaging") or compliance.get("no_promises_on")),
            format_value(geo_summary.get("dense_summary")),
            format_value(compliance.get("disclaimer")),
        )
    )


def render_analysis_report_markdown(package: Dict[str, Any]) -> str:
    metadata = package.get("package_metadata", {})
    unresolved = package.get("unresolved_items", {})
    lines = [
        "# Analysis Report / 资料分析报告",
        "- **完整度评估**: %s%%" % format_value(metadata.get("completeness_score")),
        "- **当前状态**: %s" % format_value(metadata.get("package_status")),
        "",
        "## 缺失信息",
        markdown_bullets(unresolved.get("missing_information")),
        "",
        "## 冲突信息",
        markdown_bullets(unresolved.get("conflicting_information")),
        "",
        "## 当前假设",
        markdown_bullets(unresolved.get("assumptions_made")),
        "",
        "## 追问清单",
        "### 必须补充",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("must_have")),
        "",
        "### 建议补充",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("recommended")),
        "",
        "### 后续优化",
        markdown_numbered(unresolved.get("follow_up_questions", {}).get("later")),
    ]
    return "\n".join(lines).strip() + "\n"


def build_source_bundle(raw_inputs: List[Path], intake_file: Optional[Path]) -> Dict[str, Any]:
    sections = []
    source_notes = []

    if intake_file:
        sections.append(read_source_block(intake_file, "Structured Intake"))
        source_notes.append("intake:%s" % intake_file.name)

    for index, input_path in enumerate(raw_inputs):
        sections.append(read_source_block(input_path, "Raw Material %s" % (index + 1)))
        source_notes.append("raw:%s" % input_path.name)

    return {
        "compiled_text": "\n\n---\n\n".join(sections).strip(),
        "source_notes": source_notes,
    }


def read_source_block(file_path: Path, label: str) -> str:
    ext = file_path.suffix.lower()

    if ext in TEXT_FILE_EXTENSIONS:
        raw_text = load_text_file(file_path)
        if ext == ".json":
            try:
                raw_text = json.dumps(json.loads(raw_text), ensure_ascii=False, indent=2)
            except Exception:
                pass
        elif ext in (".yaml", ".yml") and yaml is not None:
            try:
                raw_text = json.dumps(yaml.safe_load(raw_text), ensure_ascii=False, indent=2)
            except Exception:
                pass
    elif ext == ".docx":
        if Document is None:
            print("❌ 当前环境未安装 python-docx，无法读取 %s。" % file_path.name)
            print("请先安装 requirements.txt 或改为导出为 .md/.txt 后再执行。")
            sys.exit(1)
        document = Document(str(file_path))
        raw_text = "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
    elif ext == ".pdf":
        if PdfReader is None:
            print("❌ 当前环境未安装 pypdf，无法读取 %s。" % file_path.name)
            print("请先安装 requirements.txt 或改为导出为 .md/.txt 后再执行。")
            sys.exit(1)
        reader = PdfReader(str(file_path))
        page_texts = []
        for page in reader.pages:
            page_texts.append(page.extract_text() or "")
        raw_text = "\n".join(page_texts).strip()
    else:
        print("❌ 暂不支持的输入格式: %s" % file_path.suffix)
        print("目前支持: .txt .md .json .yaml .yml .csv .tsv .html .docx .pdf")
        sys.exit(1)

    return "\n".join(
        [
            "# %s" % label,
            "- 文件名: %s" % file_path.name,
            "- 类型: %s" % (ext or "unknown"),
            "",
            raw_text.strip(),
        ]
    ).strip()


def export_intake_templates(output_dir: Path) -> None:
    templates_dir = script_dir() / "templates"
    output_dir.mkdir(parents=True, exist_ok=True)

    for template_name in ("intake_form.md", "intake_form.yaml", "intake_form.json"):
        source_path = templates_dir / template_name
        target_path = output_dir / template_name
        save_text_file(target_path, load_text_file(source_path))

    print("✅ 已生成 intake 模板:")
    print("- %s" % (output_dir / "intake_form.md"))
    print("- %s" % (output_dir / "intake_form.yaml"))
    print("- %s" % (output_dir / "intake_form.json"))


def render_all_artifacts(package: Dict[str, Any], output_dir: Path, source_bundle: Optional[str] = None) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "brand_knowledge_base.json"
    yaml_path = output_dir / "brand_knowledge_base.yaml"
    md_path = output_dir / "brand_knowledge_base.md"
    llms_path = output_dir / "llms.txt"
    faq_path = output_dir / "faq.md"
    glossary_path = output_dir / "glossary.md"
    messaging_path = output_dir / "standard_messaging.md"
    analysis_path = output_dir / "analysis_report.md"

    save_text_file(json_path, json.dumps(package, ensure_ascii=False, indent=2))
    save_text_file(yaml_path, dump_yaml(package) + "\n")
    save_text_file(md_path, render_core_markdown(package))
    save_text_file(llms_path, render_llms_txt(package))
    save_text_file(faq_path, render_faq_markdown(package))
    save_text_file(glossary_path, render_glossary_markdown(package))
    save_text_file(messaging_path, render_standard_messaging_markdown(package))
    save_text_file(analysis_path, render_analysis_report_markdown(package))

    if source_bundle:
        save_text_file(output_dir / "source_bundle.md", source_bundle.strip() + "\n")


def load_prompt(prompt_name: str) -> str:
    return load_text_file(script_dir() / "prompts" / prompt_name)


def load_package_template() -> Dict[str, Any]:
    template_path = script_dir() / "templates" / "brand_knowledge_base.json"
    return load_json_file(template_path)


def prepare_input_paths(single_inputs: List[str], grouped_inputs: List[str]) -> List[Path]:
    all_values = []
    all_values.extend(single_inputs or [])
    all_values.extend(grouped_inputs or [])

    resolved_paths = []
    for path_value in all_values:
        path = resolve_path(path_value)
        ensure_allowed_path(path, "输入")
        if not path.exists():
            print("❌ 错误: 输入文件 %s 不存在。" % path)
            sys.exit(1)
        resolved_paths.append(path)
    return resolved_paths


def merge_analysis(package: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
    normalized = deep_merge(ANALYSIS_TEMPLATE, analysis)
    normalized = prune_placeholder_items(normalized)

    metadata = package.setdefault("package_metadata", {})
    metadata["completeness_score"] = normalized.get("completeness_score", 0)
    metadata["package_status"] = normalized.get("package_status", "draft")

    package["unresolved_items"] = {
        "missing_information": list_or_placeholder(normalized.get("missing_information")),
        "conflicting_information": list_or_placeholder(normalized.get("conflicting_information")),
        "assumptions_made": list_or_placeholder(normalized.get("assumptions_made")),
        "follow_up_questions": {
            "must_have": list_or_placeholder(normalized.get("follow_up_questions", {}).get("must_have")),
            "recommended": list_or_placeholder(normalized.get("follow_up_questions", {}).get("recommended")),
            "later": list_or_placeholder(normalized.get("follow_up_questions", {}).get("later")),
        },
    }
    return package


def merge_assets(package: Dict[str, Any], assets: Dict[str, Any]) -> Dict[str, Any]:
    normalized_assets = deep_merge(DERIVED_SECTION_TEMPLATE, assets)
    normalized_assets = prune_placeholder_items(normalized_assets)
    package["faq"] = list_or_placeholder(normalized_assets.get("faq"))
    package["glossary"] = list_or_placeholder(normalized_assets.get("glossary"))
    package["standard_messaging"] = normalized_assets.get("standard_messaging", {})
    package["geo_summary"] = normalized_assets.get("geo_summary", {})
    return package


def build_extraction_prompt(package_template: Dict[str, Any]) -> str:
    return (
        "%s\n\n"
        "请严格按照以下 JSON 模板结构返回结果。"
        "顶层必须是 JSON object，不能输出解释文本。"
        "未知内容请保留空字符串、空数组或空对象，不要编造。\n\n%s"
        % (
            load_prompt("extraction.md"),
            json.dumps(package_template, ensure_ascii=False, indent=2),
        )
    )


def build_analysis_prompt() -> str:
    return (
        "%s\n\n"
        "请严格返回 JSON object，结构必须如下：\n%s"
        % (
            load_prompt("normalization.md"),
            json.dumps(ANALYSIS_TEMPLATE, ensure_ascii=False, indent=2),
        )
    )


def build_asset_prompt() -> str:
    return (
        "%s\n\n"
        "请严格返回 JSON object，结构必须如下：\n%s"
        % (
            load_prompt("asset_generation.md"),
            json.dumps(DERIVED_SECTION_TEMPLATE, ensure_ascii=False, indent=2),
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Brand Knowledge Base Builder - v0.2")
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="原始资料文件路径，可重复传入多次。",
    )
    parser.add_argument(
        "--inputs",
        nargs="*",
        default=[],
        help="原始资料文件路径列表，适合一次传入多个文件。",
    )
    parser.add_argument(
        "--intake_file",
        type=str,
        help="结构化 intake 文件路径，支持 .md/.json/.yaml。",
    )
    parser.add_argument(
        "--render_from_json",
        type=str,
        help="已存在的 brand_knowledge_base.json 路径。传入后跳过模型抽取，只重新渲染全部输出。",
    )
    parser.add_argument(
        "--generate_intake_template",
        action="store_true",
        help="生成可填写的 intake 模板并退出。",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./output",
        help="生成结果的输出目录，默认为 ./output",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="底层调用的大语言模型，例如 gpt-4o / deepseek-chat。",
    )
    args = parser.parse_args()

    output_dir = resolve_path(args.output_dir)
    ensure_allowed_path(output_dir, "输出")

    if args.generate_intake_template:
        export_intake_templates(output_dir)
        return

    package_template = load_package_template()

    if args.render_from_json:
        json_path = resolve_path(args.render_from_json)
        ensure_allowed_path(json_path, "渲染输入")
        if not json_path.exists():
            print("❌ 错误: JSON 文件 %s 不存在。" % json_path)
            sys.exit(1)
        package = normalize_package(load_json_file(json_path), package_template)
        render_all_artifacts(package, output_dir)
        print("✅ 已根据现有 JSON 重新渲染完整资料包: %s" % output_dir)
        return

    raw_input_paths = prepare_input_paths(args.input, args.inputs)
    intake_path = resolve_path(args.intake_file) if args.intake_file else None
    if intake_path:
        ensure_allowed_path(intake_path, "intake")
        if not intake_path.exists():
            print("❌ 错误: intake 文件 %s 不存在。" % intake_path)
            sys.exit(1)

    if not raw_input_paths and not intake_path:
        print("❌ 错误: 请至少提供一份原始资料 (`--input/--inputs`) 或一份 intake 表单 (`--intake_file`)。")
        sys.exit(1)

    client = require_client()

    source_bundle = build_source_bundle(raw_input_paths, intake_path)
    compiled_text = source_bundle["compiled_text"]
    source_notes = source_bundle["source_notes"]

    print("🚀 开始构建品牌资料包...")
    print("   - 原始资料数: %s" % len(raw_input_paths))
    print("   - 是否包含 intake 表单: %s" % ("是" if intake_path else "否"))

    print("🧠 阶段 1/3: 抽取核心品牌资料...")
    extracted = call_llm_json(
        client=client,
        model=args.model,
        system_message=build_extraction_prompt(package_template),
        user_payload=compiled_text,
        temperature=0.2,
        stage_name="核心抽取",
    )
    package = normalize_package(extracted, package_template)
    package["package_metadata"]["source_count"] = len(source_notes)
    package["package_metadata"]["source_notes"] = source_notes

    print("🧭 阶段 2/3: 评估资料完整度并生成追问清单...")
    analysis_payload = {
        "compiled_sources": compiled_text,
        "extracted_package": package,
    }
    analysis = call_llm_json(
        client=client,
        model=args.model,
        system_message=build_analysis_prompt(),
        user_payload=analysis_payload,
        temperature=0.1,
        stage_name="资料分析",
    )
    package = merge_analysis(package, analysis)

    print("🪄 阶段 3/3: 生成 FAQ、术语库、话术库与 llms 摘要素材...")
    assets = call_llm_json(
        client=client,
        model=args.model,
        system_message=build_asset_prompt(),
        user_payload=package,
        temperature=0.3,
        stage_name="衍生资产生成",
    )
    package = merge_assets(package, assets)

    render_all_artifacts(package, output_dir, source_bundle=compiled_text)
    print("🎉 品牌资料包已生成完成: %s" % output_dir)


if __name__ == "__main__":
    main()
