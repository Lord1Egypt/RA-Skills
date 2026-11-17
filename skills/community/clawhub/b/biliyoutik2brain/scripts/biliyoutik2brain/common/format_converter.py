"""
format_converter — 纯规则格式转换

格式契约（v2.0 Phase 3）：
  输入: MD 文件路径或 MD 原始文本
  输出: HTML（用户阅读）/ JSON（程序消费）
  零外部依赖，纯规则转换，不调 LLM

消费者：
  HTML → 用户（人眼阅读）/ IMA 上传
  JSON → 下游程序（技能触发 / 知识分发）
"""

import re
import json
from typing import Dict, List, Optional


def md_to_html(md_text: str, title: str = "转录文档") -> str:
    """MD → HTML 纯规则转换（v1.0.0）
    
    Args:
        md_text: Markdown 原始文本
        title: HTML 页面标题（默认"转录文档"）
    
    Returns:
        完整的 HTML 字符串（含内联样式）
    """
    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    in_table = False
    
    for line in lines:
        # 空行
        if not line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_table:
                html_lines.append("</table>")
                in_table = False
            continue
        
        # 标题
        h_m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_m:
            if in_list: html_lines.append("</ul>"); in_list = False
            if in_table: html_lines.append("</table>"); in_table = False
            level = min(len(h_m.group(1)), 6)
            txt = h_m.group(2)
            html_lines.append(f"<h{level}>{txt}</h{level}>")
            continue
        
        # 分隔线
        if re.match(r'^---\s*$', line):
            html_lines.append("<hr>")
            continue
        
        # 表格
        if re.match(r'^\|[\s\-:|]+\|$', line):
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            continue
        
        if line.startswith("|"):
            if not in_table:
                html_lines.append("<table>")
                in_table = True
            cells = [c.strip() for c in line.strip("|").split("|")]
            tag = "th" if html_lines[-1].startswith("<table>") or html_lines[-1] == "<table>" else "td"
            row = "".join(f"<{tag}>{c}</{tag}>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue
        
        # 列表项
        m = re.match(r'^[-*] (.+)$', line)
        if m:
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = m.group(1)
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
            html_lines.append(f"<li>{content}</li>")
            continue
        
        # 普通段落
        if in_list: html_lines.append("</ul>"); in_list = False
        if in_table: html_lines.append("</table>"); in_table = False
        
        content = line
        content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
        content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', content)
        content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
        html_lines.append(f"<p>{content}</p>")
    
    if in_list: html_lines.append("</ul>")
    if in_table: html_lines.append("</table>")
    
    html = "\n".join(html_lines)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }}
h1 {{ border-bottom: 2px solid #eee; padding-bottom: 10px; }}
h2 {{ border-bottom: 1px solid #eee; padding-bottom: 5px; }}
table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
</style>
</head>
<body>
{html}
</body>
</html>"""


# ── 通道能力表（哪些通道支持什么格式） ──

CHANNEL_CAPS = {
    "jvsclaw":      {"html": False, "md": True,  "table": True,  "code": True},
    "telegram":     {"html": "limited", "md": True, "table": False, "code": True},   # 有限 HTML 子集
    "wecom":        {"html": "limited", "md": True, "table": False, "code": True},
    "feishu":       {"html": False, "md": True,  "table": True,  "code": True},
    "dingtalk":     {"html": False, "md": True,  "table": False, "code": True},
    "qqbot":        {"html": False, "md": True,  "table": False, "code": True},
    "whatsapp":     {"html": False, "md": False, "table": False, "code": False},  # 纯文本
    "signal":       {"html": False, "md": False, "table": False, "code": False},
    "imessage":     {"html": False, "md": True,  "table": True,  "code": True},
    "discord":      {"html": False, "md": True,  "table": True,  "code": True},
    "slack":        {"html": False, "md": True,  "table": True,  "code": True},
    "openim":       {"html": False, "md": True,  "table": True,  "code": True},
    "googlechat":   {"html": False, "md": True,  "table": False, "code": True},
    "irc":          {"html": False, "md": False, "table": False, "code": False},
    "line":         {"html": False, "md": False, "table": False, "code": False},
}


def get_channel_caps(channel: str) -> dict:
    """获取通道能力，未知通道默认保守（不渲染 HTML/表格）"""
    return CHANNEL_CAPS.get(channel, {"html": False, "md": True, "table": False, "code": False})


def md_for_channel(md_text: str, channel: str) -> str:
    """MD → 按通道能力降级
    
    Args:
        md_text: Markdown 文本
        channel: 通道 ID（jvsclaw / telegram / wecom ...）
    
    Returns:
        通道支持的文本格式（HTML / MD / 纯文本）
    """
    caps = get_channel_caps(channel)
    
    # 支持 MD → 原样返回
    if caps["md"]:
        return md_text
    
    # 不支持 MD 也不支持 HTML → 降级为纯文本（剥离所有格式标记）
    return _strip_markdown(md_text)


def _strip_markdown(md_text: str) -> str:
    """MD → 纯文本（剥离所有格式标记）
    
    保留结构化层次感，用缩进和分隔线替代格式：
    - ## 标题 → 大写 + 分隔线
    - **粗体** → 去掉星号
    - 表格 → 对齐列文本
    - 列表 → 缩进 + 符号
    """
    lines = md_text.split("\n")
    result = []
    
    for line in lines:
        # 标题 → 大写 + 下划线
        h_m = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_m:
            level = len(h_m.group(1))
            txt = h_m.group(2)
            if level <= 2:
                result.append(txt.upper())
                result.append("─" * min(len(txt), 60))
            else:
                result.append(f"  {txt}")
            continue
        
        # **粗体** / *斜体* / `代码` → 去标记，保留内容
        line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
        line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', line)
        line = re.sub(r'`(.+?)`', r'\1', line)
        
        # 表格 → 保留文本对齐（至少保证可读）
        # 纯文本通道不展开表格，简化处理
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            line = " | ".join(cells)
        
        result.append(line)
    
    return "\n".join(result)


def md_to_html_safe(md_text: str, channel: str) -> str:
    """MD → 按通道能力的安全 HTML
    
    - 完整 HTML 通道 → 完整 HTML
    - 有限 HTML 通道 → 只保留 b/i/a/code/p 标签
    - 不支持 HTML → 跳过（调用 md_for_channel）
    """
    caps = get_channel_caps(channel)
    
    if not caps["html"] and caps["html"] != "limited":
        return md_for_channel(md_text, channel)
    
    full_html = md_to_html(md_text)
    
    if caps["html"] == "limited":
        # 剥离复杂标签，只保留基础样式标签
        full_html = re.sub(r'</?(h[1-6]|table|tr|th|td|ul|ol|li|hr|pre|div|span|style|script)\b[^>]*>', '', full_html)
        # 表格内容保留为文本
        full_html = re.sub(r'\n\s*\n', '\n', full_html)
    
    return full_html


def md_to_json(md_text: str) -> dict:
    """MD → JSON 结构化提取（v1.0.0）
    
    提取元信息（标题/来源/UP主/时长）+ analysis JSON 块 + 转录文本
    
    Args:
        md_text: Markdown 原始文本
    
    Returns:
        {
            "title": str, "source": str, "uploader": str,
            "duration": str, "text": str, "analysis": dict
        }
    """
    result = {
        "title": "",
        "source": "",
        "uploader": "",
        "duration": "",
        "text": "",
        "analysis": {},
    }
    
    title_m = re.match(r'^#\s+(.+)$', md_text, re.M)
    if title_m: result["title"] = title_m.group(1)
    
    source_m = re.search(r'\*\*来源\*\*:\s+(.+)$', md_text, re.M)
    if source_m: result["source"] = source_m.group(1).strip()
    
    uploader_m = re.search(r'\*\*UP主\*\*:\s+(.+)$', md_text, re.M)
    if uploader_m: result["uploader"] = uploader_m.group(1).strip()
    
    duration_m = re.search(r'\*\*时长\*\*:\s+(.+)$', md_text, re.M)
    if duration_m: result["duration"] = duration_m.group(1).strip()
    
    # 优先级1: fenced code block
    json_m = re.search(r'```json\s*\n({[\s\S]*?})\s*\n```', md_text)
    # 优先级2: ## 结构化分析 下的裸 JSON
    if not json_m:
        sec_m = re.search(r'## 结构化分析\s*\n([\s\S]*?)(?=\n## |\n# |\Z)', md_text)
        if sec_m:
            json_block = sec_m.group(1).strip()
            if json_block.startswith('{'):
                json_m = re.match(r'(\{[\s\S]*\})', json_block)
    # 优先级3: 全文搜 JSON 对象
    if not json_m:
        json_m = re.search(r'({\s*"summary"[^}]*"confidence_score"[^}]*})', md_text, re.DOTALL)
    if json_m:
        try:
            result["analysis"] = json.loads(json_m.group(1))
        except json.JSONDecodeError:
            pass
    
    text_m = re.search(r'## 转录文本\s*\n([\s\S]*?)(?=## |\Z)', md_text)
    if text_m:
        result["text"] = text_m.group(1).strip()
    
    return result
