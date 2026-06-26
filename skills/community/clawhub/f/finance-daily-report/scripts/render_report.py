#!/usr/bin/env python3
"""
Render Finance Daily Report with smart chunking for Feishu.

- Tables are kept intact (not split across chunks)
- Each chunk ≤4000 chars (OpenClaw textChunkLimit)
- Sources rendered as clickable links: [来源名](URL)
- Output: list of message chunks ready to send

Usage:
    python3 render_report.py /tmp/report_data3.json
"""

import json
import sys
from datetime import datetime

FEISHU_CHUNK_LIMIT = 3800  # Feishu supports ~30K; leave margin from 4000 OpenClaw textChunkLimit


def format_number(val, decimals=2):
    """Format number with thousand separators."""
    if val is None:
        return "N/A"
    try:
        num = float(str(val).replace(',', ''))
        if decimals == 0:
            return f"{int(num):,}"
        return f"{num:,.{decimals}f}"
    except:
        return str(val)


def format_change(change_pct):
    """Format change with ▲/▼ symbol."""
    if change_pct is None:
        return "▬"
    s = str(change_pct).strip()
    if s.startswith('+') or (s[0].isdigit() and '-' not in s):
        return f"▲{s.lstrip('+')}"
    elif s.startswith('-'):
        return f"▼{s}"
    return f"▬{s}"


def render_stocks_table(stocks, max_rows=12):
    """Render stocks as markdown table."""
    lines = [
        "## 核心股市表现",
        "",
        "| 指数 | 收盘价 | 日涨跌 | 月涨跌 | 来源 |",
        "|------|--------|--------|--------|------|"
    ]
    for s in stocks[:max_rows]:
        name = s.get('name', 'N/A')
        price = format_number(s.get('price'), 2 if '6632' in str(s.get('price','')) else 0)
        change = format_change(s.get('change_pct'))
        monthly = s.get('monthly_pct', 'N/A')
        if monthly and str(monthly) != 'None':
            monthly = format_change(monthly)
        else:
            monthly = 'N/A'
        source_url = s.get('source_url', '')
        source_name = source_url.replace('https://tradingeconomics.com/', '').replace('/', ' ').title().strip()
        lines.append(f"| **{name}** | {price} | {change} | {monthly} | [TE]({source_url}) |")
    return "\n".join(lines)


def render_fx_table(fx, max_rows=10):
    """Render FX as markdown table."""
    lines = [
        "## 汇率与美元",
        "",
        "| 货币对 | 价格 | 日涨跌 | 月涨跌 | 来源 |",
        "|------|------|--------|--------|------|"
    ]
    for f in fx[:max_rows]:
        name = f.get('name', 'N/A')
        price = format_number(f.get('price'), 5 if '1.14' in str(f.get('price','')) else 3)
        change = format_change(f.get('change_pct'))
        monthly = f.get('monthly_pct', 'N/A')
        if monthly and str(monthly) != 'None':
            monthly = format_change(monthly)
        else:
            monthly = 'N/A'
        source_url = f.get('source_url', '')
        lines.append(f"| **{name}** | {price} | {change} | {monthly} | [TE]({source_url}) |")
    return "\n".join(lines)


def render_commodities_table(comms, max_rows=10):
    """Render commodities as markdown table."""
    lines = [
        "## 商品与核心资产",
        "",
        "| 品种 | 价格 | 日涨跌 | 月涨跌 | 来源 |",
        "|------|------|--------|--------|------|"
    ]
    for c in comms[:max_rows]:
        name = c.get('name', 'N/A')
        price = c.get('price', 'N/A')
        unit = c.get('unit', '')
        if unit:
            price = f"{price} {unit}"
        change = format_change(c.get('change_pct'))
        monthly = c.get('monthly_pct', 'N/A')
        if monthly and str(monthly) != 'None':
            monthly = format_change(monthly)
        else:
            monthly = 'N/A'
        source_url = c.get('source_url', '')
        lines.append(f"| **{name}** | {price} | {change} | {monthly} | [TE]({source_url}) |")
    return "\n".join(lines)


def render_bonds_table(bonds, max_rows=8):
    """Render bonds as markdown table."""
    lines = [
        "## 全球利率与美债",
        "",
        "| 国家 | 10Y 收益率 | 日变化 | 月变化 | 来源 |",
        "|------|-----------|--------|--------|------|"
    ]
    for b in bonds[:max_rows]:
        country = b.get('country', 'N/A')
        yield_10y = b.get('yield_10y', 'N/A')
        day_change = b.get('day_change', 'N/A')
        if day_change and str(day_change) != 'None':
            day_change = f"{'+' if float(str(day_change).replace('+','').replace('-','')) >= 0 else ''}{day_change}"
        monthly = b.get('monthly_change', 'N/A')
        if monthly and str(monthly) != 'None':
            monthly = format_change(monthly)
        else:
            monthly = 'N/A'
        source_url = b.get('source_url', '')
        lines.append(f"| **{country}** | {yield_10y} | {day_change} | {monthly} | [TE]({source_url}) |")
    return "\n".join(lines)


def render_narrative(narrative):
    """Render narrative section with news items and sources."""
    lines = ["## 市场主线", ""]
    
    main_theme = narrative.get('main_theme', '')
    if main_theme:
        lines.append(main_theme)
        lines.append("")
    
    themes = narrative.get('themes', [])
    if themes:
        lines.append("**核心主题：**")
        for t in themes:
            lines.append(f"• {t}")
        lines.append("")
    
    news = narrative.get('news', [])
    if news:
        lines.append("**重要新闻：**")
        for n in news[:8]:
            text = n.get('text', '')
            source_url = n.get('source_url', '')
            source_name = n.get('source_name', '来源')
            if source_url and source_url != 'N/A':
                # Extract domain name for display
                from urllib.parse import urlparse
                parsed = urlparse(source_url)
                display_name = parsed.netloc.replace('www.', '') if parsed.netloc else source_name
                lines.append(f"• {text} —— [{display_name}]({source_url})")
            else:
                lines.append(f"• {text} —— {source_name}")
        lines.append("")
    
    preview = narrative.get('preview', [])
    if preview:
        lines.append("**明日前瞻：**")
        for p in preview[:5]:
            text = p.get('text', '')
            source_url = p.get('source_url', '')
            if source_url and source_url != 'N/A':
                from urllib.parse import urlparse
                parsed = urlparse(source_url)
                display_name = parsed.netloc.replace('www.', '') if parsed.netloc else '来源'
                lines.append(f"• {text} —— [{display_name}]({source_url})")
            else:
                lines.append(f"• {text}")
    
    return "\n".join(lines)


def chunk_messages(content_list, chunk_limit=FEISHU_CHUNK_LIMIT):
    """
    Chunk content intelligently:
    - Tables are kept intact (not split)
    - If a table won't fit in current chunk, start it in a new chunk
    """
    chunks = []
    current_chunk = ""
    
    for content in content_list:
        content = content.strip()
        content_len = len(content)
        
        # If content is a table (contains |---| pattern), keep it intact
        is_table = "|---" in content or "|------" in content
        
        if not current_chunk:
            current_chunk = content
        elif is_table:
            # Table: check if it fits
            if len(current_chunk) + len(content) + 2 <= chunk_limit:
                current_chunk += "\n\n" + content
            else:
                # Start table in new chunk
                chunks.append(current_chunk)
                current_chunk = content
        else:
            # Regular text: try to append
            if len(current_chunk) + len(content) + 2 <= chunk_limit:
                current_chunk += "\n\n" + content
            else:
                chunks.append(current_chunk)
                current_chunk = content
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


def render_full_report(data):
    """Render complete report as list of sections."""
    sections = []
    
    modules = data.get('modules', {})
    
    # Header / Summary
    stocks = modules.get('stocks', {}).get('stocks', [])
    fx = modules.get('fx', {}).get('fx', [])
    comms = modules.get('commodities', {}).get('commodities', [])
    
    # Find key data points
    sp500 = next((s for s in stocks if '标普' in s.get('name', '')), {})
    wti = next((c for c in comms if 'WTI' in c.get('name', '')), {})
    gold = next((c for c in comms if '黄金' in c.get('name', '')), {})
    dxy = next((f for f in fx if 'DXY' in f.get('name', '')), {})
    
    summary_lines = [
        f"# 全球财经日报 | {data.get('date', 'N/A')}",
        "",
        f"> 数据日期：{data.get('date', 'N/A')}（T-1 交易日）",
        "",
        "## 核心速览",
        "",
    ]
    
    # Build summary bullets
    if modules.get('narrative', {}).get('narrative', {}).get('themes'):
        themes = modules['narrative']['narrative']['themes']
        summary_lines.append(f"• **主线**：{themes[0] if themes else '市场动态'}")
    
    if sp500:
        summary_lines.append(f"• **美股**：标普 {sp500.get('change_pct', 'N/A')} | 道指 {next((s.get('change_pct') for s in stocks if '道琼' in s.get('name','')), 'N/A')}")
    
    if wti:
        summary_lines.append(f"• **原油**：WTI ${wti.get('price', 'N/A')} ({wti.get('change_pct', 'N/A')})")
    
    if gold:
        summary_lines.append(f"• **黄金**：${gold.get('price', 'N/A')} ({gold.get('change_pct', 'N/A')})")
    
    if dxy:
        summary_lines.append(f"• **美元**：DXY {dxy.get('price', 'N/A')} ({dxy.get('change_pct', 'N/A')})")
    
    summary_lines.append("")
    summary_lines.append("---")
    
    sections.append("\n".join(summary_lines))
    
    # Narrative
    if modules.get('narrative', {}).get('narrative'):
        sections.append(render_narrative(modules['narrative']['narrative']))
    
    # Stocks table
    if stocks:
        sections.append(render_stocks_table(stocks))
    
    # FX table
    if fx:
        sections.append(render_fx_table(fx))
    
    # Bonds table
    if modules.get('bonds', {}).get('bonds'):
        sections.append(render_bonds_table(modules['bonds']['bonds']))
    
    # Commodities table
    if comms:
        sections.append(render_commodities_table(comms))
    
    # Footer
    footer = [
        "---",
        f"*数据来源：Trading Economics, 金十数据，财联社 | 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"*采集模型：{data.get('collector_model', 'N/A')} | 总 Token：{data.get('total_tokens', 'N/A')}*"
    ]
    sections.append("\n".join(footer))
    
    return sections


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 render_report.py <report_data.json>", file=sys.stderr)
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        data = json.load(f)
    
    sections = render_full_report(data)
    chunks = chunk_messages(sections)
    
    # Output as JSON array of chunks
    output = {
        "date": data.get('date'),
        "chunk_count": len(chunks),
        "chunks": chunks
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # Also print stats to stderr
    print(f"\nRendered {len(chunks)} chunks:", file=sys.stderr)
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk)} chars", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main() or 0)
