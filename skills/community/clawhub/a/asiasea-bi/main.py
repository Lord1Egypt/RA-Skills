#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
@Project : 金灯塔 BI Skill (OpenClaw Agent)
@Company : Asiasea (asiasea-ai)
@License : PROPRIETARY AND CONFIDENTIAL (参见 LICENSE 文件)
====================================================================
"""
import json
import os
import datetime
import requests
import base64

# ==================== 多用户状态隔离 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_session_file(user_id: str) -> str:
    safe_user_id = "".join(c for c in str(user_id) if c.isalnum() or c in ('-', '_')) if user_id else "default_user"
    return os.path.join(BASE_DIR, f".session_{safe_user_id}.json")

def load_session(user_id: str) -> dict:
    session_file = get_session_file(user_id)
    if os.path.exists(session_file):
        try:
            with open(session_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "initialized": False, 
        "user_phone": None,
        "system_name": None,
        "system_id": None,
        "system_auth_headers": {},  
        "api_registry": [],
        "last_report_url": None,
        "last_report_title": None
    }

def save_session(user_id: str, data: dict):
    with open(get_session_file(user_id), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== 工具函数 ====================
def safe_float(val) -> float:
    """安全转换：处理 null / None / 空字符串 / 非数字"""
    try:
        if val is None or val == "":
            return 0.0
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def parse_time_keywords(text: str):
    """自然语言时间 → (start_date, end_date, label)"""
    now = datetime.datetime.now()
    if "本月" in text:
        return now.replace(day=1).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "本月"
    if "上个月" in text or "上月" in text:
        first = now.replace(day=1)
        last = first - datetime.timedelta(days=1)
        return last.replace(day=1).strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d"), "上个月"
    if "昨天" in text or "昨日" in text:
        y = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        return y, y, "昨天"
    if "今天" in text or "今日" in text:
        t = now.strftime("%Y-%m-%d")
        return t, t, "今天"
    if "本周" in text:
        return (now - datetime.timedelta(days=now.weekday())).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "本周"
    if "上周" in text:
        sun = now - datetime.timedelta(days=now.weekday() + 1)
        mon = sun - datetime.timedelta(days=6)
        return mon.strftime("%Y-%m-%d"), sun.strftime("%Y-%m-%d"), "上周"
    if "今年" in text or "本年" in text:
        return now.replace(month=1, day=1).strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "今年"
    return None, None, ""

# ==================== 后端 API ====================
def api_get_supported_systems() -> list:
    try:
        resp = requests.get("https://o.yayuit.cn/dw/api/auth/supported-systems", timeout=5).json()
        if resp.get("code") == 100000:
            return resp.get("result", {}).get("list", [])
    except Exception as e:
        print(f"[bi] get_supported_systems error: {e}")
    return []

def api_get_registry(system_id: int) -> list:
    try:
        resp = requests.get(f"https://o.yayuit.cn/dw/api/system/api-registry?system_id={system_id}", timeout=5).json()
        if resp.get("code") == 100000:
            return resp.get("result", {}).get("list", [])
    except Exception as e:
        print(f"[bi] get_registry error: {e}")
    return []

def api_get_system_token(system_id: int) -> dict:
    try:
        resp = requests.get(f"https://o.yayuit.cn/dw/api/auth/system-token?system_id={system_id}", timeout=5).json()
        if resp.get("code") == 100000:
            return resp.get("result", {}).get("data", {})
    except Exception as e:
        print(f"[bi] get_system_token error: {e}")
    return {}

def api_upload_html_to_oss(html_content: str) -> str:
    try:
        resp = requests.post(
            "https://o.yayuit.cn/dw/api/skills/archive/upload",
            files={"file": ("bi_report.html", html_content.encode("utf-8"), "text/html")},
            timeout=15,
        ).json()
        if resp.get("code") == 100000:
            return resp.get("result", {}).get("preview_url", "")
    except Exception as e:
        print(f"[bi] upload_html error: {e}")
    return ""

def api_publish_report(url: str, title: str) -> tuple:
    try:
        resp = requests.post(
            "https://o.yayuit.cn/dw/api/skills/archive/publish",
            json={"url": url, "title": title},
            timeout=10,
        ).json()
        if resp.get("code") == 100000:
            return True, resp.get("result", {}).get("published_url", url)
        return False, resp.get("msg", "未知错误")
    except Exception as e:
        return False, str(e)

# ==================== 指标元数据 ====================
_METRIC_MAP = [
    {"key": "报销单", "keywords": ["bx", "报销"], "label": "费用报销", "desc": "查询指定周期内的费用报销单汇总与明细"},
    {"key": "部门周期预算", "keywords": ["yearBudget", "预算"], "label": "部门预算", "desc": "统计各部门在指定周期内的预算分配与使用情况"},
]

def get_friendly_metrics(api_registry: list) -> list:
    seen, result = set(), []
    for reg_item in api_registry:
        path = reg_item.get("path", "") + reg_item.get("name", "")
        for m in _METRIC_MAP:
            if m["key"] not in seen and any(kw in path for kw in m["keywords"]):
                seen.add(m["key"])
                result.append(m)
    if not result:
        result = _METRIC_MAP[:]
    return result

def resolve_metric(full_text: str) -> dict | None:
    if any(kw in full_text for kw in ["预算"]):
        return next(m for m in _METRIC_MAP if m["key"] == "部门周期预算")
    if any(kw in full_text for kw in ["报销", "费用", "报销单"]):
        return next(m for m in _METRIC_MAP if m["key"] == "报销单")
    return None

# ==================== HTML 大屏生成器 ====================
def generate_html_report(
    system: str, metric_label: str, metric_key: str, time_range: str,
    start_date: str, end_date: str, val1_label: str, val1: float,
    val2_label: str, val2: float, table_rows: list, 
    api_url: str, headers_dict: dict
) -> str:
    echarts_url = "https://jindengta-archive.oss-cn-beijing.aliyuncs.com/theme/web/bi/echarts.min.js"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    val_diff = val1 - val2
    used_pct = round(val2 / val1 * 100) if val1 > 0 else 0
    
    # 混淆 API 配置，防止非技术人员直接读取明文 Token
    config_payload = json.dumps({"url": api_url, "headers": headers_dict, "metric": metric_key})
    config_b64 = base64.b64encode(config_payload.encode('utf-8')).decode('utf-8')

    # ---------- 明细表 (已修正 API 字段名映射) ----------
    if metric_key == "报销单":
        thead = "<tr><th>报销单号</th><th>申请人</th><th>部门</th><th>报销总额</th><th>待核销金额</th><th>状态</th></tr>"
        tbody_rows = ""
        for row in table_rows[:50]:
            tp = safe_float(row.get("totalprice"))
            wh = safe_float(row.get("waitHxPrice"))
            # 修复：bxCode -> budgetNo, deptName -> departmentName
            tbody_rows += f"""<tr>
              <td class="mono">{row.get('budgetNo') or '—'}</td>
              <td>{row.get('applyUserName') or '—'}</td>
              <td>{row.get('departmentName') or '—'}</td>
              <td class="num">¥{tp:,.2f}</td>
              <td class="num">¥{wh:,.2f}</td>
              <td><span class="badge">{row.get('statusName') or '—'}</span></td>
            </tr>"""
    else:
        thead = "<tr><th>部门</th><th>预算总额</th><th>已用金额</th><th>剩余金额</th><th>使用进度</th></tr>"
        tbody_rows = ""
        for row in table_rows[:50]:
            bt = safe_float(row.get("budgetTotal"))
            ua = safe_float(row.get("usedAmount"))
            rem = bt - ua
            pct_row = round(ua / bt * 100) if bt > 0 else 0
            # 修复：deptName -> ewecomFepartmentName
            tbody_rows += f"""<tr>
              <td>{row.get('ewecomFepartmentName') or '—'}</td>
              <td class="num">¥{bt:,.2f}</td>
              <td class="num">¥{ua:,.2f}</td>
              <td class="num {"danger-text" if rem < 0 else ""}">¥{rem:,.2f}</td>
              <td>
                <div class="prog-wrap"><div class="prog-fill {"prog-warn" if pct_row>80 else ""}" style="width:{min(pct_row,100)}%"></div></div>
                <span class="prog-label">{pct_row}%</span>
              </td>
            </tr>"""

    if val1 > 0:
        if used_pct >= 90: insight_tip = f"⚠️ 使用率已达 <strong>{used_pct}%</strong>，余量极为有限，请重点关注资金压力。"
        elif used_pct >= 70: insight_tip = f"📌 使用率 <strong>{used_pct}%</strong>，处于偏高区间，建议跟进余量管理。"
        else: insight_tip = f"✅ 使用率 <strong>{used_pct}%</strong>，整体处于健康合理区间。"
    else:
        insight_tip = "📎 当前周期内未找到有效数据，请确认时间范围或业务产生情况。"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{metric_label} 看板 · {system}</title>
<script src="{echarts_url}"></script>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --c-primary: #3B6EF8; --c-primary-d: #2952CC; --c-primary-bg: #EEF2FF;
  --c-green: #059669; --c-green-bg: #ECFDF5;
  --c-amber: #D97706; --c-amber-bg: #FFFBEB;
  --c-red: #DC2626; --c-red-bg: #FEF2F2;
  --c-text: #111827; --c-muted: #6B7280; --c-border: #E5E7EB;
  --c-bg: #F9FAFB; --c-card: #FFFFFF;
  --radius: 10px; --shadow: 0 1px 3px rgba(0,0,0,.08), 0 1px 8px rgba(0,0,0,.04);
}}
body {{ font-family: "PingFang SC", "Helvetica Neue", Arial, sans-serif; background: var(--c-bg); color: var(--c-text); font-size: 14px; }}
.hero {{ background: linear-gradient(130deg, #1e3a8a 0%, #3B6EF8 60%, #7c3aed 100%); color: #fff; padding: 28px 32px 24px; }}
.hero-title {{ font-size: 20px; font-weight: 700; margin-bottom: 10px; }}
.hero-meta {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.hero-tag {{ background: rgba(255,255,255,.18); backdrop-filter: blur(4px); border-radius: 20px; padding: 3px 12px; font-size: 12px; }}
.wrap {{ max-width: 1300px; margin: 0 auto; padding: 20px 16px; display: flex; flex-direction: column; gap: 16px; }}
.filter-bar {{ background: var(--c-card); border-radius: var(--radius); padding: 14px 18px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; box-shadow: var(--shadow); }}
.filter-label {{ font-size: 12px; font-weight: 600; color: var(--c-muted); text-transform: uppercase; }}
.filter-bar input[type=date] {{ border: 1.5px solid var(--c-border); border-radius: 6px; padding: 6px 10px; font-size: 13px; color: var(--c-text); outline: none; }}
.btn-query {{ background: var(--c-primary); color: #fff; border: none; border-radius: 6px; padding: 7px 18px; font-size: 13px; font-weight: 600; cursor: pointer; }}
.btn-query:disabled {{ background: #93C5FD; cursor: not-allowed; }}
.status-txt {{ font-size: 12px; color: var(--c-muted); }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; }}
.kpi {{ background: var(--c-card); border-radius: var(--radius); padding: 18px 20px; box-shadow: var(--shadow); border-top: 3px solid transparent; }}
.kpi.blue {{ border-color: var(--c-primary); }} .kpi.green {{ border-color: var(--c-green); }} .kpi.amber {{ border-color: var(--c-amber); }} .kpi.red {{ border-color: var(--c-red); }}
.kpi-lbl {{ font-size: 11px; font-weight: 600; color: var(--c-muted); margin-bottom: 8px; }}
.kpi-val {{ font-size: 24px; font-weight: 700; }}
.kpi-sub {{ font-size: 11px; color: var(--c-muted); margin-top: 4px; }}
.kpi.blue .kpi-val {{ color: var(--c-primary); }} .kpi.green .kpi-val {{ color: var(--c-green); }} .kpi.amber .kpi-val {{ color: var(--c-amber); }} .kpi.red .kpi-val {{ color: var(--c-red); }}
.charts-2col {{ display: grid; grid-template-columns: 3fr 2fr; gap: 16px; }}
.charts-3col {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }}
@media(max-width:900px) {{ .charts-2col, .charts-3col {{ grid-template-columns: 1fr; }} }}
.card {{ background: var(--c-card); border-radius: var(--radius); padding: 18px 20px; box-shadow: var(--shadow); overflow: hidden; }}
.card-title {{ font-size: 13px; font-weight: 700; margin-bottom: 14px; }}
.echart {{ width: 100%; height: 260px; }} .echart-tall {{ width: 100%; height: 300px; }}
.tbl-wrap {{ overflow-x: auto; max-height: 400px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
thead tr {{ border-bottom: 2px solid var(--c-border); }}
th {{ padding: 9px 12px; text-align: left; font-size: 11px; color: var(--c-muted); position: sticky; top: 0; background: #fff; z-index: 1; }}
td {{ padding: 9px 12px; border-bottom: 1px solid var(--c-border); }}
td.num {{ text-align: right; }} td.mono {{ font-family: monospace; font-size: 12px; color: var(--c-muted); }}
.danger-text {{ color: var(--c-red); }}
.badge {{ background: var(--c-primary-bg); color: var(--c-primary); font-size: 11px; padding: 2px 8px; border-radius: 4px; }}
.prog-wrap {{ display: inline-block; width: 80px; height: 5px; background: var(--c-border); border-radius: 3px; }}
.prog-fill {{ height: 5px; background: var(--c-primary); border-radius: 3px; }} .prog-warn {{ background: var(--c-amber); }}
.prog-label {{ font-size: 11px; color: var(--c-muted); margin-left: 6px; }}
.summary {{ background: linear-gradient(135deg, var(--c-primary-bg) 0%, #F5F3FF 100%); border: 1px solid #C7D2FE; border-radius: var(--radius); padding: 22px 24px; }}
.summary-head {{ font-size: 14px; font-weight: 700; color: var(--c-primary); margin-bottom: 16px; }}
.summary-kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 10px; margin-bottom: 16px; }}
.sk {{ background: #fff; border-radius: 8px; padding: 12px 16px; }}
.sk-lbl {{ font-size: 11px; color: var(--c-muted); margin-bottom: 4px; }}
.sk-val {{ font-size: 16px; font-weight: 700; }}
.insight-box {{ background: #fff; border-left: 3px solid var(--c-primary); border-radius: 0 8px 8px 0; padding: 14px 18px; line-height: 1.9; }}
.footer {{ text-align: center; font-size: 11px; color: #9CA3AF; padding: 12px 0 20px; }}
</style>
</head>
<body>

<div class="hero">
  <div class="hero-title">📊 {metric_label} · 大屏分析看板</div>
  <div class="hero-meta">
    <span class="hero-tag">🏢 业务系统: {system}</span>
    <span class="hero-tag">📅 时间范围: {start_date} ~ {end_date}</span>
    <span class="hero-tag">🕐 生成时间: {now_str}</span>
  </div>
</div>

<div class="wrap">
  <div class="filter-bar">
    <span class="filter-label">自定义时间检索</span>
    <input type="date" id="i_start" value="{start_date}">
    <span style="color:var(--c-muted)">—</span>
    <input type="date" id="i_end" value="{end_date}">
    <button class="btn-query" id="btn_q" onclick="doQuery()">🔍 实时加载数据</button>
    <span class="status-txt" id="status_msg"></span>
  </div>

  <div class="kpi-grid">
    <div class="kpi blue"><div class="kpi-lbl">{val1_label}</div><div class="kpi-val" id="kv1">¥{val1:,.0f}</div><div class="kpi-sub">当前统计周期总计</div></div>
    <div class="kpi green"><div class="kpi-lbl">{val2_label}</div><div class="kpi-val" id="kv2">¥{val2:,.0f}</div><div class="kpi-sub">已用 / 待核销总计</div></div>
    <div class="kpi amber"><div class="kpi-lbl">当前差额</div><div class="kpi-val" id="kv_diff">¥{abs(val_diff):,.0f}</div><div class="kpi-sub">盈余或核销差值</div></div>
    <div class="kpi red"><div class="kpi-lbl">进度占比</div><div class="kpi-val" id="kv_pct">{used_pct}%</div><div class="kpi-sub">综合使用比率</div></div>
  </div>

  <div class="charts-2col">
    <div class="card"><div class="card-title">📊 核心度量双轴对比</div><div id="chart_bar" class="echart-tall"></div></div>
    <div class="card"><div class="card-title">🍩 结构占比分析</div><div id="chart_pie" class="echart-tall"></div></div>
  </div>

  <div class="charts-3col">
    <div class="card"><div class="card-title">📈 业务部门 / 时间趋势分布</div><div id="chart_line" class="echart"></div></div>
    <div class="card"><div class="card-title">📉 差额离散度分析</div><div id="chart_scatter" class="echart"></div></div>
    <div class="card"><div class="card-title">🎯 综合使用率表盘</div><div id="chart_gauge" class="echart"></div></div>
  </div>

  <div class="card">
    <div class="card-title">📋 业务数据明细矩阵 (展示前50条)</div>
    <div class="tbl-wrap">
      <table>
        <thead>{thead}</thead>
        <tbody id="tbl_body">{tbody_rows}</tbody>
      </table>
    </div>
  </div>

  <div class="summary" id="summary_block">
    <div class="summary-head">🧠 AI 智能研报摘要</div>
    <div class="summary-kpis">
      <div class="sk"><div class="sk-lbl">时间周期</div><div class="sk-val" id="sv_period">{start_date} ~ {end_date}</div></div>
      <div class="sk"><div class="sk-lbl">{val1_label}</div><div class="sk-val" id="sv_v1">¥{val1:,.2f}</div></div>
      <div class="sk"><div class="sk-lbl">{val2_label}</div><div class="sk-val" id="sv_v2">¥{val2:,.2f}</div></div>
      <div class="sk"><div class="sk-lbl">使用率</div><div class="sk-val" id="sv_pct">{used_pct}%</div></div>
    </div>
    <div class="insight-box" id="sv_insight">
      📌 截止至当前选择的统计周期，<strong>{system}</strong> 业务域下的 <strong>{metric_label}</strong> 指标情况如下：
      其中 <strong>{val1_label}</strong> 为 <strong>¥{val1:,.2f}</strong>，<strong>{val2_label}</strong> 为 <strong>¥{val2:,.2f}</strong>。
      综合换算当前进度占比约 <strong>{used_pct}%</strong>，绝对差额为 <strong>¥{abs(val_diff):,.2f}</strong>。
      {insight_tip}
    </div>
  </div>

  <div class="footer">数据引擎由 金灯塔 BI 提供技术支持 · 界面交互基于动态真实 API 渲染</div>
</div>

<script>
var L1 = "{val1_label}", L2 = "{val2_label}";
var barC = echarts.init(document.getElementById('chart_bar'));
var pieC = echarts.init(document.getElementById('chart_pie'));
var lineC = echarts.init(document.getElementById('chart_line'));
var scatC = echarts.init(document.getElementById('chart_scatter'));
var gaugeC = echarts.init(document.getElementById('chart_gauge'));

// 真实直连的 API 配置 (经 Base64 编码以防止外行直接审查源码)
const CFG = JSON.parse(atob('{config_b64}'));

function renderAll(v1, v2, rows) {{
  var diff = v1 - v2, pct = v1 > 0 ? Math.round(v2 / v1 * 100) : 0;
  
  barC.setOption({{
    tooltip: {{ trigger: 'axis', formatter: p => p.map(x => x.marker + x.seriesName + ': ¥' + x.value.toLocaleString()).join('<br>') }},
    grid: {{ left: '2%', right: '4%', bottom: '10%', top: '8%', containLabel: true }},
    xAxis: {{ type: 'category', data: ['综合度量对比'] }},
    yAxis: {{ type: 'value', axisLabel: {{ formatter: v => v >= 10000 ? (v/10000).toFixed(0) + 'w' : v }} }},
    series: [
      {{ name: L1, type: 'bar', data: [v1], barWidth: '35%', itemStyle: {{ color: '#3B6EF8', borderRadius: [4,4,0,0] }}, label: {{ show: true, position: 'top' }} }},
      {{ name: L2, type: 'bar', data: [v2], barWidth: '35%', itemStyle: {{ color: '#059669', borderRadius: [4,4,0,0] }}, label: {{ show: true, position: 'top' }} }}
    ]
  }});

  pieC.setOption({{
    tooltip: {{ trigger: 'item', formatter: '{{b}}: ¥{{c}}<br>占比 {{d}}%' }},
    legend: {{ bottom: 0 }},
    series: [{{
      type: 'pie', radius: ['45%', '70%'], center: ['50%','45%'],
      data: [ {{ value: v2, name: L2, itemStyle: {{color: '#3B6EF8'}} }}, {{ value: Math.max(0,diff), name: '差额余量', itemStyle: {{color: '#E5E7EB'}} }} ]
    }}]
  }});

  var lineX = [], ls1 = [], ls2 = [], scatData = [];
  if (rows && rows.length > 0) {{
    var grouped = {{}};
    rows.forEach((r, i) => {{
      var k, a, b;
      if (CFG.metric === '报销单') {{
        k = (r.createTime || '').substring(0, 10) || '日期';
        a = parseFloat(r.totalprice||0); b = parseFloat(r.waitHxPrice||0);
        scatData.push([a, b, r.departmentName || r.budgetNo || '明细']);
      }} else {{
        k = r.ewecomFepartmentName || '部门';
        a = parseFloat(r.budgetTotal||0); b = parseFloat(r.usedAmount||0);
        scatData.push([a, b, r.ewecomFepartmentName || '明细']);
      }}
      if (!grouped[k]) grouped[k] = {{v1:0, v2:0}};
      grouped[k].v1 += a; grouped[k].v2 += b;
    }});
    Object.keys(grouped).sort().forEach(k => {{
      lineX.push(k); ls1.push(grouped[k].v1); ls2.push(grouped[k].v2);
    }});
  }} else {{ lineX = ['暂无']; ls1 = [v1]; ls2 = [v2]; }}

  lineC.setOption({{
    tooltip: {{ trigger: 'axis' }},
    grid: {{ left: '2%', right: '4%', bottom: '10%', top: '10%', containLabel: true }},
    xAxis: {{ type: 'category', data: lineX, axisLabel: {{ rotate: lineX.length>6 ? 30 : 0 }} }},
    yAxis: {{ type: 'value', axisLabel: {{ formatter: v => v >= 10000 ? (v/10000).toFixed(0)+'w' : v }} }},
    series: [
      {{ name: L1, type: 'line', data: ls1, smooth: true, lineStyle: {{ color: '#3B6EF8' }}, itemStyle: {{ color: '#3B6EF8' }} }},
      {{ name: L2, type: 'line', data: ls2, smooth: true, lineStyle: {{ color: '#059669' }}, itemStyle: {{ color: '#059669' }} }}
    ]
  }});

  scatC.setOption({{
    tooltip: {{ formatter: p => p.data[2] + '<br>' + L1 + ': ¥' + p.data[0] + '<br>' + L2 + ': ¥' + p.data[1] }},
    grid: {{ left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true }},
    xAxis: {{ type: 'value', name: L1, axisLabel: {{ formatter: v => v >= 10000 ? (v/10000).toFixed(0)+'w' : v }} }},
    yAxis: {{ type: 'value', name: L2, axisLabel: {{ formatter: v => v >= 10000 ? (v/10000).toFixed(0)+'w' : v }} }},
    series: [{{ type: 'scatter', data: scatData, itemStyle: {{ color: '#7C3AED', opacity: .7 }} }}]
  }});

  var gColor = pct >= 90 ? '#DC2626' : pct >= 70 ? '#D97706' : '#059669';
  gaugeC.setOption({{
    series: [{{
      type: 'gauge', progress: {{ show: true, width: 12, itemStyle: {{color: gColor}} }},
      axisLine: {{ lineStyle: {{ width: 12 }} }}, detail: {{ valueAnimation: true, formatter: '{{value}}%', color: gColor }},
      data: [{{ value: pct, name: '进度' }}]
    }}]
  }});
}}

renderAll({val1}, {val2}, {json.dumps(table_rows)});
window.addEventListener('resize', () => {{ [barC, pieC, lineC, scatC, gaugeC].forEach(c => c.resize()); }});

function fmt(n) {{ return parseFloat(n||0).toLocaleString('zh-CN',{{minimumFractionDigits:2,maximumFractionDigits:2}}); }}

// 直连真实业务 API 重载数据
async function doQuery() {{
  var start = document.getElementById('i_start').value;
  var end = document.getElementById('i_end').value;
  if (!start || !end) {{ alert('请选择时间'); return; }}
  
  var btn = document.getElementById('btn_q');
  var msg = document.getElementById('status_msg');
  btn.disabled = true; btn.textContent = '数据拉取中…';
  msg.textContent = '正在连接业务系统…';

  var h = CFG.headers;
  h['Content-Type'] = 'application/json';
  var u = new URL(CFG.url);
  u.searchParams.append('method', 'ALL');
  u.searchParams.append('pageNo', '1');
  u.searchParams.append('pageSize', '50');
  
  if (CFG.metric === '部门周期预算') {{
      u.searchParams.append('startTime', start);
      u.searchParams.append('endTime', end);
  }} else {{
      u.searchParams.append('createStime', start);
      u.searchParams.append('createEtime', end);
  }}

  try {{
    var res = await fetch(u, {{ method: 'GET', headers: h }});
    var d = await res.json();
    if (d.code !== 100000) throw new Error(d.msg || '接口返回错误');
    
    var datas = (d.data && d.data.datas) || [];
    var nv1 = 0, nv2 = 0;
    var tbody = document.getElementById('tbl_body');
    tbody.innerHTML = '';
    
    datas.slice(0, 50).forEach(r => {{
      if (CFG.metric === '报销单') {{
        var tp = parseFloat(r.totalprice||0), wh = parseFloat(r.waitHxPrice||0);
        nv1 += tp; nv2 += wh;
        tbody.innerHTML += '<tr><td class="mono">' + (r.budgetNo||'—') + '</td><td>' + (r.applyUserName||'—') + '</td><td>' + (r.departmentName||'—') + '</td><td class="num">¥' + fmt(tp) + '</td><td class="num">¥' + fmt(wh) + '</td><td><span class="badge">' + (r.statusName||'—') + '</span></td></tr>';
      }} else {{
        var bt = parseFloat(r.budgetTotal||0), ua = parseFloat(r.usedAmount||0);
        var rem = bt - ua, p = bt > 0 ? Math.min(100, Math.round(ua/bt*100)) : 0;
        nv1 += bt; nv2 += ua;
        tbody.innerHTML += '<tr><td>' + (r.ewecomFepartmentName||'—') + '</td><td class="num">¥' + fmt(bt) + '</td><td class="num">¥' + fmt(ua) + '</td><td class="num' + (rem<0?' danger-text':'') + '">¥' + fmt(rem) + '</td><td><div class="prog-wrap"><div class="prog-fill' + (p>80?' prog-warn':'') + '" style="width:' + p + '%"></div></div><span class="prog-label">' + p + '%</span></td></tr>';
      }}
    }});

    document.getElementById('kv1').textContent = '¥' + Math.round(nv1).toLocaleString();
    document.getElementById('kv2').textContent = '¥' + Math.round(nv2).toLocaleString();
    document.getElementById('kv_diff').textContent = '¥' + Math.round(Math.abs(nv1-nv2)).toLocaleString();
    document.getElementById('kv_pct').textContent = (nv1>0 ? Math.round(nv2/nv1*100) : 0) + '%';
    
    document.getElementById('sv_period').textContent = start + ' ~ ' + end;
    document.getElementById('sv_v1').textContent = '¥' + fmt(nv1);
    document.getElementById('sv_v2').textContent = '¥' + fmt(nv2);
    document.getElementById('sv_pct').textContent = (nv1>0 ? Math.round(nv2/nv1*100) : 0) + '%';
    
    renderAll(nv1, nv2, datas);
    msg.textContent = '✅ 已同步最新数据';
  }} catch(e) {{
    msg.textContent = '❌ 查询异常: ' + e.message;
  }} finally {{
    btn.disabled = false; btn.textContent = '🔍 重新查询';
  }}
}}
</script>
</body>
</html>"""


# ==================== OpenClaw 主入口 ====================
def handle(command: str, args: list, **kwargs) -> str:
    user_id = kwargs.get("user_id", kwargs.get("sender_id", "default_user"))
    ctx = load_session(user_id)
    cmd = command.strip().lstrip("/")
    full_text = (cmd + " " + " ".join(args)).strip()

    def _auto_init() -> str | None:
        if ctx.get("initialized"): return None
        systems = api_get_supported_systems()
        if not systems: return "❌ 网络异常，暂时无法连接业务系统，请稍后再试或联系管理员。"
        ctx["initialized"] = True
        save_session(user_id, ctx)
        lines = ["🔐 **已完成身份鉴权。**\n\n请选择您要查询的业务板块：\n"]
        for s in systems: lines.append(f"- **{s.get('system_name')}**")
        lines.append("\n> 回复「切换系统 <名称>」即可进入，例如：`切换系统 供应链系统`")
        return "\n".join(lines)

    if cmd == "系统列表":
        init_msg = _auto_init()
        if init_msg: return init_msg
        systems = api_get_supported_systems()
        if not systems: return "❌ 获取业务板块失败，请联系管理员。"
        curr = ctx.get("system_name")
        lines = ["📋 **当前接入的业务板块：**\n"]
        for s in systems:
            mark = " ✅（当前所处）" if curr == s.get("system_name") else ""
            lines.append(f"- **{s.get('system_name')}**{mark}")
        lines.append("\n> 回复「切换系统 <名称>」进入")
        return "\n".join(lines)

    if cmd.startswith("切换系统"):
        init_msg = _auto_init()
        if init_msg: return init_msg
        if not args: return "❌ 请指定业务板块，例如：`切换系统 E网`"
        target = args[0]
        systems = api_get_supported_systems()
        target_sys = next((s for s in systems if s.get("system_name") == target), None)
        if not target_sys: return f"❌ 未找到板块「{target}」。"
        
        sys_id = target_sys.get("id")
        auth_data = api_get_system_token(sys_id)
        if not auth_data: return f"❌ 进入「{target}」失败：访问凭证拒绝，请联系管理员。"
        
        api_list = api_get_registry(sys_id)
        ctx.update({"system_name": target, "system_id": sys_id, "system_auth_headers": auth_data, "api_registry": api_list})
        save_session(user_id, ctx)
        metrics = get_friendly_metrics(api_list)
        lines = [f"✅ 已为您切入 **{target}** 业务域，当前支持以下智能检索：\n"]
        for m in metrics: lines.append(f"🔹 **{m['label']}** （{m['desc']}）")
        lines.append("\n> 💡 您现在可以直接问我了，例如：「查询本月的所有费用报销」")
        return "\n".join(lines)

    if cmd in ["初始化", "金灯塔BI 初始化"]:
        ctx["initialized"] = False
        save_session(user_id, ctx)
        return _auto_init() or "✅ 初始化流已重置。"

    QUERY_KEYWORDS = ["报表", "数据看板", "BI", "统计", "分析", "查询", "报销", "预算", "费用", "明细", "趋势", "度量"]
    if any(kw in full_text for kw in QUERY_KEYWORDS):
        init_msg = _auto_init()
        if init_msg: return init_msg

        system = ctx.get("system_name")
        if not system:
            return "⚠️ 您还未选择具体的业务板块，请先发送「系统列表」并进入相关域。"

        start_date, end_date, time_range = parse_time_keywords(full_text)
        if not start_date:
            return "⚠️ 请在指令中补充明确的统计时间范围，例如：**本月**、**上个月**、**上周**。"

        metric_info = resolve_metric(full_text)
        if not metric_info:
            return f"⚠️ 在【{system}】中未识别到明确的业务指标，请说明具体要看什么（如：报销单、部门预算）。"

        metric_key, metric_label = metric_info["key"], metric_info["label"]
        headers = {"Content-Type": "application/json"}
        headers.update(ctx.get("system_auth_headers", {}))

        val1 = val2 = 0.0
        val1_label = val2_label = api_url = ""
        table_rows = []

        try:
            if metric_key == "部门周期预算":
                api_url = "https://e.asagroup.cn/asae-e/yearBudget/query"
                params = {"method": "ALL", "pageNo": 1, "pageSize": 50, "startTime": start_date, "endTime": end_date}
                resp = requests.get(api_url, headers=headers, params=params, timeout=10).json()
                if resp.get("code") != 100000: return f"❌ 查询失败：{resp.get('msg', '未知业务异常')}"
                datas = resp.get("data", {}).get("datas", [])
                val1 = sum(safe_float(r.get("budgetTotal")) for r in datas)
                val2 = sum(safe_float(r.get("usedAmount")) for r in datas)
                val1_label, val2_label = "预算总额", "已用金额"
                table_rows = datas

            elif metric_key == "报销单":
                api_url = "https://e.asagroup.cn/asae-e/bx"
                params = {"method": "ALL", "pageNo": 1, "pageSize": 50, "createStime": start_date, "createEtime": end_date}
                resp = requests.get(api_url, headers=headers, params=params, timeout=10).json()
                if resp.get("code") != 100000: return f"❌ 查询失败：{resp.get('msg', '未知业务异常')}"
                datas = resp.get("data", {}).get("datas", [])
                val1 = sum(safe_float(r.get("totalprice")) for r in datas)
                val2 = sum(safe_float(r.get("waitHxPrice")) for r in datas)
                val1_label, val2_label = "报销总额", "待核销金额"
                table_rows = datas

        except Exception as e:
            return f"❌ 业务网络层抛出异常，请联系架构师排查。（{e}）"

        html = generate_html_report(
            system, metric_label, metric_key, time_range, start_date, end_date,
            val1_label, val1, val2_label, val2, table_rows, api_url, ctx.get("system_auth_headers", {})
        )
        
        preview_url = api_upload_html_to_oss(html)
        if not preview_url: return "❌ 数据分析完毕，但在为您生成云端可视化研报时发生存储级错误，操作已阻断。"

        ctx["last_report_url"] = preview_url
        ctx["last_report_title"] = f"{system} · {metric_label} 核心看板"
        save_session(user_id, ctx)

        used_pct = round(val2 / val1 * 100) if val1 > 0 else 0
        return (
            f"📊 **{ctx['last_report_title']}**\n"
            f"⏱️ 分析周期：{time_range} ({start_date} ~ {end_date})\n\n"
            f"🔹 **{val1_label}**：¥{val1:,.2f}\n"
            f"🔹 **{val2_label}**：¥{val2:,.2f}\n"
            f"🔹 **综合进度**：{used_pct}%\n\n"
            f"🔗 [🌐 点击进入动态数据空间（支持自主时间下钻）]({preview_url})\n\n"
            f"> 💡 数据流已封装完毕，回复「发布」可将此空间挂载至系统长期看板。"
        )

    if any(kw in full_text for kw in ["发布", "保存", "固化"]):
        if not ctx.get("last_report_url"): return "⚠️ 当前内存栈中没有可发布的数据空间，请先发起一项查询任务。"
        ok, result = api_publish_report(ctx["last_report_url"], ctx.get("last_report_title", ""))
        if ok: return f"✅ **知识库归档成功**\n\n空间《{ctx.get('last_report_title')}》已被永久固化。\n🔗 访问矩阵链接：{result}"
        return f"❌ 固化发布发生网络异常：{result}"

    init_msg = _auto_init()
    if init_msg: return init_msg
    return "未能从您的表述中解析出明确的数据流向指令，请尝试告知具体意图，例如：「提取上周的部门预算度量信息」。"