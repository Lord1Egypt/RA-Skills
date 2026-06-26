"""
微信公众号排版脚本 🐱
HTML 排版 + 封面建议 + 摘要提取
"""

import re


class WeChatFormatter:
    def __init__(self, author: str = ""):
        self.author = author

    HEADER_STYLE = """
    <section style="margin: 20px 0; padding: 8px 24px; border-radius: 20px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; font-size: 20px; font-weight: bold; text-align: center;">
        {text}
    </section>
    """

    PARAGRAPH_STYLE = """
    <section style="margin: 16px 8px; font-size: 16px; line-height: 1.8; 
        color: #333333; text-align: justify;">
        {text}
    </section>
    """

    QUOTE_STYLE = """
    <section style="margin: 20px 0; padding: 16px 20px; 
        border-left: 4px solid #667eea; background: #f8f9ff; border-radius: 0 8px 8px 0;">
        <section style="font-size: 15px; line-height: 1.8; color: #555555;">
            {text}
        </section>
    </section>
    """

    FOOTER = """
    <section style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center;">
        <section style="font-size: 14px; color: #999999;">
            🐱 如果你觉得这篇文章有用，记得点个<span style="color: #e74c3c;">「在看」</span>哦～
        </section>
    </section>
    """

    def format_article(self, title: str, content: str) -> dict:
        """格式化文章为微信公众号 HTML"""
        html = self._markdown_to_html(content)

        summary = self.extract_summary(content)
        cover = self.cover_suggestions(title)

        return {
            "platform": "微信公众号",
            "title": title,
            "html": html,
            "summary": summary,
            "cover_suggestions": cover,
            "note": "请将 HTML 粘贴到公众号编辑器的"源码模式"中",
        }

    def _markdown_to_html(self, markdown_content: str) -> str:
        lines = markdown_content.split("\n")
        html_parts = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("# "):
                html_parts.append(self.HEADER_STYLE.format(text=line[2:]))
            elif line.startswith("## "):
                html_parts.append(f'<section style="margin: 24px 0 16px; font-size: 18px; font-weight: bold; color: #333;">{line[3:]}</section>')
            elif line.startswith("### "):
                html_parts.append(f'<section style="margin: 20px 0 12px; font-size: 16px; font-weight: bold; color: #555; padding-left: 12px; border-left: 3px solid #667eea;">{line[4:]}</section>')
            elif line.startswith("> "):
                html_parts.append(self.QUOTE_STYLE.format(text=line[2:]))
            elif line.startswith("- ") or line.startswith("* "):
                html_parts.append(f'<section style="margin: 8px 0 8px 20px;">🔹 {line[2:]}</section>')
            elif re.match(r"^\d+\.\s", line):
                html_parts.append(f'<section style="margin: 8px 0 8px 20px;">📌 {re.sub(r"^\d+\.\s", "", line)}</section>')
            else:
                text = self._inline_format(line)
                if text.strip():
                    html_parts.append(self.PARAGRAPH_STYLE.format(text=text))

        html_body = "\n".join(html_parts)

        return f"""
<section style="font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;">
    {html_body}
    {self.FOOTER}
</section>
        """.strip()

    def _inline_format(self, text: str) -> str:
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        text = re.sub(
            r"`(.*?)`",
            r'<code style="background: #f5f5f5; padding: 2px 6px; border-radius: 4px;">\1</code>',
            text,
        )
        text = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2" style="color: #667eea;">\1</a>', text)
        return text

    def extract_summary(self, content: str, max_length: int = 120) -> str:
        lines = [l for l in content.split("\n") if not l.startswith("#")]
        summary = " ".join(lines).strip()
        summary = re.sub(r"[*`\[\]()>#_-]", "", summary)
        summary = re.sub(r"\s+", " ", summary)
        return summary[:max_length] + ("..." if len(summary) > max_length else "")

    def cover_suggestions(self, title: str) -> dict:
        return {
            "size": "900x383 像素（2.35:1）",
            "style_suggestions": [
                "大字报风格：突出文章标题关键词",
                "渐变背景 + 白色文字",
                "纯色背景 + Emoji 图标",
            ],
            "tools": ["Canva", "稿定设计", "创客贴"],
        }
