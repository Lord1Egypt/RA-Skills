#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Magazine PPT Generator - Core Script
Author: WuWenBin-BeiJing-ST
Version: 1.0.0

生成单文件 HTML 横向翻页 PPT
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 主题色配置
THEMES = {
    "ink-classic": {
        "primary": "#1a1a2e",
        "secondary": "#4a4e69",
        "accent": "#9a8c98",
        "background": "#fafafa",
        "text": "#2d2d2d",
        "text_light": "#666666",
    },
    "indigo-porcelain": {
        "primary": "#2c3e50",
        "secondary": "#3498db",
        "accent": "#1abc9c",
        "background": "#ffffff",
        "text": "#2c3e50",
        "text_light": "#7f8c8d",
    },
    "forest-ink": {
        "primary": "#2d3436",
        "secondary": "#00b894",
        "accent": "#55a3ff",
        "background": "#f8f9fa",
        "text": "#2d3436",
        "text_light": "#636e72",
    },
    "kraft-paper": {
        "primary": "#d4a373",
        "secondary": "#e9c46a",
        "accent": "#f4a261",
        "background": "#fefae0",
        "text": "#264653",
        "text_light": "#6c757d",
    },
    "dune": {
        "primary": "#264653",
        "secondary": "#e76f51",
        "accent": "#2a9d8f",
        "background": "#ffffff",
        "text": "#264653",
        "text_light": "#8d99ae",
    },
}

# 字体配置
FONTS = {
    "title": {
        "family": "Georgia, 'Songti SC', 'Noto Serif SC', serif",
        "sizes": {"hero": 96, "page": 64, "card": 24},
    },
    "body": {
        "family": "Inter, 'PingFang SC', 'Noto Sans SC', sans-serif",
        "sizes": {"large": 24, "normal": 18, "small": 16},
    },
    "mono": {
        "family": "'JetBrains Mono', 'SF Mono', Consolas, monospace",
        "sizes": {"normal": 14, "small": 12},
    },
}


def parse_outline(outline_path: str) -> Dict:
    """解析大纲 JSON 文件"""
    with open(outline_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_css(theme: Dict) -> str:
    """生成 CSS 样式"""
    return f"""
/* Reset & Base */
*, *::before, *::after {{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}}

:root {{
  --primary: {theme['primary']};
  --secondary: {theme['secondary']};
  --accent: {theme['accent']};
  --background: {theme['background']};
  --text: {theme['text']};
  --text-light: {theme['text_light']};
}}

html {{
  scroll-behavior: smooth;
  scroll-snap-type: x mandatory;
}}

body {{
  font-family: {FONTS['body']['family']};
  background: var(--background);
  color: var(--text);
  overflow-x: auto;
  overflow-y: hidden;
  display: flex;
  scroll-snap-type: x mandatory;
}}

/* Slide Container */
.slide {{
  min-width: 100vw;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px;
  scroll-snap-align: start;
  position: relative;
}}

/* Typography */
.title-hero {{
  font-family: {FONTS['title']['family']};
  font-size: {FONTS['title']['sizes']['hero']}px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--primary);
}}

.title-page {{
  font-family: {FONTS['title']['family']};
  font-size: {FONTS['title']['sizes']['page']}px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--primary);
}}

.body-large {{
  font-size: {FONTS['body']['sizes']['large']}px;
  line-height: 1.6;
  color: var(--text);
}}

.body-normal {{
  font-size: {FONTS['body']['sizes']['normal']}px;
  line-height: 1.6;
  color: var(--text);
}}

.meta-text {{
  font-family: {FONTS['mono']['family']};
  font-size: {FONTS['mono']['sizes']['normal']}px;
  color: var(--text-light);
}}

/* Navigation Dots */
.nav-dots {{
  position: fixed;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 12px;
  z-index: 1000;
}}

.nav-dot {{
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(0,0,0,0.2);
  cursor: pointer;
  transition: all 0.3s ease;
}}

.nav-dot.active {{
  background: var(--primary);
  transform: scale(1.3);
}}

.nav-dot:hover {{
  background: rgba(0,0,0,0.4);
}}

/* Page Number */
.page-number {{
  position: fixed;
  bottom: 40px;
  right: 60px;
  font-family: {FONTS['mono']['family']};
  font-size: {FONTS['mono']['sizes']['normal']}px;
  color: var(--text-light);
  z-index: 1000;
}}

/* Animations */
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(20px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}

.slide {{
  animation: fadeIn 0.6s ease-out;
}}
"""


def generate_html_slide(slide_data: Dict, slide_index: int) -> str:
    """生成单个幻灯片 HTML"""
    layout = slide_data.get("layout", "L01")
    title = slide_data.get("title", "")
    subtitle = slide_data.get("subtitle", "")
    content = slide_data.get("content", [])
    image = slide_data.get("image", "")

    # 根据布局生成不同结构
    if layout == "L01":  # Hero 封面
        return f"""
<div class="slide" data-slide="{slide_index}">
  <div style="text-align: center; max-width: 800px;">
    <h1 class="title-hero">{title}</h1>
    {f'<p class="body-large" style="margin-top: 24px;">{subtitle}</p>' if subtitle else ''}
  </div>
</div>
"""
    elif layout == "L02":  # 左图右文
        return f"""
<div class="slide" data-slide="{slide_index}">
  <div style="display: flex; width: 100%; gap: 80px; align-items: center;">
    <div style="flex: 1;">
      {f'<img src="{image}" alt="{title}" style="width: 100%; border-radius: 16px;">' if image else ''}
    </div>
    <div style="flex: 1;">
      <h2 class="title-page">{title}</h2>
      {f'<p class="body-normal" style="margin-top: 24px;">{subtitle}</p>' if subtitle else ''}
    </div>
  </div>
</div>
"""
    elif layout == "L05":  # 三栏并列
        items = content if isinstance(content, list) else []
        items_html = "".join(
            [
                f"""
      <div style="flex: 1; text-align: center; padding: 40px;">
        <h3 style="font-size: 24px; margin-bottom: 16px;">{item.get('title', '')}</h3>
        <p class="body-normal" style="color: var(--text-light);">{item.get('description', '')}</p>
      </div>
    """
                for item in items[:3]
            ]
        )
        return f"""
<div class="slide" data-slide="{slide_index}">
  <div style="width: 100%;">
    <h2 class="title-page" style="text-align: center; margin-bottom: 60px;">{title}</h2>
    <div style="display: flex; gap: 40px;">
      {items_html}
    </div>
  </div>
</div>
"""
    else:  # 默认布局
        return f"""
<div class="slide" data-slide="{slide_index}">
  <div style="max-width: 800px;">
    <h2 class="title-page">{title}</h2>
    {f'<p class="body-normal" style="margin-top: 24px;">{subtitle}</p>' if subtitle else ''}
  </div>
</div>
"""


def generate_full_html(
    outline: Dict, theme_name: str, output_path: str
) -> str:
    """生成完整 HTML 文件"""
    theme = THEMES.get(theme_name, THEMES["ink-classic"])
    slides = outline.get("slides", [])

    # 生成 CSS
    css = generate_css(theme)

    # 生成所有幻灯片
    slides_html = "\n".join(
        [generate_html_slide(slide, i) for i, slide in enumerate(slides, 1)]
    )

    # 生成导航点
    nav_dots = "".join(
        [
            f'<span class="nav-dot{" active" if i == 0 else ""}" data-slide="{i}"></span>'
            for i in range(1, len(slides) + 1)
        ]
    )

    # 完整 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{outline.get('title', '演示文稿')}</title>
  <style>
{css}
  </style>
</head>
<body>
{slides_html}

  <!-- Navigation -->
  <div class="nav-dots">
    {nav_dots}
  </div>

  <!-- Page Number -->
  <div class="page-number">
    <span class="current">01</span>
    <span class="separator">/</span>
    <span class="total">{len(slides):02d}</span>
  </div>

  <script>
    // Slide navigation
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.nav-dot');
    const currentNum = document.querySelector('.page-number .current');
    let currentIndex = 0;

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {{
        goToSlide(currentIndex + 1);
      }} else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {{
        goToSlide(currentIndex - 1);
      }}
    }});

    // Dot navigation
    dots.forEach((dot, index) => {{
      dot.addEventListener('click', () => goToSlide(index));
    }});

    function goToSlide(index) {{
      if (index < 0 || index >= slides.length) return;
      currentIndex = index;
      slides[index].scrollIntoView({{ behavior: 'smooth' }});

      // Update dots
      dots.forEach((dot, i) => {{
        dot.classList.toggle('active', i === index);
      }});

      // Update page number
      currentNum.textContent = String(index + 1).padStart(2, '0');
    }}
  </script>
</body>
</html>
"""

    # 写入文件
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")

    return str(output_file)


def main():
    parser = argparse.ArgumentParser(description="生成 HTML 横向翻页 PPT")
    parser.add_argument("--content", required=True, help="PPT 主题/内容描述")
    parser.add_argument("--outline", help="大纲 JSON 文件路径")
    parser.add_argument(
        "--theme", default="ink-classic", choices=THEMES.keys(), help="主题色"
    )
    parser.add_argument("--output", default="./output/presentation.html", help="输出路径")

    args = parser.parse_args()

    # 如果提供了大纲文件，使用大纲生成
    if args.outline:
        outline = parse_outline(args.outline)
    else:
        # 否则使用内容描述生成简单大纲
        outline = {
            "title": args.content,
            "slides": [
                {"layout": "L01", "title": args.content, "subtitle": "演示文稿"},
                {"layout": "L05", "title": "核心要点", "content": []},
                {"layout": "L01", "title": "感谢观看", "subtitle": ""},
            ],
        }

    # 生成 HTML
    output_file = generate_full_html(outline, args.theme, args.output)
    print(f"✅ PPT 已生成: {output_file}")

    # 自动打开（macOS）
    if sys.platform == "darwin":
        os.system(f'open "{output_file}"')


if __name__ == "__main__":
    main()
