"""
BiliYouTik2Brain — 输出格式选择器 (v4.0)

主流程跑完后，根据视频价值和用户偏好自动/手动选择输出格式。
"""

import os
import json
from typing import Dict, Optional
from dataclasses import dataclass


# ═══════════════════════════════════════════════════════════
#  输出格式枚举
# ═══════════════════════════════════════════════════════════

class OutputFormat:
    NOTE = "note"           # 纯文本笔记
    RICH = "rich"           # 图文并茂
    DATA = "data"           # 结构化 JSON
    OBSIDIAN = "obsidian"   # Obsidian 卡片


FORMAT_INFO = {
    OutputFormat.NOTE: {
        "name": "纯文本笔记",
        "extension": ".md",
        "description": "转录文本 + 章节 + 关键词 + 摘要",
        "auto_trigger": "duration < 5",
    },
    OutputFormat.RICH: {
        "name": "图文并茂",
        "extension": ".md",
        "description": "转录文本 + 关键帧截图 + OCR 数据 + 交叉验证",
        "auto_trigger": "duration > 15 or has_keyframes",
    },
    OutputFormat.DATA: {
        "name": "结构化数据",
        "extension": ".json",
        "description": "完整 JSON（视频元信息/转录/分析/评论/知识）",
        "auto_trigger": "user_request",
    },
    OutputFormat.OBSIDIAN: {
        "name": "Obsidian 卡片",
        "extension": ".md",
        "description": "Obsidian 兼容（frontmatter + 双向链接 + 标签）",
        "auto_trigger": "user_request",
    },
}


# ═══════════════════════════════════════════════════════════
#  自动选择逻辑
# ═══════════════════════════════════════════════════════════

@dataclass
class OutputContext:
    """输出上下文（用于自动决策）"""
    duration_min: float = 0
    has_keyframes: bool = False
    has_comments: bool = False
    has_ocr: bool = False
    domain: str = ""
    user_preference: str = ""  # 用户上次选择的格式


def auto_select_format(ctx: OutputContext) -> str:
    """自动选择输出格式

    规则:
    - 短视频（<5min）→ 纯文本笔记
    - 长视频（>15min）且有 OCR → 图文并茂
    - 有评论分析 → 图文并茂（包含评论）
    - 其余 → 纯文本笔记
    """
    # 用户有偏好 → 优先
    if ctx.user_preference in FORMAT_INFO:
        return ctx.user_preference

    # 有 OCR 关键帧 → 图文并茂
    if ctx.has_keyframes and ctx.has_ocr:
        return OutputFormat.RICH

    # 短视频 → 纯文本
    if ctx.duration_min < 5:
        return OutputFormat.NOTE

    # 长视频 → 图文并茂
    if ctx.duration_min > 15:
        return OutputFormat.RICH

    # 有评论 → 图文并茂
    if ctx.has_comments:
        return OutputFormat.RICH

    # 默认纯文本
    return OutputFormat.NOTE


def format_cost_dialog(formats: list, auto_format: str) -> str:
    """格式化输出选择提示（供用户确认）

    Returns:
        格式化字符串，展示可用格式和自动选择结果
    """
    lines = [
        "┌─────────────────────────────────┐",
        "│  输出格式选择                    │",
        "├─────────────────────────────────┤",
    ]

    for fmt in formats:
        info = FORMAT_INFO.get(fmt, {})
        name = info.get("name", fmt)
        auto_marker = " ← 自动选择" if fmt == auto_format else ""
        lines.append(f"│  {fmt}: {name}{auto_marker}")

    lines.extend([
        "└─────────────────────────────────┘",
        "",
        "回复格式名切换，回车确认自动选择",
    ])

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
#  模板渲染
# ═══════════════════════════════════════════════════════════

def render_template(format_name: str, data: Dict) -> str:
    """渲染输出模板

    Args:
        format_name: 输出格式（note/rich/data/obsidian）
        data: 输出数据字典

    Returns:
        渲染后的文本
    """
    template_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "output_templates")

    template_map = {
        OutputFormat.NOTE: "note_template.md",
        OutputFormat.RICH: "rich_template.md",
        OutputFormat.DATA: "data_template.json",
        OutputFormat.OBSIDIAN: "obsidian_template.md",
    }

    template_file = template_map.get(format_name)
    if not template_file:
        return ""

    template_path = os.path.join(template_dir, template_file)
    if not os.path.exists(template_path):
        return _render_fallback(format_name, data)

    with open(template_path) as f:
        template = f.read()

    return _render_simple(template, data, format_name)


def _process_if_blocks(text: str, data: Dict, prefix: str = "") -> str:
    """处理 {% if %} ... {% else %} ... {% endif %} 条件块（循环处理嵌套）"""
    import re
    # 使用非贪婪匹配，优先匹配最内层的 if/endif
    if_pattern = re.compile(r'\{%\s*if\s+([\w.]+)\s*%\}((?:(?!%\}).)*?)(?:\{%\s*else\s*%\}((?:(?!%\}).)*?))?\{%\s*endif\s*%\}', re.DOTALL)

    max_iterations = 20
    for _ in range(max_iterations):
        match = if_pattern.search(text)
        if not match:
            break

        var_ref = match.group(1)
        if_body = match.group(2)
        else_body = match.group(3) or ""
        full_match = match.group(0)

        var_name = var_ref.split('.')[-1] if '.' in var_ref else var_ref
        var_value = data.get(var_name)

        if var_value:
            text = text[:match.start()] + if_body + text[match.end():]
        else:
            text = text[:match.start()] + else_body + text[match.end():]

    return text


def _render_simple(template: str, data: Dict, format_name: str) -> str:
    """简单模板渲染（支持 {{ var }} 和 {% for %} 基础语法）

    不依赖 Jinja2，用纯 Python 实现基础模板功能。
    """
    import re
    result = template

    # 1. 处理 {% for item in list %} ... {% endfor %} 循环
    for_loop_pattern = re.compile(r'\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}', re.DOTALL)
    for match in for_loop_pattern.finditer(template):
        var_name = match.group(1)
        list_name = match.group(2)
        loop_body = match.group(3)
        full_match = match.group(0)

        if list_name in data and isinstance(data[list_name], list):
            rendered_items = []
            for item in data[list_name]:
                item_block = loop_body
                if isinstance(item, dict):
                    # 先处理 item 内部的 {% if %} 块
                    item_block = _process_if_blocks(item_block, item)
                    # 再替换变量
                    for k, v in item.items():
                        item_block = item_block.replace("{{ " + var_name + "." + k + " }}", str(v))
                else:
                    item_block = item_block.replace("{{ " + var_name + " }}", str(item))
                rendered_items.append(item_block)
            result = result.replace(full_match, "".join(rendered_items))
        else:
            result = result.replace(full_match, "")

    # 3. 处理 {% if var %} ... {% else %} ... {% endif %} 条件块
    if_pattern = re.compile(r'\{%\s*if\s+(\w+)\s*%\}(.*?)(?:\{%\s*else\s*%\}(.*?))?\{%\s*endif\s*%\}', re.DOTALL)
    for match in if_pattern.finditer(result):
        var_name = match.group(1)
        if_body = match.group(2)
        else_body = match.group(3) or ""
        full_match = match.group(0)

        var_value = data.get(var_name)
        if var_value:  # truthy check
            result = result.replace(full_match, if_body)
        else:
            result = result.replace(full_match, else_body)

    # 2. 简单变量替换 {{ var }}
    for key, value in data.items():
        placeholder = "{{ " + key + " }}"
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        result = result.replace(placeholder, str(value))

    # 2. JSON 变量 {{ var_json }}
    for key, value in data.items():
        if isinstance(value, (list, dict)):
            placeholder = "{{ " + key + "_json }}"
            result = result.replace(placeholder, json.dumps(value, ensure_ascii=False, indent=2))

    # 3. 转义
    if format_name == OutputFormat.DATA:
        result = result.replace("{{ transcript | escape }}", json.dumps(data.get("transcript", "")))

    # 4. 清理未替换的占位符
    result = re.sub(r'\{\{[^}]*\}\}', '', result)

    return result


def _render_fallback(format_name: str, data: Dict) -> str:
    """模板文件不存在时的兜底渲染"""
    if format_name == OutputFormat.DATA:
        return json.dumps(data, ensure_ascii=False, indent=2)

    lines = [f"# {data.get('title', '无标题')}", ""]
    if data.get("summary"):
        lines.extend(["## 📝 摘要", "", data["summary"], ""])
    if data.get("transcript"):
        lines.extend(["## 📖 转录文本", "", data["transcript"], ""])
    if data.get("keywords"):
        lines.extend(["## 🏷️ 关键词", "", ", ".join(data["keywords"]), ""])

    return "\n".join(lines)
