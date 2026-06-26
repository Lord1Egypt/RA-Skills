#!/usr/bin/env python3
import argparse
import html
import json
import re
import shutil
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_DIR = SKILL_DIR / 'assets' / 'landingpage-template'


def register_unicode_fonts():
    candidates = [
        ('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
        ('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'),
        ('DejaVuSans-Oblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'),
        ('DejaVuSans-BoldOblique', '/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf'),
    ]
    registered = {}
    for name, path in candidates:
        if Path(path).exists():
            pdfmetrics.registerFont(TTFont(name, path))
            registered[name] = True
    return registered


def fmt_num(value):
    if isinstance(value, float):
        return f'{value:.2f}'
    return str(value)


def parse_model_markdown(path: Path):
    text = path.read_text(encoding='utf-8')
    model_name = path.stem
    header_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if header_match:
        model_name = header_match.group(1).strip()
    pattern = re.compile(
        r'^##\s+(?P<id>[^\n]+?)\s+—\s+(?P<title>[^\n]+)\n\n### Prompt\n(?P<prompt>.*?)\n\n### Answer\n(?P<answer>.*?)(?=\n##\s+|\Z)',
        re.MULTILINE | re.DOTALL,
    )
    questions = []
    for m in pattern.finditer(text):
        questions.append({
            'id': m.group('id').strip(),
            'title': m.group('title').strip(),
            'prompt': m.group('prompt').strip(),
            'answer': m.group('answer').strip(),
        })
    return {'model': model_name, 'questions': questions}


def collect_model_details(run_dir: Path):
    details = {}
    if not run_dir or not run_dir.exists():
        return details
    for md_file in sorted(run_dir.glob('*.md')):
        if md_file.name.lower() in {'summary.md', 'summary-v2.md'}:
            continue
        parsed = parse_model_markdown(md_file)
        details[parsed['model']] = parsed['questions']
        details[md_file.stem] = parsed['questions']
    return details


def render_markdown(score_data, model_details, title='Benchmark Summary', subtitle='Model ranking snapshot'):
    lines = [f'# {title}', '', subtitle, '']
    lines.extend(['## Ranking', ''])
    lines.append('| Rank | Model | Quality | Depth | Cost | Speed | Overall | Time (s) | Tokens |')
    lines.append('| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |')
    for row in score_data['rankings']:
        lines.append(
            f"| {row['rank']} | {row['model']} | {fmt_num(row['quality_score'])} | {fmt_num(row['depth_score'])} | {fmt_num(row['cost_score'])} | {fmt_num(row.get('speed_score', 0))} | {fmt_num(row['overall_score'])} | {fmt_num(row['latency_sec'])} | {row['total_tokens']} |"
        )
    lines.extend(['', '## Cost Table', ''])
    lines.append('| Model | Input Tokens | Output Tokens | Total Tokens | Time (s) | Cost USD | Cost Score |')
    lines.append('| --- | ---: | ---: | ---: | ---: | ---: | ---: |')
    for row in score_data['rankings']:
        lines.append(
            f"| {row['model']} | {row.get('input_tokens', 0)} | {row.get('output_tokens', 0)} | {row['total_tokens']} | {fmt_num(row['latency_sec'])} | {fmt_num(row.get('cost_usd', 0))} | {fmt_num(row.get('cost_score', 0))} |"
        )
    lines.extend(['', '## Executive Summary', '', build_executive_summary_markdown(score_data), ''])
    lines.extend(['## Overall Assessment', '', build_overall_assessment_markdown(score_data), ''])
    lines.extend(['## Recommended Model Selection', '', build_recommendations_markdown(score_data), ''])
    for row in score_data['rankings']:
        questions = model_details.get(row['model']) or model_details.get(row['model'].replace('/', '-').lower()) or []
        if not questions:
            continue
        lines.extend(['', f"## {row['model']} — Answer Details", ''])
        for q in questions:
            lines.extend([
                f"### {q['id']} — {q['title']}",
                '',
                '**Prompt**',
                q['prompt'],
                '',
                '**Answer**',
                q['answer'],
                '',
            ])
    return '\n'.join(lines) + '\n'


def build_summary_cards(score_data):
    if not score_data['rankings']:
        return '<div class="card-grid"><article class="card"><h3>No data</h3><p>No ranking rows were available.</p></article></div>'
    top = score_data['rankings'][0]
    fastest = min(score_data['rankings'], key=lambda x: x.get('latency_sec', 0))
    cheapest = max(score_data['rankings'], key=lambda x: x.get('cost_score', 0))
    return (
        '<div class="card-grid">'
        f'<article class="card"><h3>Top Overall</h3><p><strong>{html.escape(top["model"])}</strong></p><p>Overall {fmt_num(top["overall_score"])} · Quality {fmt_num(top["quality_score"])} · Depth {fmt_num(top["depth_score"])}.</p></article>'
        f'<article class="card"><h3>Fastest</h3><p><strong>{html.escape(fastest["model"])}</strong></p><p>{fmt_num(fastest.get("latency_sec", 0))}s total runtime.</p></article>'
        f'<article class="card"><h3>Most Cost-Efficient</h3><p><strong>{html.escape(cheapest["model"])}</strong></p><p>Cost score {fmt_num(cheapest.get("cost_score", 0))}.</p></article>'
        '</div>'
    )


def build_executive_summary_markdown(score_data):
    if not score_data['rankings']:
        return 'Chưa có dữ liệu để tổng kết.'
    top = score_data['rankings'][0]
    fastest = min(score_data['rankings'], key=lambda x: x.get('latency_sec', 0))
    cheapest = max(score_data['rankings'], key=lambda x: x.get('cost_score', 0))
    return (
        f'- Model đứng đầu tổng thể là **{top["model"]}** với điểm Overall **{fmt_num(top["overall_score"])}**.\n'
        f'- Model có tốc độ xử lý nhanh nhất là **{fastest["model"]}** với tổng thời gian **{fmt_num(fastest.get("latency_sec", 0))} giây**.\n'
        f'- Model có hiệu quả chi phí tốt nhất là **{cheapest["model"]}** với Cost Score **{fmt_num(cheapest.get("cost_score", 0))}**.'
    )


def build_overall_assessment_markdown(score_data):
    if not score_data['rankings']:
        return 'Chưa có dữ liệu để đánh giá.'
    top = score_data['rankings'][0]
    tail = score_data['rankings'][-1]
    return (
        f'- Kết quả benchmark cho thấy **{top["model"]}** đang cân bằng tốt nhất giữa chất lượng đầu ra, độ sâu phân tích và chi phí vận hành.\n'
        f'- Nhóm model ở nửa trên bảng xếp hạng phù hợp hơn cho các tác vụ research, tổng hợp và viết báo cáo hằng ngày.\n'
        f'- Model đứng cuối hiện là **{tail["model"]}**; nên cân nhắc lại độ phù hợp thực tế trước khi đưa vào workflow dùng thường xuyên.'
    )


def build_recommendations_markdown(score_data):
    if not score_data['rankings']:
        return 'Chưa có dữ liệu để khuyến nghị.'
    top = score_data['rankings'][0]
    cheapest = max(score_data['rankings'], key=lambda x: x.get('cost_score', 0))
    fastest = min(score_data['rankings'], key=lambda x: x.get('latency_sec', 0))
    coding = next((r for r in score_data['rankings'] if 'codex' in r['model'].lower()), top)
    return (
        f'- **Phù hợp nhất cho research / báo cáo hằng ngày:** {top["model"]}\n'
        f'- **Phù hợp nhất cho coding / technical task:** {coding["model"]}\n'
        f'- **Lựa chọn tối ưu về chi phí:** {cheapest["model"]}\n'
        f'- **Lựa chọn ưu tiên tốc độ:** {fastest["model"]}'
    )


def build_ranking_table(score_data):
    rows = []
    for row in score_data['rankings']:
        rows.append(
            '<tr>'
            f"<td>{row['rank']}</td>"
            f"<td>{html.escape(row['model'])}</td>"
            f"<td>{fmt_num(row['quality_score'])}</td>"
            f"<td>{fmt_num(row['depth_score'])}</td>"
            f"<td>{fmt_num(row['cost_score'])}</td>"
            f"<td>{fmt_num(row.get('speed_score', 0))}</td>"
            f"<td>{fmt_num(row['overall_score'])}</td>"
            f"<td>{fmt_num(row['latency_sec'])}</td>"
            f"<td>{row['total_tokens']}</td>"
            '</tr>'
        )
    return (
        '<table><thead><tr>'
        '<th>Rank</th><th>Model</th><th>Quality</th><th>Depth</th><th>Cost</th><th>Speed</th><th>Overall</th><th>Time (s)</th><th>Total Tokens</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
    )


def build_cost_table(score_data):
    rows = []
    for row in score_data['rankings']:
        rows.append(
            '<tr>'
            f"<td>{html.escape(row['model'])}</td>"
            f"<td>{row.get('input_tokens', 0)}</td>"
            f"<td>{row.get('output_tokens', 0)}</td>"
            f"<td>{row.get('total_tokens', 0)}</td>"
            f"<td>{fmt_num(row.get('latency_sec', 0))}</td>"
            f"<td>{fmt_num(row.get('cost_usd', 0))}</td>"
            f"<td>{fmt_num(row.get('cost_score', 0))}</td>"
            '</tr>'
        )
    return (
        '<table><thead><tr>'
        '<th>Model</th><th>Input Tokens</th><th>Output Tokens</th><th>Total Tokens</th><th>Time (s)</th><th>Cost USD</th><th>Cost Score</th>'
        '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'
    )


def build_details(score_data):
    items = []
    for row in score_data['rankings']:
        items.append(
            '<article class="detail-card">'
            f'<h3>#{row["rank"]} {html.escape(row["model"])} </h3>'
            '<ul>'
            f'<li>Quality score: {fmt_num(row["quality_score"])} (raw: {fmt_num(row.get("quality_raw", 0))})</li>'
            f'<li>Depth score: {fmt_num(row["depth_score"])} (raw: {fmt_num(row.get("depth_raw", 0))})</li>'
            f'<li>Cost score: {fmt_num(row["cost_score"])} · Raw cost: {fmt_num(row.get("cost_usd", 0))} USD</li>'
            f'<li>Speed score: {fmt_num(row.get("speed_score", 0))} · Runtime: {fmt_num(row.get("latency_sec", 0))}s</li>'
            f'<li>Total tokens: {row.get("total_tokens", 0)}</li>'
            f'<li>Overall score: {fmt_num(row["overall_score"])} </li>'
            '</ul>'
            '</article>'
        )
    return '<div class="details-grid">' + ''.join(items) + '</div>'


def build_answer_sections(score_data, model_details):
    sections = []
    for row in score_data['rankings']:
        questions = model_details.get(row['model']) or model_details.get(row['model'].replace('/', '-').lower()) or []
        if not questions:
            continue
        blocks = [f'<section><h2>Answers — {html.escape(row["model"])} </h2>']
        for q in questions:
            blocks.append(
                '<article class="answer-card">'
                f'<h3>{html.escape(q["id"])} — {html.escape(q["title"])} </h3>'
                '<h4>Prompt</h4>'
                f'<pre>{html.escape(q["prompt"])}</pre>'
                '<h4>Answer</h4>'
                f'<pre>{html.escape(q["answer"])}</pre>'
                '</article>'
            )
        blocks.append('</section>')
        sections.append(''.join(blocks))
    return ''.join(sections)


def render_html_from_template(score_data, model_details, title='Benchmark Report', subtitle='Model ranking snapshot', footer='Generated by benchmark-model-provider'):
    template_path = TEMPLATE_DIR / 'index.html'
    template = template_path.read_text(encoding='utf-8')
    summary_cards = build_summary_cards(score_data)
    ranking_and_summary = build_ranking_table(score_data) + (
        '<section><h2>Cost Table</h2>' + build_cost_table(score_data) + '</section>'
        '<section><h2>Executive Summary</h2><pre>' + html.escape(build_executive_summary_markdown(score_data)) + '</pre></section>'
        '<section><h2>Overall Assessment</h2><pre>' + html.escape(build_overall_assessment_markdown(score_data)) + '</pre></section>'
        '<section><h2>Recommended Model Selection</h2><pre>' + html.escape(build_recommendations_markdown(score_data)) + '</pre></section>'
    )
    replacements = {
        '{{TITLE}}': html.escape(title),
        '{{SUBTITLE}}': html.escape(subtitle),
        '{{SUMMARY_HTML}}': summary_cards,
        '{{RANKING_TABLE_HTML}}': ranking_and_summary,
        '{{DETAILS_HTML}}': build_details(score_data),
        '{{ANSWERS_HTML}}': build_answer_sections(score_data, model_details),
        '{{FOOTER}}': html.escape(footer),
    }
    out = template
    for old, new in replacements.items():
        out = out.replace(old, new)
    return out


def copy_template_assets(html_path: Path):
    for name in ('style.css', 'script.js'):
        src = TEMPLATE_DIR / name
        dst = html_path.parent / name
        shutil.copy2(src, dst)


def build_pdf(score_data, model_details, pdf_path: Path, title: str, subtitle: str, footer: str):
    fonts = register_unicode_fonts()
    base_font = 'DejaVuSans' if fonts.get('DejaVuSans') else 'Helvetica'
    bold_font = 'DejaVuSans-Bold' if fonts.get('DejaVuSans-Bold') else base_font
    italic_font = 'DejaVuSans-Oblique' if fonts.get('DejaVuSans-Oblique') else base_font

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm, topMargin=14 * mm, bottomMargin=14 * mm)
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = base_font
    styles['BodyText'].fontName = base_font
    styles['Italic'].fontName = italic_font
    styles['Heading1'].fontName = bold_font
    styles['Heading2'].fontName = bold_font
    styles['Heading3'].fontName = bold_font
    body = ParagraphStyle('Body', parent=styles['BodyText'], fontName=base_font, fontSize=9.5, leading=13, textColor=colors.black)
    small = ParagraphStyle('Small', parent=body, fontName=base_font, fontSize=8.5, leading=11)
    heading = ParagraphStyle('Heading1Unicode', parent=styles['Heading1'], fontName=bold_font)
    heading2 = ParagraphStyle('Heading2Unicode', parent=styles['Heading2'], fontName=bold_font)
    story = [Paragraph(title, heading), Paragraph(subtitle, styles['Italic']), Spacer(1, 8)]

    table_data = [['Rank', 'Model', 'Quality', 'Depth', 'Cost', 'Speed', 'Overall', 'Time', 'Tokens']]
    for row in score_data['rankings']:
        table_data.append([
            str(row['rank']),
            Paragraph(html.escape(row['model']), small),
            fmt_num(row['quality_score']),
            fmt_num(row['depth_score']),
            fmt_num(row['cost_score']),
            fmt_num(row.get('speed_score', 0)),
            fmt_num(row['overall_score']),
            fmt_num(row['latency_sec']),
            str(row['total_tokens']),
        ])
    table = Table(table_data, repeatRows=1, colWidths=[12 * mm, 46 * mm, 16 * mm, 16 * mm, 16 * mm, 16 * mm, 18 * mm, 16 * mm, 20 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9e2ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#8aa0d6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f7ff')]),
    ]))
    story += [Paragraph('Ranking', heading2), table, Spacer(1, 10)]

    cost_table_data = [['Model', 'Input', 'Output', 'Total', 'Time (s)', 'Cost USD', 'Cost Score']]
    for row in score_data['rankings']:
        cost_table_data.append([
            Paragraph(html.escape(row['model']), small),
            str(row.get('input_tokens', 0)),
            str(row.get('output_tokens', 0)),
            str(row.get('total_tokens', 0)),
            fmt_num(row.get('latency_sec', 0)),
            fmt_num(row.get('cost_usd', 0)),
            fmt_num(row.get('cost_score', 0)),
        ])
    cost_table = Table(cost_table_data, repeatRows=1, colWidths=[48 * mm, 16 * mm, 16 * mm, 18 * mm, 18 * mm, 18 * mm, 18 * mm])
    cost_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ffe7cc')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#d6a36a')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('LEADING', (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fff8ef')]),
    ]))
    story += [
        Paragraph('Cost Table', heading2),
        cost_table,
        Spacer(1, 8),
        Paragraph('Executive Summary', heading2),
        Paragraph(html.escape(build_executive_summary_markdown(score_data)).replace('\n', '<br/>'), body),
        Spacer(1, 6),
        Paragraph('Overall Assessment', heading2),
        Paragraph(html.escape(build_overall_assessment_markdown(score_data)).replace('\n', '<br/>'), body),
        Spacer(1, 6),
        Paragraph('Recommended Model Selection', heading2),
        Paragraph(html.escape(build_recommendations_markdown(score_data)).replace('\n', '<br/>'), body),
        Spacer(1, 10),
    ]

    for row in score_data['rankings']:
        story.append(PageBreak())
        story.append(Paragraph(f"Model Detail — {html.escape(row['model'])}", heading2))
        story.append(Paragraph(
            f"Overall: {fmt_num(row['overall_score'])} | Quality: {fmt_num(row['quality_score'])} | Depth: {fmt_num(row['depth_score'])} | Cost: {fmt_num(row['cost_score'])} | Speed: {fmt_num(row.get('speed_score', 0))}",
            body,
        ))
        story.append(Spacer(1, 8))
        questions = model_details.get(row['model']) or model_details.get(row['model'].replace('/', '-').lower()) or []
        for q in questions:
            story.append(Paragraph(f"{html.escape(q['id'])} — {html.escape(q['title'])}", styles['Heading3']))
            story.append(Paragraph('<b>Prompt</b>', body))
            story.append(Paragraph(html.escape(q['prompt']).replace('\n', '<br/>'), small))
            story.append(Spacer(1, 4))
            story.append(Paragraph('<b>Answer</b>', body))
            story.append(Paragraph(html.escape(q['answer']).replace('\n', '<br/>'), small))
            story.append(Spacer(1, 8))
    story.append(Paragraph(footer, styles['Italic']))
    doc.build(story)


def main():
    ap = argparse.ArgumentParser(description='Build markdown, HTML, and optional PDF benchmark reports')
    ap.add_argument('score_breakdown_file')
    ap.add_argument('--run-dir', help='Run directory containing per-model markdown answer files')
    ap.add_argument('--markdown-out', required=True)
    ap.add_argument('--html-out', required=True)
    ap.add_argument('--pdf-out')
    ap.add_argument('--title', default='Benchmark Report')
    ap.add_argument('--subtitle', default='Model ranking snapshot')
    ap.add_argument('--footer', default='Generated by benchmark-model-provider')
    args = ap.parse_args()

    score_data = json.loads(Path(args.score_breakdown_file).read_text(encoding='utf-8'))
    run_dir = Path(args.run_dir) if args.run_dir else Path(args.score_breakdown_file).parent
    model_details = collect_model_details(run_dir)

    md = render_markdown(score_data, model_details, args.title, args.subtitle)
    html_out = render_html_from_template(score_data, model_details, args.title, args.subtitle, args.footer)

    md_path = Path(args.markdown_out)
    html_path = Path(args.html_out)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(md, encoding='utf-8')
    html_path.write_text(html_out, encoding='utf-8')
    copy_template_assets(html_path)
    print(f'Wrote markdown report to {md_path}')
    print(f'Wrote HTML report to {html_path}')

    if args.pdf_out:
        pdf_path = Path(args.pdf_out)
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        build_pdf(score_data, model_details, pdf_path, args.title, args.subtitle, args.footer)
        print(f'Wrote PDF report to {pdf_path}')


if __name__ == '__main__':
    main()
