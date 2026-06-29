#!/usr/bin/env python3
"""
Code Review Report Generator (Bilingual: Chinese / English)

Reads findings from JSON (stdin or file) and generates an HTML report
with optional language toggle (zh / en / both).

Usage:
    # Default: bilingual report with toggle
    python generate_report.py findings.json --project "My Project"

    # Chinese only
    python generate_report.py findings.json --lang zh

    # English only
    python generate_report.py findings.json --lang en

    # From pipe
    python scan_patterns.py ./src --format json | python generate_report.py -
"""

import argparse
import datetime
import json
import os
import sys
from pathlib import Path


# ─── i18n strings ─────────────────────────────────────────────────────────────

I18N = {
    'en': {
        'title': 'Code Review Report',
        'generated': 'Generated',
        'category_summary': 'Category Summary',
        'category': 'Category',
        'critical': 'Critical',
        'high': 'High',
        'medium': 'Medium',
        'low': 'Low',
        'info': 'Info',
        'total': 'Total',
        'findings': 'Findings',
        'all': 'All',
        'no_results': 'No findings match the current filter',
        'no_description': 'No description',
        'file': 'File',
        'type': 'Type',
        'no_findings': 'No findings to report.',
        'report_generated': 'Report generated',
        'total_findings': 'Total findings',
        'toggle_to_zh': '中文',
        'toggle_to_en': 'EN',
        'summary_text': '<strong>{total}</strong> findings across <strong>{files}</strong> file(s). '
                        '<strong>{critical}</strong> critical, <strong>{high}</strong> high, '
                        '<strong>{medium}</strong> medium, <strong>{low}</strong> low.',
    },
    'zh': {
        'title': '代码审核报告',
        'generated': '生成时间',
        'category_summary': '分类汇总',
        'category': '分类',
        'critical': '严重',
        'high': '高危',
        'medium': '中危',
        'low': '低危',
        'info': '提示',
        'total': '合计',
        'findings': '问题列表',
        'all': '全部',
        'no_results': '没有匹配当前筛选条件的问题',
        'no_description': '无描述',
        'file': '文件',
        'type': '类型',
        'no_findings': '没有可报告的问题。',
        'report_generated': '报告已生成',
        'total_findings': '问题总数',
        'toggle_to_zh': '中文',
        'toggle_to_en': 'EN',
        'summary_text': '共发现 <strong>{total}</strong> 个问题，涉及 <strong>{files}</strong> 个文件。'
                        '严重 <strong>{critical}</strong> 个，高危 <strong>{high}</strong> 个，'
                        '中危 <strong>{medium}</strong> 个，低危 <strong>{low}</strong> 个。',
    },
}


def get_text(lang, key, **kwargs):
    """Get localized text, with English fallback."""
    text = I18N.get(lang, I18N['en']).get(key, I18N['en'].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text


# ─── Findings loading ─────────────────────────────────────────────────────────

def load_findings(sources):
    """Load findings from one or more JSON sources (files or stdin)."""
    all_findings = []
    for source in sources:
        if source == '-':
            data = json.load(sys.stdin)
        elif os.path.exists(source):
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            try:
                data = json.loads(source)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse '{source}', skipping", file=sys.stderr)
                continue
        if isinstance(data, list):
            all_findings.extend(data)
        elif isinstance(data, dict) and 'findings' in data:
            all_findings.extend(data['findings'])
    return all_findings


def deduplicate(findings):
    """Remove duplicate findings (same file, line, type)."""
    seen = set()
    unique = []
    for f in findings:
        key = (f.get('file', ''), f.get('line', 0), f.get('type', ''), f.get('message', ''))
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return unique


def generate_stats(findings):
    """Generate summary statistics."""
    stats = {
        'total': len(findings),
        'critical': 0,
        'high': 0,
        'medium': 0,
        'low': 0,
        'info': 0,
        'files': set(),
        'categories': {},
    }

    for f in findings:
        sev = f.get('severity', 'Low').lower()
        if sev in stats:
            stats[sev] += 1

        if f.get('file'):
            stats['files'].add(f['file'])

        cat = f.get('category', 'General')
        if cat not in stats['categories']:
            stats['categories'][cat] = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0, 'total': 0}
        stats['categories'][cat][sev] = stats['categories'][cat].get(sev, 0) + 1
        stats['categories'][cat]['total'] += 1

    stats['files'] = len(stats['files'])
    return stats


# ─── HTML generation ──────────────────────────────────────────────────────────

SEVERITY_COLORS = {
    'critical': '#dc2626',
    'high': '#ea580c',
    'medium': '#ca8a04',
    'low': '#2563eb',
    'info': '#6b7280',
}


def build_stats_cards(stats, lang):
    """Build the severity summary cards HTML."""
    cards = ''
    for sev_key, sev_label_key in [('critical', 'critical'), ('high', 'high'),
                                    ('medium', 'medium'), ('low', 'low'), ('info', 'info')]:
        count = stats[sev_key]
        color = SEVERITY_COLORS[sev_key]
        label = get_text(lang, sev_label_key)
        cards += f'''
        <div class="stat-card" style="border-top: 3px solid {color};">
            <div class="stat-number" style="color: {color};">{count}</div>
            <div class="stat-label" data-i18n="{sev_label_key}">{label}</div>
        </div>'''
    return cards


def build_category_table(stats, lang):
    """Build the category breakdown table rows."""
    rows = ''
    for cat, data in sorted(stats['categories'].items(), key=lambda x: -x[1]['total']):
        rows += f'''
        <tr>
            <td class="cat-name">{cat}</td>
            <td class="center"><span class="badge" style="background:#dc2626;">{data.get('critical', 0)}</span></td>
            <td class="center"><span class="badge" style="background:#ea580c;">{data.get('high', 0)}</span></td>
            <td class="center"><span class="badge" style="background:#ca8a04;">{data.get('medium', 0)}</span></td>
            <td class="center"><span class="badge" style="background:#2563eb;">{data.get('low', 0)}</span></td>
            <td class="center"><strong>{data['total']}</strong></td>
        </tr>'''
    return rows


def build_filter_buttons(stats, lang):
    """Build the severity filter buttons."""
    buttons = ''
    for sev_key, sev_label_key, count_key in [
        ('all', 'all', 'total'),
        ('Critical', 'critical', 'critical'),
        ('High', 'high', 'high'),
        ('Medium', 'medium', 'medium'),
        ('Low', 'low', 'low'),
    ]:
        label = get_text(lang, sev_label_key)
        count = stats[count_key]
        active = 'active' if sev_key == 'all' else ''
        buttons += f'<button class="filter-btn {active}" data-sev="{sev_key}" data-i18n="{sev_label_key}">{label} ({count})</button>'
    return buttons


def generate_html_report(findings, stats, project_name='Code Review', lang='both'):
    """Generate a self-contained HTML report with optional bilingual toggle.

    Args:
        findings: list of finding dicts
        stats: stats dict from generate_stats()
        project_name: project name shown in header
        lang: 'zh', 'en', or 'both' (default: 'both')
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    findings_json = json.dumps(findings, ensure_ascii=False)

    # Determine which languages to include
    include_zh = lang in ('zh', 'both')
    include_en = lang in ('en', 'both')
    show_toggle = lang == 'both'
    default_lang = 'zh' if include_zh else 'en'

    # Build i18n data for client-side switching
    i18n_json = json.dumps(I18N, ensure_ascii=False)

    # Build content for default language
    stats_cards = build_stats_cards(stats, default_lang)
    category_rows = build_category_table(stats, lang=default_lang)
    filter_buttons = build_filter_buttons(stats, default_lang)

    title_text = get_text(default_lang, 'title')
    generated_text = get_text(default_lang, 'generated')
    cat_summary_text = get_text(default_lang, 'category_summary')
    findings_text = get_text(default_lang, 'findings')
    no_results_text = get_text(default_lang, 'no_results')
    summary_html = get_text(default_lang, 'summary_text',
                            total=stats['total'], files=stats['files'],
                            critical=stats['critical'], high=stats['high'],
                            medium=stats['medium'], low=stats['low'])

    # Table header labels (with data-i18n attributes for switching)
    th_category = get_text(default_lang, 'category')
    th_critical = get_text(default_lang, 'critical')
    th_high = get_text(default_lang, 'high')
    th_medium = get_text(default_lang, 'medium')
    th_low = get_text(default_lang, 'low')
    th_total = get_text(default_lang, 'total')

    # Toggle button HTML
    toggle_html = ''
    if show_toggle:
        toggle_html = f'''
        <button class="lang-toggle" id="langToggle" onclick="toggleLang()">
            <span class="lang-current" id="langCurrent">{get_text(default_lang, 'toggle_to_en') if default_lang == 'zh' else get_text(default_lang, 'toggle_to_zh')}</span>
        </button>'''

    html = f'''<!DOCTYPE html>
<html lang="{'zh-CN' if default_lang == 'zh' else 'en'}" data-lang="{default_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - {project_name}</title>
    <style>
        :root {{
            --bg: #0d1117;
            --card-bg: #161b22;
            --border: #30363d;
            --text: #e6edf3;
            --text-muted: #8b949e;
            --link: #58a6ff;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 32px;
            padding: 24px;
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            position: relative;
        }}
        .header h1 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .header .meta {{
            color: var(--text-muted);
            font-size: 14px;
        }}
        .lang-toggle {{
            position: absolute;
            top: 20px;
            right: 20px;
            padding: 6px 16px;
            border-radius: 20px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--text);
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .lang-toggle:hover {{
            border-color: var(--link);
            color: var(--link);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            margin-bottom: 32px;
        }}
        .stat-card {{
            background: var(--card-bg);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            border: 1px solid var(--border);
        }}
        .stat-number {{
            font-size: 36px;
            font-weight: 800;
            line-height: 1;
        }}
        .stat-label {{
            color: var(--text-muted);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 6px;
        }}
        .section {{
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border);
            margin-bottom: 24px;
            overflow: hidden;
        }}
        .section-header {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            font-size: 18px;
            font-weight: 600;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .section-body {{ padding: 0; }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 10px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }}
        th {{
            color: var(--text-muted);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        .center {{ text-align: center; }}
        .cat-name {{ font-weight: 600; }}
        .badge {{
            display: inline-block;
            min-width: 28px;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
            color: #fff;
        }}
        .filters {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        .filter-btn {{
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid var(--border);
            background: var(--card-bg);
            color: var(--text);
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }}
        .filter-btn:hover {{ border-color: var(--link); }}
        .filter-btn.active {{
            background: var(--link);
            border-color: var(--link);
            color: #fff;
        }}
        .finding-item {{
            padding: 14px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            gap: 12px;
            align-items: start;
        }}
        .finding-item:last-child {{ border-bottom: none; }}
        .severity-tag {{
            display: inline-block;
            padding: 2px 10px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            min-width: 70px;
            text-align: center;
        }}
        .sev-critical {{ background: #dc2626; color: #fff; }}
        .sev-high {{ background: #ea580c; color: #fff; }}
        .sev-medium {{ background: #ca8a04; color: #fff; }}
        .sev-low {{ background: #2563eb; color: #fff; }}
        .sev-info {{ background: #6b7280; color: #fff; }}
        .finding-content {{ flex: 1; min-width: 0; }}
        .finding-message {{ font-weight: 600; margin-bottom: 4px; }}
        .finding-meta {{
            color: var(--text-muted);
            font-size: 12px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .finding-meta a {{ color: var(--link); text-decoration: none; }}
        .finding-snippet {{
            margin-top: 6px;
            padding: 8px 12px;
            background: #1c2128;
            border-radius: 6px;
            font-family: 'SFMono-Regular', Consolas, monospace;
            font-size: 12px;
            color: #f0883e;
            overflow-x: auto;
        }}
        .empty {{
            padding: 40px;
            text-align: center;
            color: var(--text-muted);
        }}
        .summary-box {{
            padding: 20px;
            color: var(--text-muted);
            font-size: 14px;
        }}
        .summary-box strong {{ color: var(--text); }}
    </style>
</head>
<body>
    <div class="header">
        {toggle_html}
        <h1 data-i18n="title">{title_text}</h1>
        <div class="meta">{project_name} &middot; <span data-i18n="generated">{generated_text}</span> {now}</div>
    </div>

    <div class="stats-grid">
        {stats_cards}
    </div>

    <div class="section">
        <div class="section-header" data-i18n="category_summary">{cat_summary_text}</div>
        <div class="summary-box" id="summaryBox">{summary_html}</div>
        <table>
            <thead>
                <tr>
                    <th data-i18n="category">{th_category}</th>
                    <th class="center" data-i18n="critical">{th_critical}</th>
                    <th class="center" data-i18n="high">{th_high}</th>
                    <th class="center" data-i18n="medium">{th_medium}</th>
                    <th class="center" data-i18n="low">{th_low}</th>
                    <th class="center" data-i18n="total">{th_total}</th>
                </tr>
            </thead>
            <tbody>
                {category_rows}
            </tbody>
        </table>
    </div>

    <div class="section">
        <div class="section-header">
            <span data-i18n="findings">{findings_text}</span>
            <div class="filters">
                {filter_buttons}
            </div>
        </div>
        <div class="section-body" id="findings-list">
            <div class="empty" id="no-results" style="display:none;" data-i18n="no_results">{no_results_text}</div>
        </div>
    </div>

    <script>
        const findings = {findings_json};
        const i18nData = {i18n_json};
        let currentLang = '{default_lang}';
        const showToggle = {str(show_toggle).lower()};

        const sevClass = {{
            'Critical': 'sev-critical',
            'High': 'sev-high',
            'Medium': 'sev-medium',
            'Low': 'sev-low',
            'Info': 'sev-info'
        }};

        const sevOrder = {{'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3, 'Info': 4}};

        // Severity label mapping for display in finding items
        function sevLabel(sev) {{
            const key = (sev || 'Low').toLowerCase();
            return i18nData[currentLang][key] || sev;
        }}

        function t(key) {{
            return i18nData[currentLang][key] || i18nData['en'][key] || key;
        }}

        function applyI18n() {{
            document.querySelectorAll('[data-i18n]').forEach(el => {{
                const key = el.getAttribute('data-i18n');
                el.textContent = t(key);
            }});
            // Update summary box
            const stats = window.__stats;
            document.getElementById('summaryBox').innerHTML = i18nData[currentLang]['summary_text']
                .replace('{{total}}', stats.total)
                .replace('{{files}}', stats.files)
                .replace('{{critical}}', stats.critical)
                .replace('{{high}}', stats.high)
                .replace('{{medium}}', stats.medium)
                .replace('{{low}}', stats.low);
            // Update filter button labels
            const filterMap = [
                ['all', 'total'],
                ['Critical', 'critical'],
                ['High', 'high'],
                ['Medium', 'medium'],
                ['Low', 'low']
            ];
            document.querySelectorAll('.filter-btn').forEach((btn, i) => {{
                const [sevKey, countKey] = filterMap[i];
                const labelKey = sevKey === 'all' ? 'all' : sevKey.toLowerCase();
                btn.textContent = t(labelKey) + ' (' + window.__stats[countKey] + ')';
            }});
            // Update toggle button
            if (showToggle) {{
                const toggle = document.getElementById('langCurrent');
                toggle.textContent = currentLang === 'zh' ? t('toggle_to_en') : t('toggle_to_zh');
            }}
        }}

        function toggleLang() {{
            currentLang = currentLang === 'zh' ? 'en' : 'zh';
            document.documentElement.setAttribute('data-lang', currentLang);
            document.documentElement.setAttribute('lang', currentLang === 'zh' ? 'zh-CN' : 'en');
            applyI18n();
            // Re-render findings with new labels
            const activeFilter = document.querySelector('.filter-btn.active');
            renderFindings(activeFilter ? activeFilter.dataset.sev : 'all');
        }}

        function renderFindings(filter) {{
            const list = document.getElementById('findings-list');
            const noResults = document.getElementById('no-results');

            list.querySelectorAll('.finding-item').forEach(el => el.remove());

            let filtered = filter === 'all'
                ? findings
                : findings.filter(f => f.severity === filter);

            filtered.sort((a, b) => (sevOrder[a.severity] ?? 9) - (sevOrder[b.severity] ?? 9));

            if (filtered.length === 0) {{
                noResults.style.display = 'block';
                return;
            }}
            noResults.style.display = 'none';

            filtered.forEach(f => {{
                const div = document.createElement('div');
                div.className = 'finding-item';
                const sev = f.severity || 'Low';
                const sevTag = '<span class="severity-tag ' + (sevClass[sev] || 'sev-info') + '">' + sevLabel(sev) + '</span>';

                let metaParts = [];
                let fileIcon = '\U0001F4C4 ';
                let tagIcon = '\U0001F3F7\uFE0F ';
                let toolIcon = '\U0001F527 ';
                if (f.file) metaParts.push(fileIcon + f.file + (f.line ? ':' + f.line : ''));
                if (f.category) metaParts.push(tagIcon + f.category);
                if (f.type) metaParts.push(toolIcon + f.type);

                let snippet = '';
                if (f.snippet) {{
                    snippet = '<div class="finding-snippet">' + escapeHtml(f.snippet) + '</div>';
                }}

                const noDesc = t('no_description');
                div.innerHTML =
                    sevTag +
                    '<div class="finding-content">' +
                        '<div class="finding-message">' + escapeHtml(f.message || noDesc) + '</div>' +
                        '<div class="finding-meta">' + metaParts.join(' &nbsp;|&nbsp; ') + '</div>' +
                        snippet +
                    '</div>';
                list.appendChild(div);
            }});
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderFindings(btn.dataset.sev);
            }});
        }});

        // Store stats for i18n re-rendering
        window.__stats = {{
            total: {stats['total']},
            critical: {stats['critical']},
            high: {stats['high']},
            medium: {stats['medium']},
            low: {stats['low']},
            info: {stats['info']},
            files: {stats['files']}
        }};

        // Initial render
        renderFindings('all');
    </script>
</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description='Generate HTML code review report (bilingual)')
    parser.add_argument('sources', nargs='+', help='JSON file(s) or "-" for stdin')
    parser.add_argument('--project', default='Code Review', help='Project name for the report')
    parser.add_argument('--output', '-o', default=None, help='Output file (default: code-review-report.html)')
    parser.add_argument('--lang', default='both', choices=['zh', 'en', 'both'],
                        help='Report language: zh (Chinese), en (English), or both (bilingual with toggle, default)')
    args = parser.parse_args()

    findings = load_findings(args.sources)
    findings = deduplicate(findings)

    if not findings:
        print("No findings to report.", file=sys.stderr)

    stats = generate_stats(findings)
    html = generate_html_report(findings, stats, args.project, args.lang)

    output_path = args.output or 'code-review-report.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Report generated: {output_path}", file=sys.stderr)
    print(f"  Language: {args.lang}", file=sys.stderr)
    print(f"  Total findings: {stats['total']}", file=sys.stderr)
    print(f"  Critical: {stats['critical']} | High: {stats['high']} | Medium: {stats['medium']} | Low: {stats['low']}", file=sys.stderr)


if __name__ == '__main__':
    main()
