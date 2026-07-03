#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
convert_for_wechat.py — Convert HTML with <style> tags to WeChat-compatible inline-style HTML.

WeChat Official Account strips <style> tags, <link> stylesheets, CSS variables,
position:fixed/sticky, and many other CSS features. This script converts standard
HTML+CSS to WeChat-safe inline styles.

Features:
  - Extracts CSS from <style> tags and inlines as style attributes
  - Recursively resolves CSS variables (var(--xxx)) to literal values
  - Converts dark theme backgrounds to light equivalents
  - Removes WeChat-incompatible CSS properties
  - Removes <script> tags
  - Wraps output in <section> for WeChat compatibility
  - Auto-installs missing dependencies (beautifulsoup4, cssutils)

Usage:
    python convert_for_wechat.py --input article.html --output wechat_article.html
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("[INFO] Installing beautifulsoup4...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"])
    from bs4 import BeautifulSoup, Tag

try:
    import cssutils
    cssutils.log.setLevel(50)  # suppress verbose warnings
except ImportError:
    print("[INFO] Installing cssutils...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cssutils", "-q"])
    import cssutils
    cssutils.log.setLevel(50)


# ── Clockless CSS variable defaults (light theme) ──
# These serve as fallback values when resolving var(--xxx) references.
CLOCKLESS_VARS = {
    # Brand colors
    "--primary": "#a03b00",
    "--primary-container": "#c94c00",
    "--primary-fixed": "#ffdbcd",
    "--primary-fixed-dim": "#ffb597",
    "--on-primary": "#ffffff",
    "--accent-glow": "#E8400D",
    # Secondary / tertiary
    "--secondary": "#d5baff",
    "--secondary-container": "#7b40e0",
    "--tertiary": "#4d44e3",
    "--accent-cyan": "#00D4FF",
    # Surfaces
    "--bg": "#fff8f6",
    "--surface": "#fff8f6",
    "--surface-container-lowest": "#ffffff",
    "--surface-container-low": "#fbf2ef",
    "--surface-container": "#f5ece9",
    "--surface-container-high": "#efe6e3",
    # Text
    "--fg-1": "#1e1b19",
    "--fg-2": "#594138",
    "--fg-muted": "#8d7166",
    # Borders
    "--border": "rgba(0,0,0,0.06)",
    "--border-strong": "rgba(0,0,0,0.12)",
    "--outline-variant": "#e1bfb2",
    # Status
    "--green": "#10b981",
    "--blue": "#3b82f6",
    "--yellow": "#f59e0b",
    "--red": "#ef4444",
    # Typography
    "--font-headline": "'Space Grotesk', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif",
    "--font-body": "'Plus Jakarta Sans', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif",
    "--font-mono": "'SF Mono', 'Menlo', monospace",
    # Spacing (4px base)
    "--space-xs": "4px",
    "--space-sm": "8px",
    "--space-md": "12px",
    "--space-lg": "16px",
    "--space-xl": "20px",
    "--space-2xl": "24px",
    "--space-3xl": "32px",
    "--space-4xl": "48px",
    "--space-5xl": "64px",
    # Radius
    "--radius-sm": "8px",
    "--radius-md": "12px",
    "--radius-lg": "16px",
    "--radius-xl": "20px",
    "--radius-2xl": "28px",
    "--radius-pill": "9999px",
    # Shadows
    "--shadow-sm": "0 1px 2px rgba(30,27,25,0.04)",
    "--shadow-md": "0 4px 12px rgba(30,27,25,0.08)",
    "--shadow-lg": "0 8px 24px rgba(30,27,25,0.12)",
    "--shadow-accent": "0 8px 24px rgba(160,59,0,0.15)",
    # Gradients
    "--gradient-primary": "linear-gradient(135deg, #a03b00 0%, #c94c00 100%)",
    "--gradient-hero": "linear-gradient(135deg, #a03b00 0%, #7b40e0 100%)",
    "--gradient-text": "linear-gradient(135deg, #a03b00 0%, #7b40e0 100%)",
}

# ── Dark → light color mapping ──
# Maps common dark theme colors to their light equivalents.
DARK_TO_LIGHT = {
    "#060b18": "#fff8f6",
    "#0b1426": "#fff8f6",
    "#101d35": "#ffffff",
    "#162544": "#f5ece9",
    "#1c2d52": "#efe6e3",
    "#0a0e1a": "#ffffff",
    "#111827": "#f9fafb",
    "#1e1b19": "#ffffff",
    "#1a1a2e": "#ffffff",
    "#16213e": "#ffffff",
    "#0f0f23": "#ffffff",
    "#1e293b": "#f8fafc",
    "#0f172a": "#f8fafc",
    # Foreground swaps (light text → dark text)
    "#f8fafc": "#1e1b19",
    "#cbd5e1": "#594138",
    "#64748b": "#8d7166",
}

# ── CSS properties WeChat strips ──
WECHAT_BLOCKED_PROPS = {
    "position",         # WeChat only allows static/relative
    "z-index",
    "backdrop-filter",
    "filter",
    "mix-blend-mode",
    "clip-path",
    "mask",
    "overflow",         # sometimes stripped
    "-webkit-overflow-scrolling",
    "scroll-behavior",
    "scroll-snap-type",
    "scroll-snap-align",
}

# ── WeChat base styles applied to the wrapper ──
WECHAT_BASE_STYLE = (
    "max-width: 680px; margin: 0 auto; padding: 20px 16px; "
    "font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif; "
    "color: #333333; line-height: 1.8; background-color: #ffffff;"
)


# ────────────────────────────────────────────────────
# CSS Processing Functions
# ────────────────────────────────────────────────────


def extract_css_variables(style_text):
    """Extract CSS custom properties from :root or any selector block."""
    variables = dict(CLOCKLESS_VARS)
    var_pattern = re.compile(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;]+);")
    for match in var_pattern.finditer(style_text):
        name = "--" + match.group(1)
        value = match.group(2).strip()
        variables[name] = value
    return variables


def resolve_var(value, variables, depth=0):
    """Recursively resolve var(--xxx) references with fallback support."""
    if depth > 10:
        return value
    var_pattern = re.compile(r"var\(\s*(--[a-zA-Z0-9_-]+)\s*(?:,\s*([^)]+))?\)")

    def replacer(match):
        var_name = match.group(1)
        fallback = match.group(2)
        resolved = variables.get(var_name, fallback or match.group(0))
        if resolved and "var(" in resolved:
            resolved = resolve_var(resolved, variables, depth + 1)
        return resolved or match.group(0)

    return var_pattern.sub(replacer, value)


def resolve_gradient(gradient_str, variables):
    """Resolve CSS variables inside gradient expressions."""
    if "var(" not in gradient_str:
        return gradient_str
    return resolve_var(gradient_str, variables)


def convert_dark_colors(value):
    """Convert common dark theme colors to light equivalents."""
    lower = value.lower().strip()
    for dark, light in DARK_TO_LIGHT.items():
        if dark in lower:
            value = value.replace(dark, light).replace(dark.upper(), light)
    return value


def parse_stylesheet(style_text, variables):
    """
    Parse CSS text and build a dict of selector → {property: value}.

    Resolves variables, converts dark colors, and skips blocked properties.
    """
    rules = {}
    try:
        sheet = cssutils.parseString(style_text)
        for rule in sheet:
            if rule.type == rule.STYLE_RULE:
                selector = rule.selectorText
                props = {}
                for prop in rule.style:
                    name = prop.name
                    val = prop.value

                    # Skip blocked properties
                    if name in WECHAT_BLOCKED_PROPS:
                        continue

                    # Resolve variables and convert colors
                    val = resolve_var(val, variables)
                    val = convert_dark_colors(val)

                    props[name] = val
                if props:
                    rules[selector] = props
    except Exception:
        pass
    return rules


def selector_matches(tag, selector):
    """Match a CSS selector against a BeautifulSoup tag (simple selectors only)."""
    selector = selector.strip()
    if not selector or not isinstance(tag, Tag):
        return False

    parts = re.split(r'(?=[.#\[])', selector)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if part.startswith('.'):
            cls = part[1:]
            classes = tag.get('class', [])
            if cls not in classes:
                return False
        elif part.startswith('#'):
            tid = part[1:]
            if tag.get('id') != tid:
                return False
        elif part.startswith('['):
            m = re.match(r'\[([a-zA-Z_-]+)(?:=([^\]]+))?\]', part)
            if m:
                attr = m.group(1)
                val = m.group(2)
                if val:
                    val = val.strip("'\"")
                    if tag.get(attr) != val:
                        return False
                elif not tag.has_attr(attr):
                    return False
        else:
            if tag.name != part.lower():
                return False
    return True


def get_specificity(selector):
    """Calculate a rough specificity score for sorting (higher = more specific)."""
    score = 0
    score += selector.count('#') * 100
    score += selector.count('.') * 10
    score += len(re.findall(r'^[a-z]', selector, re.I)) * 1
    return score


def apply_styles_to_soup(soup, rules, variables):
    """
    Apply parsed CSS rules as inline styles to matching BeautifulSoup elements.

    Rules are sorted by specificity (low → high) so specific rules override general ones.
    Existing inline styles are preserved (not overridden).
    """
    sorted_selectors = sorted(rules.keys(), key=get_specificity)

    for selector in sorted_selectors:
        props = rules[selector]

        # Skip pseudo-selectors and comma-separated selectors
        if '::' in selector or ',' in selector:
            continue

        # Handle descendant/child combinators (take the last part)
        if ' ' in selector:
            target_sel = selector.split(' ')[-1]
        elif '>' in selector:
            target_sel = selector.split('>')[-1].strip()
        else:
            target_sel = selector

        for tag in soup.find_all(True):
            if selector_matches(tag, target_sel):
                existing = tag.get('style', '')
                new_styles = []
                for prop, val in props.items():
                    style_decl = f"{prop}: {val};"
                    # Don't override if property already in inline style
                    if prop + ':' not in existing.replace(' ', ''):
                        new_styles.append(style_decl)
                if new_styles:
                    combined = (existing.rstrip('; ') + '; ' + ' '.join(new_styles)).strip('; ')
                    tag['style'] = combined


def remove_style_tags(soup):
    """Remove all <style> and <link rel='stylesheet'> tags from the document."""
    for tag in soup.find_all('style'):
        tag.decompose()
    for tag in soup.find_all('link'):
        if tag.get('rel') and 'stylesheet' in tag.get('rel', []):
            tag.decompose()


def resolve_inline_vars(soup, variables):
    """Resolve any remaining var() references in existing inline styles."""
    for tag in soup.find_all(True):
        style = tag.get('style', '')
        if 'var(' in style:
            tag['style'] = resolve_var(style, variables)


def convert_html(input_path, output_path, base_style=None):
    """
    Main conversion pipeline: HTML+CSS → WeChat-ready inline-style HTML.

    Steps:
        1. Read HTML file
        2. Extract CSS from <style> tags
        3. Parse CSS variables
        4. Parse stylesheet rules
        5. Apply styles inline (specificity-sorted)
        6. Remove <style> and <link> tags
        7. Remove <script> tags
        8. Resolve remaining var() in inline styles
        9. Convert <body> to <section> with WeChat base styles
        10. Output inner content only (no <html>/<head>/<body> wrappers)
    """
    input_file = Path(input_path)
    print(f"[READ] Reading: {input_file}")
    html_text = input_file.read_text(encoding='utf-8')

    soup = BeautifulSoup(html_text, 'html.parser')

    # 1. Extract all CSS from <style> tags
    all_css = ""
    for style_tag in soup.find_all('style'):
        all_css += (style_tag.string or "")

    # 2. Parse CSS variables
    variables = extract_css_variables(all_css)
    print(f"[CSS] Found {len(variables)} CSS variables")

    # 3. Parse stylesheet rules
    rules = parse_stylesheet(all_css, variables)
    print(f"[CSS] Parsed {len(rules)} CSS rules")

    # 4. Apply styles inline
    if rules:
        apply_styles_to_soup(soup, rules, variables)

    # 5. Remove <style> and <link> tags
    remove_style_tags(soup)

    # 6. Remove <script> tags
    for script in soup.find_all('script'):
        script.decompose()

    # 7. Resolve remaining var() in inline styles
    resolve_inline_vars(soup, variables)

    # 8. Convert body to section for WeChat
    body = soup.find('body')
    if body:
        body.name = 'section'
        body.attrs = {}
        body['style'] = base_style or WECHAT_BASE_STYLE

    # 9. Output only the body content (WeChat only accepts inner content)
    body_tag = soup.find('section') or soup.find('body')
    if body_tag:
        output_html = str(body_tag)
    else:
        output_html = str(soup)

    # 10. Write output
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(output_html, encoding='utf-8')

    size = len(output_html.encode('utf-8'))
    print(f"[DONE] WeChat-ready HTML: {output_path}")
    print(f"[INFO] Output size: {size} bytes ({size/1024:.1f} KB)")

    if size > 2 * 1024 * 1024:
        print("[WARN] Output exceeds WeChat's 2MB limit!")

    return output_html


def main():
    parser = argparse.ArgumentParser(
        description='Convert HTML to WeChat-compatible inline-style HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python convert_for_wechat.py --input article.html --output wechat_article.html

  # With custom base style
  python convert_for_wechat.py --input article.html --output out.html \\
      --base-style "max-width: 600px; padding: 16px; font-family: sans-serif;"

What it does:
  - Inlines all CSS from <style> tags as style="" attributes
  - Resolves CSS variables (var(--xxx)) to literal values
  - Converts dark theme colors to light equivalents
  - Removes WeChat-incompatible CSS properties
  - Removes <script> tags
  - Outputs WeChat-safe inner HTML (no <html>/<head>/<body> wrappers)
        """,
    )
    parser.add_argument('--input', required=True, help='Input HTML file path')
    parser.add_argument('--output', required=True, help='Output HTML file path')
    parser.add_argument('--base-style', default=None, help='Custom base style for wrapper element (optional)')

    args = parser.parse_args()

    input_file = Path(args.input)
    if not input_file.exists():
        print(f"[ERROR] Input file not found: {args.input}")
        sys.exit(1)

    convert_html(str(input_file), args.output, args.base_style)


if __name__ == '__main__':
    main()
