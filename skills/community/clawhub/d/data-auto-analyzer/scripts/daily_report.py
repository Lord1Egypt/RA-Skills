"""
每日投放日报生成器 - data-auto-analyzer 模式 D
完全动态识别指标（消耗/曝光/点击/转化/CPA/CTR/转化率等按表格智能推断，不写死字段名）。
输出：钉钉/飞书可直接粘贴的纯文本 + 浅色主题 HTML（卡片阴影 · 可折叠 · 环比 · 趋势图）。
用法: python3 daily_report.py --today today.xlsx [--yesterday yesterday.xlsx]
若 today 文件本身含多日数据，自动取最新一天为“今日”、前一天为“昨日”做环比，并画趋势。
"""
import sys, os, argparse, warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (load_file, preprocess, detect_columns, detect_roles, pick_main_dim,
                     entity_dims, entity_label, resolve_output_path, render_page, json_dumps, html_escape)


def _num(df, c):
    return pd.to_numeric(df[c], errors="coerce") if (c and c in df) else None


def summarize(df, roles, metric_cols, pct_cols):
    """动态汇总核心指标，返回 [(label, value, kind)]，kind ∈ {'num','pct'}。"""
    out = []
    add = lambda l, v, k: out.append((l, float(v), k))
    cost, conv = _num(df, roles.get("cost")), _num(df, roles.get("conversion"))
    click, imp, rev = _num(df, roles.get("click")), _num(df, roles.get("impression")), _num(df, roles.get("revenue"))
    has_ad = any(roles.get(k) for k in ("cost", "conversion", "click", "impression"))
    if has_ad:
        if cost is not None: add("消耗", cost.sum(), "num")
        if imp is not None: add("曝光", imp.sum(), "num")
        if click is not None: add("点击", click.sum(), "num")
        if conv is not None: add("转化", conv.sum(), "num")
        if cost is not None and conv is not None and conv.sum() > 0:
            add("CPA", cost.sum() / conv.sum(), "num")
        elif roles.get("cpa"):
            add("CPA", _num(df, roles["cpa"]).mean(), "num")
        if click is not None and imp is not None and imp.sum() > 0:
            add("CTR", click.sum() / imp.sum() * 100, "pct")
        if conv is not None and click is not None and click.sum() > 0:
            add("转化率", conv.sum() / click.sum() * 100, "pct")
        if rev is not None: add("收入", rev.sum(), "num")
        if rev is not None and cost is not None and cost.sum() > 0:
            add("ROI", rev.sum() / cost.sum(), "num")
    else:
        for c in metric_cols[:6]:
            s = pd.to_numeric(df[c], errors="coerce")
            add(str(c), (s.mean() if c in pct_cols else s.sum()), "pct" if c in pct_cols else "num")
    return out


def entity_rank(df, gdims, roles, main_metric):
    """按实体维度聚合，返回每个实体的 消耗/转化/CPA/主指标（全动态）。"""
    if not gdims or main_metric is None:
        return []
    cost_c, conv_c = roles.get("cost"), roles.get("conversion")
    agg = {}
    for c in [cost_c, conv_c, main_metric]:
        if c:
            agg[c] = "sum"
    g = df.groupby(gdims, dropna=False).agg(agg)
    rows = []
    for idx, r in g.iterrows():
        cost = float(r[cost_c]) if cost_c else None
        conv = float(r[conv_c]) if conv_c else None
        cpa = round(cost / conv, 2) if (cost is not None and conv) else None
        rows.append({"name": entity_label(idx, gdims), "main": float(r[main_metric]),
                     "cost": cost, "conv": conv, "cpa": cpa})
    return rows


def row_line(r):
    parts = []
    if r.get("cost") is not None:
        parts.append(f"消耗 {fmt_cn(r['cost'],'num')}")
    if r.get("conv") is not None:
        parts.append(f"转化 {fmt_cn(r['conv'],'num')}")
    if r.get("cpa") is not None:
        parts.append(f"CPA {fmt_cn(r['cpa'],'num')}")
    if not parts:
        parts.append(fmt_cn(r["main"], "num"))
    return "，".join(parts)


def fmt_cn(v, kind):
    if kind == "pct":
        return f"{v:.2f}%"
    if abs(v) >= 1e8:
        return f"{v/1e8:.2f}亿"
    if abs(v) >= 1e4:
        return f"{v/1e4:.2f}万"
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"


def pct_change(new, old):
    if old in (None, 0) or pd.isna(old):
        return None
    return (new - old) / abs(old) * 100


def build_text(date_str, today, yest_map, top, bottom, ent_label, rank_by, suggestions):
    L = ["━━━━━━━━━━━━━━━━━━━━━━━", f"📊 投放日报 · {date_str}", "━━━━━━━━━━━━━━━━━━━━━━━", "", "【核心指标】"]
    for label, val, kind in today:
        line = f"• {label}：{fmt_cn(val, kind)}"
        ch = pct_change(val, yest_map.get(label)) if yest_map else None
        if ch is not None:
            line += f"（{'↑' if ch>0 else '↓' if ch<0 else '→'}{abs(ch):.1f}%）"
        L.append(line)
    if top:
        L += ["", f"【TOP 最佳{ent_label}（按{rank_by}）】"]
        for i, t in enumerate(top, 1):
            L.append(f"{i}. {t['name']}：{row_line(t)}")
    if bottom:
        L += ["", f"【待优化{ent_label}（按{rank_by}）】"]
        for i, b in enumerate(bottom, 1):
            L.append(f"{i}. {b['name']}：{row_line(b)}")
    if suggestions:
        L += ["", "【明日建议】"] + [f"• {s}" for s in suggestions]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="每日投放日报 模式 D")
    ap.add_argument("--today", required=True, help="今日（或含多日）报表文件")
    ap.add_argument("--yesterday", help="昨日报表文件（可选；不传则尝试从多日数据自动取前一天）")
    ap.add_argument("--out-dir", default="", help="输出目录（默认 data-auto-analyzer/）")
    args = ap.parse_args()
    if not os.path.exists(args.today):
        print(f"❌ 文件不存在: {args.today}"); sys.exit(1)

    print(f"\n读取今日报表: {args.today}")
    df_all = preprocess(load_file(args.today))
    date_col, dim_cols, metric_cols, pct_cols = detect_columns(df_all)
    if not metric_cols:
        print("❌ 未识别到数值指标列"); sys.exit(1)
    roles = detect_roles(metric_cols, pct_cols)
    gdims = entity_dims(df_all, dim_cols)
    ent_label = "+".join(str(g) for g in gdims) if gdims else "实体"
    main_metric = roles.get("cost") or (metric_cols[0] if metric_cols else None)
    main_label = str(main_metric) if main_metric else ""
    print(f"实体维度: {ent_label} · 主指标: {main_label} · 角色: {roles or '通用'}")

    df_today, df_yest, date_str, trend = df_all, None, "全部数据", None
    if date_col and df_all[date_col].notna().any():
        ds = pd.to_datetime(df_all[date_col], errors="coerce")
        dstr = ds.dt.strftime("%Y-%m-%d")
        uniq = sorted(x for x in dstr.dropna().unique())
        if uniq:
            date_str = uniq[-1]
            df_today = df_all[dstr == uniq[-1]]
            if len(uniq) >= 2 and not args.yesterday:
                df_yest = df_all[dstr == uniq[-2]]
            if len(uniq) >= 2 and main_metric:
                gt = df_all.groupby(dstr)[main_metric].sum()
                trend = {"dates": list(gt.index), "values": [round(float(v), 2) for v in gt.values]}
    if args.yesterday and os.path.exists(args.yesterday):
        print(f"读取昨日报表: {args.yesterday}")
        df_yest = preprocess(load_file(args.yesterday))

    today = summarize(df_today, roles, metric_cols, pct_cols)
    yest_map = {l: v for l, v, k in summarize(df_yest, roles, metric_cols, pct_cols)} if df_yest is not None else {}

    rows = entity_rank(df_today, gdims, roles, main_metric)
    has_cpa = any(r["cpa"] is not None for r in rows)
    if has_cpa:
        valid = [r for r in rows if r["cpa"] is not None and (r["conv"] or 0) > 0]
        top = sorted(valid, key=lambda r: r["cpa"])[:3]          # CPA 越低越好
        bottom = sorted(valid, key=lambda r: -r["cpa"])[:3]       # CPA 越高越待优化
        rank_by = "CPA"
    else:
        top = sorted(rows, key=lambda r: -r["main"])[:3]
        bottom = sorted(rows, key=lambda r: r["main"])[:3]
        rank_by = main_label

    sug = []
    if bottom:
        sug.append(f"重点优化或暂停 {ent_label}【{bottom[0]['name']}】（{rank_by} 偏差）")
    if top:
        sug.append(f"可向 {ent_label}【{top[0]['name']}】等头部倾斜预算（{rank_by} 最优）")
    if yest_map:
        for l, v, k in today:
            ch = pct_change(v, yest_map.get(l))
            if ch is not None and abs(ch) >= 30:
                sug.append(f"{l} 环比{'上升' if ch>0 else '下降'} {abs(ch):.0f}%，留意波动")
                break
    if not sug:
        sug.append("各项指标平稳，保持当前投放节奏")

    text = build_text(date_str, today, yest_map, top, bottom, ent_label, rank_by, sug)
    print("\n【日报预览】\n" + text)

    metric_cards = []
    for label, val, kind in today:
        ch = pct_change(val, yest_map.get(label)) if yest_map else None
        sub = ""
        if ch is not None:
            arrow = "↑" if ch > 0 else ("↓" if ch < 0 else "→")
            cls = "up" if ch > 0 else ("down" if ch < 0 else "")
            sub = f'<span class="{cls}">{arrow} {abs(ch):.1f}% 环比</span>'
        metric_cards.append(f'<div class="card"><div class="label">{html_escape(label)}</div>'
                            f'<div class="value">{fmt_cn(val,kind)}</div><div class="sub">{sub}</div></div>')
    metrics_html = f'<div class="cards">{"".join(metric_cards)}</div>'

    def lst(items):
        if not items:
            return '<div class="info-box">无数据</div>'
        return ('<div class="table-wrap"><div class="table-container"><table class="dt"><tbody>'
                + ''.join(f'<tr><td>{i+1}. {html_escape(x["name"])}</td>'
                          f'<td class="num" style="color:var(--text-secondary)">{html_escape(row_line(x))}</td></tr>'
                          for i, x in enumerate(items)) + '</tbody></table></div></div>')
    rank_html = (f'<div class="chart2"><div><h4 style="margin-bottom:10px;font-size:.9rem;color:var(--accent-green)">TOP 最佳{html_escape(ent_label)}（按 {html_escape(rank_by)}）</h4>{lst(top)}</div>'
                 f'<div><h4 style="margin-bottom:10px;font-size:.9rem;color:var(--accent-red)">待优化{html_escape(ent_label)}（按 {html_escape(rank_by)}）</h4>{lst(bottom)}</div></div>')
    sug_html = "".join(f'<div class="info-box tip">💡 {html_escape(s)}</div>' for s in sug)
    txt_html = (f'<div class="info-box"><div style="color:var(--text-secondary);font-size:.8rem;margin-bottom:8px">可直接复制到钉钉/飞书/微信 👇</div>'
                f'<pre style="white-space:pre-wrap;font-family:inherit;margin:0">{html_escape(text)}</pre></div>')

    sections = [
        {"id": "sec-m", "nav": "核心指标", "title": f"核心指标 · {date_str}", "html": metrics_html},
        {"id": "sec-r", "nav": "排行", "title": "TOP / 待优化", "html": rank_html},
    ]
    body = ""
    if trend:
        sections.append({"id": "sec-t", "nav": "趋势", "title": f"{main_label} 趋势",
                         "html": '<div class="chart-card"><div class="chart-box" id="c-trend"></div></div>'})
        body = "const TR=" + json_dumps({"dates": trend["dates"], "values": trend["values"], "label": main_label}) + ";" + r"""
const EC={text:'#5a6478',axis:'#e3e7ef',split:'#eef1f6'};
const ch=echarts.init(document.getElementById('c-trend'));window.__charts.push(ch);
function fmt(n){if(Math.abs(n)>=1e8)return(n/1e8).toFixed(2)+'亿';if(Math.abs(n)>=1e4)return(n/1e4).toFixed(2)+'万';return n.toLocaleString();}
ch.setOption({backgroundColor:'transparent',tooltip:{trigger:'axis',backgroundColor:'#fff',borderColor:'#e9ecf2',textStyle:{color:'#1d2433'}},
 grid:{top:24,bottom:60,left:64,right:24},
 xAxis:{type:'category',data:TR.dates,boundaryGap:false,axisLabel:{color:EC.text,rotate:30,hideOverlap:true},axisLine:{lineStyle:{color:EC.axis}}},
 yAxis:{type:'value',name:TR.label,nameTextStyle:{color:EC.text},axisLabel:{color:EC.text,formatter:fmt},splitLine:{lineStyle:{color:EC.split}}},
 series:[{type:'line',data:TR.values,smooth:true,symbol:'circle',symbolSize:6,lineStyle:{width:3,color:'#3b6cff'},itemStyle:{color:'#3b6cff'},
   areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(59,108,255,.18)'},{offset:1,color:'rgba(59,108,255,.02)'}])}}]});
"""
    sections.append({"id": "sec-s", "nav": "建议", "title": "明日建议", "html": sug_html})
    sections.append({"id": "sec-x", "nav": "纯文本", "title": "纯文本日报（可粘贴）", "html": txt_html})

    html = render_page("投放日报", f"{html_escape(os.path.basename(args.today))} · {date_str}", sections, body)
    out_html = resolve_output_path(os.path.join(args.out_dir, "daily_report.html") if args.out_dir else "daily_report.html")
    out_txt = resolve_output_path(os.path.join(args.out_dir, "daily_report.txt") if args.out_dir else "daily_report.txt")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"\n{'='*60}\n✅ 日报已生成（浅色主题）")
    print(f"   纯文本: {out_txt}\n   HTML:   {out_html}\n{'='*60}")


if __name__ == "__main__":
    main()
