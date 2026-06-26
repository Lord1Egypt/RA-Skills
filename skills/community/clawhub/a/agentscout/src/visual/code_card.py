"""代码高亮卡片 - Carbon 风格"""

from pathlib import Path
from jinja2 import Template

# Carbon 风格代码卡片 HTML
CODE_CARD_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1080px; height: 1440px;
    background: {{ bg_color }};
    display: flex; align-items: center; justify-content: center;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }
  .card {
    width: 960px;
    background: #1e1e2e;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  }
  .titlebar {
    height: 40px;
    background: #181825;
    display: flex; align-items: center;
    padding: 0 16px; gap: 8px;
  }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot-red { background: #f38ba8; }
  .dot-yellow { background: #f9e2af; }
  .dot-green { background: #a6e3a1; }
  .filename {
    color: #a6adc8; font-size: 13px;
    margin-left: 8px;
  }
  .code {
    padding: 24px;
    font-family: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    font-size: 15px; line-height: 1.6;
    color: #cdd6f4;
    white-space: pre-wrap;
    overflow: hidden;
  }
  .comment { color: #6c7086; }
  .keyword { color: #cba6f7; }
  .string { color: #a6e3a1; }
  .function { color: #89b4fa; }
  .label {
    text-align: center; padding: 16px;
    color: #a6adc8; font-size: 14px;
    background: #181825;
  }
</style>
</head>
<body>
  <div class="card">
    <div class="titlebar">
      <div class="dot dot-red"></div>
      <div class="dot dot-yellow"></div>
      <div class="dot dot-green"></div>
      <span class="filename">{{ filename }}</span>
    </div>
    <div class="code">{{ code_html }}</div>
    {% if label %}
    <div class="label">{{ label }}</div>
    {% endif %}
  </div>
</body>
</html>"""


class CodeCardGenerator:
    """代码卡片生成器"""

    def __init__(self):
        self.template = Template(CODE_CARD_TEMPLATE)

    def generate_html(
        self,
        code: str,
        filename: str = "",
        label: str = "",
        bg_color: str = "#313244",
    ) -> str:
        """生成代码卡片 HTML"""
        # 基础语法高亮（简单替换，不依赖外部库）
        code_html = self._simple_highlight(code)
        return self.template.render(
            code_html=code_html,
            filename=filename,
            label=label,
            bg_color=bg_color,
        )

    def generate_image(
        self,
        code: str,
        output_path: str,
        filename: str = "",
        label: str = "",
    ) -> str:
        """生成代码卡片图片"""
        from src.visual.composer import html_to_image
        html = self.generate_html(code, filename, label)
        return html_to_image(html, output_path, width=1080, height=1440)

    def _simple_highlight(self, code: str) -> str:
        """简单的语法高亮（HTML 标签包裹）"""
        import html
        code = html.escape(code)

        # Python 关键词
        keywords = [
            "import", "from", "def", "class", "return", "if", "else", "elif",
            "for", "while", "in", "not", "and", "or", "is", "None", "True",
            "False", "with", "as", "try", "except", "finally", "raise",
            "async", "await", "yield",
        ]
        for kw in keywords:
            code = code.replace(
                f" {kw} ", f' <span class="keyword">{kw}</span> '
            )
            if code.startswith(f"{kw} "):
                code = f'<span class="keyword">{kw}</span> ' + code[len(kw) + 1:]

        # 注释
        lines = code.split("\n")
        highlighted = []
        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith("#"):
                line = f'<span class="comment">{line}</span>'
            highlighted.append(line)

        return "\n".join(highlighted)
