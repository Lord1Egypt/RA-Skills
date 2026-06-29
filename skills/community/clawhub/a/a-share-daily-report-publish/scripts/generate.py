#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股每日复盘报告生成器 v6
读取 report_data.json + template.html → 输出 a-share-report-YYYY-MM-DD.html
"""
import json, sys, os, re
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 模板路径：优先从脚本同级 assets/ 目录读取，fallback 到 skill 安装目录
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(_SCRIPT_DIR, '..', 'assets', 'template.html')
if not os.path.isfile(TEMPLATE_PATH):
    TEMPLATE_PATH = os.path.expanduser("~/.workbuddy/skills/a-share-daily-report/template.html")

# ═══════════════════════════════════════════════
# 数据来源标签
# ═══════════════════════════════════════════════

_SRC_COLORS = {
    "通达信MCP": "#f85149",
    "同花顺问财": "#58a6ff",
    "东方财富": "#d29922",
    "数据驱动": "#8b949e",
    "综合分析": "#8b949e",
    "预估数据": "#d29922",
}

# 每个模块的默认数据来源（report_data.json 中 data_sources 可覆盖）
_DEFAULT_SOURCES = {
    "indices": "通达信MCP",
    "advance_decline": "通达信MCP",
    "renqi": "同花顺问财",
    "seal_rate": "通达信MCP",
    "limit_down": "通达信MCP",
    "sentiment": "通达信MCP",
    "emotion_monitor": "通达信MCP",
    "ladder": "通达信MCP",
    "sector": "同花顺问财",
    "mainline": "通达信MCP",
    "zt_review": "通达信MCP",
    "zb_analysis": "通达信MCP",
    "strategy": "数据驱动",
    "outlook": "综合分析",
    "turnover": "同花顺问财",
    "decline": "同花顺问财",
    "fund": "同花顺问财",
    "core_stocks": "通达信MCP",
    "margin": "同花顺问财",
    "tracking": "通达信MCP",
    "mindset": "数据驱动",
    "special_events": "通达信MCP",
    "sector_flow": "同花顺问财",
}

def get_src(d, key):
    """从 data 读取模块实际来源，未配置则用默认值"""
    actual = d.get("data_sources", {}).get(key, "")
    return actual if actual else _DEFAULT_SOURCES.get(key, "综合分析")

def src(source):
    """生成数据来源标签HTML"""
    c = _SRC_COLORS.get(source, "#8b949e")
    return f'<span style="font-size:11px;color:{c};background:{c}15;padding:2px 8px;border-radius:4px;margin-left:6px;">{source}</span>'

def src_from(d, key):
    """快捷方式：从数据字典读取来源并生成标签HTML"""
    return src(get_src(d, key))

# ═══════════════════════════════════════════════
# 通用卡片样式（统一背景+圆角）
# ═══════════════════════════════════════════════

_CARD = 'background:#21262d;border-radius:8px;padding:12px;text-align:center;'

def card(label, value, value_style="", sub=""):
    """通用指标卡片"""
    sub_html = f'<div style="font-size:11px;color:#8b949e;">{sub}</div>' if sub else ""
    return f'<div style="{_CARD}"><div style="font-size:12px;color:#8b949e;">{label}</div><div style="font-size:22px;font-weight:700;{value_style}">{value}</div>{sub_html}</div>'

# ═══════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════

def fmt_amt(v):
    """格式化金额：亿/万"""
    if v is None: return "-"
    v = float(v)
    av = abs(v)
    if av >= 1e12: return f"{v/1e12:.2f}万亿"
    if av >= 1e8: return f"{v/1e8:.2f}亿"
    if av >= 1e4: return f"{v/1e4:.0f}万"
    return f"{v:.0f}"

def fmt_flow(v):
    """格式化资金流向（带正负号），统一转亿元"""
    if v is None: return "-"
    v = float(v)
    yi = v / 1e8
    if yi == 0:
        return "0"
    sign = "+" if v > 0 else ""
    return f"{sign}{yi:.2f}"

def fmt_pct(v):
    """格式化百分比"""
    if v is None: return "-"
    v = float(v)
    return f"+{v:.2f}%" if v > 0 else f"{v:.2f}%"

def cls(v):
    """涨跌CSS类: up/down"""
    return "up" if float(v) >= 0 else "down"

def arrow(v):
    """涨跌箭头"""
    return "▲" if float(v) >= 0 else "▼"

def tag_html(v):
    """资金流向HTML（带颜色），统一转亿元"""
    v = float(v)
    c = "#3fb950" if v >= 0 else "#f85149"
    return f'<span style="color:{c};">{fmt_flow(v)}</span>'

def board_type_tag(bt):
    """板型标签"""
    if bt in ("一字", "一字板"):
        return '<span style="color:#3fb950;font-size:10px;">一字</span>'
    if bt in ("T字", "T字板"):
        return '<span style="color:#d29922;font-size:10px;">T字</span>'
    return ""

# ═══════════════════════════════════════════════
# 公共数据提取（消除重复计算）
# ═══════════════════════════════════════════════

class DataContext:
    """缓存常用计算结果，避免各模块重复计算"""
    def __init__(self, d):
        self.d = d
        lb = d['lianban']
        self.lb_total = sum(v for k, v in lb.items() if int(k) >= 2)
        self.max_board = max((int(k) for k, v in lb.items() if v > 0), default=1)
        self.touch = d['zt_total'] + d['zb_total']
        self.zr = round(d['zb_total'] / max(self.touch, 1) * 100)
        self.sr = d.get('seal_rate', 50)
        # 空间板代表
        lb_detail = d.get('lianban_detail', {})
        self.top_reps = []
        for k in sorted(lb_detail.keys(), key=int, reverse=True):
            if lb_detail[k]:
                self.top_reps = [s['name'] for s in lb_detail[k][:2]]
                break
        self.top_reps_str = ' / '.join(self.top_reps) if self.top_reps else '—'
        # 连板详情字符串
        self.lb_detail_str = '+'.join(
            [f'{k}板{v}' for k, v in sorted(lb.items(), key=lambda x: int(x[0])) if int(k) >= 2 and v > 0]
        )
        # 晋级率
        jinji_parts = []
        for i in range(2, self.max_board + 1):
            prev = lb.get(str(i-1), 0)
            curr = lb.get(str(i), 0)
            if prev > 0:
                jinji_parts.append(f"{i-1}进{i} {round(curr/prev*100)}%")
        self.jinji_str = " / ".join(jinji_parts) if jinji_parts else "数据不足"
        # 情绪周期
        if self.sr >= 75 and d['nonst_dt'] <= 5:
            self.cycle = "主升期 → 高位博弈"
            self.cycle_color = "#f0883e"
        elif self.sr >= 60:
            self.cycle = "上升期 → 活跃"
            self.cycle_color = "#3fb950"
        elif self.sr >= 40:
            self.cycle = "震荡期 → 分化"
            self.cycle_color = "#d29922"
        else:
            self.cycle = "退潮期 → 谨慎"
            self.cycle_color = "#f85149"

# ═══════════════════════════════════════════════
# 模块生成器
# ═══════════════════════════════════════════════

def gen_header(d):
    """模块1: Header"""
    date = d['date']
    wd = d['weekday']
    tl = d['time_label']
    tc = d['time_cutoff']
    mt = d.get('market_tag', '')
    ms = d.get('market_summary', '')
    return f'''<div class="header">
    <h1>📊 A股市场复盘报告</h1>
    <div class="date">📅 {date[:4]}年{date[5:7]}月{date[8:10]}日（{wd}）· {tl} · 数据截至{tc} · 来源：通达信 / 东方财富 / 同花顺问财</div>
    <div class="tags">
      <span class="tag">{tl}</span>
      <span class="tag">A股市场</span>
      <span class="tag">短线情绪</span>
      <span class="tag">收盘数据</span>
      <span class="tag" style="border-color:#d29922;color:#d29922;">⚡ {mt} · {ms}</span>
    </div>
  </div>'''

def gen_index_cards(d):
    """模块2: 4指数卡片"""
    idx = d['indices']
    cards = ""
    for key, name in [("sh","上证指数"),("sz","深证成指"),("cy","创业板指"),("kc","科创50")]:
        v = idx[key]
        p, c = v['price'], v['chg']
        cards += f'''    <div class="card">
      <div class="label">{name}</div>
      <div class="value {cls(c)}">{p:.2f}</div>
      <div class="sub {cls(c)}">{fmt_pct(c)} {arrow(c)}</div>
    </div>
'''
    return f'  <div class="section"><div style="display:flex;align-items:center;margin-bottom:12px;"><span style="font-size:17px;font-weight:700;">📈 四大指数</span>{src_from(d, "indices")}</div>\n<div class="cards">\n{cards}  </div></div>'

def gen_advance_decline(d, ctx):
    """模块3: 涨跌家数概览"""
    ad = d['advance_decline']
    adv = ad.get('total_adv', ad['sh_adv'] + ad['sz_adv'])
    dec = ad.get('total_dec', ad['sh_dec'] + ad['sz_dec'])
    flat = ad.get('total_flat', ad['sh_flat'] + ad['sz_flat'])
    has_total = 'total_adv' in ad
    ratio = round(adv / max(dec, 1), 2)
    pct = round(adv / max(adv + dec + flat, 1) * 100, 1)
    ta = fmt_amt(d['total_amount'])
    ac = d.get('amount_change', '')
    source_label = "通达信全市场" if has_total else "沪深合计"
    sh_total = ad['sh_adv'] + ad['sh_dec'] + ad['sh_flat']
    sz_total = ad['sz_adv'] + ad['sz_dec'] + ad['sz_flat']
    bj_count = adv + dec + flat - sh_total - sz_total if has_total else 0
    split_info = f"沪{sh_total}+深{sz_total}" + (f"+北交{bj_count}" if bj_count > 0 else "")
    # 统一用src()
    source_tag = src(source_label) if has_total else src_from(d, "advance_decline")
    return f'''<div class="section">
    <div class="section-title"><span class="icon">📊</span> 涨跌家数概览 {source_tag}</div>
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;text-align:center;">
      {card("上涨家数", adv, "color:#f85149;", f"沪{ad['sh_adv']}+深{ad['sz_adv']}")}
      {card("下跌家数", dec, "color:#3fb950;", f"沪{ad['sh_dec']}+深{ad['sz_dec']}")}
      {card("平盘家数", flat, "color:#8b949e;", f"沪{ad['sh_flat']}+深{ad['sz_flat']}")}
      {card("涨跌比", ratio, "color:#f0883e;", f"{adv}/{dec}")}
      {card("沪深总成交", ta, "color:#d29922;", ac)}
      {card("上涨占比", f"{pct}%", "color:#f85149;", f"{adv}/{adv+dec+flat} · {'多头主导' if ratio > 1 else '空头主导'}")}
    </div>
    <div style="margin-top:8px;font-size:11px;color:#6e7681;text-align:right;">{split_info} · 全市场共{adv+dec+flat}只</div>
  </div>'''

def gen_popularity(d):
    """模块4: 人气龙头Top10"""
    top = d.get('renqi_top', [])
    if not top:
        return '<div class="section"><div class="section-title"><span class="icon">👑</span> 短线人气龙头 Top10 ' + src_from(d, "renqi") + '</div><div style="padding:20px;color:#8b949e;text-align:center;">暂无数据</div></div>'
    rows = ""
    for i, s in enumerate(top[:10], 1):
        rk_cls = "#d29922" if i <= 3 else "#8b949e"
        rk_fw = "700" if i <= 3 else "600"
        tags = s.get('tags', '')
        tag_html_str = ' · '.join([f'<span style="color:#f85149;font-size:11px;">{t}</span>' for t in tags.split('·')]) if tags else ''
        rows += f'''          <tr style="border-bottom:1px solid #21262d;">
            <td style="padding:8px 8px;text-align:center;color:{rk_cls};font-weight:{rk_fw};">{i}</td>
            <td style="padding:8px 8px;color:#58a6ff;">{s.get('code','')}</td>
            <td style="padding:8px 8px;color:#f0f6fc;font-weight:600;">{s.get('name','')}</td>
            <td style="padding:8px 8px;text-align:right;color:#f0f6fc;">{s.get('price','-')}</td>
            <td style="padding:8px 8px;text-align:right;color:{"#f85149" if float(s.get('chg',0)) >= 0 else "#3fb950"};font-weight:600;">{fmt_pct(s.get('chg',0))}</td>
            <td style="padding:8px 8px;text-align:right;color:{"#d29922" if float(s.get('turnover_rate',0)) > 5 else "#8b949e"};">{s.get('turnover_rate','-')}%</td>
            <td style="padding:8px 8px;text-align:right;">{s.get('volume_ratio','-')}</td>
            <td style="padding:8px 8px;text-align:right;color:#f0f6fc;">{s.get('market_cap','-')}</td>
            <td style="padding:8px 8px;color:#8b949e;">{tag_html_str}</td>
          </tr>
'''
    return f'''<div class="section">
    <div class="section-title"><span class="icon">👑</span> 短线人气龙头 Top10 {src_from(d, "renqi")}</div>
    <div style="overflow-x:auto;">
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="border-bottom:2px solid #30363d;color:#8b949e;">
            <th style="padding:8px 8px;text-align:center;">排名</th>
            <th style="padding:8px 8px;text-align:left;">代码</th>
            <th style="padding:8px 8px;text-align:left;">名称</th>
            <th style="padding:8px 8px;text-align:right;">最新价</th>
            <th style="padding:8px 8px;text-align:right;">涨跌幅</th>
            <th style="padding:8px 8px;text-align:right;">换手率</th>
            <th style="padding:8px 8px;text-align:right;">量比</th>
            <th style="padding:8px 8px;text-align:right;">总市值</th>
            <th style="padding:8px 8px;text-align:left;">题材标签</th>
          </tr>
        </thead>
        <tbody>
{rows}        </tbody>
      </table>
    </div>
  </div>'''

def gen_seal_rate(d, ctx):
    """模块5: 涨停封板率核心指标卡"""
    zt = d['zt_total']
    fst = d['fst_zt']
    st = d['st_zt']
    ts = d['ts_zt']
    zb = d['zb_total']
    touch = ctx.touch
    sr = ctx.sr
    zr = ctx.zr
    cy = d.get('cy_zt', 0)
    kc = d.get('kc_zt', 0)
    lb_total = ctx.lb_total
    max_board = ctx.max_board
    st_detail = d.get('st_zt_detail', f'ST {st}只')

    return f'''<div class="section">
    <div class="section-title"><span class="icon">📊</span> 涨停封板率核心指标 {src_from(d, "seal_rate")}</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:10px;">
      {card("🎯 触及涨停", touch, "color:#d29922;", f"封板{zt}+炸板{zb}")}
      {card("✅ 封板", zt, "color:#f85149;", f"非ST {fst} + ST {st} + 退市 {ts}")}
      {card("📊 涨停封板率", f"{sr}%", "color:#58a6ff;", f"{zt}/{touch} · {'封板率强' if sr >= 75 else '封板率中等' if sr >= 60 else '封板率弱'}")}
      {card("💥 炸板", zb, "color:#d29922;", f"只 · 炸板率{zr}% {'偏高' if zr > 30 else '正常' if zr > 20 else '偏低'}")}
    </div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;">
      {card("🔴 非ST涨停", fst, "color:#f85149;", "主板10%/创科创20%")}
      {card("🟡 ST涨停", st, "color:#d29922;", st_detail)}
      {card("⚫ 退市整理涨停", ts, "color:#8b949e;", "—")}
      {card("创业板 / 科创", f"{cy} / {kc}", "color:#bc8cff;", "只 · 20cm涨停")}
      {card("🏆 连板总数", lb_total, "color:#f0883e;", f"只 · 空间板{max_board}板")}
    </div>
  </div>'''

def gen_limit_down(d):
    """模块6: 跌停专题"""
    dt = d['dt_total']
    st_dt = d['st_dt']
    nonst_dt = d['nonst_dt']
    panic = "极低 · 市场无恐慌" if nonst_dt <= 3 else "较低 · 风险可控" if nonst_dt <= 7 else "偏高 · 需警惕" if nonst_dt <= 15 else "高 · 市场恐慌"

    dt_stocks = d.get('dt_stocks', [])
    nonst_html = ""
    st_html = ""
    for s in dt_stocks:
        line = f'<span class="badge badge-cold">跌停</span> <b>{s["name"]}</b> {s["code"]} <span style="color:#3fb950;">{fmt_pct(s["chg"])}</span>'
        if s.get('reason'): line += f' · {s["reason"]}'
        if s.get('board_type'): line += f' · {s["board_type"]}'
        if s.get('lianban_days', 1) > 1: line += f' · {s["lianban_days"]}连跌停'
        if s.get('is_st'):
            st_html += f'<div style="padding:4px 0;border-bottom:1px solid #21262d;color:#8b949e;">{line}</div>'
        else:
            nonst_html += f'<div style="padding:4px 0;border-bottom:1px solid #21262d;">{line}</div>'

    detail_html = ""
    if nonst_html or st_html:
        detail_html = f'''    <div style="margin-top:14px;font-size:12px;">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
        <div>
          <h4 style="color:#d29922;margin-bottom:6px;font-size:13px;">⚠ 非ST跌停（重点监控）</h4>
          {nonst_html or '<div style="color:#8b949e;">无</div>'}
        </div>
        <div>
          <h4 style="color:#8b949e;margin-bottom:6px;font-size:13px;">ST跌停（{st_dt}只·常规风险）</h4>
          {st_html or '<div style="color:#8b949e;">无</div>'}
        </div>
      </div>
    </div>'''

    panic_color = "#3fb950" if nonst_dt <= 7 else "#f85149"
    return f'''<div class="section">
    <div class="section-title"><span class="icon">⛔</span> 跌停专题 {src_from(d, "limit_down")}</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;text-align:center;">
      {card("跌停家数", dt, "color:#3fb950;font-size:26px;", "")}
      {card("ST跌停", st_dt, "color:#f85149;font-size:26px;", "")}
      {card("非ST跌停", nonst_dt, "color:#d29922;font-size:26px;", "")}
      <div style="background:#21262d;border-radius:8px;padding:14px;text-align:center;">
        <div style="font-size:14px;font-weight:600;color:{panic_color};margin-top:4px;">{panic}</div>
        <div style="font-size:11px;color:#8b949e;">非ST仅{nonst_dt}只</div>
      </div>
    </div>
{detail_html}
  </div>'''

def gen_sentiment(d, ctx):
    """模块7: 短线情绪全景"""
    sr = ctx.sr
    cy = d.get('cy_zt', 0)
    kc = d.get('kc_zt', 0)

    sr_color = "#3fb950" if sr >= 70 else "#d29922" if sr >= 50 else "#f85149"
    sr_label = "偏强" if sr >= 70 else "中等" if sr >= 50 else "偏弱"

    return f'''<div class="section">
    <div class="section-title"><span class="icon">⚡</span> 短线情绪全景 {src_from(d, "sentiment")}</div>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;text-align:center;margin-bottom:16px;">
      <div style="background:#21262d;border-radius:8px;padding:14px;">
        <div style="font-size:12px;color:#8b949e;">连板总数</div>
        <div style="font-size:24px;font-weight:700;color:#e1e8ed;margin-top:4px;">{ctx.lb_total}</div>
        <div style="font-size:11px;color:#f85149;">{ctx.lb_detail_str or "—"}</div>
      </div>
      <div style="background:#21262d;border-radius:8px;padding:14px;">
        <div style="font-size:12px;color:#8b949e;">空间板</div>
        <div style="font-size:24px;font-weight:700;color:#f85149;margin-top:4px;">{ctx.max_board}板</div>
        <div style="font-size:11px;color:#8b949e;">{ctx.top_reps_str}</div>
      </div>
      <div style="background:#21262d;border-radius:8px;padding:14px;">
        <div style="font-size:12px;color:#8b949e;">封板率</div>
        <div style="font-size:24px;font-weight:700;color:{sr_color};margin-top:4px;">{sr}%</div>
        <div style="font-size:11px;color:{sr_color};">{sr_label}</div>
      </div>
      <div style="background:#21262d;border-radius:8px;padding:14px;">
        <div style="font-size:12px;color:#8b949e;">昨板表现</div>
        <div style="font-size:24px;font-weight:700;color:#8b949e;margin-top:4px;">—</div>
        <div style="font-size:11px;color:#8b949e;">暂无数据</div>
      </div>
      <div style="background:#21262d;border-radius:8px;padding:14px;">
        <div style="font-size:12px;color:#8b949e;">创/科创</div>
        <div style="font-size:24px;font-weight:700;color:#e1e8ed;margin-top:4px;">{cy}/{kc}</div>
        <div style="font-size:11px;color:#8b949e;">创业板{cy}只/科创{kc}只</div>
      </div>
    </div>
  </div>'''

def gen_emotion_monitor(d, ctx):
    """模块8: 情绪监测 & 极端值"""
    zr = ctx.zr
    dt = d['dt_total']
    nonst_dt = d['nonst_dt']
    zt = d['zt_total']
    zb = d['zb_total']
    sr = ctx.sr

    zr_color = "#3fb950" if zr <= 25 else "#d29922" if zr <= 35 else "#f85149"
    zr_label = "偏低 打板安全边际高" if zr <= 25 else "正常" if zr <= 35 else "偏高 注意风险"
    dt_color = "#3fb950" if dt <= 10 else "#d29922" if dt <= 20 else "#f85149"

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🚨</span> 情绪监测 & 极端值 {src_from(d, "emotion_monitor")}</div>
    <div class="sentiment-grid">
      <div class="sentiment-item">
        <div class="s-label">炸板率</div>
        <div class="s-value" style="color:{zr_color};">{zr}%</div>
        <div style="font-size:12px;color:{zr_color};margin-top:4px;">{zr_label}</div>
      </div>
      <div class="sentiment-item">
        <div class="s-label">跌停家数</div>
        <div class="s-value" style="color:{dt_color};">{dt}</div>
        <div style="font-size:12px;color:#d29922;margin-top:4px;">非ST仅{nonst_dt}只 {"恐慌度极低" if nonst_dt <= 5 else "风险可控"}</div>
      </div>
      <div class="sentiment-item">
        <div class="s-label">连板晋级率</div>
        <div class="s-value" style="color:#58a6ff;">分化明显</div>
        <div style="font-size:12px;color:#d29922;margin-top:4px;">{ctx.jinji_str}</div>
      </div>
      <div class="sentiment-item">
        <div class="s-label">空间高度</div>
        <div class="s-value" style="color:#f0883e;">{ctx.max_board}板</div>
        <div style="font-size:12px;color:#f85149;margin-top:4px;">{ctx.top_reps_str}</div>
      </div>
      <div class="sentiment-item">
        <div class="s-label">封板数 / 炸板数</div>
        <div class="s-value" style="color:#e1e8ed;">{zt} / {zb}</div>
        <div style="font-size:12px;color:{"#3fb950" if sr >= 60 else "#d29922"};margin-top:4px;">{"封板充足" if sr >= 60 else "封板偏弱"}</div>
      </div>
      <div class="sentiment-item">
        <div class="s-label">情绪周期判断</div>
        <div class="s-value" style="color:{ctx.cycle_color};font-size:17px;">{ctx.cycle}</div>
        <div style="font-size:12px;color:#d29922;margin-top:4px;">空间板{ctx.max_board}板，{ctx.top_reps_str}</div>
      </div>
    </div>
  </div>'''

def gen_ladder(d, ctx):
    """模块9: 连板天梯"""
    lb = d['lianban']
    lb_detail = d.get('lianban_detail', {})
    zt_total = d['zt_total']

    rows = ""
    for level in range(1, 7):
        key = str(level)
        count = lb.get(key, 0)
        label = "首板" if level == 1 else f"{level}连板"

        if level >= 5 and count == 0:
            if all(lb.get(str(l), 0) == 0 for l in range(level, 7)):
                rows += f'        <tr><td style="font-weight:600;">{label}</td><td>0只</td><td>—</td><td>—</td><td>—</td><td style="color:#f85149;">空间高度受限 {level}板未突破</td></tr>\n'
                break
            continue

        detail = lb_detail.get(key, [])
        if detail:
            reps = ' / '.join([f'{s["name"]}({s.get("board_type","")})' for s in detail[:10]])
            if len(detail) > 10:
                reps += f' 等{len(detail)}只'
            bt_set = set(s.get('board_type', '换手') for s in detail)
            bt_str = '+'.join(bt_set) if bt_set else '—'
            themes = set()
            for s in detail:
                concepts = s.get('concepts', '')
                if concepts:
                    for c in concepts.split('.'):
                        if c.strip(): themes.add(c.strip())
                else:
                    for t in _split_reasons(s.get('reason', ''))[:2]:
                        if t: themes.add(t)
            theme_str = '/'.join(list(themes)[:5]) if themes else '—'
        else:
            reps = bt_str = theme_str = '—'

        if level == 1 and count > 0:
            signal = f'<span style="color:#d29922;">首板基数{count}只 {"不错" if count >= 30 else "一般"}</span>'
        elif count == 0:
            signal = '<span style="color:#f85149;">—</span>'
        elif count >= 10:
            signal = '<span style="color:#3fb950;">接力极其活跃 基数庞大</span>'
        elif count >= 5:
            signal = '<span style="color:#3fb950;">接力活跃</span>'
        elif count >= 2:
            signal = '<span style="color:#d29922;">正常</span>'
        else:
            signal = '<span style="color:#f0883e;">断层风险</span>'

        rows += f'        <tr><td style="font-weight:600;">{label}</td><td>{count}只</td><td>{reps}</td><td>{bt_str}</td><td>{theme_str}</td><td>{signal}</td></tr>\n'

    calc_total = sum(lb.values())
    verify = f'涨停总数{zt_total}只={"+".join([f"{k}连板{v}" for k,v in sorted(lb.items(), key=lambda x:int(x[0]))])}={calc_total} {"✓验证通过" if calc_total == zt_total else "⚠不一致"}'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🏆</span> 连板天梯 {src_from(d, "ladder")}</div>
    <table class="jinji-table">
      <thead><tr><th>连板级别</th><th>数量</th><th>代表个股</th><th>板型</th><th>题材</th><th>信号解读</th></tr></thead>
      <tbody>
{rows}      </tbody>
    </table>
    <div style="margin-top:12px;padding:10px;background:#f8514910;border-radius:8px;font-size:13px;color:#f85149;">
      ⚠ <strong>核心观察：</strong>{verify}。空间板{ctx.max_board}板。
    </div>
  </div>'''

def gen_sector(d):
    """模块10: 板块涨跌榜Top5"""
    up = d.get('sector_up', [])
    down = d.get('sector_down', [])

    up_rows = ""
    for s in up[:5]:
        up_rows += f'          <tr><td>{s["name"]}</td><td class="positive">{fmt_pct(s["chg"])}</td><td>{tag_html(s.get("flow",0))}</td></tr>\n'

    down_rows = ""
    for s in down[:5]:
        down_rows += f'          <tr><td>{s["name"]}</td><td class="negative">{fmt_pct(s["chg"])}</td><td>{tag_html(s.get("flow",0))}</td></tr>\n'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🔥</span> 板块涨跌榜 Top5 {src_from(d, "sector")}</div>
    <div class="two-col">
      <div class="col">
        <h4 style="color:#f85149;">🔴 涨幅榜 Top5</h4>
        <table><tr><th>板块</th><th>涨幅</th><th>主力净流入</th></tr>
{up_rows}        </table>
      </div>
      <div class="col">
        <h4 style="color:#3fb950;">🟢 跌幅榜 Top5</h4>
        <table><tr><th>板块</th><th>跌幅</th><th>主力净流出</th></tr>
{down_rows}        </table>
      </div>
    </div>
  </div>'''

def gen_mainline(d, ctx):
    """模块11: 主线板块深度分析"""
    zt = d.get('zt_stocks', [])
    # 按涨停原因概念标签聚合（优先用concepts字段）
    theme_count = {}
    for s in zt:
        concepts = s.get('concepts', '')
        if concepts:
            # 概念标签用点号分隔
            for c in concepts.split('.'):
                c = c.strip()
                if c:
                    theme_count[c] = theme_count.get(c, 0) + 1
        else:
            # fallback到reason字段
            reason = s.get('reason', '其他')
            parts = _split_reasons(reason)
            for r in parts[:2]:
                r = r.strip()
                if r:
                    theme_count[r] = theme_count.get(r, 0) + 1

    top_themes = sorted(theme_count.items(), key=lambda x: -x[1])[:4]
    lines = []
    for i, (theme, count) in enumerate(top_themes, 1):
        lines.append(f'主线{i}·{theme}：<b style="color:#f85149;">{count}只涨停</b>')

    mainline_str = '        <span>' + '</span>\n        <span>'.join(lines) + '</span>'

    # 统计一字/换手 — 修复原bug：or优先级错误
    yizi = sum(1 for s in zt if s.get('board_type') in ('一字', '一字板'))
    huanshou = len(zt) - yizi

    main_themes = [t[0] for t in top_themes[:3]]
    analysis = f'今日核心主线：{"+".join(main_themes)}。涨停{d["zt_total"]}只，封板率{ctx.sr}%，{"市场偏强" if ctx.sr >= 70 else "市场分化" if ctx.sr >= 50 else "市场偏弱"}。'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🔶</span> 主线板块深度分析 · {"+".join(main_themes)} {src_from(d, "mainline")}</div>
    <div style="background:#21262d;border-radius:8px;padding:16px;margin-bottom:12px;">
      <div style="display:flex;gap:20px;flex-wrap:wrap;font-size:13px;margin-bottom:12px;">
{mainline_str}
        <span>最高板：<b style="color:#f85149;">{ctx.max_board}板</b></span>
        <span>一字板：<b>{yizi}只</b></span>
        <span>换手板：<b>{huanshou}只</b></span>
      </div>
      <div style="font-size:13px;color:#8b949e;line-height:1.8;">
        <b style="color:#e1e8ed;">核心逻辑：</b>{analysis}
      </div>
    </div>
  </div>'''

def _split_reasons(reason):
    """将涨停原因文本拆分为独立原因列表
    
    通达信tdx_screener返回的reason格式多样：
    - "reason1；reason2" (中文分号)
    - "reason1;reason2" (英文分号)
    - "main_reasonI1、detail1；\n2、detail2" (编号格式)
    - "reason1\n2、reason2" (换行编号)
    """
    if not reason:
        return []

    text = reason.strip()

    # 第1步：按编号标记切分（I1、I2、等 或 换行后的 1、2、等）
    # 先把 "I1、" "I2、" 等替换为统一的分隔符
    import re as _re
    text = _re.sub(r'I(\d+)、', r'§SPLIT§\1、', text)
    # 把换行后的 "1、" "2、" 编号也替换
    text = _re.sub(r'\n(\d+)、', r'§SPLIT§\1、', text)

    # 第2步：按中文/英文分号切分
    text = text.replace('；', '§SPLIT§').replace(';', '§SPLIT§')

    # 第3步：按句号切分（仅在句号后紧跟大段文字时）
    text = _re.sub(r'。(?=.{4,})', '§SPLIT§', text)

    # 第4步：拆分并清理
    parts = [p.strip() for p in text.split('§SPLIT§') if p.strip()]

    # 第5步：去除编号前缀（如 "1、" "2、"）
    cleaned = []
    for p in parts:
        p = _re.sub(r'^\d+、', '', p).strip()
        p = p.rstrip('。；;,、')
        if p:
            cleaned.append(p)

    return cleaned


def _extract_concept_tag(concepts, max_len=20):
    """从通达信'涨停原因'字段（点号分隔的概念标签）提取题材分组标签
    
    通达信返回的'涨停原因'格式如："PCB概念.锂电池概念" 或 "可控核聚变.人形机器人.华为概念"
    用点号分隔，取第一个概念标签作为分组依据。
    如果concepts字段为空，fallback到reason字段的_extract_theme_tag。
    """
    if not concepts:
        return '其他'
    # 点号分隔取第一个概念
    parts = [p.strip() for p in concepts.split('.') if p.strip()]
    if not parts:
        return '其他'
    tag = parts[0][:max_len].strip()
    while tag and tag[-1] in '，,；;。.、：:':
        tag = tag[:-1]
    return tag or '其他'


def _concepts_html(concepts):
    """将概念标签格式化为HTML展示：第一个高亮，其余标签式排列
    
    输入格式如："PCB概念.锂电池概念"
    输出：<span>PCB概念</span> <span>锂电池概念</span>
    """
    if not concepts:
        return ''
    parts = [p.strip() for p in concepts.split('.') if p.strip()]
    if not parts:
        return ''
    html = f'<span style="color:#d29922;font-weight:600;">{parts[0]}</span>'
    for p in parts[1:]:
        html += f' <span style="color:#8b949e;font-size:11px;background:#21262d;padding:1px 6px;border-radius:3px;">{p}</span>'
    return html


def _extract_theme_tag(reason, max_len=30):
    """从涨停原因长文本中提取题材关键词作为分组标签"""
    if not reason:
        return '其他'

    # 用_split_reasons拆分，取第一个有效片段
    parts = _split_reasons(reason)
    part = parts[0] if parts else reason.strip()

    # 去除常见噪声前缀
    noise_prefixes = [
        '据2026年', '据悉', '据报道', '消息指',
        '公司', '公告显示',
    ]
    for p in noise_prefixes:
        if part.startswith(p):
            part = part[len(p):].strip()

    # 截取指定长度
    tag = part[:max_len].strip()
    # 清理末尾标点
    while tag and tag[-1] in '，,；;。.、：:':
        tag = tag[:-1]
    return tag or '其他'


def _short_reason(reason, max_len=24):
    """提取题材短标签（用于股票行内显示）—— 取第一个原因前N字"""
    if not reason:
        return ''
    parts = _split_reasons(reason)
    primary = parts[0] if parts else reason
    # 截取并清理
    tag = primary[:max_len].strip()
    while tag and tag[-1] in '，,；;。.、':
        tag = tag[:-1]
    return tag


def _full_reason_html(reason):
    """将涨停原因格式化为HTML展示：第一个原因高亮，其余折行小字"""
    if not reason:
        return ''
    parts = _split_reasons(reason)
    if not parts:
        return ''
    # 第一个原因：加粗高亮
    html = f'<span style="color:#e1e8ed;font-weight:600;">{parts[0]}</span>'
    # 后续原因：折行小字
    if len(parts) > 1:
        rest = '；'.join(parts[1:])
        html += f'<span style="color:#8b949e;font-size:11px;"><br>↳ {rest}</span>'
    return html


def gen_zt_review(d):
    """模块12: 涨停板复盘·按题材分类（截图参考格式）"""
    zt = d.get('zt_stocks', [])
    if not zt:
        return '<div class="section"><div class="section-title"><span class="icon">🎯</span> 涨停板复盘 · 按题材分类 ' + src_from(d, "zt_review") + '</div><div style="padding:20px;color:#8b949e;">暂无涨停数据</div></div>'

    # 统计封板强度
    yizi_count = sum(1 for s in zt if s.get('board_type') in ('一字', '一字板'))
    tzi_count = sum(1 for s in zt if s.get('board_type') in ('T字', 'T字板'))
    hs_count = len(zt) - yizi_count - tzi_count  # 换手板
    wb_tail = sum(1 for s in zt if s.get('first_time', '').startswith('14') or s.get('first_time', '').startswith('9:3'))  # 尾盘/集合竞价封

    # 按概念标签分组（优先用concepts字段，fallback到reason）
    theme_groups = {}
    for s in zt:
        tag = _extract_concept_tag(s.get('concepts', '') or s.get('reason', ''))
        if tag not in theme_groups:
            theme_groups[tag] = []
        theme_groups[tag].append(s)

    # 动态分组：>=3只独立成组，其余归入"其他重要题材"
    major_groups = [(tag, stocks) for tag, stocks in sorted(theme_groups.items(), key=lambda x: -len(x[1])) if len(stocks) >= 3]
    minor_stocks = [s for tag, sl in theme_groups.items() if len(sl) < 3 for s in sl]
    if minor_stocks:
        major_groups.append(('其他重要题材', minor_stocks))

    # 分组图标和颜色
    icons = ['◆', '🔷', '🔶', '⚡', '🚀', '📦', '🏗️', '💊', '🌾']
    colors = ['#f85149', '#d29922', '#3fb950', '#58a6ff', '#bc8cff', '#f0883e', '#a371f7', '#39d353']

    grids = ""
    for i, (theme, stocks) in enumerate(major_groups):
        icon = icons[i % len(icons)]
        color = colors[i % len(colors)]

        items = ""
        for s in stocks[:10]:
            name = s["name"]
            code = s.get("code", "")
            chg = s.get("chg", 0)
            bt = s.get("board_type", '')
            # 连板标签
            lb_label = s.get('lianban_label', '') or (f"{s['lianban_days']}板" if s.get('lianban_days', 0) > 1 else "首板")
            # 封单金额
            seal_amt = f"封单{fmt_amt(s.get('seal_amount', 0))}" if s.get('seal_amount') else ""
            # 概念标签HTML（涨停原因字段，点号分隔的概念标签）
            concepts_html = _concepts_html(s.get('concepts', ''))
            # 原因揭秘HTML（详细叙事归因）
            reason_html = _full_reason_html(s.get('reason', ''))
            # 涨幅
            chg_str = fmt_pct(chg)
            # 开板次数
            ot = s.get('open_times', 0)
            extra = f" 开板{ot}次" if ot > 5 else ""
            # 板型标签
            bt_tag = board_type_tag(bt)

            # 归因行：优先显示概念标签，有原因揭秘则折行显示
            attribution = concepts_html
            if reason_html:
                attribution += f'<br><span style="color:#8b949e;font-size:11px;">↳ {reason_html}</span>'
            if not attribution:
                attribution = '<span style="color:#6e7681;">无归因</span>'

            items += f'''<div style="padding:5px 8px;border-bottom:1px solid #21262d30;">
            <div><span class="badge badge-seal">封板</span> <b>{name}</b> <span style="color:#58a6ff;font-size:11px;">{code}</span> {lb_label} {bt_tag} <span style="color:#f85149;font-weight:600;">{chg_str}</span> {seal_amt}{extra}</div>
            <div style="font-size:12px;line-height:1.6;margin-top:2px;padding-left:42px;">📌 {attribution}</div>
          </div>
'''

        more_hint = f' <span style="color:#8b949e;font-size:10px;">展示前10只/共{len(stocks)}只</span>' if len(stocks) > 10 else ''
        grids += f'''      <div>
        <h4 style="color:{color};margin-bottom:6px;font-size:13px;">{icon} {theme}（<b>{len(stocks)}</b>只涨停）{more_hint}</h4>
        <div style="font-size:12px;line-height:1.8;">
{items}        </div>
      </div>
'''

    # 炸板清单
    zb = d.get('zb_stocks', [])
    zb_html = ""
    for s in zb[:10]:
        concepts_html = _concepts_html(s.get("concepts",""))
        reason_html = _full_reason_html(s.get("reason",""))
        attribution = concepts_html
        if reason_html:
            attribution += f'<br><span style="color:#8b949e;font-size:11px;">↳ {reason_html}</span>'
        if not attribution:
            attribution = '<span style="color:#6e7681;">无归因</span>'
        zb_html += f'''<div style="padding:5px 8px;border-bottom:1px solid #21262d30;">
            <div><span class="badge badge-broken">炸板</span> <b style="color:#d29922;">{s["name"]}</b> <span style="color:#58a6ff;font-size:11px;">{s.get("code","")}</span> {fmt_pct(s.get("chg",0))} · 开板{s.get("open_times",0)}次</div>
            <div style="font-size:12px;line-height:1.6;margin-top:2px;padding-left:42px;">📌 {attribution}</div>
          </div>
'''

    zb_section = ""
    if zb_html:
        zr = round(d["zb_total"] / max(d["zt_total"] + d["zb_total"], 1) * 100)
        zb_more = f' <span style="color:#8b949e;font-size:10px;">展示前10只/共{d["zb_total"]}只</span>' if d["zb_total"] > 10 else ''
        zb_section = f'''      <div style="grid-column:1/-1;">
        <h4 style="color:#f85149;margin-bottom:6px;font-size:13px;">💥 今日炸板股（{d["zb_total"]}只 · 炸板率{zr}%）{zb_more}</h4>
        <div style="font-size:12px;line-height:1.8;">
{zb_html}        </div>
      </div>'''

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🎯</span> 涨停板复盘 · 按题材分类（含涨停归因） {src_from(d, "zt_review")}</div>
    <div style="background:#1c2128;border:1px solid #2d333b;border-radius:6px;padding:8px 12px;margin-bottom:12px;font-size:11px;color:#8b949e;line-height:1.8;">
      📌 <b style="color:#d29922;">涨停归因</b>来源：通达信tdx_screener涨停专题 · 封板判断：涨停打开次数+现价对比<br>
      📌 <b>封板强度</b>：一字板({yizi_count}只/开板0次) &gt; T字板({tzi_count}只/1次) &gt; 换手板({hs_count}只/多次开板/尾盘封板)
    </div>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;align-items:start;">
{grids}{zb_section}
    </div>
  </div>'''

def gen_zb_analysis(d, ctx):
    """模块13: 炸板深度分析"""
    zb = d.get('zb_stocks', [])
    zb_total = d['zb_total']
    zr = ctx.zr

    high_html = ""
    for s in zb[:8]:
        high_html += f'''<div class="zhaban-high" style="padding:6px 10px;border-radius:6px;margin-bottom:6px;">
            <b>{s["name"]}</b> {fmt_pct(s.get("chg",0))} · 开板{s.get("open_times",0)}次<br>
            <span style="color:#d29922;font-size:11px;">{s.get("reason","")}</span>
          </div>'''

    low_html = f'''<div class="zhaban-low" style="padding:6px 10px;border-radius:6px;margin-bottom:6px;">
            <b>今日炸板率{zr}%</b><br>
            <span style="color:#3fb950;font-size:11px;">✅ {"偏低，打板安全边际高" if zr <= 25 else "正常" if zr <= 35 else "偏高，注意风险"}</span>
          </div>'''

    return f'''<div class="section">
    <div class="section-title"><span class="icon">💥</span> 炸板深度分析（炸板{zb_total}只 · 炸板率{zr}%） {src_from(d, "zb_analysis")}</div>
    <div class="two-col">
      <div class="col">
        <h4 style="color:#f85149;">🚨 高换手炸板（明天规避）</h4>
        <div style="font-size:12px;">
{high_html or '<div style="color:#8b949e;">无高换手炸板</div>'}        </div>
      </div>
      <div class="col">
        <h4 style="color:#3fb950;">✅ 低换手封板（反包策略关注）</h4>
        <div style="font-size:12px;">
{low_html}        </div>
      </div>
    </div>
  </div>'''

def gen_strategy(d):
    """模块14: 短线策略"""
    lb_detail = d.get('lianban_detail', {})

    focus_items = []
    for level in sorted(lb_detail.keys(), key=int, reverse=True):
        for s in lb_detail[level][:5]:
            focus_items.append(f'<b>{s["name"]}</b>（{level}板{s.get("board_type","")}）— {s.get("reason","")}')

    dip_items = []
    for s in d.get('zb_stocks', [])[:5]:
        if float(s.get('chg', 0)) >= 0:
            dip_items.append(f'<b>{s["name"]}</b>（{fmt_pct(s.get("chg",0))} 炸板）— {s.get("reason","")}')

    avoid_items = []
    for s in d.get('sector_down', [])[:3]:
        avoid_items.append(f'<b>{s["name"]}板块</b>— 今日{fmt_pct(s["chg"])}')

    def li(items):
        return ''.join([f'<li>{x}</li>' for x in items[:6]]) or '<li>暂无</li>'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">💡</span> 短线策略 & 明日接力计划 {src_from(d, "strategy")}</div>
    <div class="strategy-cols">
      <div class="strategy-col">
        <h4 style="color:#3fb950;">✅ 重点接力（明日关注）</h4>
        <ul>{li(focus_items)}</ul>
      </div>
      <div class="strategy-col">
        <h4 style="color:#58a6ff;">🔍 分歧低吸（回调关注）</h4>
        <ul>{li(dip_items)}</ul>
      </div>
      <div class="strategy-col">
        <h4 style="color:#f85149;">🚫 坚决规避（明日回避）</h4>
        <ul>{li(avoid_items)}</ul>
      </div>
    </div>
  </div>'''

def gen_outlook(d, ctx):
    """模块15: 行情回顾 & 后市展望"""
    idx = d['indices']
    ad = d['advance_decline']
    adv = ad.get('total_adv', ad['sh_adv'] + ad['sz_adv'])
    dec = ad.get('total_dec', ad['sh_dec'] + ad['sz_dec'])
    zt = d['zt_total']
    zb = d['zb_total']
    sr = ctx.sr

    leaders = []
    for key, name in [("cy","创业板指"),("sz","深证成指"),("sh","上证指数"),("kc","科创50")]:
        leaders.append(f'{name}{fmt_pct(idx[key]["chg"])}')
    review = f'今日A股震荡{"分化" if adv > dec * 0.8 and adv < dec * 1.2 else "走强" if adv > dec else "调整"}，{", ".join(leaders)}。涨跌家数{adv}涨vs{dec}跌，封板率{sr}%。'

    outlook = f'封板率{sr}%{"偏高，市场偏强" if sr >= 70 else "中等" if sr >= 50 else "偏低，市场偏弱"}。涨停{zt}只，炸板{zb}只。'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">📝</span> 行情回顾 & 后市展望 {src_from(d, "outlook")}</div>
    <div class="two-col">
      <div class="col">
        <h4 style="color:#f85149;">📈 今日行情回顾</h4>
        <p style="font-size:13px;line-height:1.8;color:#8b949e;">{review}</p>
      </div>
      <div class="col">
        <h4 style="color:#f85149;">🔮 后市展望</h4>
        <p style="font-size:13px;line-height:1.8;color:#8b949e;">{outlook}</p>
      </div>
    </div>
  </div>'''

def gen_turnover(d):
    """模块16: 成交额排行Top10"""
    top = d.get('turnover_top', [])
    if not top:
        return '<div class="section"><div class="section-title"><span class="icon">💰</span> 成交额排行 Top10 ' + src_from(d, "turnover") + '</div><div style="padding:20px;color:#8b949e;">暂无数据</div></div>'

    rows = ""
    for i, s in enumerate(top[:10], 1):
        chg_cls = "positive" if float(s.get("chg",0)) >= 0 else "negative"
        rows += f'      <tr><td>{i}</td><td>{s.get("code","")}</td><td><b>{s.get("name","")}</b></td><td class="{chg_cls}">{fmt_pct(s.get("chg",0))}</td><td>{s.get("price","-")}</td><td style="color:#d29922;">{fmt_amt(s.get("amount",0))}</td><td>{s.get("turnover_rate","-")}%</td><td>{tag_html(s.get("flow",0))}</td></tr>\n'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">💰</span> 成交额排行 Top10 {src_from(d, "turnover")}</div>
    <table>
      <tr><th>排名</th><th>代码</th><th>名称</th><th>涨幅</th><th>最新价</th><th>成交额</th><th>换手率</th><th>主力净流入</th></tr>
{rows}    </table>
  </div>'''

def gen_decline_top(d):
    """模块17: 跌幅榜Top5"""
    top = d.get('decline_top', [])
    if not top:
        return '<div class="section"><div class="section-title"><span class="icon">📉</span> 今日跌幅榜 Top5（风险警示） ' + src_from(d, "decline") + '</div><div style="padding:20px;color:#8b949e;">暂无数据</div></div>'

    rows = ""
    for s in top[:5]:
        risk = s.get('risk', '')
        rows += f'      <tr><td>{s.get("code","")}</td><td><b>{s.get("name","")}</b></td><td class="negative">{fmt_pct(s.get("chg",0))}</td><td>{s.get("price","-")}</td><td>{tag_html(s.get("flow",0))}</td><td style="color:#f85149;font-size:12px;">⚠ {risk}</td></tr>\n'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">📉</span> 今日跌幅榜 Top5（风险警示） {src_from(d, "decline")}</div>
    <table>
      <tr><th>代码</th><th>名称</th><th>跌幅</th><th>最新价</th><th>主力净流出</th><th>风险提示</th></tr>
{rows}    </table>
  </div>'''

def gen_fund_flow(d):
    """模块18: 资金风向"""
    fi = d.get('fund_in', [])
    fo = d.get('fund_out', [])

    fi_rows = "".join(f'        <div class="money-row"><span class="stock-name">{s["name"]}</span><span class="money-plus">{fmt_flow(s["flow"])}</span></div>\n' for s in fi[:5])
    fo_rows = "".join(f'        <div class="money-row"><span class="stock-name">{s["name"]}</span><span class="money-minus">{fmt_flow(s["flow"])}</span></div>\n' for s in fo[:5])

    return f'''<div class="section">
    <div class="section-title"><span class="icon">💹</span> 资金风向 · 主力净流入/流出 Top5 {src_from(d, "fund")}</div>
    <div class="two-col">
      <div class="col">
        <h4 style="color:#3fb950;">✅ 今日主力净流入 Top5</h4>
{fi_rows}      </div>
      <div class="col">
        <h4 style="color:#f85149;">🚨 今日主力净流出 Top5</h4>
{fo_rows}      </div>
    </div>
  </div>'''

def gen_sector_flow(d):
    """板块主力资金流向：行业/概念/地区 净流入+净流出 Top5"""
    sf = d.get('sector_flow', {})

    def bar_chart(items, key_name='name', key_val='flow', max_val=None):
        """生成水平柱状图HTML，红涨绿跌"""
        if not items:
            return '<p style="color:#8b949e;">暂无数据</p>'
        abs_vals = [abs(float(s.get(key_val, 0))) for s in items]
        mv = max(abs_vals) if abs_vals else 1
        if max_val:
            mv = max(mv, max_val)
        bars = ""
        for s in items:
            name = s[key_name]
            val = float(s.get(key_val, 0))
            abs_v = abs(val)
            pct = max(abs_v / mv * 100, 3) if mv > 0 else 3
            color = "#f85149" if val >= 0 else "#3fb950"
            label = fmt_flow(val)
            bars += f'''      <div style="display:flex;align-items:center;margin-bottom:10px;min-height:28px;">
        <div style="width:70px;font-size:12px;color:#c9d1d9;flex-shrink:0;text-align:right;padding-right:8px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="{name}">{name}</div>
        <div style="flex:1;min-width:0;display:flex;align-items:center;">
          <div style="width:{pct:.1f}%;height:24px;background:{color};border-radius:4px;min-width:20px;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:11px;color:#fff;font-weight:600;white-space:nowrap;">{label}</div>
        </div>
      </div>\n'''
        return bars

    def make_panel(title, inflow_key, outflow_key, icon):
        inflow = sf.get(inflow_key, [])
        outflow = sf.get(outflow_key, [])
        # 统一最大值让流入流出比例协调
        all_vals = [abs(float(s.get('flow', 0))) for s in inflow + outflow]
        mv = max(all_vals) if all_vals else 1
        in_bars = bar_chart(inflow, max_val=mv)
        out_bars = bar_chart(outflow, max_val=mv)
        return f'''      <div style="background:#161b22;border-radius:8px;padding:16px;">
        <h4 style="color:#58a6ff;margin:0 0 14px 0;font-size:14px;">{icon} {title}</h4>
        <div style="margin-bottom:6px;font-size:11px;color:#3fb950;">净流入 Top5</div>
{in_bars}        <div style="margin:14px 0 6px 0;border-top:1px solid #21262d;"></div>
        <div style="margin-bottom:6px;font-size:11px;color:#f85149;">净流出 Top5</div>
{out_bars}      </div>'''

    panels = make_panel("行业主力净流向(亿)", "industry_in", "industry_out", "🏭")
    panels += make_panel("概念主力净流向(亿)", "concept_in", "concept_out", "💡")
    panels += make_panel("地域主力净流向(亿)", "region_in", "region_out", "🗺️")

    return f'''<div class="section">
    <div class="section-title"><span class="icon">📊</span> 板块主力资金流向（行业·概念·地区） {src_from(d, "sector_flow")}</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
{panels}    </div>
  </div>'''

def gen_core_stocks(d):
    """模块19: 核心个股筛选"""
    lb_detail = d.get('lianban_detail', {})
    items = ""

    # 空间板 = 趋势加速
    for level in sorted(lb_detail.keys(), key=int, reverse=True):
        for s in lb_detail[level][:4]:
            chg_val = s.get('chg', 10.0)
            items += f'''      <div class="stock-item">
        <div class="name">{s["name"]} <span class="badge badge-hot">趋势加速</span></div>
        <div class="change {"up" if float(chg_val) >= 0 else "down"}">{fmt_pct(chg_val)} · {level}板{s.get("board_type","")}</div>
        <div class="info">{s.get("reason","")}</div>
      </div>\n'''

    # 炸板人气 = 关注
    for s in d.get('zb_stocks', [])[:4]:
        items += f'''      <div class="stock-item">
        <div class="name">{s["name"]} <span class="badge badge-warn">炸板关注</span></div>
        <div class="change up">{fmt_pct(s.get("chg",0))} · 炸板{s.get("open_times",0)}次</div>
        <div class="info">{s.get("reason","")}</div>
      </div>\n'''

    # 跌停 = 回避
    for s in d.get('dt_stocks', [])[:4]:
        if not s.get('is_st'):
            items += f'''      <div class="stock-item" style="border-left-color:#f85149;">
        <div class="name">{s["name"]} <span class="badge badge-warn">回避预警</span></div>
        <div class="change" style="color:#3fb950;">{fmt_pct(s.get("chg",0))} · 跌停</div>
        <div class="info" style="color:#f85149;">{s.get("reason","")}</div>
      </div>\n'''

    return f'''<div class="section">
    <div class="section-title"><span class="icon">⭐</span> 核心个股筛选（5类） {src_from(d, "core_stocks")}</div>
    <div class="stock-grid">
{items}    </div>
  </div>'''

def gen_margin(d):
    """模块20: 融资融券数据"""
    m = d.get('margin', {})
    rz_sub = m.get("rz_change", "")
    if m.get("rz_change_pct"):
        rz_sub += f' ({m["rz_change_pct"]})'
    rq_sub = m.get("rq_change", "")
    if m.get("rq_change_pct"):
        rq_sub += f' ({m["rq_change_pct"]})'
    return f'''<div class="section">
    <div class="section-title"><span class="icon">📊</span> 融资融券数据 {src_from(d, "margin")}</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;text-align:center;">
      {card("融资余额", m.get("rz_balance","—"), "color:#e1e8ed;font-size:22px;margin-top:6px;", rz_sub)}
      {card("融券余额", m.get("rq_balance","—"), "color:#e1e8ed;font-size:22px;margin-top:6px;", rq_sub)}
      {card("两融合计", m.get("total","—"), "color:#e1e8ed;font-size:22px;margin-top:6px;", m.get("total_change",""))}
      {card("杠杆占比", m.get("ratio","—"), "color:#58a6ff;font-size:22px;margin-top:6px;", m.get("ratio_label",""))}
    </div>
  </div>'''

def gen_tracking(d):
    """模块21: 重要个股跟踪表"""
    lb_detail = d.get('lianban_detail', {})
    zb = d.get('zb_stocks', [])

    tracked = []
    for level in sorted(lb_detail.keys(), key=int, reverse=True):
        for s in lb_detail[level][:4]:
            tracked.append({
                'code': s.get('code', ''), 'name': s['name'],
                'chg': s.get('chg', 10.0), 'status': f'{level}板{s.get("board_type","")}',
                'seal': True, 'turnover': s.get('board_type',''),
                'strategy': f'{level}进{int(level)+1}关键战'
            })
    for s in zb[:4]:
        if float(s.get('chg', 0)) >= 5:
            tracked.append({
                'code': s.get('code',''), 'name': s['name'],
                'chg': s.get('chg',0), 'status': f'炸板{s.get("open_times",0)}次',
                'seal': False, 'turnover': '活跃',
                'strategy': '关注反包'
            })

    rows = ""
    for t in tracked[:16]:
        seal_str = '<span class="badge badge-seal">封板✅</span>' if t['seal'] else '<span class="badge badge-broken">炸板💥</span>'
        chg_cls = 'positive' if float(t['chg']) >= 0 else 'negative'
        rows += f'      <tr><td>{t.get("code","")}</td><td><b>{t["name"]}</b></td><td class="{chg_cls}">{fmt_pct(t["chg"])}</td><td>{t["status"]}</td><td>{seal_str}</td><td>{t.get("turnover","")}</td><td style="color:#f0883e;">{t["strategy"]}</td></tr>\n'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">📌</span> 重要个股跟踪表（核心标的） {src_from(d, "tracking")}</div>
    <table>
      <tr><th>代码</th><th>名称</th><th>今日涨幅</th><th>当前状态</th><th>封板/炸板</th><th>换手率</th><th>明天策略</th></tr>
{rows}    </table>
  </div>'''

def gen_mindset(d, ctx):
    """模块22: 投资策略 & 心态管理"""
    sr = ctx.sr
    zt = d['zt_total']
    max_board = ctx.max_board

    return f'''<div class="section">
    <div class="section-title"><span class="icon">🧠</span> 投资策略 & 心态管理 {src_from(d, "mindset")}</div>
    <div class="strategy-cols">
      <div class="strategy-col">
        <h4 style="color:#58a6ff;">🎯 选股策略</h4>
        <ul>
          <li>主线优先：从涨停板块中选择最强方向</li>
          <li>空间板关注：当前空间板{max_board}板</li>
          <li>封板率{sr}%：{"打板仓位可适度提高" if sr >= 70 else "控制打板仓位" if sr >= 50 else "减少打板操作"}</li>
          <li>规避：跌停股、一字炸板翻绿股</li>
        </ul>
      </div>
      <div class="strategy-col">
        <h4 style="color:#d29922;">🛡️ 风控策略</h4>
        <ul>
          <li>炸板率{ctx.zr}% → {"偏低，打板安全边际高" if ctx.zr <= 25 else "中等，注意仓位" if ctx.zr <= 35 else "偏高，减少打板"}</li>
          <li>止损严格执行：-5%无条件止损</li>
          <li>控制总仓位不超过7成</li>
        </ul>
      </div>
      <div class="strategy-col">
        <h4 style="color:#3fb950;">💪 心态管理</h4>
        <ul>
          <li>{"题材活跃" if zt >= 100 else "题材一般" if zt >= 50 else "市场冷淡"} → {"重个股轻指数" if zt >= 50 else "轻仓观望"}</li>
          <li>连板接力{"活跃" if max_board >= 4 else "一般" if max_board >= 2 else "冷清"}</li>
          <li>严格执行交易纪律</li>
        </ul>
      </div>
    </div>
  </div>'''

def gen_events(d):
    """模块23: 特殊事件 & 监管关注"""
    zt = d.get('zt_stocks', [])
    events = {}
    for s in zt[:30]:
        concepts = s.get('concepts', '')
        reason = s.get('reason', '')
        if concepts:
            for c in concepts.split('.'):
                c = c.strip()
                if c and c not in events:
                    events[c] = reason
        elif reason:
            for r in _split_reasons(reason)[:2]:
                r = r.strip()
                if r and r not in events:
                    events[r] = reason

    event_items = ""
    for i, (theme, desc) in enumerate(list(events.items())[:5]):
        color = '#d29922' if i < 2 else '#58a6ff' if i < 4 else '#8b949e'
        icon = '⚡' if i < 2 else '📡' if i < 4 else '📌'
        event_items += f'      <b style="color:{color};">{icon} {theme}</b> — {desc if desc else "题材持续活跃"}<br>\n'

    return f'''<div class="section">
    <div class="section-title"><span class="icon">⚠️</span> 特殊事件 & 监管关注 {src_from(d, "special_events")}</div>
    <div style="background:#f8514910;border:1px solid #f8514933;border-radius:8px;padding:14px;margin-bottom:12px;font-size:13px;">
{event_items}    </div>
  </div>'''

def gen_footer(d):
    """模块24: Footer"""
    date = d['date']
    tc = d['time_cutoff']
    return f'''<div class="footer">
    <div class="disclaimer">
      ⚠️ <b>免责声明：</b>本报告仅供参考，不构成投资建议。A股市场有风险，投资需谨慎。数据来源：通达信/同花顺问财/东方财富，数据截至{date} {tc}。
    </div>
    <div>📊 A股市场复盘报告 · 生成于 {date} {tc} · 由 WorkBuddy AI 自动生成</div>
    <div style="margin-top:8px;font-size:11px;color:#6e7681;">
      数据源：通达信tdx-connector（实时行情+涨停专题）· 同花顺问财iwencai（板块/人气/资金）· 东方财富（备选）
    </div>
  </div>'''


# ═══════════════════════════════════════════════
# 模板替换引擎
# ═══════════════════════════════════════════════

# 模块锚点 → 生成器映射
# 需要 ctx 的生成器用 (func, True) 标记
SECTION_MAP = [
    ("Header",              gen_header,           False),
    ("4 Cards",             gen_index_cards,       False),
    ("涨跌家数概览",        gen_advance_decline,   True),
    ("人气龙头",            gen_popularity,        False),
    ("涨停封板率",          gen_seal_rate,         True),
    ("跌停专题",            gen_limit_down,        False),
    ("短线情绪全景",        gen_sentiment,         True),
    ("情绪监测",            gen_emotion_monitor,   True),
    ("连板天梯",            gen_ladder,            True),
    ("板块涨跌榜",          gen_sector,            False),
    ("主线板块深度分析",     gen_mainline,          True),
    ("核心个股筛选",        gen_core_stocks,        False),
    ("涨停板复盘",          gen_zt_review,         False),
    ("炸板深度分析",         gen_zb_analysis,       True),
    ("短线策略",            gen_strategy,           False),
    ("行情回顾",            gen_outlook,            True),
    ("成交额排行",          gen_turnover,           False),
    ("跌幅榜",              gen_decline_top,        False),
    ("资金风向",            gen_fund_flow,          False),
    ("板块主力资金流向",      gen_sector_flow,        False),
    ("重要个股跟踪表",       gen_tracking,           False),
    ("投资策略",            gen_mindset,            True),
    ("特殊事件",            gen_events,             False),
    ("融资融券数据",        gen_margin,             False),
    ("Footer",              gen_footer,             False),
]

def replace_sections(html, data, ctx):
    """用HTML注释锚点替换模板各模块"""
    comment_pattern = r'<!--\s*(.*?)\s*-->'
    comments = [(m.start(), m.end(), m.group(1).strip()) for m in re.finditer(comment_pattern, html)]

    # 先确定哪些注释有匹配的生成器
    matched_indices = []
    for i, (start, end, comment_text) in enumerate(comments):
        for anchor_key, gen_func, needs_ctx in SECTION_MAP:
            if anchor_key in comment_text:
                matched_indices.append((i, anchor_key, gen_func, needs_ctx))
                break

    # 为每个匹配的section确定范围
    replacements = []
    for j, (i, anchor_key, gen_func, needs_ctx) in enumerate(matched_indices):
        start = comments[i][0]
        if j + 1 < len(matched_indices):
            section_end = comments[matched_indices[j + 1][0]][0]
        else:
            section_end = len(html)
        try:
            if needs_ctx:
                new_html = gen_func(data, ctx)
            else:
                new_html = gen_func(data)
        except Exception as e:
            print(f"[WARN] {anchor_key} 生成失败: {e}")
            continue
        replacements.append((start, section_end, new_html))

    # 从后往前替换
    for start, end, new_html in sorted(replacements, key=lambda x: x[0], reverse=True):
        html = html[:start] + new_html + html[end:]

    return html


# ═══════════════════════════════════════════════
# 主程序
# ═══════════════════════════════════════════════

def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "report_data.json"

    if not os.path.exists(data_path):
        print(f"❌ 数据文件不存在: {data_path}")
        sys.exit(1)

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"📊 数据加载: {data_path} ({len(json.dumps(data))} chars)")

    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ 模板不存在: {TEMPLATE_PATH}")
        sys.exit(1)

    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()
    print(f"📄 模板加载: {len(html)} chars")

    # 预计算公共数据
    ctx = DataContext(data)

    # 替换各模块
    html = replace_sections(html, data, ctx)

    # 验证CSS完整
    style_match = re.search(r'<style>.*?</style>', html, re.DOTALL)
    if style_match:
        print(f"✅ CSS完整: {len(style_match.group())} chars")

    # 写输出
    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    out_path = f"a-share-report-{date}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 报告已生成: {out_path} ({len(html)} chars)")


if __name__ == "__main__":
    main()
