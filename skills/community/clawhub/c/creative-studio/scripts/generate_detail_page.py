#!/usr/bin/env python3
"""Generate a complete product detail page HTML from a YAML config file.

Usage:
  python generate_detail_page.py --product-config product.yaml -o detail.html
  python generate_detail_page.py --product-config product.yaml --lang en -o detail_en.html
  python generate_detail_page.py --product-config product.yaml --lang both -o detail.html

The script reads the brand template from assets/detail-page-template.html,
merges product data from the YAML config, and writes a self-contained HTML file.
"""

import argparse
import datetime
import io
import os
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LANG = {
    "zh": {
        "specs_header": "参数项目",
        "specs_value": "数值",
        "missing_yaml": "PyYAML 未安装。请执行: pip install pyyaml",
        "missing_config": "配置文件不存在",
        "generating": "生成详情页",
        "done": "完成",
        "error": "错误",
        "output": "输出",
        "lang_mode": "语言模式",
    },
    "en": {
        "specs_header": "Parameter",
        "specs_value": "Value",
        "missing_yaml": "PyYAML not installed. Run: pip install pyyaml",
        "missing_config": "Config file not found",
        "generating": "Generating detail page",
        "done": "Done",
        "error": "Error",
        "output": "Output",
        "lang_mode": "Language mode",
    },
}

ICON_EMOJI = {
    "zap": "⚡", "cpu": "🖥️", "volume": "🔇", "shield": "🛡️",
    "thermometer": "🌡️", "wrench": "🔧", "leaf": "🌿",
    "gauge": "📊", "droplet": "💧", "wind": "💨",
}


def load_template(skill_dir):
    """Load the detail page HTML template."""
    template_path = os.path.join(skill_dir, "assets", "detail-page-template.html")
    if not os.path.isfile(template_path):
        print(f"Error: Template not found at {template_path}")
        sys.exit(1)
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def load_product_config(config_path):
    """Load YAML product configuration."""
    try:
        import yaml
    except ImportError:
        print("[✗] PyYAML not installed. Run: pip install pyyaml")
        sys.exit(1)

    if not os.path.isfile(config_path):
        print(f"[✗] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_specs_rows(specs):
    """Generate <tr> rows for the specs table."""
    rows = []
    for spec in specs:
        label = spec.get("label", "")
        value = spec.get("value", "")
        rows.append(f'<tr><td>{label}</td><td>{value}</td></tr>')
    return "\n        ".join(rows)


def build_features_html(features):
    """Generate feature cards HTML."""
    cards = []
    for feat in features:
        icon_key = feat.get("icon", "zap")
        emoji = ICON_EMOJI.get(icon_key, "⭐")
        title = feat.get("title", "")
        title_en = feat.get("title_en", "")
        desc = feat.get("desc", "")
        desc_en = feat.get("desc_en", "")

        title_display = title
        desc_display = desc
        if title_en:
            title_display += f" / {title_en}"
        if desc_en:
            desc_display += f"<br/><small style='color:#888'>{desc_en}</small>"

        card = f"""<div class="feature-card">
      <div class="feature-card__icon">{emoji}</div>
      <div class="feature-card__title">{title_display}</div>
      <div class="feature-card__desc">{desc_display}</div>
    </div>"""
        cards.append(card)
    return "\n".join(cards)


def build_metrics_html(metrics):
    """Generate metrics bar HTML."""
    if not metrics:
        return ""

    items = []
    for m in metrics:
        value = m.get("value", "")
        label = m.get("label", "")
        label_en = m.get("label_en", "")
        label_display = f"{label} / {label_en}" if label_en else label
        items.append(f"""<div>
      <div class="metric__value">{value}</div>
      <div class="metric__label">{label_display}</div>
    </div>""")

    return f"""<section class="metrics">
  <div class="container">
    <div class="metrics__grid">
      {''.join(items)}
    </div>
  </div>
</section>"""


def build_gallery_html(images):
    """Generate thumbnail gallery HTML."""
    if not images:
        return ""

    thumbs = images.get("thumbnails", [])
    if not thumbs:
        return ""

    items = []
    for img in thumbs:
        items.append(f'<img src="{img}" alt="Product view" style="width:120px;height:120px;object-fit:cover;border-radius:8px;cursor:pointer" onclick="document.querySelector(\'#mainImage\').src=this.src" />')

    return f"""<section class="gallery" style="padding:40px 0;background:var(--color-white)">
  <div class="container" style="text-align:center">
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
      {''.join(items)}
    </div>
  </div>
</section>"""


def build_main_image_html(images):
    """Generate main hero image HTML."""
    main = images.get("main", "") if images else ""
    if main:
        return f'<img src="{main}" alt="{{{{PRODUCT_NAME}}}}" id="mainImage" />'
    return '<div class="placeholder">产品图片 / Product Image</div>'


def build_viewer3d_html(config):
    """Generate optional 3D viewer section."""
    if not config.get("enable_3d"):
        return ""

    return """<section class="viewer3d">
  <div class="container">
    <div class="section-title">
      <h2>3D 产品展示 / 3D Product Viewer</h2>
      <p>拖拽旋转 · 滚轮缩放 · 右键平移</p>
    </div>
    <div class="viewer3d__container">
      <iframe src="3d-viewer.html" id="viewer3d__canvas" frameborder="0"></iframe>
    </div>
  </div>
</section>"""


def generate_page(template, config, lang):
    """Merge product config into template, return final HTML."""
    prod = config.get("product", config)
    images = prod.get("images", {})
    metrics = prod.get("metrics", [])
    cta = prod.get("cta", {})

    replacements = {
        "{{PRODUCT_NAME}}": prod.get("name", "Product Name"),
        "{{PRODUCT_NAME_EN}}": prod.get("name_en", ""),
        "{{PRODUCT_CATEGORY}}": prod.get("category", ""),
        "{{PRODUCT_DESCRIPTION}}": prod.get("description", ""),
        "{{PRODUCT_DESCRIPTION_EN}}": prod.get("description_en", ""),
        "{{SPECS_TABLE_ROWS}}": build_specs_rows(prod.get("specs", [])),
        "{{FEATURES_HTML}}": build_features_html(prod.get("features", [])),
        "{{METRICS_HTML}}": build_metrics_html(metrics),
        "{{GALLERY_HTML}}": build_gallery_html(images),
        "{{MAIN_IMAGE_HTML}}": build_main_image_html(images),
        "{{VIEWER3D_HTML}}": build_viewer3d_html(config),
        "{{CTA_PHONE}}": cta.get("phone", "13825202084"),
        "{{CTA_PERSON}}": cta.get("contact_person", "邹先生"),
        "{{CTA_WEBSITE}}": cta.get("website", "www.fireflies.net.cn"),
        "{{LOGO_PATH}}": "assets/brand-logo.svg",
        "{{CURRENT_YEAR}}": str(datetime.datetime.now().year),
        "{{EXTRA_CSS}}": "",
        "{{BRAND_PRIMARY_COLOR}}": "#1B8C3A",
        "{{BRAND_ACCENT_COLOR}}": "#F57C00",
    }

    result = template
    for key, value in replacements.items():
        result = result.replace(key, str(value))

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate product detail page HTML")
    parser.add_argument("--product-config", "-c", required=True, help="YAML config file")
    parser.add_argument("--output", "-o", default="product_detail.html", help="Output HTML file")
    parser.add_argument("--lang", default="zh", choices=["zh", "en", "both"],
                        help="Language: zh, en, or both")
    parser.add_argument("--skill-dir", help="Skill directory (auto-detected if not specified)")
    args = parser.parse_args()

    msg = LANG["zh"] if args.lang in ("zh", "both") else LANG["en"]

    # Auto-detect skill directory
    if args.skill_dir:
        skill_dir = args.skill_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)

    # Load template
    template = load_template(skill_dir)

    # Load product config
    config = load_product_config(args.product_config)

    print(f"[{msg['generating']}] {args.product_config}")
    print(f"  {msg['lang_mode']}: {args.lang}")

    # Generate
    html = generate_page(template, config, args.lang)

    # Write output
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(args.output) / 1024
    print(f"  {msg['done']} ({size_kb:.1f} KB)")
    print(f"  {msg['output']}: {args.output}")


if __name__ == "__main__":
    main()
