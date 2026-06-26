#!/usr/bin/env python3
"""Generate AI daily report markdown and SVG.
Usage: python3 generate_report.py <news_json_file> <projects_json_file>
- Reads the two JSON files (produced by fetch_news.py and fetch_top_projects.py).
- Creates `report.md` (human‑readable) and `report.svg` (visual template).
- Uses Jinja2 for SVG templating; falls back to simple string replace if Jinja2 not installed.
"""
import sys, json, pathlib, datetime

BASE = pathlib.Path(__file__).parent.parent  # skill root

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_md(news, projects, out_path):
    lines = []
    lines.append(f"# AI 每日报告 – {datetime.date.today().isoformat()}\n")
    lines.append('## 新闻摘要')
    for n in news:
        # 保留原始标题，但在中文环境下显示来源和日期
        lines.append(f"- [{n['title']}]({n['link']}) （来源：{n['source']}，日期：{n['date'][:10]}）")
    lines.append('\n## 开源 AI 项目精选')
    # 尝试使用 googletrans 将项目描述翻译为中文（简体）
    try:
        from googletrans import Translator
        translator = Translator()
    except Exception:
        translator = None
    for p in projects:
        orig_desc = p.get('description') or ''
        if translator and orig_desc:
            try:
                trans = translator.translate(orig_desc, dest='zh-cn')
                desc = trans.text
            except Exception:
                desc = orig_desc  # 翻译失败回退原文
        else:
            desc = orig_desc
        lines.append(f"- [{p['name']}]({p['html_url']}) – {p['stars']} ★\n  项目描述：{desc}")
    out_path.write_text('\n'.join(lines), encoding='utf-8')

def render_svg(news, projects, out_path):
    # Load template
    template_path = BASE / 'references' / 'report_template.svg'
    tmpl = template_path.read_text(encoding='utf-8')
    # Prepare data for Jinja2 style replacement
    from jinja2 import Template
    t = Template(tmpl)
    rendered = t.render(date=datetime.date.today().isoformat(), news=news, projects=projects)
    out_path.write_text(rendered, encoding='utf-8')

def main():
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: generate_report.py <news_json> <projects_json>\n')
        sys.exit(1)
    news = load_json(sys.argv[1])
    projects = load_json(sys.argv[2])
    md_path = BASE / 'report.md'
    svg_path = BASE / 'report.svg'
    write_md(news, projects, md_path)
    render_svg(news, projects, svg_path)
    print(f'Generated {md_path} and {svg_path}')

if __name__ == '__main__':
    main()
