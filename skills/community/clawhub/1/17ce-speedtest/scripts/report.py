#!/usr/bin/env python3
"""
17CE 测速结果 HTML 报表生成器 (支持移动端 + 图表对比)
用法：python report.py results.json > report.html
     或在 speedtest_ws.py 的 --html 模式下直接生成
"""

import json
import sys
from datetime import datetime

def speed_color(ms: float, code: int) -> str:
    if code != 200 and code != 301 and code != 302: return "#ef4444" # 红色 (错误)
    if ms < 50:   return "#22c55e"   # 绿
    if ms < 150:  return "#eab308"   # 黄
    return         "#f97316"          # 橙

def speed_label(ms: float, code: int) -> str:
    if code != 200 and code != 301 and code != 302:
        if code == 0: return "超时/阻断"
        return f"错误 {code}"
    if ms < 50:   return "极快"
    if ms < 100:  return "快"
    if ms < 200:  return "正常"
    if ms < 500:  return "慢"
    return "极慢"


def generate_html(results: list, url: str = "", test_time: str = "") -> str:
    if not test_time:
        test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    valid_results = [r for r in results if r.get("HttpCode") in (200, 301, 302) and r.get("TotalTime_ms")]
    err_results = [r for r in results if r not in valid_results]
    
    all_total = [r["TotalTime_ms"] for r in valid_results]
    avg_ms  = sum(all_total) / len(all_total) if all_total else 0
    min_ms  = min(all_total) if all_total else 0
    max_ms  = max(all_total) if all_total else 0
    success = len(valid_results)
    total_nodes = len(results)
    
    max_bar = max_ms * 1.1 if max_ms > 0 else 500

    # 生成图表和表格行 (按耗时排序)
    sorted_results = sorted(valid_results, key=lambda x: x.get("TotalTime_ms", 9999)) + err_results
    
    chart_html = ""
    table_rows = ""
    
    for r in sorted_results:
        code    = r.get("HttpCode", 0)
        total   = r.get("TotalTime_ms", 0)
        ttfb    = r.get("TTFBTime_ms",  0)
        dns     = r.get("DNS_ms", 0)
        prov    = r.get("Province", "未知")
        isp     = r.get("ISP", "未知")
        loc     = f"{prov}{isp}"
        
        color   = speed_color(total, code)
        label   = speed_label(total, code)
        is_ok   = code in (200, 301, 302)
        code_cls = "ok" if is_ok else "err"
        
        # 图表和表格共用的进度条属性
        pct = min(int(total / max_bar * 100), 100) if is_ok and max_bar > 0 else (100 if not is_ok else 0)
        bar_bg = color if is_ok else "#ef444455"
        
        # 图表条目 (仅展示成功连接的节点)
        if is_ok:
            display_val = f"{total:.1f}ms"
            chart_html += f"""
            <div class="chart-row">
                <div class="chart-lbl">{loc}</div>
                <div class="chart-bar-wrap">
                    <div class="chart-bar" style="width:{pct}%; background:{color}"></div>
                    <div class="chart-val" style="color:{color}">{display_val}</div>
                </div>
            </div>"""

        # 表格行
        bar_width = f"width:{pct}%" if is_ok else "width:100%"
        table_rows += f"""
        <tr>
          <td><span class="loc">{loc}</span></td>
          <td>
            <div class="bar-wrap"><div class="bar-fill" style="{bar_width};background:{bar_bg}"></div></div>
            <span style="color:{color};font-weight:600">{f"{total:.1f}" if is_ok else '--'}</span>
            <span class="badge" style="background:{color}20;color:{color}">{label}</span>
          </td>
          <td class="fade">{f"{ttfb:.1f}" if is_ok else '--'}</td>
          <td class="fade">{f"{dns:.1f}" if is_ok else '--'}</td>
          <td><span class="code {code_cls}">{code if code > 0 else '-'}</span></td>
          <td class="fade ip-col">{r.get('SrcIP','-')}</td>
        </tr>"""

    avg_color = 'green' if avg_ms < 100 else 'yellow' if avg_ms < 300 else 'red'
    max_color = 'red' if max_ms > 300 else 'yellow'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>17CE 测速报告</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:'Inter',system-ui,-apple-system,sans-serif;background:#0f172a;color:#e2e8f0;min-height:100vh;padding:24px 16px;line-height:1.5}}
  .container{{max-width:1000px;margin:0 auto}}
  
  /* 头部区域 */
  .header{{margin-bottom:20px}}
  h1{{font-size:20px;font-weight:700;background:linear-gradient(135deg,#38bdf8,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px}}
  .url-box{{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:10px 14px;font-size:13px;word-break:break-all}}
  .url-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}}
  .url-top .lbl{{color:#64748b;font-size:12px}}
  .url-top .t{{color:#64748b;font-size:11px}}
  .url-bot .u{{color:#38bdf8;font-weight:500;line-height:1.4}}
  
  /* 统计卡片 */
  .cards{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:20px}}
  @media(min-width:600px){{ 
      .cards{{grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px}} 
      h1{{font-size:22px;margin-bottom:16px}}
      .url-box{{display:flex;align-items:center;gap:12px;padding:14px 16px}}
      .url-top{{margin-bottom:0;display:inline-flex;gap:12px}}
      .url-bot{{flex:1}}
      .url-top .t{{margin-left:auto}}
  }}
  .card{{background:#1e293b;border:1px solid #334155;border-radius:10px;padding:14px}}
  .card .val{{font-size:22px;font-weight:700;line-height:1.2}}
  .card .unit{{font-size:12px;font-weight:400;opacity:0.7;margin-left:2px}}
  .card .lbl{{font-size:12px;color:#94a3b8;margin-top:4px}}
  .green{{color:#22c55e}}.yellow{{color:#eab308}}.red{{color:#ef4444}}.blue{{color:#38bdf8}}
  
  /* 图表区域 */
  .chart-box{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:20px;margin-bottom:24px}}
  .chart-title{{font-size:14px;font-weight:600;color:#cbd5e1;margin-bottom:16px}}
  .chart-row{{display:flex;align-items:center;margin-bottom:10px;font-size:12px}}
  .chart-lbl{{width:90px;flex-shrink:0;color:#94a3b8;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding-right:8px}}
  .chart-bar-wrap{{flex:1;display:flex;align-items:center;gap:8px}}
  .chart-bar{{height:10px;border-radius:5px;min-width:4px;transition:width 0.5s ease-out}}
  .chart-val{{font-weight:600}}
  
  @media(min-width:600px){{ .chart-lbl{{width:120px;font-size:13px}} .chart-bar{{height:12px;border-radius:6px}} }}

  /* 表格区域 (移动端适配) */
  .table-wrap{{background:#1e293b;border:1px solid #334155;border-radius:12px;overflow-x:auto;-webkit-overflow-scrolling:touch}}
  table{{width:100%;min-width:600px;border-collapse:collapse;text-align:left}}
  thead{{background:#0f172a80}}
  th{{padding:14px 16px;font-size:12px;color:#94a3b8;font-weight:600;white-space:nowrap}}
  td{{padding:14px 16px;border-top:1px solid #33415580;font-size:14px;vertical-align:middle;white-space:nowrap}}
  tr:hover td{{background:#fbbf240a}}
  
  .loc{{color:#f8fafc;font-weight:500}}
  .bar-wrap{{width:80px;background:#334155;border-radius:4px;overflow:hidden;margin-bottom:4px}}
  .bar-fill{{height:4px}}
  .badge{{display:inline-block;padding:2px 6px;border-radius:4px;font-size:11px;margin-left:6px;vertical-align:middle}}
  .code{{display:inline-block;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:700}}
  .ok{{background:#22c55e20;color:#4ade80}}
  .err{{background:#ef444420;color:#f87171}}
  .fade{{color:#64748b}}
  .ip-col{{font-size:13px}}

  footer{{text-align:center;color:#475569;font-size:12px;margin-top:32px;padding-bottom:16px}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🚀 17CE 测速报告</h1>
    <div class="url-box">
      <div class="url-top">
        <span class="lbl">目标</span>
        <span class="t">{test_time}</span>
      </div>
      <div class="url-bot">
        <span class="u">{url or "未指定"}</span>
      </div>
    </div>
  </div>

  <div class="cards">
    <div class="card">
      <div class="val {avg_color}">{avg_ms:.0f}<span class="unit">ms</span></div>
      <div class="lbl">平均响应时间</div>
    </div>
    <div class="card">
      <div class="val green">{min_ms:.0f}<span class="unit">ms</span></div>
      <div class="lbl">最快节点</div>
    </div>
    <div class="card">
      <div class="val {max_color}">{max_ms:.0f}<span class="unit">ms</span></div>
      <div class="lbl">最慢节点</div>
    </div>
    <div class="card">
      <div class="val {'blue' if success==total_nodes else 'red'}">{success} / {total_nodes}</div>
      <div class="lbl">连通节点数</div>
    </div>
  </div>

  <div class="chart-box">
    <div class="chart-title">📊 节点响应时间对比 (越短越好)</div>
    {chart_html}
  </div>

  <div class="table-wrap">
    <table>
      <thead>
        <tr>
          <th>节点位置</th>
          <th>总耗时 (ms)</th>
          <th>首字节 (ms)</th>
          <th>DNS (ms)</th>
          <th>HTTP</th>
          <th>解析IP</th>
        </tr>
      </thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>

  <footer>17CE WebSocket API · {total_nodes} 节点 · 由 OpenClaw 生成</footer>
</div>
</body>
</html>"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
        results = data if isinstance(data, list) else data.get("results", [])
        url = data.get("url", "") if isinstance(data, dict) else ""
    else:
        # allow piping json
        content = sys.stdin.read()
        try:
            data = json.loads(content)
            results = data if isinstance(data, list) else data.get("results", [])
            url = data.get("url", "") if isinstance(data, dict) else ""
        except:
            results = []
            url = ""

    print(generate_html(results, url))
