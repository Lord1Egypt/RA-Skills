#!/usr/bin/env python3
"""Convert a Markdown report to styled HTML with inline CSS."""

import argparse
import re
import sys
import os

TEMPLATES = {
    'default': {
        'bg': '#ffffff',
        'text': '#333333',
        'accent': '#2563eb',
        'header_bg': '#f8fafc',
        'border': '#e2e8f0',
        'font': "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
    },
    'minimal': {
        'bg': '#ffffff',
        'text': '#1a1a1a',
        'accent': '#000000',
        'header_bg': '#fafafa',
        'border': '#eeeeee',
        'font': "'Georgia', 'Times New Roman', serif",
    },
    'branded': {
        'bg': '#ffffff',
        'text': '#1e293b',
        'accent': '#7c3aed',
        'header_bg': '#faf5ff',
        'border': '#e9d5ff',
        'font': "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif",
    },
}


def markdown_to_html(md_text, template='default'):
    """Convert markdown report to styled HTML."""
    colors = TEMPLATES.get(template, TEMPLATES['default'])
    lines = md_text.split('\n')
    html_parts = []
    in_table = False
    in_list = False
    in_code = False
    table_rows = []

    for line in lines:
        stripped = line.strip()

        # Code blocks
        if stripped.startswith('```'):
            if in_code:
                html_parts.append('</pre>')
                in_code = False
            else:
                html_parts.append(f'<pre style="background:{colors["header_bg"]};border:1px solid {colors["border"]};border-radius:6px;padding:12px;overflow-x:auto;font-size:13px;">')
                in_code = True
            continue
        if in_code:
            html_parts.append(re.sub(r'[<>&]', lambda m: {'<': '&lt;', '>': '&gt;', '&': '&amp;'}[m.group()], line))
            continue

        # Close list if needed
        if in_list and not stripped.startswith('- ') and not stripped.startswith('* ') and not re.match(r'^\d+\.\s', stripped):
            html_parts.append('</ul>' if html_parts[-1] != '</ol>' else '')
            in_list = False

        # Tables
        if '|' in stripped and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if all(re.match(r'^[-:]+$', c) for c in cells):
                continue  # separator row
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(cells)
            continue
        elif in_table:
            # Render table
            html_parts.append(f'<table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px;">')
            for i, row in enumerate(table_rows):
                tag = 'th' if i == 0 else 'td'
                bg = colors['header_bg'] if i == 0 else (colors['bg'] if i % 2 == 0 else '#f9fafb')
                weight = 'font-weight:600;' if i == 0 else ''
                cells_html = ''.join(
                    f'<{tag} style="padding:10px 14px;border:1px solid {colors["border"]};text-align:left;{weight}">{apply_inline(c)}</{tag}>'
                    for c in row
                )
                html_parts.append(f'<tr style="background:{bg}">{cells_html}</tr>')
            html_parts.append('</table>')
            in_table = False
            table_rows = []

        # Headers
        if stripped.startswith('# '):
            text = stripped[2:]
            html_parts.append(f'<h1 style="color:{colors["accent"]};font-size:28px;margin:32px 0 16px;padding-bottom:8px;border-bottom:3px solid {colors["accent"]};">{apply_inline(text)}</h1>')
        elif stripped.startswith('## '):
            text = stripped[3:]
            html_parts.append(f'<h2 style="color:{colors["text"]};font-size:22px;margin:28px 0 12px;padding-bottom:6px;border-bottom:1px solid {colors["border"]};">{apply_inline(text)}</h2>')
        elif stripped.startswith('### '):
            text = stripped[4:]
            html_parts.append(f'<h3 style="color:{colors["text"]};font-size:18px;margin:24px 0 10px;">{apply_inline(text)}</h3>')
        # Unordered list
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                html_parts.append('<ul style="margin:8px 0;padding-left:24px;">')
                in_list = True
            text = stripped[2:]
            html_parts.append(f'<li style="margin:4px 0;line-height:1.6;">{apply_inline(text)}</li>')
        # Ordered list
        elif re.match(r'^\d+\.\s', stripped):
            if not in_list:
                html_parts.append('<ol style="margin:8px 0;padding-left:24px;">')
                in_list = True
            text = re.sub(r'^\d+\.\s', '', stripped)
            html_parts.append(f'<li style="margin:4px 0;line-height:1.6;">{apply_inline(text)}</li>')
        # Horizontal rule
        elif stripped in ('---', '***', '___'):
            html_parts.append(f'<hr style="border:none;border-top:1px solid {colors["border"]};margin:24px 0;">')
        # Empty line
        elif not stripped:
            html_parts.append('')
        # Paragraph
        else:
            html_parts.append(f'<p style="margin:8px 0;line-height:1.7;">{apply_inline(stripped)}</p>')

    # Close any open elements
    if in_list:
        html_parts.append('</ul>')
    if in_table and table_rows:
        html_parts.append(f'<table style="width:100%;border-collapse:collapse;margin:16px 0;">')
        for i, row in enumerate(table_rows):
            tag = 'th' if i == 0 else 'td'
            cells_html = ''.join(f'<{tag} style="padding:10px 14px;border:1px solid {colors["border"]};text-align:left;">{apply_inline(c)}</{tag}>' for c in row)
            html_parts.append(f'<tr>{cells_html}</tr>')
        html_parts.append('</table>')

    body = '\n'.join(html_parts)

    return f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  @media print {{
    body {{ padding: 0; max-width: 100%; }}
  }}
</style>
</head>
<body style="font-family:{colors['font']};color:{colors['text']};background:{colors['bg']};max-width:800px;margin:0 auto;padding:32px 24px;line-height:1.6;">
{body}
<footer style="margin-top:48px;padding-top:16px;border-top:1px solid {colors['border']};font-size:12px;color:#94a3b8;text-align:center;">
Generated by Client Report Generator
</footer>
</body>
</html>'''


def apply_inline(text):
    """Apply inline markdown formatting."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code style="background:#f1f5f9;padding:2px 6px;border-radius:3px;font-size:13px;">\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:#2563eb;">\1</a>', text)
    return text


def main():
    parser = argparse.ArgumentParser(description='Convert Markdown report to styled HTML')
    parser.add_argument('input', help='Input Markdown file')
    parser.add_argument('--template', choices=['default', 'minimal', 'branded'], default='default',
                        help='HTML template style (default: default)')
    parser.add_argument('--output', '-o', help='Output HTML file (default: same name with .html)')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f'Error: File not found: {args.input}', file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html = markdown_to_html(md_content, args.template)

    output_path = args.output or os.path.splitext(args.input)[0] + '.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'HTML report written to {output_path}')


if __name__ == '__main__':
    main()
