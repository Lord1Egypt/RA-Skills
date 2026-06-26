"""
账户/计划诊断器 - data-auto-analyzer 模式 B
完全动态识别：维度、消耗/转化/点击/曝光等指标均按表格智能推断，不写死任何字段名。
按统计规则给每个实体打红/黄/绿三级预警并给出处置建议。浅色主题 · 卡片阴影 · 可折叠。
用法: python3 diagnose.py --file ads.xlsx [--out diagnose_report.html]
"""
import sys, os, argparse, warnings
warnings.filterwarnings("ignore")
import pandas as pd, numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import (load_file, preprocess, detect_columns, detect_roles, pick_main_dim,
                     entity_dims, entity_label, resolve_output_path, render_page, json_dumps, html_escape)


def _safe_div(a, b):
    return a / b   # b 已用 .replace(0, np.nan) 处理过，除零得 NaN（Series 安全）


def build_entities(df, date_col, dim_cols, metric_cols, pct_cols, gdims, roles):
    """按实体维度(gdims)聚合并计算派生指标。绝对量求和、百分比取均值。"""
    if gdims:
        agg = {c: ("mean" if c in pct_cols else "sum") for c in metric_cols}
        ent = df.groupby(gdims, dropna=False).agg(agg).reset_index()
        if len(gdims) == 1:
            names = [entity_label(ent.iloc[i][gdims[0]], gdims) for i in range(len(ent))]
        else:
            names = [entity_label(tuple(ent.iloc[i][g] for g in gdims), gdims) for i in range(len(ent))]
        name_label = "+".join(str(g) for g in gdims)
    else:
        ent = df.copy().reset_index(drop=True)
        names = [f"行{i+1}" for i in range(len(ent))]
        name_label = "行"

    def col(role):
        return roles.get(role)

    g = lambda c: pd.to_numeric(ent[c], errors="coerce").fillna(0) if c in ent else pd.Series([0]*len(ent))
    cost, conv, click, imp, rev = g(col("cost")), g(col("conversion")), g(col("click")), g(col("impression")), g(col("revenue"))

    # 派生（仅在缺失时计算）
    cpa = pd.to_numeric(ent[col("cpa")], errors="coerce") if col("cpa") else _safe_div(cost, conv.replace(0, np.nan))
    ctr = pd.to_numeric(ent[col("ctr")], errors="coerce") if col("ctr") else _safe_div(click, imp.replace(0, np.nan)) * 100
    cvr = pd.to_numeric(ent[col("cvr")], errors="coerce") if col("cvr") else _safe_div(conv, click.replace(0, np.nan)) * 100

    present = {
        "cost": bool(col("cost")), "conversion": bool(col("conversion")),
        "click": bool(col("click")), "impression": bool(col("impression")), "revenue": bool(col("revenue")),
        "cpa": bool(col("cpa")) or (bool(col("cost")) and bool(col("conversion"))),
        "ctr": bool(col("ctr")) or (bool(col("click")) and bool(col("impression"))),
        "cvr": bool(col("cvr")) or (bool(col("conversion")) and bool(col("click"))),
    }
    has_ad = any(present[k] for k in ("cost", "conversion", "cpa", "ctr", "cvr"))

    # 均值基准
    m_cost = cost.mean()
    m_cpa = cpa[conv > 0].mean() if (present["cpa"] and (conv > 0).any()) else cpa.mean()
    m_ctr = ctr[imp > 1000].mean() if (present["ctr"] and (imp > 1000).any()) else (ctr.mean() if present["ctr"] else np.nan)
    m_cvr = cvr.mean() if present["cvr"] else np.nan

    # 通用兜底基准（无广告指标时用首个指标）
    fb_col = metric_cols[0] if metric_cols else None
    fb = g(fb_col) if fb_col else pd.Series([0]*len(ent))
    fb_mean, fb_std = fb.mean(), fb.std()

    entities = []
    cnt = {"red": 0, "yellow": 0, "green": 0}
    for i in range(len(ent)):
        reasons, actions, level = [], [], "green"
        c, cv, cl, im = cost.iloc[i], conv.iloc[i], click.iloc[i], imp.iloc[i]
        pa = cpa.iloc[i] if hasattr(cpa, "iloc") else np.nan
        tr = ctr.iloc[i] if hasattr(ctr, "iloc") else np.nan
        vr = cvr.iloc[i] if hasattr(cvr, "iloc") else np.nan

        if has_ad:
            # 红
            if present["cost"] and present["conversion"] and m_cost > 0 and c >= m_cost*2 and cv == 0:
                reasons.append(f"消耗为均值 {c/m_cost:.1f} 倍但 0 转化"); actions.append("立即暂停排查"); level = "red"
            if present["cpa"] and m_cpa and m_cpa > 0 and cv > 0 and pa >= m_cpa*3:
                reasons.append(f"CPA 为均值 {pa/m_cpa:.1f} 倍"); actions.append("暂停或大幅降价"); level = "red"
            if present["ctr"] and m_ctr and m_ctr > 0 and im > 1000 and tr <= m_ctr*0.3:
                reasons.append(f"点击率 {tr:.2f}% 仅为均值的 {tr/m_ctr*100:.0f}%"); actions.append("更换素材/创意"); level = "red"
            if present["cvr"] and m_cvr and m_cvr > 0 and present["cost"] and c >= m_cost and vr <= m_cvr*0.2:
                reasons.append(f"转化率 {vr:.2f}% 远低于均值 {m_cvr:.2f}%"); actions.append("检查转化路径"); level = "red"
            # 黄（未判红）
            if level != "red":
                if present["cpa"] and m_cpa and m_cpa > 0 and cv > 0 and pa >= m_cpa*1.5:
                    reasons.append(f"CPA 偏高（均值 {pa/m_cpa:.1f} 倍）"); actions.append("优化或适度降价"); level = "yellow"
                if present["ctr"] and m_ctr and m_ctr > 0 and im > 500 and tr <= m_ctr*0.6:
                    reasons.append(f"点击率偏低（{tr:.2f}%）"); actions.append("A/B 测试新素材"); level = "yellow"
                if present["cvr"] and m_cvr and m_cvr > 0 and vr <= m_cvr*0.5:
                    reasons.append(f"转化率偏低（{vr:.2f}%）"); actions.append("优化转化链路"); level = "yellow"
                if present["cost"] and present["conversion"] and m_cost > 0 and c >= m_cost*1.5 and cv <= max(conv.mean()*0.5, 0):
                    reasons.append("高消耗低转化"); actions.append("控制预算观察"); level = "yellow"
            if level == "green" and present["cpa"] and m_cpa and m_cpa > 0 and cv > 0 and pa <= m_cpa*0.7:
                reasons.append(f"CPA 优于均值 {(1-pa/m_cpa)*100:.0f}%"); actions.append("可加预算扩量")
        else:
            # 通用统计兜底：首个指标离群
            if fb_std and fb_std > 0:
                z = (fb.iloc[i] - fb_mean) / fb_std
                if abs(z) >= 3:
                    level = "red"; reasons.append(f"{fb_col} 显著异常（{'偏高' if z>0 else '偏低'}，z={z:.1f}）"); actions.append("重点核查")
                elif abs(z) >= 2:
                    level = "yellow"; reasons.append(f"{fb_col} 偏离均值（{'偏高' if z>0 else '偏低'}，z={z:.1f}）"); actions.append("关注")

        cnt[level] += 1
        name = names[i]
        vals = {}
        if present["cost"]: vals["消耗"] = round(float(c), 2)
        if present["conversion"]: vals["转化"] = round(float(cv), 2)
        if present["cpa"] and not pd.isna(pa): vals["CPA"] = round(float(pa), 2)
        if present["ctr"] and not pd.isna(tr): vals["点击率%"] = round(float(tr), 2)
        if present["cvr"] and not pd.isna(vr): vals["转化率%"] = round(float(vr), 2)
        if present["impression"]: vals["曝光"] = round(float(im), 2)
        if present["click"]: vals["点击"] = round(float(cl), 2)
        if not has_ad and fb_col: vals[str(fb_col)] = round(float(fb.iloc[i]), 2)
        entities.append({"name": name, "level": level,
                         "reason": "；".join(reasons) or "指标正常", "action": "；".join(actions) or "保持",
                         "vals": vals})

    metric_keys = list(entities[0]["vals"].keys()) if entities else []
    totals = {"实体数": len(entities)}
    if present["cost"]: totals["总消耗"] = round(float(cost.sum()), 2)
    if present["conversion"]: totals["总转化"] = round(float(conv.sum()), 2)
    if present["cpa"]: totals["平均CPA"] = round(float(cpa[conv > 0].mean() if (conv > 0).any() else cpa.mean()), 2)
    if present["revenue"]: totals["总收入"] = round(float(rev.sum()), 2)
    return entities, metric_keys, cnt, totals, name_label, has_ad


def main():
    ap = argparse.ArgumentParser(description="账户/计划诊断器 模式 B")
    ap.add_argument("--file", required=True)
    ap.add_argument("--out", default="diagnose_report.html")
    args = ap.parse_args()
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}"); sys.exit(1)

    print(f"\n正在读取: {args.file}")
    df = preprocess(load_file(args.file))
    print(f"读取成功，{len(df)} 行 × {len(df.columns)} 列")
    date_col, dim_cols, metric_cols, pct_cols = detect_columns(df)
    if not metric_cols:
        print("❌ 未识别到数值指标列"); sys.exit(1)
    gdims = entity_dims(df, dim_cols)
    roles = detect_roles(metric_cols, pct_cols)
    print(f"实体维度: {'+'.join(str(g) for g in gdims) or '（按行）'}")
    print(f"识别指标角色: {roles or '（无广告指标，启用通用统计诊断）'}")

    entities, metric_keys, cnt, totals, name_label, has_ad = build_entities(
        df, date_col, dim_cols, metric_cols, pct_cols, gdims, roles)
    print(f"诊断完成：🔴 {cnt['red']}  🟡 {cnt['yellow']}  🟢 {cnt['green']}")

    DATA = {"entities": entities, "metric_keys": metric_keys, "cnt": cnt,
            "name_label": name_label, "has_ad": has_ad}

    # ---- 概览卡片 ----
    ov = (f'<div class="card"><div class="label">实体数</div><div class="value">{totals["实体数"]}</div>'
          f'<div class="sub">诊断维度：{html_escape(DATA["name_label"])}</div></div>')
    ov += (f'<div class="card"><div class="label">预警分布</div>'
           f'<div class="value">🔴{cnt["red"]} 🟡{cnt["yellow"]} 🟢{cnt["green"]}</div>'
           f'<div class="sub">红/黄/绿计划数</div></div>')
    for k, v in totals.items():
        if k == "实体数":
            continue
        ov += f'<div class="card"><div class="label">{html_escape(k)}</div><div class="value" data-fmt>{v}</div></div>'
    overview_html = f'<div class="cards">{ov}</div>'

    table_html = """
    <div class="table-wrap">
      <div class="table-toolbar">
        <input class="search-box" id="q" placeholder="搜索..." oninput="render()">
        <div class="seg" id="lvseg">
          <button class="on" data-lv="all" onclick="setLv(this)">全部</button>
          <button data-lv="red" onclick="setLv(this)">🔴 红</button>
          <button data-lv="yellow" onclick="setLv(this)">🟡 黄</button>
          <button data-lv="green" onclick="setLv(this)">🟢 绿</button>
        </div>
        <span style="margin-left:auto;color:var(--text-secondary);font-size:.82rem" id="cnt"></span>
      </div>
      <div class="table-container"><table class="dt" id="tb"><thead id="th"></thead><tbody id="tbd"></tbody></table></div>
      <div class="pagination" id="pg"></div>
    </div>"""

    charts_html = '<div class="chart2"><div class="chart-card"><div class="chart-head"><span class="ctitle">诊断分布</span></div><div class="chart-box" id="c-pie"></div></div>' \
                  '<div class="chart-card"><div class="chart-head"><span class="ctitle">主指标排行 TOP15</span></div><div class="chart-box" id="c-bar"></div></div></div>'

    sections = [
        {"id": "sec-ov", "nav": "概览", "title": "诊断总览", "html": overview_html},
        {"id": "sec-tb", "nav": "明细", "title": "诊断明细", "html": table_html},
        {"id": "sec-ch", "nav": "图表", "title": "可视化", "html": charts_html},
    ]

    body = "const D=" + json_dumps(DATA) + ";" + r"""
const EC={text:'#5a6478',sub:'#9aa3b2',axis:'#e3e7ef',split:'#eef1f6',tipBg:'#fff',tipText:'#1d2433',tipBorder:'#e9ecf2'};
const COLORS=['#3b6cff','#10b981','#f59e0b','#ef4444','#7c5cff','#0ea5b7'];
const LVNAME={red:'🔴 红色预警',yellow:'🟡 黄色关注',green:'🟢 健康'};
let lv='all',page=1,PS=10;
function fmt(n){if(n===''||n==null)return'-';if(typeof n!=='number')return n;
  if(Math.abs(n)>=1e8)return(n/1e8).toFixed(2)+'亿';if(Math.abs(n)>=1e4)return(n/1e4).toFixed(2)+'万';
  return Number.isInteger(n)?n.toLocaleString():n.toLocaleString(undefined,{maximumFractionDigits:2});}
document.querySelectorAll('[data-fmt]').forEach(e=>{const v=parseFloat(e.textContent);if(!isNaN(v))e.textContent=fmt(v);});
function filtered(){const q=(document.getElementById('q').value||'').toLowerCase();
  return D.entities.filter(e=>(lv==='all'||e.level===lv)&&(!q||e.name.toLowerCase().includes(q)||e.reason.toLowerCase().includes(q)));}
function setLv(b){lv=b.dataset.lv;document.querySelectorAll('#lvseg button').forEach(x=>x.classList.toggle('on',x===b));page=1;render();}
function render(){const rows=filtered();const tp=Math.ceil(rows.length/PS)||1;if(page>tp)page=tp;
  document.getElementById('th').innerHTML='<tr><th>'+D.name_label+'</th><th>状态</th>'+D.metric_keys.map(k=>`<th class="num">${k}</th>`).join('')+'<th>诊断 / 建议</th></tr>';
  const pr=rows.slice((page-1)*PS,page*PS);
  document.getElementById('tbd').innerHTML=pr.map(e=>`<tr><td title="${e.name}">${e.name}</td>
    <td><span class="pill ${e.level}">${e.level==='red'?'红':e.level==='yellow'?'黄':'绿'}</span></td>
    ${D.metric_keys.map(k=>`<td class="num">${fmt(e.vals[k])}</td>`).join('')}
    <td style="white-space:normal;max-width:420px">${e.reason}${e.action&&e.action!=='保持'?` <span style="color:var(--accent-blue)">→ ${e.action}</span>`:''}</td></tr>`).join('')
    ||`<tr><td colspan="${D.metric_keys.length+3}" style="text-align:center;color:var(--text-dim);padding:24px">无匹配</td></tr>`;
  document.getElementById('cnt').textContent=`共 ${rows.length} 条`;
  let pg='';if(tp>1){pg+=`<button ${page===1?'disabled':''} onclick="page--;render()">‹</button>`;
    for(let i=1;i<=tp;i++){if(i===1||i===tp||Math.abs(i-page)<=1)pg+=`<button class="${i===page?'active':''}" onclick="page=${i};render()">${i}</button>`;else if(Math.abs(i-page)===2)pg+='<span style="color:var(--text-dim)">…</span>';}
    pg+=`<button ${page===tp?'disabled':''} onclick="page++;render()">›</button>`;}
  document.getElementById('pg').innerHTML=pg;}
function ecBase(o){return Object.assign({backgroundColor:'transparent',textStyle:{color:EC.text},
  tooltip:{backgroundColor:EC.tipBg,borderColor:EC.tipBorder,textStyle:{color:EC.tipText},confine:true,extraCssText:'box-shadow:0 8px 28px rgba(20,28,48,.14);border-radius:8px;'}},o);}
function drawCharts(){
  const pie=echarts.init(document.getElementById('c-pie'));window.__charts.push(pie);
  pie.setOption(ecBase({tooltip:{trigger:'item',formatter:'{b}: {c} ({d}%)'},legend:{bottom:0,textStyle:{color:EC.text}},
    color:['#ef4444','#f59e0b','#10b981'],series:[{type:'pie',radius:['42%','70%'],center:['50%','46%'],
    data:[{name:'🔴 红色预警',value:D.cnt.red},{name:'🟡 黄色关注',value:D.cnt.yellow},{name:'🟢 健康',value:D.cnt.green}],
    label:{color:EC.text},itemStyle:{borderRadius:6,borderColor:'#fff',borderWidth:2}}]}));
  const mk=D.metric_keys[0];
  if(mk){const top=[...D.entities].sort((a,b)=>(b.vals[mk]||0)-(a.vals[mk]||0)).slice(0,15);
    const bar=echarts.init(document.getElementById('c-bar'));window.__charts.push(bar);
    bar.setOption(ecBase({tooltip:{trigger:'axis',axisPointer:{type:'shadow'}},grid:{top:20,bottom:80,left:60,right:20},
      xAxis:{type:'category',data:top.map(e=>e.name),axisLabel:{color:EC.text,rotate:35,fontSize:10,hideOverlap:true},axisLine:{lineStyle:{color:EC.axis}}},
      yAxis:{type:'value',name:mk,axisLabel:{color:EC.text,formatter:fmt},splitLine:{lineStyle:{color:EC.split}}},
      series:[{type:'bar',data:top.map((e,i)=>({value:e.vals[mk]||0,itemStyle:{color:e.level==='red'?'#ef4444':e.level==='yellow'?'#f59e0b':'#3b6cff',borderRadius:[4,4,0,0]}})),barMaxWidth:30}]}));}
}
render();drawCharts();
"""

    html = render_page("账户诊断报告", f"{html_escape(os.path.basename(args.file))} · "
                       f"🔴{cnt['red']} 🟡{cnt['yellow']} 🟢{cnt['green']}", sections, body)
    out = resolve_output_path(args.out)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n{'='*60}\n✅ 诊断报告已生成（浅色主题）: {out}\n{'='*60}")


if __name__ == "__main__":
    main()
