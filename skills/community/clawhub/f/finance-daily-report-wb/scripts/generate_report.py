#!/usr/bin/env python3
"""
财经日报生成器 (Finance Daily Report Generator) v2.1
使用 AKShare (Sina/THS sources) 获取实时金融数据，生成交互式 HTML 可视化日报。

Usage:
    python generate_report.py [--output <path>] [--date YYYY-MM-DD]
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# ── Retry wrapper ──────────────────────────────────────────────────────

def retry_fetch(func, name, max_retries=2, delay=1.0):
    """Execute a data fetch with retries for transient connection errors."""
    last_error = None
    for attempt in range(max_retries):
        try:
            result = func()
            if result is not None and hasattr(result, '__len__') and len(result) == 0:
                print(f"  ! {name}: empty data (attempt {attempt+1}/{max_retries})", file=sys.stderr)
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                return None
            return result
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:
                print(f"  R {name}: retry {attempt+2}/{max_retries}...", file=sys.stderr)
                time.sleep(delay)
            else:
                print(f"  X {name}: {type(e).__name__}: {e}", file=sys.stderr)
    return None


# ── Data fetching functions ────────────────────────────────────────────

def fetch_index_data():
    """Fetch A-share index spot data via Sina (more reliable in China)."""
    import akshare as ak

    def _fetch():
        df = ak.stock_zh_index_spot_sina()
        targets = {
            'sh000001': '上证指数',
            'sz399001': '深证成指',
            'sz399006': '创业板指',
            'sh000688': '科创50',
        }
        results = []
        for code, name in targets.items():
            row = df[df['代码'] == code]
            if not row.empty:
                r = row.iloc[0]
                results.append({
                    'name': name, 'code': code,
                    'price': _sf(r.get('最新价', 0)),
                    'change_pct': _sf(r.get('涨跌幅', 0)),
                    'change_amt': _sf(r.get('涨跌额', 0)),
                })
        return results if results else None
    return retry_fetch(_fetch, 'A-share index')


def fetch_hk_index_data():
    """Fetch Hong Kong index data via Sina."""
    import akshare as ak

    def _fetch():
        df = ak.stock_hk_index_spot_sina()
        targets = ['恒生指数', '恒生科技指数']
        results = []
        for name in targets:
            row = df[df['名称'] == name]
            if not row.empty:
                r = row.iloc[0]
                results.append({
                    'name': name,
                    'price': _sf(r.get('最新价', 0)),
                    'change_pct': _sf(r.get('涨跌幅', 0)),
                    'change_amt': _sf(r.get('涨跌额', 0)),
                })
        return results if results else None
    return retry_fetch(_fetch, 'HK index')


def fetch_sector_data():
    """Fetch industry sector rankings via THS (TongHuaShun)."""
    import akshare as ak

    def _fetch():
        df = ak.stock_board_industry_summary_ths()
        df_sorted = df.sort_values('涨跌幅', ascending=False)

        top_gainers = []
        for _, r in df_sorted.head(5).iterrows():
            top_gainers.append({
                'name': str(r['板块']),
                'change_pct': _sf(r['涨跌幅']),
                'lead_stock': str(r.get('领涨股', '')),
                'lead_change': _sf(r.get('领涨股-涨跌幅', 0)),
                'up_count': int(r.get('上涨家数', 0) or 0),
                'down_count': int(r.get('下跌家数', 0) or 0),
            })

        top_losers = []
        for _, r in df_sorted.tail(5).iterrows():
            top_losers.append({
                'name': str(r['板块']),
                'change_pct': _sf(r['涨跌幅']),
                'lead_stock': str(r.get('领涨股', '')),
                'lead_change': _sf(r.get('领涨股-涨跌幅', 0)),
                'up_count': int(r.get('上涨家数', 0) or 0),
                'down_count': int(r.get('下跌家数', 0) or 0),
            })

        return {'gainers': top_gainers, 'losers': list(reversed(top_losers))}
    return retry_fetch(_fetch, 'Industry sector')


def fetch_north_flow():
    """Fetch north-bound capital flow data."""
    import akshare as ak

    def _fetch():
        df = ak.stock_hsgt_hist_em(symbol='沪股通')
        latest = df.iloc[-1]
        today_flow = _sf(latest.get('当日成交净买额', 0))

        recent = df.tail(5)
        flow_list = []
        for _, r in recent.iterrows():
            val = _sf(r.get('当日成交净买额', 0))
            date_str = str(r.get('日期', ''))
            flow_list.append({'date': date_str, 'value': round(val, 2)})

        return {'today_net_flow': round(today_flow, 2), 'recent_flows': flow_list}
    return retry_fetch(_fetch, 'North-bound flow')


def fetch_market_turnover():
    """Fetch total market turnover from A-share spot data."""
    import akshare as ak

    def _fetch():
        try:
            df = ak.stock_zh_index_spot_sina()
            # Sum 成交额 for sh000001 (SSE) and sz399001 (SZSE) as approximation
            sse = df[df['代码'] == 'sh000001']
            szse = df[df['代码'] == 'sz399001']
            if not sse.empty and not szse.empty:
                total = (_sf(sse.iloc[0].get('成交额', 0)) + _sf(szse.iloc[0].get('成交额', 0))) / 1e8
                return round(total, 2)
            # Fallback: use total from any available index
            total_amt = df['成交额'].apply(_sf).sum() / 1e8
            return round(total_amt, 2) if total_amt > 0 else None
        except Exception:
            return None
    return retry_fetch(_fetch, 'Turnover')


def fetch_forex():
    """Fetch forex data (USD/CNY, EUR/CNY)."""
    import akshare as ak

    def _fetch():
        df = ak.fx_spot_quote()
        results = []
        for _, r in df.iterrows():
            pair = str(r.get('货币对', ''))
            if 'USD/CNY' in pair:
                results.append({
                    'name': '美元/人民币 (USD/CNY)',
                    'price': _sf(r.get('买报价', 0)),
                    'change_pct': 0.0,
                })
            if 'EUR/CNY' in pair:
                results.append({
                    'name': '欧元/人民币 (EUR/CNY)',
                    'price': _sf(r.get('买报价', 0)),
                    'change_pct': 0.0,
                })
        return results if results else None
    return retry_fetch(_fetch, 'Forex')


def fetch_commodities():
    """Fetch global commodity prices (gold, crude oil)."""
    import akshare as ak

    def _fetch():
        df = ak.futures_global_spot_em()
        results = []
        for _, r in df.iterrows():
            name = str(r.get('名称', ''))
            price = _sf(r.get('最新价', 0))
            if price <= 0:
                continue
            if ('黄金' in name or 'XAU' in name) and not any('黄金' in x['name'] for x in results):
                results.append({
                    'name': name,
                    'price': price,
                    'change_pct': _sf(r.get('涨跌幅', 0)),
                })
            if ('原油' in name or 'WTI' in name or '布伦特' in name) and len(results) < 2:
                if not any('原油' in x['name'] for x in results):
                    results.append({
                        'name': name,
                        'price': price,
                        'change_pct': _sf(r.get('涨跌幅', 0)),
                    })
        return results if results else None
    return retry_fetch(_fetch, 'Commodities')


def fetch_news():
    """Fetch latest financial news headlines from East Money."""
    import akshare as ak

    def _fetch():
        df = ak.stock_news_em()
        news_list = []
        for _, r in df.head(10).iterrows():
            title = str(r.get('新闻标题', ''))
            if title and title != 'nan':
                news_list.append({
                    'title': title,
                    'time': str(r.get('发布时间', '')),
                })
        return news_list if news_list else None
    return retry_fetch(_fetch, 'Financial news')


def fetch_calendar():
    """Fiscal calendar notes."""
    return [{'date': '持续关注', 'event': '央行公开市场操作、LPR报价窗口、上市公司业绩预告'}]


# ── Helpers ────────────────────────────────────────────────────────────

def _sf(val):
    """Safely convert value to float, handling None/NaN/strings."""
    try:
        if val is None:
            return 0.0
        if isinstance(val, str) and val.strip() in ('', '-', '--', 'nan'):
            return 0.0
        return float(val)
    except (ValueError, TypeError):
        return 0.0


# ── HTML Generation ────────────────────────────────────────────────────

def generate_html(report_data, report_date):
    """Generate complete interactive HTML report."""
    data_json = json.dumps(report_data, ensure_ascii=False, default=str)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>财经日报 — {report_date}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
* {{ margin:0;padding:0;box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:#f5f6fa;color:#2c3e50;line-height:1.6; }}
.container {{ max-width:960px;margin:0 auto;padding:20px; }}
.header {{ background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);color:white;padding:40px 30px;border-radius:16px;margin-bottom:24px;text-align:center; }}
.header h1 {{ font-size:2em;margin-bottom:8px; }}
.header .date {{ color:#a0aec0;font-size:1em; }}
.header .disclaimer {{ color:#718096;font-size:0.75em;margin-top:12px; }}
.card {{ background:white;border-radius:12px;padding:24px;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.06); }}
.card h2 {{ font-size:1.3em;margin-bottom:16px;padding-bottom:10px;border-bottom:2px solid #edf2f7;display:flex;align-items:center;gap:8px; }}
.index-grid {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px; }}
.index-item {{ background:#f7fafc;border-radius:10px;padding:16px;text-align:center;border:1px solid #e2e8f0;transition:transform .2s; }}
.index-item:hover {{ transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.1); }}
.index-item .idx-name {{ font-size:0.85em;color:#718096;margin-bottom:4px; }}
.index-item .idx-price {{ font-size:1.4em;font-weight:700;margin-bottom:4px; }}
.index-item .idx-change {{ font-size:0.95em;font-weight:600; }}
.sector-table {{ width:100%;border-collapse:collapse;font-size:0.9em; }}
.sector-table th {{ background:#f7fafc;padding:10px 12px;text-align:left;font-weight:600;color:#4a5568;border-bottom:2px solid #e2e8f0; }}
.sector-table td {{ padding:10px 12px;border-bottom:1px solid #edf2f7; }}
.sector-table tr:hover td {{ background:#f7fafc; }}
.section-subtitle {{ font-size:1em;color:#718096;margin:16px 0 8px; }}
.flow-row {{ display:flex;gap:16px;flex-wrap:wrap; }}
.flow-card {{ flex:1;min-width:200px;background:#f7fafc;border-radius:10px;padding:16px;text-align:center;border:1px solid #e2e8f0; }}
.flow-card .flow-label {{ font-size:0.85em;color:#718096;margin-bottom:4px; }}
.flow-card .flow-value {{ font-size:1.5em;font-weight:700; }}
.comm-grid {{ display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px; }}
.comm-item {{ background:#f7fafc;border-radius:10px;padding:16px;text-align:center;border:1px solid #e2e8f0; }}
.comm-item .comm-name {{ font-size:0.85em;color:#718096;margin-bottom:4px; }}
.comm-item .comm-price {{ font-size:1.3em;font-weight:700;margin-bottom:4px; }}
.comm-item .comm-change {{ font-size:0.95em;font-weight:600; }}
.news-list {{ list-style:none; }}
.news-list li {{ padding:10px 0;border-bottom:1px solid #edf2f7;display:flex;gap:12px;align-items:flex-start; }}
.news-list li:last-child {{ border-bottom:none; }}
.news-list .news-time {{ color:#a0aec0;font-size:0.8em;white-space:nowrap;min-width:60px; }}
.news-list .news-title {{ font-size:0.9em; }}
.cal-list {{ list-style:none; }}
.cal-list li {{ padding:8px 0;display:flex;gap:12px;align-items:flex-start; }}
.cal-list .cal-date {{ color:#e74c3c;font-weight:600;font-size:0.85em;white-space:nowrap;min-width:90px; }}
.chart-container {{ position:relative;height:280px;margin-top:12px; }}
.footer {{ text-align:center;color:#a0aec0;font-size:0.8em;padding:20px; }}
.no-data {{ text-align:center;color:#a0aec0;padding:20px;font-style:italic; }}
@media (max-width:600px) {{ .container{{padding:10px;}} .header{{padding:24px 16px;}} .header h1{{font-size:1.4em;}} .card{{padding:16px;}} .index-grid{{grid-template-columns:1fr 1fr;}} .flow-row{{flex-direction:column;}} }}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>财经日报</h1><div class="date">{report_date}</div><div class="disclaimer">数据仅供参考，不构成投资建议 | 数据来源: AKShare (Sina/THS/EastMoney)</div></div>
<div class="card"><h2>大盘指数概览</h2><div class="index-grid" id="indexGrid"></div></div>
<div class="card"><h2>行业板块热力</h2>
<div class="section-subtitle">涨幅 TOP5</div>
<table class="sector-table" id="gainersTable"><thead><tr><th>板块</th><th>涨跌幅</th><th>领涨股</th><th>涨/跌家数</th></tr></thead><tbody></tbody></table>
<div class="section-subtitle">跌幅 TOP5</div>
<table class="sector-table" id="losersTable"><thead><tr><th>板块</th><th>涨跌幅</th><th>领跌股</th><th>涨/跌家数</th></tr></thead><tbody></tbody></table>
</div>
<div class="card"><h2>资金流向</h2><div class="flow-row" id="flowRow"></div><div class="chart-container"><canvas id="flowChart"></canvas></div></div>
<div class="card"><h2>外汇与商品</h2><div class="comm-grid" id="commGrid"></div></div>
<div class="card"><h2>财经要闻</h2><ul class="news-list" id="newsList"></ul></div>
<div class="card"><h2>明日关注</h2><ul class="cal-list" id="calList"></ul></div>
<div class="footer"><p>Generated by WorkBuddy Finance Daily Report Skill</p><p>报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p></div>
</div>
<script>
const D = {data_json};
function gc(v){{return v===null||v===undefined?'#666':v>0?'#e74c3c':v<0?'#27ae60':'#666';}}
function ga(v){{return v===null||v===undefined?'':v>0?'':v<0?'':'';}}
function fp(v){{return(v>0?'+':'')+v.toFixed(2)+'%';}}
function fa(v){{return(v>0?'+':'')+v.toFixed(2);}}

(function(){{
 const g=document.getElementById('indexGrid');
 const its=(D.indices||[]).concat(D.hk_indices||[]);
 if(!its.length){{g.innerHTML='<div class="no-data">暂无指数数据</div>';return;}}
 its.forEach(i=>{{const d=document.createElement('div');d.className='index-item';
 d.innerHTML='<div class="idx-name">'+i.name+'</div><div class="idx-price">'+i.price.toFixed(2)+'</div><div class="idx-change" style="color:'+gc(i.change_pct)+'">'+ga(i.change_pct)+' '+fp(i.change_pct)+' '+fa(i.change_amt)+'</div>';
 g.appendChild(d);}});
}})();

(function(){{
 const s=D.sectors;if(!s)return;
 function f(tid,its){{const tb=document.getElementById(tid).querySelector('tbody');
 its.forEach(s=>{{const tr=document.createElement('tr');
 tr.innerHTML='<td><strong>'+s.name+'</strong></td><td style="color:'+gc(s.change_pct)+';font-weight:600">'+ga(s.change_pct)+' '+fp(s.change_pct)+'</td><td>'+(s.lead_stock||'--')+'</td><td><span style="color:#e74c3c">'+(s.up_count||0)+'</span> / <span style="color:#27ae60">'+(s.down_count||0)+'</span></td>';
 tb.appendChild(tr);}});}}
 f('gainersTable',s.gainers||[]);f('losersTable',s.losers||[]);
}})();

(function(){{
 const fl=D.north_flow,to=D.turnover,row=document.getElementById('flowRow');
 if(fl&&fl.today_net_flow!==undefined){{row.innerHTML+='<div class="flow-card"><div class="flow-label">北向资金净流入</div><div class="flow-value" style="color:'+gc(fl.today_net_flow)+'">'+ga(fl.today_net_flow)+' '+(fl.today_net_flow>0?'+':'')+fl.today_net_flow.toFixed(2)+' 亿</div></div>';}}
 if(to){{row.innerHTML+='<div class="flow-card"><div class="flow-label">两市成交额</div><div class="flow-value">'+to.toFixed(0)+' 亿</div></div>';}}
 if(!row.innerHTML){{row.innerHTML='<div class="no-data" style="width:100%">暂无资金流向数据</div>';}}
 if(fl&&fl.recent_flows&&fl.recent_flows.length){{
  const ctx=document.getElementById('flowChart').getContext('2d');
  const ls=fl.recent_flows.map(x=>x.date),vs=fl.recent_flows.map(x=>x.value);
  new Chart(ctx,{{type:'bar',data:{{labels:ls,datasets:[{{label:'北向资金(亿元)',data:vs,backgroundColor:vs.map(v=>v>=0?'rgba(231,76,60,0.6)':'rgba(39,174,96,0.6)'),borderColor:vs.map(v=>v>=0?'#e74c3c':'#27ae60'),borderWidth:1}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{grid:{{color:'#edf2f7'}}}},x:{{grid:{{display:false}}}}}}}}}});
 }}
}})();

(function(){{
 const g=document.getElementById('commGrid'),its=(D.forex||[]).concat(D.commodities||[]);
 if(!its.length){{g.innerHTML='<div class="no-data">暂无外汇商品数据</div>';return;}}
 its.forEach(i=>{{const d=document.createElement('div');d.className='comm-item';
 d.innerHTML='<div class="comm-name">'+i.name+'</div><div class="comm-price">'+i.price.toFixed(2)+'</div><div class="comm-change" style="color:'+gc(i.change_pct)+'">'+ga(i.change_pct)+' '+fp(i.change_pct||0)+'</div>';
 g.appendChild(d);}});
}})();

(function(){{
 const l=document.getElementById('newsList'),ns=D.news||[];
 if(!ns.length){{l.innerHTML='<div class="no-data">暂无财经新闻</div>';return;}}
 ns.forEach(n=>{{const li=document.createElement('li');li.innerHTML='<span class="news-time">'+(n.time||'')+'</span><span class="news-title">'+n.title+'</span>';l.appendChild(li);}});
}})();

(function(){{
 const l=document.getElementById('calList'),cl=D.calendar||[];
 if(!cl.length){{l.innerHTML='<div class="no-data">暂无日历数据</div>';return;}}
 cl.forEach(c=>{{const li=document.createElement('li');li.innerHTML='<span class="cal-date">'+c.date+'</span><span>'+c.event+'</span>';l.appendChild(li);}});
}})();
</script>
</body>
</html>'''


# ── Main ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Finance Daily Report Generator')
    parser.add_argument('--output', '-o', type=str, default=None, help='Output HTML file path')
    parser.add_argument('--date', '-d', type=str, default=None, help='Target date YYYY-MM-DD')
    args = parser.parse_args()

    report_date = args.date or datetime.now().strftime('%Y-%m-%d')
    print(f'Generating finance daily report for {report_date}...')

    try:
        import akshare  # noqa: F401
    except ImportError:
        print('Error: pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple', file=sys.stderr)
        sys.exit(1)

    print('\nFetching data...')
    print('  [1/6] A-share indices...')
    indices = fetch_index_data()
    print('  [2/6] HK indices...')
    hk_indices = fetch_hk_index_data()
    print('  [3/6] Industry sectors...')
    sectors = fetch_sector_data()
    print('  [4/6] Capital flow...')
    north_flow = fetch_north_flow()
    turnover = fetch_market_turnover()
    print('  [5/6] Forex & commodities...')
    forex = fetch_forex()
    commodities = fetch_commodities()
    print('  [6/6] News & calendar...')
    news = fetch_news()
    calendar = fetch_calendar()

    report_data = {
        'report_date': report_date,
        'indices': indices or [],
        'hk_indices': hk_indices or [],
        'sectors': sectors or {'gainers': [], 'losers': []},
        'north_flow': north_flow or {},
        'turnover': turnover,
        'forex': forex or [],
        'commodities': commodities or [],
        'news': news or [],
        'calendar': calendar or [],
    }

    success_count = sum([
        1 if indices else 0, 1 if hk_indices else 0,
        1 if sectors else 0, 1 if north_flow or turnover else 0,
        1 if forex or commodities else 0, 1 if news else 0,
    ])
    print(f'\nData fetch complete ({success_count}/6 modules)')

    print('Generating HTML report...')
    html = generate_html(report_data, report_date)

    output_path = args.output or f'finance_daily_report_{report_date}.html'
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    size_kb = os.path.getsize(output_path) / 1024
    print(f'\nReport generated: {output_path}')
    print(f'File size: {size_kb:.1f} KB')
    return output_path


if __name__ == '__main__':
    main()
