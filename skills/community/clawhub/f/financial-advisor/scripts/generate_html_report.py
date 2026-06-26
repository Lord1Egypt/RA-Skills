#!/usr/bin/env python3
"""
HTML报告生成脚本 — 多模板支持

支持 4 种报告模板（--template 参数）：
  stock       — 个股分析（默认）：结论→行情/K线/技术→宏观/新闻→免责
  market      — 大盘总览：多市场指数概览→涨跌统计/板块排行→宏观/热点→免责
  comprehensive — 综合研报：大盘总览→行业聚焦→重点个股→宏观/热点→策略建议→免责
  compare     — 多股对比：对比结论→核心指标对比→收益率对比→AI分析→免责

核心功能：
- 读取所有数据文件（实时、历史、指标、风险）
- 基于客观数据自动生成分析结论
- 支持 DCF 估值、可比公司分析、三表财务分析报告区块
- 支持宏观经济分析（经济周期/利率/通胀/PMI）报告区块
- 支持时政热点区块渲染（fetch_trending.py 采集数据）
- AI 综合研判区块（--ai-analysis-json + --ai-deep-analysis-json）
- 大盘数据区块（--market-json，market_review.py 输出）
- 多股对比区块（--stocks dir1,dir2,dir3）
- 全新专业报告模板设计（CSS设计系统/KPI网格/SVG评分环/标签组件/响应式/打印样式）
- 量化评分客观化（结合夏普/Sortino/Calmar/波动率/Beta/VaR等金融指标）
- 新闻热点自动推断影响方向 + 关键事件影响判断相似度去重
- 主体关联分析 + 财报时效性二次过滤 + 关联性标题内容二次验证
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install pandas numpy")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def _find_file(data_dir, pattern, recursive=False):
    """在 data_dir 下查找文件，支持递归（用于默认 data-dir 时）"""
    p = Path(data_dir)
    if not p.exists():
        return []
    files = list(p.rglob(pattern)) if recursive else list(p.glob(pattern))
    return [f for f in files if f.is_file()]


def load_realtime_data(data_dir):
    """加载实时数据"""
    csv_files = _find_file(data_dir, '*_realtime.csv') or _find_file(data_dir, '*_realtime.csv', recursive=True)
    if not csv_files:
        return None
    df = pd.read_csv(csv_files[0])
    return df.iloc[0].to_dict() if not df.empty else None


def load_history_data(data_dir):
    """加载历史数据"""
    csv_files = _find_file(data_dir, '*_history.csv') or _find_file(data_dir, '*_history.csv', recursive=True)
    if not csv_files:
        return None
    return pd.read_csv(csv_files[0])


def load_indicators(data_dir):
    """加载技术指标数据"""
    csv_files = _find_file(data_dir, '*_indicators.csv') or _find_file(data_dir, '*_indicators.csv', recursive=True)
    if not csv_files:
        return None
    return pd.read_csv(csv_files[0])


def load_risk_metrics(data_dir):
    """加载风险指标数据"""
    json_files = _find_file(data_dir, '*_risk_metrics.json') or _find_file(data_dir, '*_risk_metrics.json', recursive=True)
    if not json_files:
        return None
    with open(json_files[0], 'r', encoding='utf-8') as f:
        return json.load(f)


def load_fundamental_data(data_dir):
    """加载基本面/估值数据（fundamental 或 valuation CSV），用于补充 PE/PB 等缺失字段"""
    for pattern in ['*_fundamental.csv', '*_valuation.csv']:
        csv_files = _find_file(data_dir, pattern) or _find_file(data_dir, pattern, recursive=True)
        if csv_files:
            try:
                df = pd.read_csv(csv_files[0])
                if not df.empty:
                    return df.iloc[0].to_dict()
            except Exception:
                pass
    return None


def detect_data_source(data_dir):
    """
    从数据文件中自动检测数据来源，正确标注腾讯财经 API 或 yfinance。
    避免标注错误。
    """
    sources = set()
    p = Path(data_dir)
    csv_paths = list(p.glob('*.csv')) if p.exists() else []
    if not csv_paths:
        csv_paths = list(p.rglob('*.csv'))
    for csv_path in csv_paths:
        try:
            df = pd.read_csv(csv_path, nrows=1)
            if '数据来源' in df.columns:
                val = df['数据来源'].iloc[0]
                if pd.notna(val) and str(val).strip():
                    s = str(val).strip().lower()
                    if s == 'tencent':
                        sources.add('腾讯财经 API')
                    elif s == 'yfinance':
                        sources.add('yfinance')
                    else:
                        sources.add(str(val))
        except Exception:
            pass
    if sources:
        return ' + '.join(sorted(sources))
    return 'yfinance'  # 默认（无数据来源列时）





def load_valuation_data(valuation_json_path):
    """加载 DCF / 三表估值分析 JSON（calculate_valuation.py 输出）"""
    if not valuation_json_path or not Path(valuation_json_path).exists():
        return None
    try:
        with open(valuation_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载估值分析数据失败: {e}")
        return None


def load_comps_data(comps_json_path):
    """加载可比公司分析 JSON（calculate_valuation.py --mode comps 输出）"""
    if not comps_json_path or not Path(comps_json_path).exists():
        return None
    try:
        with open(comps_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载可比公司分析数据失败: {e}")
        return None


def _fmt_number(val, decimals=2, prefix='', suffix='', pct=False):
    """格式化数值：支持前缀、后缀、百分比、大数缩写"""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return 'N/A'
    if pct:
        return f'{prefix}{val * 100 if abs(val) < 10 else val:,.{decimals}f}%{suffix}'
    if isinstance(val, (int, float)):
        if abs(val) >= 1e12:
            return f'{prefix}{val / 1e12:,.{decimals}f} 万亿{suffix}'
        if abs(val) >= 1e8:
            return f'{prefix}{val / 1e8:,.{decimals}f} 亿{suffix}'
        if abs(val) >= 1e4:
            return f'{prefix}{val / 1e4:,.{decimals}f} 万{suffix}'
        return f'{prefix}{val:,.{decimals}f}{suffix}'
    return str(val)


def render_dcf_section(valuation_data):
    """渲染 DCF 估值分析报告区块"""
    if not valuation_data:
        return ""
    dcf = valuation_data.get('dcf')
    if not dcf:
        return ""

    html = '<h3 class="sub-header">📊 DCF 估值模型</h3>'

    # 核心估值结果
    base = dcf.get('base_case', {})
    bear = dcf.get('bear_case', {})
    bull = dcf.get('bull_case', {})
    current_price = dcf.get('current_price', 0)

    html += '<table class="data-table"><thead><tr><th>场景</th><th>企业价值</th><th>股权价值</th><th>每股价值</th><th>上涨/下跌空间</th></tr></thead><tbody>'
    for label, case_data in [('🐻 悲观', bear), ('📊 基准', base), ('🐂 乐观', bull)]:
        ev = _fmt_number(case_data.get('enterprise_value', 0))
        eq = _fmt_number(case_data.get('equity_value', 0))
        per_share = case_data.get('per_share_value', 0)
        upside = ((per_share / current_price - 1) * 100) if current_price > 0 and per_share else 0
        cls = 'positive' if upside > 0 else 'negative'
        html += f'<tr><td><strong>{label}</strong></td><td class="col-num">{ev}</td><td class="col-num">{eq}</td><td class="col-num">{_fmt_number(per_share)} 元</td>'
        html += f'<td class="col-num {cls}">{upside:+.1f}%</td></tr>'
    html += '</tbody></table>'

    # WACC 参数
    params = dcf.get('parameters', {})
    if params:
        html += '<div class="kpi-row" style="margin:16px 0;">'
        html += f'<div class="kpi-card"><div class="kpi-label">WACC</div><div class="kpi-value" style="font-size:22px;">{_fmt_number(params.get("wacc", 0), pct=True)}</div></div>'
        html += f'<div class="kpi-card"><div class="kpi-label">终值增长率</div><div class="kpi-value" style="font-size:22px;">{_fmt_number(params.get("terminal_growth_rate", 0), pct=True)}</div></div>'
        html += f'<div class="kpi-card"><div class="kpi-label">预测期</div><div class="kpi-value" style="font-size:22px;">{params.get("projection_years", 5)} 年</div></div>'
        html += f'<div class="kpi-card"><div class="kpi-label">无风险利率</div><div class="kpi-value" style="font-size:22px;">{_fmt_number(params.get("risk_free_rate", 0), pct=True)}</div></div>'
        html += '</div>'

    # 敏感性矩阵
    sensitivity = dcf.get('sensitivity_matrix')
    if sensitivity and isinstance(sensitivity, dict):
        wacc_range = sensitivity.get('wacc_range', [])
        tgr_range = sensitivity.get('terminal_growth_range', [])
        matrix = sensitivity.get('values', [])
        if wacc_range and tgr_range and matrix:
            html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">敏感性分析（每股价值 vs WACC / 终值增长率）</h4>'
            html += '<table class="data-table"><thead><tr><th>WACC \\ 终值增长率</th>'
            for tg in tgr_range:
                html += f'<th>{tg * 100 if abs(tg) < 1 else tg:.1f}%</th>'
            html += '</tr></thead><tbody>'
            for i, wacc_val in enumerate(wacc_range):
                html += f'<tr><td><strong>{wacc_val * 100 if abs(wacc_val) < 1 else wacc_val:.1f}%</strong></td>'
                if i < len(matrix):
                    for j, cell_val in enumerate(matrix[i]):
                        cls = 'positive' if cell_val > current_price else 'negative'
                        html += f'<td class="col-num {cls}">{_fmt_number(cell_val)}</td>'
                html += '</tr>'
            html += '</tbody></table>'

    # 预测现金流
    projections = dcf.get('projected_fcf', [])
    if projections:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">自由现金流预测</h4>'
        html += '<table class="data-table"><thead><tr><th>年份</th><th>营收</th><th>UFCF</th><th>现值 (PV)</th></tr></thead><tbody>'
        for proj in projections:
            year = proj.get('year', '')
            rev = _fmt_number(proj.get('revenue', 0))
            fcf = _fmt_number(proj.get('ufcf', proj.get('fcf', 0)))
            pv = _fmt_number(proj.get('pv', 0))
            html += f'<tr><td>{year}</td><td class="col-num">{rev}</td><td class="col-num">{fcf}</td><td class="col-num">{pv}</td></tr>'
        html += '</tbody></table>'

    return html


def render_comps_section(comps_data):
    """渲染可比公司分析报告区块"""
    if not comps_data:
        return ""
    comps = comps_data if isinstance(comps_data, dict) and 'peers' in comps_data else comps_data.get('comps', {})
    if not comps:
        return ""

    html = '<h3 class="sub-header">🏢 可比公司分析 (Comps)</h3>'

    # 可比公司表
    peers = comps.get('peers', [])
    if peers:
        html += '<table class="data-table"><thead><tr><th>公司</th><th>代码</th><th>市值</th><th>PE</th><th>PB</th><th>PS</th><th>EV/EBITDA</th></tr></thead><tbody>'
        for p in peers:
            name = p.get('name', p.get('symbol', ''))
            symbol = p.get('symbol', '')
            mcap = _fmt_number(p.get('market_cap', 0))
            pe = _fmt_number(p.get('pe_ratio', p.get('trailing_pe', None)))
            pb = _fmt_number(p.get('pb_ratio', p.get('price_to_book', None)))
            ps = _fmt_number(p.get('ps_ratio', p.get('price_to_sales', None)))
            ev_ebitda = _fmt_number(p.get('ev_ebitda', p.get('enterprise_to_ebitda', None)))
            html += f'<tr><td><strong>{name}</strong></td><td>{symbol}</td><td class="col-num">{mcap}</td><td class="col-num">{pe}</td><td class="col-num">{pb}</td><td class="col-num">{ps}</td><td class="col-num">{ev_ebitda}</td></tr>'
        html += '</tbody></table>'

    # 统计基准
    benchmarks = comps.get('benchmarks', comps.get('statistics', {}))
    if benchmarks:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">统计基准</h4>'
        html += '<table class="data-table"><thead><tr><th>指标</th><th>均值</th><th>中位数</th><th>最小值</th><th>最大值</th></tr></thead><tbody>'
        for metric_name, stats in benchmarks.items():
            if isinstance(stats, dict):
                html += f'<tr><td><strong>{metric_name}</strong></td>'
                html += f'<td class="col-num">{_fmt_number(stats.get("mean"))}</td>'
                html += f'<td class="col-num">{_fmt_number(stats.get("median"))}</td>'
                html += f'<td class="col-num">{_fmt_number(stats.get("min"))}</td>'
                html += f'<td class="col-num">{_fmt_number(stats.get("max"))}</td></tr>'
        html += '</tbody></table>'

    # 隐含估值
    implied = comps.get('implied_valuation', {})
    if implied:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">隐含估值（基于可比公司中位数倍数）</h4>'
        html += '<table class="data-table"><thead><tr><th>方法</th><th>隐含每股价值</th><th>上涨/下跌空间</th></tr></thead><tbody>'
        current_price = comps.get('current_price', implied.get('current_price', 0))
        for method, val in implied.items():
            if method == 'current_price':
                continue
            if isinstance(val, (int, float)):
                upside = ((val / current_price - 1) * 100) if current_price > 0 else 0
                cls = 'positive' if upside > 0 else 'negative'
                html += f'<tr><td><strong>{method}</strong></td><td class="col-num">{_fmt_number(val)} 元</td><td class="col-num {cls}">{upside:+.1f}%</td></tr>'
        html += '</tbody></table>'

    return html


def render_statements_section(valuation_data):
    """渲染三表财务分析报告区块"""
    if not valuation_data:
        return ""
    statements = valuation_data.get('statements')
    if not statements:
        return ""

    html = '<h3 class="sub-header">📋 三表财务分析</h3>'

    # 利润表
    income = statements.get('income_statement', {})
    if income:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">利润表摘要</h4>'
        items = income.get('items', income)
        if isinstance(items, list):
            html += '<table class="data-table"><thead><tr><th>项目</th>'
            if items and isinstance(items[0], dict):
                years = [k for k in items[0].keys() if k != 'item']
                for y in years:
                    html += f'<th>{y}</th>'
                html += '</tr></thead><tbody>'
                for row in items:
                    html += f'<tr><td><strong>{row.get("item", "")}</strong></td>'
                    for y in years:
                        html += f'<td class="col-num">{_fmt_number(row.get(y, 0))}</td>'
                    html += '</tr>'
            html += '</tbody></table>'
        elif isinstance(items, dict):
            html += '<table class="data-table"><thead><tr><th>指标</th><th>最新值</th><th>同比增长</th></tr></thead><tbody>'
            for k, v in items.items():
                if isinstance(v, dict):
                    html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(v.get("value", 0))}</td><td class="col-num">{_fmt_number(v.get("yoy_growth"), pct=True)}</td></tr>'
                else:
                    html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(v)}</td><td>-</td></tr>'
            html += '</tbody></table>'

    # 资产负债表
    balance = statements.get('balance_sheet', {})
    if balance:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">资产负债表摘要</h4>'
        items = balance.get('items', balance)
        if isinstance(items, dict):
            html += '<table class="data-table"><thead><tr><th>指标</th><th>金额</th></tr></thead><tbody>'
            for k, v in items.items():
                val = v.get('value', v) if isinstance(v, dict) else v
                html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(val)}</td></tr>'
            html += '</tbody></table>'

    # 现金流量表
    cashflow = statements.get('cash_flow', {})
    if cashflow:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">现金流量表摘要</h4>'
        items = cashflow.get('items', cashflow)
        if isinstance(items, dict):
            html += '<table class="data-table"><thead><tr><th>指标</th><th>金额</th></tr></thead><tbody>'
            for k, v in items.items():
                val = v.get('value', v) if isinstance(v, dict) else v
                html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(val)}</td></tr>'
            html += '</tbody></table>'

    # 联动验证
    checks = statements.get('consistency_checks', [])
    if checks:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">联动验证</h4>'
        for chk in checks:
            if isinstance(chk, dict):
                passed = chk.get('passed', chk.get('status') == 'pass')
                banner_cls = 'success' if passed else 'danger'
                icon = '✅' if passed else '❌'
                html += f'<div class="banner {banner_cls}"><span class="banner-icon">{icon}</span><div><strong>{chk.get("name", chk.get("check", ""))}</strong><br><span class="text-sm">{chk.get("detail", chk.get("message", ""))}</span></div></div>'
            else:
                html += f'<div class="banner info"><span class="banner-icon">📋</span>{chk}</div>'

    # 关键财务比率
    ratios = statements.get('key_ratios', {})
    if ratios:
        html += '<h4 style="font-size:15px;margin:20px 0 12px;font-weight:600;">关键财务比率</h4>'
        html += '<table class="data-table"><thead><tr><th>指标</th><th>数值</th><th>评价</th></tr></thead><tbody>'
        for k, v in ratios.items():
            if isinstance(v, dict):
                assessment = v.get('assessment', '')
                tag_cls = 'up' if '良好' in assessment or '优' in assessment else 'down' if '差' in assessment or '低' in assessment or '高风险' in assessment else 'flat'
                html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(v.get("value"))}</td><td><span class="tag {tag_cls}">{assessment}</span></td></tr>'
            else:
                html += f'<tr><td><strong>{k}</strong></td><td class="col-num">{_fmt_number(v)}</td><td>-</td></tr>'
        html += '</tbody></table>'

    return html


def load_macro_data(macro_json_path):
    """加载宏观经济分析 JSON（macro_analysis.py 输出）"""
    if not macro_json_path or not Path(macro_json_path).exists():
        return None
    try:
        with open(macro_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载宏观分析数据失败: {e}")
        return None


def load_ai_analysis(ai_json_path):
    """加载 AI 综合分析 JSON（ai_analysis.json）"""
    if not ai_json_path or not Path(ai_json_path).exists():
        return None
    try:
        with open(ai_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载 AI 分析数据失败: {e}")
        return None


def render_ai_analysis_section(ai_data, ai_deep_data=None):
    """渲染 AI 综合分析报告区块（支持拆分的深度分析数据）

    支持将 thinking_trace/sections 放在独立的 ai_deep_data 中传入，
    降低单个 JSON 文件体积，减少 AI 生成时截断/格式错误的概率。
    如果 ai_deep_data 不为空，优先从中读取 thinking_trace/sections；
    否则回退到从 ai_data 中读取（向后兼容）。

    返回 (brief_html, events_html, deep_analysis_html) 元组：
    - brief_html: 核心结论与投资评级（放在报告顶部"投资结论"区）
    - events_html: 关键事件与影响判断（放在"新闻与宏观"区，紧邻新闻/宏观内容）
    - deep_analysis_html: 推理链路 + 多维度分析（放在"新闻与宏观"区的末尾）
    """
    if not ai_data:
        return "", "", ""

    brief_html = ''
    events_html = ''
    deep_analysis_html = ''

    # ===== 简要结论（brief_html）：核心结论 + 评级 + 目标价 =====
    summary = ai_data.get('summary', '')
    recommendation = ai_data.get('recommendation', '')
    target_price = ai_data.get('target_price', {})
    stop_loss = ai_data.get('stop_loss')

    if summary or recommendation:
        rec_class = 'positive' if '买入' in recommendation else 'negative' if '卖出' in recommendation else 'neutral'
        rec_icon = '🟢' if '买入' in recommendation else '🔴' if '卖出' in recommendation else '🟡'

        brief_html += '<div style="padding:24px;border-radius:var(--radius-sm);background:linear-gradient(135deg,#f0f9ff,#e0f2fe);border:1px solid #bae6fd;margin-bottom:24px;">'
        if summary:
            brief_html += f'<p style="font-size:16px;font-weight:600;color:#0c4a6e;margin-bottom:12px;">💡 {summary}</p>'

        if recommendation:
            brief_html += f'<div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">'
            brief_html += f'<span class="recommendation-badge {rec_class}">{rec_icon} {recommendation}</span>'

            if target_price:
                low = target_price.get('low', '')
                mid = target_price.get('mid', '')
                high = target_price.get('high', '')
                if mid:
                    brief_html += f'<span style="font-size:14px;color:var(--text-secondary);">目标价：'
                    if low:
                        brief_html += f'<strong>{low}</strong> / '
                    brief_html += f'<strong style="color:var(--primary);font-size:18px;">{mid}</strong>'
                    if high:
                        brief_html += f' / <strong>{high}</strong>'
                    brief_html += '</span>'

            if stop_loss:
                brief_html += f'<span style="font-size:14px;color:var(--danger);">止损：<strong>{stop_loss}</strong></span>'

            brief_html += '</div>'
        brief_html += '</div>'

    # ===== 事件影响（events_html）：关键事件与影响判断 =====

    # 关键事件与影响判断
    news_intel = ai_data.get('news_intelligence', {})
    impact_assessment = ai_data.get('impact_assessment', [])
    if news_intel or impact_assessment:
        events_html += '<h4 class="sub-header" style="margin-top:24px;">⚡ 关键事件与影响判断</h4>'

        event_rows = []
        # 使用列表存储已接受的事件文本，用于相似度去重
        accepted_event_texts = []

        if impact_assessment:
            for item in impact_assessment[:8]:
                if isinstance(item, dict):
                    event_text = item.get('event', '')
                    if not event_text:
                        continue
                    # 时效性过滤（过滤过期财报相关事件）
                    if not _is_title_timely(event_text):
                        continue
                    # 相似度去重 — 检查与已接受事件的相似度
                    if _is_event_duplicate(event_text, accepted_event_texts):
                        continue
                    accepted_event_texts.append(event_text)
                    event_rows.append({
                        'event': event_text,
                        'direction': item.get('direction', ''),
                        'strength': item.get('strength', item.get('intensity', '')),
                        'summary': item.get('transmission', item.get('path', '')),
                    })

        if news_intel and len(event_rows) < 8:
            intel_config = [
                ('key_events', '🔴'), ('company_specific', '🎯'),
                ('geopolitical', '⚔️'), ('macro_policy', '🏛️'),
                ('industry_dynamics', '🏭'), ('market_sentiment', '📊'),
            ]
            for key, icon in intel_config:
                items = news_intel.get(key, [])
                if isinstance(items, str):
                    items = [items]
                for item in items[:2]:
                    if len(event_rows) >= 10:
                        break
                    if isinstance(item, dict):
                        title = item.get('title', item.get('event', ''))
                        if not title:
                            continue
                        # 时效性过滤
                        if not _is_title_timely(title):
                            continue
                        # 相似度去重（替代原有的精确匹配）
                        if _is_event_duplicate(title, accepted_event_texts):
                            continue
                        accepted_event_texts.append(title)
                        event_rows.append({
                            'event': f'{icon} {title}',
                            'direction': item.get('direction', ''),
                            'strength': item.get('strength', ''),
                            'summary': item.get('impact', ''),
                        })
                    elif isinstance(item, str):
                        # 时效性过滤
                        if not _is_title_timely(item):
                            continue
                        if _is_event_duplicate(item, accepted_event_texts):
                            continue
                        accepted_event_texts.append(item)
                        event_rows.append({
                            'event': f'{icon} {item}',
                            'direction': '',
                            'strength': '',
                            'summary': '',
                        })

        if event_rows:
            events_html += '<table class="data-table"><thead><tr><th>事件</th><th>方向</th><th>强度</th><th>影响路径</th></tr></thead><tbody>'
            for row in event_rows:
                direction = row['direction']
                dir_cls = 'up' if '利好' in direction or '正' in direction else 'down' if '利空' in direction or '负' in direction else 'flat'
                strength = row['strength']
                str_color = '#dc2626' if '强' in strength else '#d97706' if '中' in strength else '#6b7280'
                events_html += f'<tr><td><strong>{row["event"]}</strong></td>'
                events_html += f'<td><span class="tag {dir_cls}">{direction}</span></td>' if direction else '<td>—</td>'
                events_html += f'<td><span style="color:{str_color};font-weight:600;">{strength}</span></td>' if strength else '<td>—</td>'
                events_html += f'<td class="text-sm">{row["summary"]}</td></tr>'
            events_html += '</tbody></table>'

    # ===== 深度分析（deep_analysis_html）：推理链路 + 多维分析 =====
    # 优先从独立的 ai_deep_data 读取，回退到 ai_data（向后兼容）
    deep_source = ai_deep_data if ai_deep_data else ai_data

    # 思考推理链路（thinking_trace）
    thinking = deep_source.get('thinking_trace', {})
    if thinking:
        deep_analysis_html += '<h4 class="sub-header" style="margin-top:24px;">🧠 分析推理链路</h4>'

        trace_config = [
            ('information_scan', '信息全景扫描', '📋', '#eff6ff', '#1d4ed8'),
            ('impact_transmission', '事件传导分析', '🔗', '#fffbeb', '#d97706'),
            ('cross_validation', '多维交叉验证', '🔍', '#ecfdf5', '#059669'),
            ('risk_matrix', '风险矩阵', '⚠️', '#fef2f2', '#dc2626'),
            ('decision_logic', '投资决策推导', '🎯', '#f5f3ff', '#7c3aed'),
        ]

        for key, label, icon, bg, color in trace_config:
            content = thinking.get(key, '')
            if not content:
                continue
            deep_analysis_html += f'<div style="padding:16px 20px;margin:10px 0;border-radius:var(--radius-sm);background:{bg};border:1px solid var(--border-light);border-left:3px solid {color};">'
            deep_analysis_html += f'<div style="font-weight:600;font-size:14px;color:{color};margin-bottom:8px;">{icon} {label}</div>'
            content_html = content.replace('\n', '<br>')
            deep_analysis_html += f'<div style="font-size:14px;color:var(--text-secondary);line-height:1.8;">{content_html}</div>'
            deep_analysis_html += '</div>'

    # 多维度分析板块（sections）
    sections = deep_source.get('sections', [])
    if sections:
        deep_analysis_html += '<h4 class="sub-header" style="margin-top:24px;">📊 多维度深度分析</h4>'

        section_icons = {
            '技术面': '📈', '基本面': '📋', '业绩': '📋', '行业': '🏭',
            '政策': '🏛️', '宏观': '🌍', '热点': '🔥', '投资': '💰',
            '策略': '🎯', '风险': '⚠️', '估值': '💎', '资金': '💹',
        }

        for i, section in enumerate(sections):
            sec_title = section.get('title', f'分析维度 {i + 1}')
            sec_content = section.get('content', '')
            if not sec_content:
                continue

            icon = '📌'
            for keyword, ic in section_icons.items():
                if keyword in sec_title:
                    icon = ic
                    break

            content_html = sec_content.replace('\n', '<br>')
            deep_analysis_html += f'''<div class="metric-card" style="border-left-color:var(--primary);">
                <h3>{icon} {sec_title}</h3>
                <div style="font-size:14px;color:var(--text-secondary);line-height:1.8;">{content_html}</div>
            </div>'''

    return brief_html, events_html, deep_analysis_html


def _infer_sentiment_from_title(title, stock_name='', industry=''):
    """基于标题关键词自动推断影响方向。

    当新闻没有显式的 sentiment/direction 标注时，根据标题中的积极/消极关键词
    自动推断为利好/利空/中性，避免所有未标注新闻都显示"待分析"。

    接收 stock_name/industry 参数，分析结果围绕报告主体。
    """
    result = _infer_sentiment_detail(title, stock_name=stock_name, industry=industry)
    return result['tag']


def _assess_relevance_to_subject(title, cat_key, stock_name='', industry=''):
    """评估新闻与报告主体（stock_name/industry）的关联度。

    核心改动：
    - indirect 不再仅依赖分类归属，必须通过「标题内容二次验证」确认与主体有实质关联
    - national_policy / geopolitical / industry_tech 等分类的新闻，只有标题中
      包含与主体行业相关的关键词时才算 indirect，否则为 none
    - 避免"马布里入驻拼多多"之类匹配到"补贴"→national_policy→indirect 的误判

    Returns:
        str: 'direct' | 'indirect' | 'market' | 'none'
            - direct: 标题中直接提到主体公司/行业名
            - indirect: 标题内容与主体行业有实质性关联
            - market: 属于大盘/市场整体类别（对所有股票都有影响）
            - none: 与主体无明显关联
    """
    title_lower = title.lower()

    # 1. 直接关联：标题包含公司名或行业名
    if stock_name and stock_name in title_lower:
        return 'direct'
    if industry and industry in title_lower:
        return 'direct'
    if cat_key in ('company_related', 'industry_related'):
        return 'direct'

    # 2. 市场整体类别：对所有标的都有宏观影响（央行/宏观/大盘/商品汇率/金融）
    market_categories = {
        'central_bank', 'macro_economy', 'stock_market',
        'commodities_forex', 'banking_finance',
    }
    if cat_key in market_categories:
        return 'market'

    # 3. 间接关联：需要「分类归属 + 标题内容二次验证」双重条件
    # 仅仅被分到 national_policy/geopolitical 等类别不够，
    # 标题中还必须包含与主体行业相关的关键词，才能算 indirect
    indirect_categories = {
        'geopolitical', 'us_china', 'national_policy', 'industry_tech',
    }
    if cat_key in indirect_categories:
        # 二次验证：标题是否包含与主体行业相关的关键词
        if industry:
            industry_related_terms = _get_industry_related_terms(industry)
            for term in industry_related_terms:
                if term in title_lower:
                    return 'indirect'
        # 补充：检查是否包含通用的宏观影响关键词（这些对任何企业都有影响）
        macro_impact_keywords = [
            '降息', '降准', '加息', 'GDP', '经济', '通胀', '衰退',
            '利率', '汇率', '股市', '大盘', 'A股', '港股',
            '制裁', '禁令', '封锁', '脱钩', '贸易战', '关税',
        ]
        for kw in macro_impact_keywords:
            if kw in title_lower:
                return 'indirect'
        # 未通过二次验证 → 虽然分类属于 indirect 类别，但实际与主体无关
        return 'none'

    # 4. global_events / general 类别：检查是否有行业关联关键词
    if industry:
        industry_related_terms = _get_industry_related_terms(industry)
        for term in industry_related_terms:
            if term in title_lower:
                return 'indirect'

    return 'none'


def _get_industry_related_terms(industry):
    """根据行业名称返回相关联的关键词列表。

    用于判断一条通用新闻是否与目标行业有间接关联。

    改进：移除过于宽泛的关键词（如"在线"、"科技"、"消费"、"内容"等），
    这些词在各类新闻中出现频率极高，容易导致误匹配。只保留具有行业特异性的关键词。
    """
    industry_lower = industry.lower() if industry else ''

    # 行业→关键词映射（只保留行业特异性强的关键词，移除泛化词汇）
    industry_term_map = {
        '互联网': ['互联网', '数字经济', '平台经济', '电商平台', '社交平台', '云计算', '人工智能', '大数据', '算法监管', '互联网平台', '网络安全'],
        '游戏': ['游戏', '电竞', '手游', '网游', '版号', '游戏监管', '虚拟现实', 'VR', 'AR', '元宇宙'],
        '金融': ['银行业', '保险业', '证券业', '基金', '信托', '资管', '金融科技', 'fintech', '信贷政策'],
        '半导体': ['芯片', '半导体', '晶圆', '光刻', '封测', '集成电路', 'GPU', 'CPU', 'AI芯片', '国产替代'],
        '新能源': ['新能源', '光伏', '风电', '锂电', '储能', '充电桩', '碳中和', '碳达峰', '绿电'],
        '汽车': ['汽车', '新能源车', '电动车', '智能驾驶', '自动驾驶', '造车', '车企', '动力电池'],
        '消费': ['消费升级', '消费降级', '零售业', '奢侈品', '白酒', '食品安全', '餐饮业'],
        '医药': ['医药', '医疗', '疫苗', '创新药', '集采', '医保改革', '制药', '临床试验'],
        '房地产': ['房地产', '地产', '楼市', '房价', '住房政策', '保交楼', '开发商'],
        '通信': ['通信', '5G', '6G', '运营商', '物联网', '基站', '卫星通信'],
        '传媒': ['传媒', '影视', '广告行业', '短视频', '直播行业', '流媒体', '版权'],
    }

    matched_terms = set()
    for ind_key, terms in industry_term_map.items():
        if ind_key in industry_lower or industry_lower in ind_key:
            matched_terms.update(terms)

    # 如果没有匹配到特定行业，返回行业名本身作为关键词
    if not matched_terms and industry:
        matched_terms.add(industry)

    return matched_terms


def _is_title_timely(title, reference_date=None):
    """渲染层的财报/数据时效性检查。

    在渲染新闻列表时，对每条新闻标题做轻量级时效性验证。
    主要针对：含有过期财报数据的新闻（如 2026年3月看到 2024年财报）。

    与 macro_analysis.py 的 _is_news_within_period 逻辑一致，但更精简，
    作为渲染层的二次防线。

    Args:
        title: 新闻标题
        reference_date: 参考日期（datetime），默认当前时间

    Returns:
        bool: True=有效, False=过时应过滤
    """
    import re

    now = reference_date if reference_date else datetime.now()
    y = now.year
    m = now.month

    # 计算当前应关注的最新财务时期（与 macro_analysis 逻辑一致）
    if m <= 4:
        relevant_periods = [(y - 1, 12), (y, 3)]
    elif m <= 8:
        relevant_periods = [(y, 3), (y, 6)]
    elif m <= 10:
        relevant_periods = [(y, 6), (y, 9)]
    else:
        relevant_periods = [(y, 9), (y, 12)]

    oldest_relevant = min(relevant_periods, key=lambda p: (p[0], p[1]))

    # 财报/年报/季报时期匹配
    report_period_patterns = [
        (r'(\d{4})\s*年?\s*(?:Q1|一季[度报]|第一季[度报]|1季[度报])', lambda yr: (yr, 3)),
        (r'(\d{4})\s*年?\s*(?:Q2|二季[度报]|第二季[度报]|2季[度报]|半年[报度]|中报|上半年)', lambda yr: (yr, 6)),
        (r'(\d{4})\s*年?\s*(?:Q3|三季[度报]|第三季[度报]|3季[度报]|前三季[度报])', lambda yr: (yr, 9)),
        (r'(\d{4})\s*年?\s*(?:Q4|四季[度报]|第四季[度报]|4季[度报]|年报|财报|年度报告|全年业绩|全年营收|全年净利)', lambda yr: (yr, 12)),
    ]

    for pattern, period_fn in report_period_patterns:
        match = re.search(pattern, title)
        if match:
            try:
                year = int(match.group(1))
                report_year, report_quarter_end = period_fn(year)
                if (report_year, report_quarter_end) < oldest_relevant:
                    return False
            except (ValueError, OverflowError):
                continue

    # 纯年份 + 财务关键词检查
    yearly_pattern = r'(\d{4})\s*年\s*(?:财报|年报|业绩|营收|净利|利润)'
    yearly_match = re.search(yearly_pattern, title)
    if yearly_match:
        try:
            data_year = int(yearly_match.group(1))
            if data_year < y - 1:
                return False
        except (ValueError, OverflowError):
            pass

    return True


def _infer_sentiment_detail(title, stock_name='', industry='', cat_key=''):
    """基于标题关键词推断影响方向，返回详细信息。

    核心改动：
    - 增加 stock_name/industry/cat_key 参数
    - 利好/利空判断围绕报告主体（而非新闻本身主体）
    - analysis 字段说明「为什么对主体利好/利空」的逻辑链
    - 与主体无关的新闻返回 neutral（即使标题本身有利好/利空关键词）

    Returns:
        dict: {
            'direction': 'positive'|'negative'|'neutral',
            'tag': HTML 标签字符串,
            'score': int (正负得分差，绝对值越大越确定),
            'analysis': str (对主体的影响逻辑链),
            'relevance': str ('direct'|'indirect'|'market'|'none'),
        }
    """
    # 利好关键词（政策利好、市场上行、公司正面）
    positive_keywords = [
        '上涨', '暴涨', '大涨', '涨停', '新高', '突破', '飙升', '走强', '回暖', '反弹',
        '利好', '重大利好', '正面', '看好', '乐观', '超预期', '创新高',
        '降息', '降准', '宽松', '刺激', '补贴', '减税', '降费', '扶持', '支持',
        '增长', '增速', '扩张', '复苏', '繁荣', '景气', '向好', '回升',
        '增持', '回购', '分红', '利润增长', '营收增长', '业绩大增', '净利大增',
        '签约', '合作', '订单', '中标', '突破', '创新', '量产',
        '牛市', '资金流入', '北向资金流入', '外资加仓',
        '停火', '和谈', '缓和', '缓解', '好转',
    ]
    # 利空关键词（政策收紧、市场下行、风险事件）
    negative_keywords = [
        '下跌', '暴跌', '大跌', '跌停', '新低', '跳水', '崩盘', '走弱', '承压', '下挫',
        '利空', '重大利空', '负面', '看空', '悲观', '不及预期', '低于预期',
        '加息', '紧缩', '收紧', '监管', '处罚', '罚款', '整顿', '约谈',
        '下滑', '萎缩', '衰退', '萧条', '低迷', '恶化', '放缓',
        '减持', '清仓', '亏损', '利润下滑', '营收下降', '业绩暴雷', '爆雷',
        '违约', '暴雷', '退市', '破产', '停牌',
        '冲突', '战争', '袭击', '制裁', '封锁', '禁令', '脱钩', '对抗',
        '地震', '台风', '洪水', '疫情', '灾害',
        '熊市', '资金流出', '外资撤离', '恐慌',
    ]

    title_lower = title.lower()
    pos_hits = [kw for kw in positive_keywords if kw in title_lower]
    neg_hits = [kw for kw in negative_keywords if kw in title_lower]
    pos_count = len(pos_hits)
    neg_count = len(neg_hits)

    # 评估与主体的关联度
    relevance = _assess_relevance_to_subject(title, cat_key, stock_name, industry)
    subject_label = stock_name or industry or '标的'

    # 与主体完全无关的新闻 → 强制中性（即使标题有利好/利空关键词）
    if relevance == 'none' and stock_name:
        return {
            'direction': 'neutral',
            'tag': '<span class="tag flat">➖ 无关</span>',
            'score': 0,
            'analysis': '',
            'relevance': 'none',
        }

    # 基于关联度 + 关键词命中生成「对主体的影响分析」逻辑链
    raw_direction = 'positive' if pos_count > neg_count else ('negative' if neg_count > pos_count else 'neutral')
    hit_keywords = pos_hits + neg_hits

    # 根据关联类型和关键词生成逻辑链分析
    analysis = _build_impact_chain(
        title, hit_keywords, raw_direction, relevance, subject_label, cat_key
    )

    if pos_count > neg_count:
        return {
            'direction': 'positive',
            'tag': '<span class="tag up">📈 利好</span>',
            'score': pos_count - neg_count,
            'analysis': analysis or f'存在正面因素，可能对{subject_label}形成间接利好',
            'relevance': relevance,
        }
    elif neg_count > pos_count:
        return {
            'direction': 'negative',
            'tag': '<span class="tag down">📉 利空</span>',
            'score': neg_count - pos_count,
            'analysis': analysis or f'存在风险因素，可能对{subject_label}形成间接利空',
            'relevance': relevance,
        }
    else:
        return {
            'direction': 'neutral',
            'tag': '<span class="tag flat">➖ 中性</span>',
            'score': 0,
            'analysis': analysis or '',
            'relevance': relevance,
        }


def _build_impact_chain(title, hit_keywords, direction, relevance, subject_label, cat_key):
    """构建「新闻事件 → 传导路径 → 对主体的影响」的逻辑链。

    核心设计：分析必须说明为什么这条新闻对主体（stock_name）利好/利空，
    而不是分析新闻本身的主体。

    Args:
        title: 新闻标题
        hit_keywords: 命中的利好/利空关键词
        direction: 'positive'|'negative'|'neutral'
        relevance: 'direct'|'indirect'|'market'|'none'
        subject_label: 报告主体名称
        cat_key: 新闻分类 key

    Returns:
        str: 影响逻辑链描述
    """
    if not hit_keywords or direction == 'neutral':
        return ''

    # ============ 直接关联：标题包含主体公司/行业 ============
    if relevance == 'direct':
        # 直接影响，分析较简单
        direct_analysis_map = {
            '增持': f'{subject_label}获大股东/高管增持，彰显对公司前景信心',
            '回购': f'{subject_label}实施股份回购，提升每股价值和股东回报',
            '分红': f'{subject_label}分红方案提升股东回报，增强投资吸引力',
            '合作': f'{subject_label}达成战略合作，有望拓展业务边界和收入来源',
            '订单': f'{subject_label}获得新订单，带来业绩增长确定性',
            '创新': f'{subject_label}技术创新突破，有望打开新增长空间',
            '涨停': f'{subject_label}市场关注度高，资金强势追捧',
            '业绩大增': f'{subject_label}业绩表现超预期，基本面强劲',
            '营收增长': f'{subject_label}营收增长趋势向好，业务扩张顺利',
            '减持': f'{subject_label}遭大股东减持，可能引发市场对公司前景的担忧',
            '亏损': f'{subject_label}出现亏损，盈利能力恶化需关注',
            '处罚': f'{subject_label}遭监管处罚，可能影响运营和声誉',
            '罚款': f'{subject_label}被罚款，合规风险暴露',
            '爆雷': f'{subject_label}出现突发风险，需警惕连锁反应',
            '退市': f'{subject_label}面临退市风险，投资者信心受打击',
            '暴跌': f'{subject_label}股价大幅下挫，短期风险加剧',
            '上涨': f'{subject_label}股价走强，市场情绪积极',
        }
        for kw in hit_keywords:
            if kw in direct_analysis_map:
                return direct_analysis_map[kw]
        if direction == 'positive':
            return f'{subject_label}直接受益于该利好消息'
        else:
            return f'{subject_label}直接受该利空因素冲击'

    # ============ 市场整体类别：宏观/央行/大盘对所有标的都有影响 ============
    if relevance == 'market':
        market_analysis_map = {
            '降息': f'央行降息 → 市场流动性宽松 → {subject_label}融资成本降低+估值提升',
            '降准': f'央行降准 → 银行信贷扩张 → 市场资金充裕 → 利好{subject_label}估值',
            '加息': f'加息预期 → 流动性收紧 → {subject_label}估值承压+融资成本上升',
            '牛市': f'大盘走强 → 市场风险偏好提升 → {subject_label}估值水涨船高',
            '熊市': f'大盘走弱 → 市场风险偏好下降 → {subject_label}估值面临压缩',
            '资金流入': f'市场资金净流入 → 整体流动性改善 → {subject_label}可能受益于资金面宽松',
            '北向资金流入': f'外资持续流入 → 偏好蓝筹/白马 → {subject_label}可能获外资关注',
            '资金流出': f'市场资金净流出 → 流动性趋紧 → {subject_label}面临资金面压力',
            '外资撤离': f'外资撤离 → 市场信心下降 → {subject_label}可能承受抛压',
            '复苏': f'经济复苏 → 消费/投资回暖 → {subject_label}业务需求有望改善',
            '衰退': f'经济衰退压力 → 市场需求萎缩 → {subject_label}业绩预期面临下调',
            '涨停': f'板块/大盘涨停潮 → 市场情绪亢奋 → {subject_label}可能受板块轮动带动',
            '暴跌': f'市场系统性下跌 → 恐慌情绪蔓延 → {subject_label}难以独善其身',
            '宽松': f'货币政策宽松 → 市场流动性充裕 → {subject_label}估值环境改善',
            '紧缩': f'货币政策收紧 → 市场流动性收缩 → {subject_label}估值面临压力',
            '上涨': f'市场整体走强 → 风险偏好回升 → {subject_label}估值环境改善',
            '下跌': f'市场整体走弱 → 风险偏好下降 → {subject_label}估值面临拖累',
        }
        for kw in hit_keywords:
            if kw in market_analysis_map:
                return market_analysis_map[kw]
        if direction == 'positive':
            return f'宏观/市场面利好 → 整体投资环境改善 → {subject_label}间接受益'
        else:
            return f'宏观/市场面承压 → 整体投资环境恶化 → {subject_label}间接受拖累'

    # ============ 间接关联：地缘/政策/中美/行业科技 ============
    if relevance == 'indirect':
        indirect_analysis_map = {
            # 地缘政治
            '冲突': f'地缘冲突 → 全球风险偏好下降+供应链扰动 → {subject_label}估值和业务面临不确定性',
            '战争': f'地缘冲突升级 → 避险情绪上升+贸易受阻 → {subject_label}海外业务和市场情绪承压',
            '制裁': f'国际制裁 → 相关产业链受限 → {subject_label}可能面临供应链/市场准入风险',
            '封锁': f'贸易封锁 → 进出口受阻 → {subject_label}供应链稳定性存在隐忧',
            '停火': f'地缘局势缓和 → 全球风险偏好回升 → {subject_label}估值环境改善',
            '和谈': f'和平谈判推进 → 地缘不确定性降低 → {subject_label}市场环境趋于稳定',
            # 中美关系
            '脱钩': f'中美脱钩风险 → 科技/贸易壁垒加高 → {subject_label}可能受供应链重构影响',
            '对抗': f'中美对抗升级 → 政策不确定性加大 → {subject_label}面临外部环境压力',
            '缓和': f'中美关系缓和 → 贸易/科技合作空间打开 → {subject_label}外部环境改善',
            # 政策
            '监管': f'政策监管趋严 → 行业合规成本上升 → {subject_label}运营环境面临挑战',
            '补贴': f'政策补贴出台 → 行业需求受到提振 → {subject_label}可能间接受益于政策红利',
            '减税': f'减税政策 → 企业税负降低 → {subject_label}盈利预期改善',
            '支持': f'政策支持 → 行业发展环境优化 → {subject_label}可能受益于政策导向',
            '整顿': f'行业整顿 → 短期阵痛但长期利好合规企业 → {subject_label}需关注政策走向',
            # 科技/产业
            '创新': f'产业技术创新 → 行业竞争格局变化 → {subject_label}需关注技术演进方向',
            '量产': f'关键技术量产 → 产业链成本下降 → {subject_label}可能受益于产业链升级',
        }
        for kw in hit_keywords:
            if kw in indirect_analysis_map:
                return indirect_analysis_map[kw]
        if direction == 'positive':
            return f'相关政策/行业利好 → 传导至{subject_label}所在领域 → 间接提振'
        else:
            return f'相关政策/行业风险 → 传导至{subject_label}所在领域 → 间接承压'

    # 兜底（不应到达此处，因为 none 已在上方返回）
    return ''


def _event_text_similarity(text_a, text_b):
    """计算两个事件文本的相似度（用于关键事件去重）。

    使用字符级 2-gram Jaccard 相似度，适合中文短文本。
    """
    import re
    clean_a = re.sub(r'[^\u4e00-\u9fff\w]', '', text_a)
    clean_b = re.sub(r'[^\u4e00-\u9fff\w]', '', text_b)
    if len(clean_a) < 2 or len(clean_b) < 2:
        return 0.0
    tokens_a = {clean_a[i:i + 2] for i in range(len(clean_a) - 1)}
    tokens_b = {clean_b[i:i + 2] for i in range(len(clean_b) - 1)}
    if not tokens_a or not tokens_b:
        return 0.0
    intersection = tokens_a & tokens_b
    union = tokens_a | tokens_b
    return len(intersection) / len(union) if union else 0.0


def _is_event_duplicate(event_text, existing_events, threshold=0.50):
    """检测事件文本是否与已有事件高度相似。

    用于关键事件影响判断表中的去重，避免 impact_assessment 和 news_intelligence
    中表述略有不同但实质相同的事件重复出现。

    Args:
        event_text: 待检查的事件文本
        existing_events: 已有事件文本集合
        threshold: 相似度阈值（默认0.50，较宽松以覆盖不同表述）

    Returns:
        bool: True 表示重复
    """
    import re
    # 去除 emoji 前缀后比较
    clean_text = re.sub(r'^[^\u4e00-\u9fff\w]+', '', event_text).strip()
    for existing in existing_events:
        clean_existing = re.sub(r'^[^\u4e00-\u9fff\w]+', '', existing).strip()
        # 精确包含检测
        if clean_text and clean_existing:
            if clean_text in clean_existing or clean_existing in clean_text:
                return True
        # 相似度检测
        sim = _event_text_similarity(clean_text, clean_existing)
        if sim >= threshold:
            return True
    return False


def render_macro_section(macro_data):
    """渲染宏观经济与国际局势分析报告区块"""
    if not macro_data:
        return ""

    html = ''

    # 从 trending_classified 中提取报告主体信息
    trending_data = macro_data.get('trending_classified', macro_data.get('trending_filtered', {}))
    report_stock_name = ''
    report_industry = ''
    if trending_data:
        report_stock_name = trending_data.get('stock_name', '')
        report_industry = trending_data.get('industry', '')

    # 经济周期
    cycle = macro_data.get('business_cycle', {})
    if cycle and not cycle.get('error'):
        phase = cycle.get('phase', 'unknown')
        desc = cycle.get('description', '')
        market_impact = cycle.get('market_impact', '')
        policy_dir = cycle.get('policy_direction', '')

        phase_config = {
            'recovery': ('🟢 复苏期', '#059669', '#ecfdf5', '#a7f3d0'),
            'expansion': ('🔵 扩张期', '#1a56db', '#e8effc', '#bfdbfe'),
            'contraction': ('🔴 收缩期', '#dc2626', '#fef2f2', '#fecaca'),
            'transition': ('🟡 过渡期', '#d97706', '#fffbeb', '#fde68a'),
        }
        label, color, bg, border_c = phase_config.get(phase, ('⚪ 未知', '#6b7280', '#f9fafb', '#e5e7eb'))

        html += f'''<div style="padding:20px;border-radius:var(--radius-sm);border:1px solid {border_c};background:{bg};margin-bottom:20px;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
                <span style="font-size:28px;font-weight:700;color:{color};">{label}</span>
            </div>
            <p style="color:var(--text-secondary);margin-bottom:8px;">{desc}</p>'''
        if market_impact:
            html += f'<p style="margin:4px 0;"><strong>市场影响：</strong>{market_impact}</p>'
        if policy_dir:
            html += f'<p style="margin:4px 0;"><strong>政策方向：</strong>{policy_dir}</p>'
        html += '</div>'

        # 行业轮动
        sector = cycle.get('sector_implications', {})
        favored = sector.get('favored', [])
        disfavored = sector.get('disfavored', [])
        if favored or disfavored:
            html += '<div class="grid-2" style="margin-bottom:20px;">'
            if favored:
                html += f'<div class="banner success"><span class="banner-icon">✅</span><div><strong>利好行业</strong><br>{"、".join(favored)}</div></div>'
            if disfavored:
                html += f'<div class="banner danger"><span class="banner-icon">⚠️</span><div><strong>利空行业</strong><br>{"、".join(disfavored)}</div></div>'
            html += '</div>'

    # 关键宏观指标表
    indicators_rows = []

    rates = macro_data.get('rates', {})
    lpr_1y = rates.get('lpr_1y', {})
    if lpr_1y and lpr_1y.get('latest') is not None:
        indicators_rows.append(('LPR 1年期', f'{lpr_1y["latest"]}%', lpr_1y.get('direction', ''), lpr_1y.get('interpretation', '')))
    lpr_5y = rates.get('lpr_5y', {})
    if lpr_5y and lpr_5y.get('latest') is not None:
        indicators_rows.append(('LPR 5年期', f'{lpr_5y["latest"]}%', lpr_5y.get('direction', ''), lpr_5y.get('interpretation', '')))

    inflation = macro_data.get('inflation', {})
    cpi = inflation.get('cpi', {})
    if cpi and cpi.get('latest') is not None:
        indicators_rows.append(('CPI 同比', f'{cpi["latest"]}%', cpi.get('direction', ''), cpi.get('interpretation', '')))
    ppi = inflation.get('ppi', {})
    if ppi and ppi.get('latest') is not None:
        indicators_rows.append(('PPI 同比', f'{ppi["latest"]}%', ppi.get('direction', ''), ppi.get('interpretation', '')))

    pmi = macro_data.get('pmi', {})
    mfg_pmi = pmi.get('manufacturing_pmi', {})
    if mfg_pmi and mfg_pmi.get('latest') is not None:
        indicators_rows.append(('制造业 PMI', str(mfg_pmi['latest']), mfg_pmi.get('direction', ''), mfg_pmi.get('interpretation', '')))

    sf = macro_data.get('social_financing', {})
    m2 = sf.get('m2_growth', {}) if isinstance(sf, dict) else {}
    if m2 and m2.get('latest') is not None:
        indicators_rows.append(('M2 同比增速', f'{m2["latest"]}%', m2.get('direction', ''), m2.get('interpretation', '')))

    if indicators_rows:
        direction_map = {'rising': '↑ 上升', 'falling': '↓ 下降', 'stable': '→ 持平', 'insufficient_data': '—'}
        html += '<h4 class="sub-header">关键宏观指标</h4>'
        html += '<table class="data-table"><thead><tr><th>指标</th><th>最新值</th><th>趋势</th><th>解读</th></tr></thead><tbody>'
        for name, value, direction, interp in indicators_rows:
            dir_text = direction_map.get(direction, direction)
            if direction == 'rising':
                tag = '<span class="tag up">' + dir_text + '</span>'
            elif direction == 'falling':
                tag = '<span class="tag down">' + dir_text + '</span>'
            else:
                tag = '<span class="tag flat">' + dir_text + '</span>'
            html += f'<tr><td><strong>{name}</strong></td><td class="col-num">{value}</td><td>{tag}</td><td class="text-sm">{interp}</td></tr>'
        html += '</tbody></table>'

    # 国际局势
    global_context = macro_data.get('global_context', {})
    if global_context:
        html += '<h4 class="sub-header">国际局势与全球市场</h4>'
        for key, content in global_context.items():
            if isinstance(content, str) and content.strip():
                icon_map = {
                    'geopolitical': '🌐 地缘政治',
                    'global_markets': '📈 全球市场',
                    'commodities': '🛢️ 大宗商品',
                    'forex': '💱 汇率与资金',
                    'policy': '📋 宏观政策',
                }
                label = icon_map.get(key, key)
                html += f'<div class="banner info" style="margin:8px 0;"><span class="banner-icon" style="font-size:14px;">📌</span><div><strong>{label}</strong><br><span class="text-sm">{content}</span></div></div>'

    return html


def build_echarts_kline(history_df):
    """从历史数据构建 ECharts K 线图 HTML"""
    if history_df is None or history_df.empty or len(history_df) < 2:
        return ""
    # 列名兼容：Open/High/Low/Close/Volume 或 中文
    date_col = 'Date' if 'Date' in history_df.columns else '日期'
    o_col = 'Open' if 'Open' in history_df.columns else '今开'
    c_col = 'Close' if 'Close' in history_df.columns else '收盘'
    h_col = 'High' if 'High' in history_df.columns else '最高'
    l_col = 'Low' if 'Low' in history_df.columns else '最低'
    v_col = 'Volume' if 'Volume' in history_df.columns else '成交量'
    for col in [date_col, o_col, c_col, h_col, l_col]:
        if col not in history_df.columns:
            return ""
    df = history_df.tail(120).copy()  # 最近约半年
    try:
        df[date_col] = pd.to_datetime(df[date_col], utc=True).dt.strftime('%Y-%m-%d')
    except Exception:
        try:
            df[date_col] = pd.to_datetime(df[date_col]).dt.strftime('%Y-%m-%d')
        except Exception:
            df[date_col] = df[date_col].astype(str)
    dates = df[date_col].tolist()
    # ECharts candlestick: [open, close, low, high]
    k_data = [[float(df[o_col].iloc[i]), float(df[c_col].iloc[i]), float(df[l_col].iloc[i]), float(df[h_col].iloc[i])] for i in range(len(df))]
    vol = df[v_col].tolist() if v_col in df.columns else []
    import json
    dates_js = json.dumps(dates, ensure_ascii=False)
    k_js = json.dumps(k_data, ensure_ascii=False)
    vol_js = json.dumps(vol, ensure_ascii=False) if vol else '[]'
    return f'''
    <div class="chart-container" style="width:100%;margin:20px 0;"></div>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <script>
    (function(){{
        var dates = {dates_js};
        var kData = {k_js};
        var vol = {vol_js};
        var dom = document.querySelector('.chart-container');
        if (!dom || typeof echarts === 'undefined') return;
        var chart = echarts.init(dom);
        chart.setOption({{
            title: {{ text: '价格走势（K线）', left: 'center' }},
            tooltip: {{ trigger: 'axis', axisPointer: {{ type: 'cross' }}, confine: true }},
            toolbox: {{ feature: {{ dataZoom: {{}}, restore: {{}}, saveAsImage: {{}} }}, right: 20 }},
            grid: [{{ left: '10%', right: '8%', top: '15%', height: '50%' }}, {{ left: '10%', right: '8%', top: '72%', height: '15%' }}],
            xAxis: [{{ type: 'category', data: dates, gridIndex: 0, axisLabel: {{ rotate: 45 }} }}, {{ type: 'category', data: dates, gridIndex: 1, axisLabel: {{ show: false }} }}],
            yAxis: [{{ type: 'value', scale: true, gridIndex: 0, splitLine: {{ show: false }} }}, {{ type: 'value', gridIndex: 1, splitLine: {{ show: false }} }}],
            dataZoom: [{{ type: 'inside', xAxisIndex: [0,1], start: 70, end: 100 }}, {{ type: 'slider', xAxisIndex: [0,1], start: 70, end: 100 }}],
            series: [
                {{ type: 'candlestick', data: kData, xAxisIndex: 0, yAxisIndex: 0 }},
                {{ type: 'bar', data: vol, xAxisIndex: 1, yAxisIndex: 1, itemStyle: {{ color: '#ccc' }} }}
            ]
        }});
    }})();
    </script>
    '''


def analyze_realtime(realtime_data, supplemental_data=None):
    """分析实时数据

    Args:
        realtime_data: 实时行情 dict
        supplemental_data: 补充的基本面/估值 dict（可选），当实时数据中 PE/PB 缺失时使用
    """
    if not realtime_data:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到实时数据</div>', {}

    price = realtime_data.get('最新价', 0)
    change_pct = realtime_data.get('涨跌幅(%)', 0)
    volume = realtime_data.get('成交量', 0)
    pe = realtime_data.get('市盈率', 0)
    pb = realtime_data.get('市净率', 0)

    # 当 PE/PB 为 0 或 None 时，从 fundamental/valuation 补充
    sup = supplemental_data or {}
    if not pe or pe == 0:
        pe = sup.get('市盈率', 0) or 0
    if not pb or pb == 0:
        pb = sup.get('市净率', 0) or 0
    pe_str = f'{pe:.2f}' if pe and pe > 0 else 'N/A'
    pb_str = f'{pb:.2f}' if pb and pb > 0 else 'N/A'
    change_cls = 'positive' if change_pct > 0 else 'negative' if change_pct < 0 else ''

    html = f'''
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">最新价</div>
            <div class="kpi-value">{price:.2f}</div>
            <div class="kpi-sub">元/股</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">涨跌幅</div>
            <div class="kpi-value {change_cls}">{change_pct:+.2f}%</div>
            <div class="kpi-sub">当日变动</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">成交量</div>
            <div class="kpi-value" style="font-size:22px;">{volume:,.0f}</div>
            <div class="kpi-sub">手</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">市盈率 / 市净率</div>
            <div class="kpi-value" style="font-size:22px;">{pe_str} / {pb_str}</div>
            <div class="kpi-sub">PE / PB</div>
        </div>
    </div>
    '''

    metrics = {'price': price, 'change_pct': change_pct, 'pe': pe, 'pb': pb}
    return html, metrics


def analyze_history(history_df):
    """分析历史数据"""
    if history_df is None or history_df.empty:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到历史数据</div>', {}

    returns = history_df['Close'].pct_change().dropna()
    total_return = ((history_df['Close'].iloc[-1] / history_df['Close'].iloc[0]) - 1) * 100
    mean_return = returns.mean() * 252 * 100
    volatility = returns.std() * np.sqrt(252) * 100
    max_price = history_df['Close'].max()
    min_price = history_df['Close'].min()
    current_price = history_df['Close'].iloc[-1]
    from_peak = ((current_price / max_price - 1) * 100)

    ret_cls = 'positive' if total_return > 0 else 'negative'

    html = f'''
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">累计收益率</div>
            <div class="kpi-value {ret_cls}">{total_return:+.2f}%</div>
            <div class="kpi-sub">{len(history_df)} 个交易日</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">年化收益率</div>
            <div class="kpi-value" style="font-size:22px;">{mean_return:.2f}%</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">年化波动率</div>
            <div class="kpi-value" style="font-size:22px;">{volatility:.2f}%</div>
            <div class="kpi-sub">{"较稳定" if volatility < 25 else "波动较大" if volatility < 40 else "高波动"}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">区间价格</div>
            <div class="kpi-value" style="font-size:18px;">{min_price:.2f} — {max_price:.2f}</div>
            <div class="kpi-sub">当前 {current_price:.2f}，距高点 <span class="negative">{from_peak:.1f}%</span></div>
        </div>
    </div>
    '''

    metrics = {
        'total_return': total_return,
        'annual_return': mean_return,
        'volatility': volatility,
        'max_drawdown_from_peak': from_peak,
    }
    return html, metrics


def analyze_indicators(indicators_df):
    """分析技术指标"""
    if indicators_df is None or indicators_df.empty:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到技术指标数据</div>', {}

    latest = indicators_df.iloc[-1]
    ma_cols = [col for col in indicators_df.columns if col.startswith('MA_')]
    rsi = latest.get('RSI_14', latest.get('RSI', None))
    macd = latest.get('MACD', latest.get('MACD_DIF', None))
    signal = latest.get('MACD_Signal', latest.get('MACD_DEA', None))

    html = '<table class="data-table"><thead><tr><th>指标</th><th>数值</th><th>信号</th></tr></thead><tbody>'

    # MA
    if ma_cols:
        for col in sorted(ma_cols):
            value = latest.get(col, None)
            if pd.notna(value):
                html += f'<tr><td>{col}</td><td class="col-num">{value:.2f}</td><td>—</td></tr>'

    # RSI
    if pd.notna(rsi):
        if rsi > 70:
            sig_html = '<span class="tag down">超买</span>'
        elif rsi < 30:
            sig_html = '<span class="tag up">超卖</span>'
        else:
            sig_html = '<span class="tag flat">中性</span>'
        html += f'<tr><td><strong>RSI (14日)</strong></td><td class="col-num">{rsi:.2f}</td><td>{sig_html}</td></tr>'

    # MACD
    if pd.notna(macd) and pd.notna(signal):
        if macd > signal:
            sig_html = '<span class="tag up">多头</span>'
        else:
            sig_html = '<span class="tag down">空头</span>'
        html += f'<tr><td><strong>MACD</strong></td><td class="col-num">{macd:.4f}</td><td>{sig_html} (Signal: {signal:.4f})</td></tr>'

    html += '</tbody></table>'

    metrics = {
        'rsi': rsi if pd.notna(rsi) else None,
        'macd': macd if pd.notna(macd) else None,
        'macd_signal': signal if pd.notna(signal) else None,
    }
    return html, metrics


def analyze_risk(risk_data):
    """分析风险指标"""
    if not risk_data:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到风险指标数据</div>', {}

    max_dd = risk_data.get('max_drawdown', 0) * 100
    sharpe = risk_data.get('sharpe_ratio', 0)
    volatility = risk_data.get('annual_volatility', 0) * 100
    var_95 = risk_data.get('VaR_95', 0) * 100
    sortino = risk_data.get('sortino_ratio', None)
    calmar = risk_data.get('calmar_ratio', None)
    beta = risk_data.get('beta', None)
    info_ratio = risk_data.get('information_ratio', None)

    html = f'''
    <div class="kpi-row">
        <div class="kpi-card">
            <div class="kpi-label">最大回撤</div>
            <div class="kpi-value negative">{max_dd:.2f}%</div>
            <div class="kpi-sub">{"低于-30%需警惕" if max_dd < -30 else "回撤可控"}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">夏普比率</div>
            <div class="kpi-value {"positive" if sharpe > 1 else ""}">{sharpe:.2f}</div>
            <div class="kpi-sub">{">1 优秀" if sharpe > 1 else ">0.5 良好" if sharpe > 0.5 else "较差"}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">年化波动率</div>
            <div class="kpi-value" style="font-size:22px;">{volatility:.2f}%</div>
            <div class="kpi-sub">{"<25% 较稳定" if volatility < 25 else "波动较大"}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">VaR (95%)</div>
            <div class="kpi-value negative" style="font-size:22px;">{var_95:.2f}%</div>
            <div class="kpi-sub">单日最大可能亏损</div>
        </div>
    '''

    # 如有更多风险指标也展示
    if sortino is not None:
        html += f'''<div class="kpi-card">
            <div class="kpi-label">Sortino比率</div>
            <div class="kpi-value {"positive" if sortino > 1 else ""}" style="font-size:22px;">{sortino:.2f}</div>
            <div class="kpi-sub">{">1 优秀" if sortino > 1 else ">0.5 良好" if sortino > 0.5 else "较差"}</div>
        </div>'''
    if calmar is not None:
        html += f'''<div class="kpi-card">
            <div class="kpi-label">Calmar比率</div>
            <div class="kpi-value {"positive" if calmar > 1 else ""}" style="font-size:22px;">{calmar:.2f}</div>
            <div class="kpi-sub">年化收益/最大回撤</div>
        </div>'''
    if beta is not None:
        html += f'''<div class="kpi-card">
            <div class="kpi-label">Beta</div>
            <div class="kpi-value" style="font-size:22px;">{beta:.2f}</div>
            <div class="kpi-sub">{"低波动" if beta < 0.8 else "跟随市场" if beta < 1.2 else "高波动"}</div>
        </div>'''
    if info_ratio is not None:
        html += f'''<div class="kpi-card">
            <div class="kpi-label">信息比率</div>
            <div class="kpi-value" style="font-size:22px;">{info_ratio:.2f}</div>
            <div class="kpi-sub">{"优秀" if info_ratio > 0.5 else "一般" if info_ratio > 0 else "较差"}</div>
        </div>'''

    html += '</div>'

    metrics = {
        'max_drawdown': max_dd,
        'sharpe_ratio': sharpe,
        'volatility': volatility,
        'var_95': var_95,
        'sortino_ratio': sortino,
        'calmar_ratio': calmar,
        'beta': beta,
        'information_ratio': info_ratio,
    }
    return html, metrics


def generate_conclusion(all_metrics):
    """基于客观金融指标生成投资结论（多维度量化评分）

    评分维度（100分满分）：
    1. 风险调整收益（25分）：夏普比率 + Sortino比率 + Calmar比率
    2. 收益表现（20分）：年化收益率 + 近期动量
    3. 风险控制（25分）：最大回撤 + VaR + 年化波动率
    4. 技术面（15分）：RSI + MACD
    5. 估值（15分）：PE + PB
    """
    rt = all_metrics.get('realtime', {})
    hist = all_metrics.get('history', {})
    ind = all_metrics.get('indicators', {})
    risk = all_metrics.get('risk', {})

    score = 0
    reasons = []
    detail_rows = []

    # ---- 1. 风险调整收益（25分）----
    dim1_score = 0
    dim1_max = 25

    # 夏普比率（10分）
    sharpe = risk.get('sharpe_ratio', 0)
    sharpe_score = 0
    if sharpe >= 2.0:
        sharpe_score = 10
    elif sharpe >= 1.0:
        sharpe_score = 8
    elif sharpe >= 0.5:
        sharpe_score = 5
    elif sharpe >= 0:
        sharpe_score = 2
    dim1_score += sharpe_score
    detail_rows.append(('夏普比率', f'{sharpe:.2f}', f'{sharpe_score}/10',
                         '≥2优秀 | ≥1良好 | ≥0.5一般 | <0.5差'))

    # Sortino比率（8分）——从risk_data直接读取或根据收益算
    sortino = risk.get('sortino_ratio', None)
    sortino_score = 0
    if sortino is not None:
        if sortino >= 2.0:
            sortino_score = 8
        elif sortino >= 1.0:
            sortino_score = 6
        elif sortino >= 0.5:
            sortino_score = 3
        elif sortino >= 0:
            sortino_score = 1
        dim1_score += sortino_score
        detail_rows.append(('Sortino比率', f'{sortino:.2f}', f'{sortino_score}/8',
                             '≥2优秀 | ≥1良好 | ≥0.5一般'))
    else:
        # 无Sortino数据时，将8分权重分配给夏普
        bonus = min(2, sharpe_score)
        dim1_score += bonus
        detail_rows.append(('Sortino比率', 'N/A', f'{bonus}/8', '数据不足，参照夏普'))

    # Calmar比率（7分）= 年化收益 / |最大回撤|
    annual_ret = hist.get('annual_return', 0)
    max_dd = risk.get('max_drawdown', 0)
    calmar = risk.get('calmar_ratio', None)
    if calmar is None and max_dd != 0:
        calmar = annual_ret / abs(max_dd) if max_dd != 0 else 0
    calmar_score = 0
    if calmar is not None:
        if calmar >= 3.0:
            calmar_score = 7
        elif calmar >= 1.5:
            calmar_score = 5
        elif calmar >= 0.5:
            calmar_score = 3
        elif calmar >= 0:
            calmar_score = 1
        dim1_score += calmar_score
        detail_rows.append(('Calmar比率', f'{calmar:.2f}', f'{calmar_score}/7',
                             '≥3优秀 | ≥1.5良好 | ≥0.5一般'))

    score += dim1_score
    if dim1_score >= 20:
        reasons.append(f'<span class="positive">✓</span> 风险调整收益优秀（{dim1_score}/{dim1_max}分：夏普{sharpe:.2f}）')
    elif dim1_score >= 12:
        reasons.append(f'<span class="positive">○</span> 风险调整收益良好（{dim1_score}/{dim1_max}分）')
    elif dim1_score >= 6:
        reasons.append(f'<span style="color:var(--warning);">○</span> 风险调整收益一般（{dim1_score}/{dim1_max}分）')
    else:
        reasons.append(f'<span class="negative">✗</span> 风险调整收益较差（{dim1_score}/{dim1_max}分）')

    # ---- 2. 收益表现（20分）----
    dim2_score = 0
    dim2_max = 20

    # 年化收益率（12分）
    ann_ret_score = 0
    if annual_ret >= 25:
        ann_ret_score = 12
    elif annual_ret >= 15:
        ann_ret_score = 9
    elif annual_ret >= 5:
        ann_ret_score = 6
    elif annual_ret >= 0:
        ann_ret_score = 3
    dim2_score += ann_ret_score
    detail_rows.append(('年化收益率', f'{annual_ret:.2f}%', f'{ann_ret_score}/12',
                         '≥25%优秀 | ≥15%良好 | ≥5%一般'))

    # 近期动量——距高点跌幅（8分）
    from_peak = hist.get('max_drawdown_from_peak', 0)
    momentum_score = 0
    if from_peak >= -5:
        momentum_score = 8
    elif from_peak >= -15:
        momentum_score = 6
    elif from_peak >= -30:
        momentum_score = 3
    else:
        momentum_score = 0
    dim2_score += momentum_score
    detail_rows.append(('距高点回落', f'{from_peak:.1f}%', f'{momentum_score}/8',
                         '≥-5%强势 | ≥-15%正常 | <-30%弱势'))

    score += dim2_score
    if dim2_score >= 16:
        reasons.append(f'<span class="positive">✓</span> 收益表现优秀（{dim2_score}/{dim2_max}分：年化{annual_ret:.1f}%）')
    elif dim2_score >= 10:
        reasons.append(f'<span class="positive">○</span> 收益表现良好（{dim2_score}/{dim2_max}分）')
    elif dim2_score >= 5:
        reasons.append(f'<span style="color:var(--warning);">○</span> 收益表现一般（{dim2_score}/{dim2_max}分）')
    else:
        reasons.append(f'<span class="negative">✗</span> 收益表现较差（{dim2_score}/{dim2_max}分）')

    # ---- 3. 风险控制（25分）----
    dim3_score = 0
    dim3_max = 25

    # 最大回撤（10分）
    dd_score = 0
    if max_dd > -10:
        dd_score = 10
    elif max_dd > -20:
        dd_score = 7
    elif max_dd > -30:
        dd_score = 4
    elif max_dd > -50:
        dd_score = 1
    dim3_score += dd_score
    detail_rows.append(('最大回撤', f'{max_dd:.2f}%', f'{dd_score}/10',
                         '>-10%优 | >-20%良 | >-30%中 | >-50%差'))

    # VaR 95%（8分）
    var_95 = risk.get('var_95', 0)
    var_score = 0
    if var_95 > -2:
        var_score = 8
    elif var_95 > -3:
        var_score = 6
    elif var_95 > -5:
        var_score = 3
    else:
        var_score = 1
    dim3_score += var_score
    detail_rows.append(('VaR (95%)', f'{var_95:.2f}%', f'{var_score}/8',
                         '>-2%低风险 | >-3%中等 | >-5%较高'))

    # 年化波动率（7分）
    vol = risk.get('volatility', hist.get('volatility', 0))
    vol_score = 0
    if vol < 15:
        vol_score = 7
    elif vol < 25:
        vol_score = 5
    elif vol < 35:
        vol_score = 3
    else:
        vol_score = 1
    dim3_score += vol_score
    detail_rows.append(('年化波动率', f'{vol:.2f}%', f'{vol_score}/7',
                         '<15%低 | <25%中 | <35%偏高 | ≥35%高'))

    score += dim3_score
    if dim3_score >= 20:
        reasons.append(f'<span class="positive">✓</span> 风险控制优秀（{dim3_score}/{dim3_max}分：回撤{max_dd:.1f}%）')
    elif dim3_score >= 13:
        reasons.append(f'<span class="positive">○</span> 风险控制良好（{dim3_score}/{dim3_max}分）')
    elif dim3_score >= 7:
        reasons.append(f'<span style="color:var(--warning);">○</span> 风险控制一般（{dim3_score}/{dim3_max}分）')
    else:
        reasons.append(f'<span class="negative">✗</span> 风险控制较差（{dim3_score}/{dim3_max}分）')

    # ---- 4. 技术面（15分）----
    dim4_score = 0
    dim4_max = 15

    # RSI（8分）
    rsi = ind.get('rsi', None)
    rsi_score = 0
    if rsi is not None:
        if 40 <= rsi <= 60:
            rsi_score = 8
        elif 30 <= rsi <= 70:
            rsi_score = 5
        elif rsi < 30:
            rsi_score = 3  # 超卖有反弹空间
        else:
            rsi_score = 1  # 超买
        detail_rows.append(('RSI (14)', f'{rsi:.2f}', f'{rsi_score}/8',
                             '40~60中性最佳 | 30~70正常 | <30超卖 | >70超买'))
    else:
        rsi_score = 4  # 无数据给中间值
        detail_rows.append(('RSI (14)', 'N/A', f'{rsi_score}/8', '数据不足，取中值'))
    dim4_score += rsi_score

    # MACD（7分）
    macd = ind.get('macd', None)
    macd_signal = ind.get('macd_signal', None)
    macd_score = 0
    if macd is not None:
        if macd_signal is not None:
            if macd > macd_signal and macd > 0:
                macd_score = 7
            elif macd > macd_signal:
                macd_score = 5
            elif macd > 0:
                macd_score = 3
            else:
                macd_score = 1
            detail_rows.append(('MACD', f'{macd:.4f}', f'{macd_score}/7',
                                 'MACD>Signal且>0多头 | MACD>Signal偏多 | 其他偏空'))
        else:
            macd_score = 4 if macd > 0 else 2
            detail_rows.append(('MACD', f'{macd:.4f}', f'{macd_score}/7',
                                 '>0偏多 | <0偏空'))
    else:
        macd_score = 3
        detail_rows.append(('MACD', 'N/A', f'{macd_score}/7', '数据不足，取中值'))
    dim4_score += macd_score

    score += dim4_score
    if dim4_score >= 12:
        reasons.append(f'<span class="positive">✓</span> 技术面偏多（{dim4_score}/{dim4_max}分）')
    elif dim4_score >= 8:
        reasons.append(f'<span style="color:var(--warning);">○</span> 技术面中性（{dim4_score}/{dim4_max}分）')
    else:
        reasons.append(f'<span class="negative">✗</span> 技术面偏空（{dim4_score}/{dim4_max}分）')

    # ---- 5. 估值（15分）----
    dim5_score = 0
    dim5_max = 15

    pe = rt.get('pe', 0)
    pb = rt.get('pb', 0)

    # PE（8分）
    pe_score = 0
    if pe > 0:
        if pe <= 15:
            pe_score = 8
        elif pe <= 25:
            pe_score = 6
        elif pe <= 40:
            pe_score = 3
        else:
            pe_score = 1
        detail_rows.append(('市盈率 PE', f'{pe:.2f}', f'{pe_score}/8',
                             '≤15低估 | ≤25合理 | ≤40偏高 | >40高估'))
    else:
        pe_score = 0
        detail_rows.append(('市盈率 PE', 'N/A（亏损）', f'{pe_score}/8', '亏损企业无PE'))

    # PB（7分）
    pb_score = 0
    if pb > 0:
        if pb <= 1.0:
            pb_score = 7
        elif pb <= 2.0:
            pb_score = 5
        elif pb <= 5.0:
            pb_score = 3
        else:
            pb_score = 1
        detail_rows.append(('市净率 PB', f'{pb:.2f}', f'{pb_score}/7',
                             '≤1破净 | ≤2合理 | ≤5偏高 | >5高估'))
    else:
        pb_score = 0
        detail_rows.append(('市净率 PB', 'N/A', f'{pb_score}/7', '数据不足'))
    dim5_score = pe_score + pb_score

    score += dim5_score
    if dim5_score >= 12:
        reasons.append(f'<span class="positive">✓</span> 估值较低（{dim5_score}/{dim5_max}分：PE={pe:.1f}, PB={pb:.2f}）')
    elif dim5_score >= 7:
        reasons.append(f'<span style="color:var(--warning);">○</span> 估值合理（{dim5_score}/{dim5_max}分）')
    else:
        reasons.append(f'<span class="negative">✗</span> 估值偏高（{dim5_score}/{dim5_max}分）')

    # ---- 综合建议 ----
    if score >= 80:
        recommendation = "积极配置"
        rec_class = "positive"
        ring_color = "var(--success)"
    elif score >= 60:
        recommendation = "谨慎买入"
        rec_class = "positive"
        ring_color = "var(--success)"
    elif score >= 40:
        recommendation = "观望为主"
        rec_class = "neutral"
        ring_color = "var(--warning)"
    else:
        recommendation = "规避风险"
        rec_class = "negative"
        ring_color = "var(--danger)"

    circumference = 2 * 3.14159 * 56
    offset = circumference * (1 - score / 100)

    # 构建评分明细表
    detail_table = '<table class="data-table" style="margin-top:16px;"><thead><tr><th>指标</th><th>数值</th><th>得分</th><th>评分标准</th></tr></thead><tbody>'
    for name, val, sc, rule in detail_rows:
        detail_table += f'<tr><td><strong>{name}</strong></td><td class="col-num">{val}</td><td class="col-num">{sc}</td><td class="text-sm text-muted">{rule}</td></tr>'
    detail_table += '</tbody></table>'

    html = f'''
    <div class="score-container">
        <div class="score-ring">
            <svg width="140" height="140" viewBox="0 0 140 140">
                <circle class="ring-bg" cx="70" cy="70" r="56"/>
                <circle class="ring-fill" cx="70" cy="70" r="56"
                    stroke="{ring_color}"
                    stroke-dasharray="{circumference:.1f}"
                    stroke-dashoffset="{offset:.1f}"/>
            </svg>
            <div class="score-text">
                <div class="score-number" style="color:{ring_color};">{score}</div>
                <div class="score-label">/ 100 分</div>
            </div>
        </div>
        <div class="score-details">
            <p style="font-size:14px;color:var(--text-muted);margin-bottom:8px;">五维评分：风险调整收益 25 + 收益表现 20 + 风险控制 25 + 技术面 15 + 估值 15</p>
            <ul style="list-style:none;padding:0;">
                {''.join([f'<li>{r}</li>' for r in reasons])}
            </ul>
            <div class="recommendation-badge {rec_class}" style="margin-top:16px;">
                投资建议：{recommendation}
            </div>
        </div>
    </div>
    {detail_table}
    '''

    return html, recommendation


def build_summary_html(realtime_data, history_df, risk_data):
    """构建关键指标速览（KPI卡片网格布局 + 1周/1月/1年收益率 + 多种金融核心指标）"""
    cards = []
    if realtime_data:
        price = realtime_data.get('最新价', 0)
        change = realtime_data.get('涨跌幅(%)', 0)
        pe = realtime_data.get('市盈率', 0)
        pb = realtime_data.get('市净率', 0)
        change_cls = 'positive' if change > 0 else 'negative' if change < 0 else ''
        cards.append(f'<div class="kpi-card"><div class="kpi-label">最新价</div><div class="kpi-value">{price:.2f}</div><div class="kpi-sub"><span class="{change_cls}">{change:+.2f}%</span> · 元/股</div></div>')
        if pe > 0:
            cards.append(f'<div class="kpi-card"><div class="kpi-label">市盈率 PE</div><div class="kpi-value">{pe:.1f}</div><div class="kpi-sub">{"估值偏高" if pe > 40 else "估值合理" if pe > 10 else "估值偏低"}</div></div>')
        if pb > 0:
            cards.append(f'<div class="kpi-card"><div class="kpi-label">市净率 PB</div><div class="kpi-value">{pb:.2f}</div><div class="kpi-sub">{"偏高" if pb > 5 else "合理" if pb > 1 else "破净"}</div></div>')

    # 1周 / 1月 / 1年 收益率
    if history_df is not None and not history_df.empty and 'Close' in history_df.columns:
        total_days = len(history_df)
        current_price = history_df['Close'].iloc[-1]

        period_configs = [
            ('1周收益率', 5),
            ('1月收益率', 21),
            ('1年收益率', 250),
        ]

        for label, days in period_configs:
            if total_days >= days:
                past_price = history_df['Close'].iloc[-days]
                ret = ((current_price / past_price) - 1) * 100
                ret_cls = 'positive' if ret > 0 else 'negative'
                cards.append(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value {ret_cls}" style="font-size:22px;">{ret:+.2f}%</div></div>')

    # 风险/收益核心指标
    if risk_data:
        sharpe = risk_data.get('sharpe_ratio', risk_data.get('夏普比率', 0))
        max_dd = risk_data.get('max_drawdown', 0)
        if isinstance(max_dd, dict):
            max_dd = max_dd.get('max_drawdown_pct', 0)
        else:
            max_dd = max_dd * 100 if abs(max_dd) < 1 else max_dd
        vol_raw = risk_data.get('annual_volatility', 0)
        vol = vol_raw * 100 if abs(vol_raw) < 1 else vol_raw
        var_95_raw = risk_data.get('VaR_95', 0)
        var_95 = var_95_raw * 100 if abs(var_95_raw) < 1 else var_95_raw

        sharpe_color = 'positive' if sharpe > 1 else 'negative' if sharpe < 0 else ''
        cards.append(f'<div class="kpi-card"><div class="kpi-label">夏普比率</div><div class="kpi-value {sharpe_color}">{sharpe:.2f}</div><div class="kpi-sub">{"优秀" if sharpe > 1 else "良好" if sharpe > 0.5 else "较差"}</div></div>')
        cards.append(f'<div class="kpi-card"><div class="kpi-label">最大回撤</div><div class="kpi-value negative">{max_dd:.1f}%</div><div class="kpi-sub">{"风险可控" if max_dd > -20 else "需警惕" if max_dd > -35 else "风险较高"}</div></div>')
        cards.append(f'<div class="kpi-card"><div class="kpi-label">年化波动率</div><div class="kpi-value" style="font-size:22px;">{vol:.1f}%</div><div class="kpi-sub">{"低波动" if vol < 15 else "中等" if vol < 25 else "高波动"}</div></div>')
        cards.append(f'<div class="kpi-card"><div class="kpi-label">VaR (95%)</div><div class="kpi-value negative" style="font-size:22px;">{var_95:.2f}%</div><div class="kpi-sub">单日最大可能亏损</div></div>')

        # 额外金融指标（如有）
        sortino = risk_data.get('sortino_ratio', None)
        if sortino is not None:
            s_cls = 'positive' if sortino > 1 else ''
            cards.append(f'<div class="kpi-card"><div class="kpi-label">Sortino比率</div><div class="kpi-value {s_cls}" style="font-size:22px;">{sortino:.2f}</div><div class="kpi-sub">{"优秀" if sortino > 1 else "良好" if sortino > 0.5 else "较差"}</div></div>')

        calmar = risk_data.get('calmar_ratio', None)
        if calmar is not None:
            c_cls = 'positive' if calmar > 1 else ''
            cards.append(f'<div class="kpi-card"><div class="kpi-label">Calmar比率</div><div class="kpi-value {c_cls}" style="font-size:22px;">{calmar:.2f}</div><div class="kpi-sub">年化收益/最大回撤</div></div>')

        beta = risk_data.get('beta', None)
        if beta is not None:
            cards.append(f'<div class="kpi-card"><div class="kpi-label">Beta</div><div class="kpi-value" style="font-size:22px;">{beta:.2f}</div><div class="kpi-sub">{"低波动" if beta < 0.8 else "跟随市场" if beta < 1.2 else "高波动"}</div></div>')

        info_ratio = risk_data.get('information_ratio', None)
        if info_ratio is not None:
            cards.append(f'<div class="kpi-card"><div class="kpi-label">信息比率</div><div class="kpi-value" style="font-size:22px;">{info_ratio:.2f}</div><div class="kpi-sub">{"优秀" if info_ratio > 0.5 else "一般" if info_ratio > 0 else "较差"}</div></div>')

    if not cards:
        return ""
    return '<div class="kpi-row">' + ''.join(cards) + '</div>'


def build_recent_days_table(history_df, n=10):
    """构建最近 N 日行情摘要表"""
    if history_df is None or history_df.empty or len(history_df) < 2:
        return ""
    df = history_df.tail(n).copy()
    date_col = 'Date' if 'Date' in df.columns else '日期'
    close_col = 'Close' if 'Close' in df.columns else '收盘'
    vol_col = 'Volume' if 'Volume' in df.columns else '成交量'
    if date_col not in df.columns or close_col not in df.columns:
        return ""
    df['涨跌幅'] = df[close_col].pct_change() * 100
    df = df.iloc[1:]
    rows = []
    for _, r in df.iterrows():
        chg = r.get('涨跌幅', 0)
        cls = 'positive' if chg > 0 else 'negative' if chg < 0 else ''
        vol_str = f"{r[vol_col]:,.0f}" if vol_col in r else "-"
        rows.append(f'<tr><td>{r[date_col]}</td><td class="col-num">{r[close_col]:.2f}</td><td class="col-num {cls}">{chg:+.2f}%</td><td class="col-num">{vol_str}</td></tr>')
    return '<table class="data-table"><thead><tr><th>日期</th><th>收盘价</th><th>涨跌幅</th><th>成交量</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table>'


def generate_data_files_table(data_dir):
    """生成数据文件清单表格（含子目录）"""
    p = Path(data_dir)
    files = []
    seen = set()
    for file_path in (list(p.glob('*')) + list(p.rglob('*'))) if p.exists() else []:
        if file_path.is_file() and file_path.suffix.lower() in ('.csv', '.json', '.xlsx') and str(file_path) not in seen:
            seen.add(str(file_path))
            files.append({
                'name': file_path.name,
                'size': f"{file_path.stat().st_size / 1024:.2f} KB",
                'type': file_path.suffix,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })

    if not files:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未找到数据文件</div>'

    type_icons = {'.csv': '📄', '.json': '📋', '.xlsx': '📊'}
    html = '<table class="data-table"><thead><tr><th>文件名</th><th>类型</th><th>大小</th><th>修改时间</th></tr></thead><tbody>'
    for file in sorted(files, key=lambda x: x['name']):
        icon = type_icons.get(file['type'], '📁')
        html += f'<tr><td><strong>{icon} {file["name"]}</strong></td><td><span class="tag flat">{file["type"]}</span></td><td class="col-num">{file["size"]}</td><td>{file["modified"]}</td></tr>'
    html += '</tbody></table>'

    return html


def load_market_data(market_json_path):
    """加载大盘复盘数据（market_review.py 输出）"""
    if not market_json_path or not Path(market_json_path).exists():
        return None
    try:
        with open(market_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载大盘数据失败: {e}")
        return None


def render_market_indices(market_data):
    """渲染多市场指数仪表盘（KPI卡片 + 涨跌色）

    兼容 market_review.py 的两种输出格式：
      1. 单区域 dict: {region, region_label, indices, market_stats, top_gainers, top_losers, ...}
      2. 多区域 list: [{region, ...}, {region, ...}, ...]
    """
    if not market_data:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到大盘数据</div>'

    # 统一为列表格式
    if isinstance(market_data, dict):
        # 可能是 {cn: {...}, hk: {...}} 旧格式或单区域 {region: 'cn', indices: [...]}
        if 'region' in market_data and 'indices' in market_data:
            reviews = [market_data]
        else:
            # 旧格式兼容：{cn: {indices: [...]}, hk: {indices: [...]}}
            reviews = []
            region_labels = {'cn': 'A股', 'hk': '港股', 'us': '美股'}
            for key in ['cn', 'hk', 'us']:
                if key in market_data:
                    rd = market_data[key]
                    if isinstance(rd, dict):
                        rd.setdefault('region', key)
                        rd.setdefault('region_label', region_labels.get(key, key))
                        reviews.append(rd)
            if not reviews:
                # 尝试当作单区域
                reviews = [market_data]
    elif isinstance(market_data, list):
        reviews = market_data
    else:
        return '<div class="banner info"><span class="banner-icon">ℹ️</span>未获取到大盘数据</div>'

    region_emoji = {'cn': '🇨🇳', 'hk': '🇭🇰', 'us': '🇺🇸'}
    html = ''
    all_sources = set()
    latest_time = ''

    for review in reviews:
        if not isinstance(review, dict):
            continue

        region = review.get('region', '')
        label = review.get('region_label', region)
        emoji = region_emoji.get(region, '🌐')
        indices = review.get('indices', [])
        if not indices:
            continue

        # 记录元数据
        gen_at = review.get('generated_at', review.get('date', ''))
        if gen_at and gen_at > latest_time:
            latest_time = gen_at

        # === 指数卡片 ===
        html += f'<h4 class="sub-header">{emoji} {label}</h4>'
        html += '<div class="kpi-row">'
        for idx in indices:
            name = idx.get('name', idx.get('代码', ''))
            price = idx.get('price', idx.get('latest', idx.get('最新价', 0)))
            change_pct = idx.get('change_pct', idx.get('涨跌幅', 0))
            if isinstance(change_pct, str):
                try:
                    change_pct = float(change_pct.replace('%', ''))
                except ValueError:
                    change_pct = 0
            change_cls = 'positive' if change_pct > 0 else 'negative' if change_pct < 0 else ''
            price_str = f'{price:,.2f}' if isinstance(price, (int, float)) and price else str(price)
            change_val = idx.get('change', 0)
            change_str = f'{change_val:+.2f}' if isinstance(change_val, (int, float)) and change_val else ''

            # 收集数据源
            src = idx.get('source', '')
            if src:
                all_sources.add(src)

            html += f'''<div class="kpi-card">
                <div class="kpi-label">{name}</div>
                <div class="kpi-value" style="font-size:22px;">{price_str}</div>
                <div class="kpi-sub"><span class="{change_cls}">{change_pct:+.2f}%</span>'''
            if change_str:
                html += f' <span class="text-muted text-sm">({change_str})</span>'
            html += '</div></div>'
        html += '</div>'

        # === 板块排行 ===
        top_gainers = review.get('top_gainers', [])
        top_losers = review.get('top_losers', [])
        # 也兼容旧格式 sectors.top / sectors.bottom
        sectors = review.get('sectors', {})
        if not top_gainers and isinstance(sectors, dict):
            top_gainers = sectors.get('top', [])
        if not top_losers and isinstance(sectors, dict):
            top_losers = sectors.get('bottom', [])

        if top_gainers or top_losers:
            html += '<div class="grid-2" style="margin:16px 0;">'
            if top_gainers:
                html += '<div class="banner success"><span class="banner-icon">📈</span><div><strong>领涨板块</strong><br>'
                for s in top_gainers[:5]:
                    if isinstance(s, dict):
                        sname = s.get('name', s.get('板块名称', ''))
                        spct = s.get('change_pct', s.get('涨跌幅', ''))
                    else:
                        sname = str(s)
                        spct = ''
                    html += f'{sname} '
                    if spct:
                        if isinstance(spct, (int, float)):
                            html += f'<span class="positive">({spct:+.2f}%)</span> '
                        else:
                            html += f'({spct}) '
                html += '</div></div>'
            if top_losers:
                html += '<div class="banner danger"><span class="banner-icon">📉</span><div><strong>领跌板块</strong><br>'
                for s in top_losers[:5]:
                    if isinstance(s, dict):
                        sname = s.get('name', s.get('板块名称', ''))
                        spct = s.get('change_pct', s.get('涨跌幅', ''))
                    else:
                        sname = str(s)
                        spct = ''
                    html += f'{sname} '
                    if spct:
                        if isinstance(spct, (int, float)):
                            html += f'<span class="negative">({spct:+.2f}%)</span> '
                        else:
                            html += f'({spct}) '
                html += '</div></div>'
            html += '</div>'

        # === 涨跌统计 ===
        stats = review.get('market_stats', review.get('stats', {}))
        if stats:
            up_count = stats.get('up_count', stats.get('up', stats.get('上涨', '')))
            down_count = stats.get('down_count', stats.get('down', stats.get('下跌', '')))
            limit_up = stats.get('limit_up', stats.get('涨停', ''))
            limit_down = stats.get('limit_down', stats.get('跌停', ''))
            flat_count = stats.get('flat_count', stats.get('flat', stats.get('平盘', '')))
            total = stats.get('total', '')
            if up_count or down_count:
                html += '<div class="kpi-row" style="margin:12px 0;">'
                if up_count:
                    html += f'<div class="kpi-card"><div class="kpi-label">上涨</div><div class="kpi-value positive" style="font-size:22px;">{up_count}</div></div>'
                if down_count:
                    html += f'<div class="kpi-card"><div class="kpi-label">下跌</div><div class="kpi-value negative" style="font-size:22px;">{down_count}</div></div>'
                if flat_count:
                    html += f'<div class="kpi-card"><div class="kpi-label">平盘</div><div class="kpi-value" style="font-size:22px;">{flat_count}</div></div>'
                if limit_up:
                    html += f'<div class="kpi-card"><div class="kpi-label">涨停</div><div class="kpi-value positive" style="font-size:22px;">{limit_up}</div></div>'
                if limit_down:
                    html += f'<div class="kpi-card"><div class="kpi-label">跌停</div><div class="kpi-value negative" style="font-size:22px;">{limit_down}</div></div>'
                if total:
                    html += f'<div class="kpi-card"><div class="kpi-label">总数</div><div class="kpi-value" style="font-size:22px;">{total}</div></div>'
                html += '</div>'

    # 数据来源和时间
    if latest_time or all_sources:
        source_str = ' / '.join(sorted(all_sources)) if all_sources else ''
        html += f'<p class="text-muted text-sm" style="margin-top:12px;">数据时间：{latest_time}'
        if source_str:
            html += f' · 来源：{source_str}'
        html += '</p>'

    return html


def render_compare_stocks(stocks_dirs):
    """加载多只股票数据并渲染对比表格"""
    if not stocks_dirs:
        return '', ''

    dirs = [d.strip() for d in stocks_dirs.split(',') if d.strip()]
    if len(dirs) < 2:
        return '', ''

    stocks_info = []
    for d in dirs:
        rt = load_realtime_data(d)
        risk = load_risk_metrics(d)
        if rt:
            stocks_info.append({
                'name': rt.get('名称', rt.get('代码', Path(d).name)),
                'code': rt.get('代码', Path(d).name),
                'price': rt.get('最新价', 0),
                'change_pct': rt.get('涨跌幅(%)', 0),
                'pe': rt.get('市盈率', 0),
                'pb': rt.get('市净率', 0),
                'market_cap': rt.get('总市值', rt.get('流通市值', 0)),
                'volume': rt.get('成交量', 0),
                'sharpe': risk.get('sharpe_ratio', 0) if risk else 0,
                'max_dd': (risk.get('max_drawdown', 0) * 100) if risk else 0,
                'volatility': (risk.get('annual_volatility', 0) * 100) if risk else 0,
            })

    if not stocks_info:
        return '', ''

    # 核心指标对比表
    compare_html = '<h4 class="sub-header">核心指标对比</h4>'
    compare_html += '<table class="data-table"><thead><tr><th>指标</th>'
    for s in stocks_info:
        compare_html += f'<th>{s["name"]}</th>'
    compare_html += '</tr></thead><tbody>'

    rows = [
        ('最新价', 'price', lambda v: f'{v:.2f}' if v else 'N/A', ''),
        ('涨跌幅', 'change_pct', lambda v: f'{v:+.2f}%', lambda v: 'positive' if v > 0 else 'negative'),
        ('市盈率 PE', 'pe', lambda v: f'{v:.2f}' if v > 0 else 'N/A', ''),
        ('市净率 PB', 'pb', lambda v: f'{v:.2f}' if v > 0 else 'N/A', ''),
        ('总市值', 'market_cap', lambda v: _fmt_number(v) if v else 'N/A', ''),
        ('夏普比率', 'sharpe', lambda v: f'{v:.2f}', lambda v: 'positive' if v > 1 else ('negative' if v < 0 else '')),
        ('最大回撤', 'max_dd', lambda v: f'{v:.2f}%', 'negative'),
        ('年化波动率', 'volatility', lambda v: f'{v:.2f}%', ''),
    ]

    for label, key, fmt_fn, cls_fn in rows:
        compare_html += f'<tr><td><strong>{label}</strong></td>'
        for s in stocks_info:
            val = s.get(key, 0)
            formatted = fmt_fn(val)
            if callable(cls_fn):
                cls = cls_fn(val)
            elif cls_fn:
                cls = cls_fn
            else:
                cls = ''
            compare_html += f'<td class="col-num {cls}">{formatted}</td>'
        compare_html += '</tr>'
    compare_html += '</tbody></table>'

    # 归一化收益率对比（加载历史数据）
    returns_html = ''
    histories = []
    for d in dirs:
        hdf = load_history_data(d)
        if hdf is not None and not hdf.empty and 'Close' in hdf.columns:
            name = Path(d).name
            rt = load_realtime_data(d)
            if rt:
                name = rt.get('名称', rt.get('代码', name))
            total_days = len(hdf)
            current = hdf['Close'].iloc[-1]
            ret_1w = ((current / hdf['Close'].iloc[-5] - 1) * 100) if total_days >= 5 else None
            ret_1m = ((current / hdf['Close'].iloc[-21] - 1) * 100) if total_days >= 21 else None
            ret_1y = ((current / hdf['Close'].iloc[-250] - 1) * 100) if total_days >= 250 else None
            histories.append({'name': name, 'ret_1w': ret_1w, 'ret_1m': ret_1m, 'ret_1y': ret_1y})

    if histories:
        returns_html = '<h4 class="sub-header">收益率对比</h4>'
        returns_html += '<table class="data-table"><thead><tr><th>股票</th><th>1周</th><th>1月</th><th>1年</th></tr></thead><tbody>'
        for h in histories:
            returns_html += f'<tr><td><strong>{h["name"]}</strong></td>'
            for key in ['ret_1w', 'ret_1m', 'ret_1y']:
                val = h.get(key)
                if val is not None:
                    cls = 'positive' if val > 0 else 'negative'
                    returns_html += f'<td class="col-num {cls}">{val:+.2f}%</td>'
                else:
                    returns_html += '<td class="col-num">—</td>'
            returns_html += '</tr>'
        returns_html += '</tbody></table>'

    return compare_html, returns_html


# ====================================================================
# 模板加载
# ====================================================================

# 模板目录：与本脚本同级的 templates/ 文件夹
_TEMPLATES_DIR = Path(__file__).parent / 'templates'


def _load_template_file(name):
    """从 templates/ 目录加载模板文件内容"""
    path = _TEMPLATES_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"模板文件不存在: {path}")
    return path.read_text(encoding='utf-8')


def load_shared_assets():
    """加载共享 CSS 和导航 JS"""
    shared_css = _load_template_file('shared.css')
    nav_scroll_js = _load_template_file('nav_scroll.js')
    return shared_css, nav_scroll_js


# 向后兼容：HTML_TEMPLATE 仍保留，便于直接 import；但内容从外部文件加载
# 使用 lazy loading 避免文件不存在时 import 失败
class _LazyTemplate:
    """延迟加载模板字符串"""
    def __init__(self, filename):
        self._filename = filename
        self._content = None

    def __str__(self):
        if self._content is None:
            self._content = _load_template_file(self._filename)
        return self._content


HTML_TEMPLATE_MARKET = _LazyTemplate('market.html')
HTML_TEMPLATE_COMPREHENSIVE = _LazyTemplate('comprehensive.html')
HTML_TEMPLATE_COMPARE = _LazyTemplate('compare.html')
HTML_TEMPLATE = _LazyTemplate('stock.html')


def main():
    parser = argparse.ArgumentParser(
        description='HTML报告生成工具（数据驱动版）',
        epilog='示例: python generate_html_report.py --title "贵州茅台分析" --data-dir ./output/xxx/financial_data/600519_SH --output ./output/xxx/report.html'
    )
    parser.add_argument('--title', default='投资分析报告', help='报告标题（默认：投资分析报告）')
    parser.add_argument('--template', default='stock', choices=['stock', 'market', 'comprehensive', 'compare'],
                        help='报告模板：stock（个股分析，默认）| market（大盘总览）| comprehensive（综合研报）| compare（多股对比）')
    parser.add_argument('--data-dir', default='', help='数据文件目录（含 CSV/JSON）；若省略且指定了 --output，则使用 --output 所在目录）')
    parser.add_argument('--output', required=True, help='输出HTML文件路径')
    parser.add_argument('--analyst', default='AI Financial Advisor', help='分析师名称')
    parser.add_argument('--data-source', default='', help='数据来源（留空则从数据文件自动检测）')
    parser.add_argument('--valuation-json', default='', help='估值分析 JSON 文件路径（calculate_valuation.py 输出，可选）')
    parser.add_argument('--comps-json', default='', help='可比公司分析 JSON 文件路径（calculate_valuation.py --mode comps 输出，可选）')
    parser.add_argument('--macro-json', default='', help='宏观经济分析 JSON 文件路径（macro_analysis.py 输出，可选）')
    parser.add_argument('--market-json', default='', help='大盘数据 JSON 文件路径（market_review.py 输出，market/comprehensive 模板使用）')
    parser.add_argument('--stocks', default='', help='多股数据目录（逗号分隔，compare 模板使用）如：dir1,dir2,dir3')
    parser.add_argument('--ai-analysis-json', default='', help='AI 综合分析 JSON 文件路径（ai_analysis.json，含结论/影响评估/新闻情报，可选）')
    parser.add_argument('--ai-deep-analysis-json', default='', help='AI 深度分析 JSON 文件路径（ai_deep_analysis.json，含推理链路/多维分析，可选；若不指定则从 --ai-analysis-json 中读取）')
    args = parser.parse_args()

    # 若未指定 --data-dir，使用 --output 所在目录（支持递归查找 CSV）
    if not args.data_dir or not Path(args.data_dir).exists():
        args.data_dir = str(Path(args.output).parent)
        logger.info(f"未指定或无效的 --data-dir，使用: {args.data_dir}")

    logger.info("=" * 60)
    logger.info(f"开始生成HTML报告（模板: {args.template}）")
    logger.info("=" * 60)

    from jinja2 import Template

    # 加载共享 CSS 和导航 JS（从 templates/ 目录）
    shared_css, nav_scroll_js = load_shared_assets()

    # 公共数据加载
    generation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date_str = datetime.now().strftime('%Y年%m月%d日')

    # 宏观经济分析（可选，所有模板通用）
    macro_data_raw = load_macro_data(args.macro_json) if args.macro_json else None
    macro_html = render_macro_section(macro_data_raw) if macro_data_raw else ""
    if macro_html:
        logger.info("已加载宏观经济分析数据")

    # AI 综合分析（可选，所有模板通用）
    ai_analysis_data = load_ai_analysis(args.ai_analysis_json) if args.ai_analysis_json else None
    ai_deep_data = load_ai_analysis(args.ai_deep_analysis_json) if args.ai_deep_analysis_json else None
    ai_brief_html, ai_events_html, ai_deep_html = render_ai_analysis_section(ai_analysis_data, ai_deep_data) if ai_analysis_data else ("", "", "")
    if ai_brief_html or ai_events_html or ai_deep_html:
        logger.info("已加载 AI 综合分析数据")

    # 大盘数据（market / comprehensive 模板使用）
    market_data_raw = load_market_data(args.market_json) if args.market_json else None
    market_indices_html = render_market_indices(market_data_raw) if market_data_raw else ""
    if market_indices_html:
        logger.info("已加载大盘数据")

    # ===================================================================
    # 模板路由
    # ===================================================================

    if args.template == 'market':
        # ----- 大盘总览模板 -----
        logger.info("使用大盘总览模板（market）")
        template = Template(str(HTML_TEMPLATE_MARKET))
        html_content = template.render(
            title=args.title,
            date=date_str,
            generation_time=generation_time,
            analyst=args.analyst,
            shared_css=shared_css,
            nav_scroll_js=nav_scroll_js,
            market_indices_html=market_indices_html,
            macro_html=macro_html,
            ai_brief_html=ai_brief_html,
            ai_events_html=ai_events_html,
            ai_deep_html=ai_deep_html,
        )
        recommendation = "大盘总览"

    elif args.template == 'comprehensive':
        # ----- 综合研报模板 -----
        logger.info("使用综合研报模板（comprehensive）")

        # 加载个股数据（如有）
        realtime_data = load_realtime_data(args.data_dir)
        history_df = load_history_data(args.data_dir)
        indicators_df = load_indicators(args.data_dir)
        risk_data = load_risk_metrics(args.data_dir)
        fundamental_data = load_fundamental_data(args.data_dir)

        realtime_html, _ = analyze_realtime(realtime_data, fundamental_data) if realtime_data else ("", {})
        indicators_html, _ = analyze_indicators(indicators_df) if indicators_df is not None else ("", {})
        risk_html, _ = analyze_risk(risk_data) if risk_data else ("", {})
        echarts_html = build_echarts_kline(history_df)
        summary_html = build_summary_html(realtime_data, history_df, risk_data)

        template = Template(str(HTML_TEMPLATE_COMPREHENSIVE))
        html_content = template.render(
            title=args.title,
            date=date_str,
            generation_time=generation_time,
            analyst=args.analyst,
            shared_css=shared_css,
            nav_scroll_js=nav_scroll_js,
            market_indices_html=market_indices_html,
            summary_html=summary_html,
            realtime_html=realtime_html,
            echarts_html=echarts_html,
            indicators_html=indicators_html,
            risk_html=risk_html,
            macro_html=macro_html,
            ai_brief_html=ai_brief_html,
            ai_events_html=ai_events_html,
            ai_deep_html=ai_deep_html,
        )
        recommendation = "综合研报"

    elif args.template == 'compare':
        # ----- 多股对比模板 -----
        logger.info("使用多股对比模板（compare）")
        compare_html, returns_html = render_compare_stocks(args.stocks)
        if not compare_html:
            logger.warning("未提供有效的 --stocks 参数或数据不足，回退到默认模板")
            args.template = 'stock'  # fallback

        if args.template == 'compare':
            template = Template(str(HTML_TEMPLATE_COMPARE))
            html_content = template.render(
                title=args.title,
                date=date_str,
                generation_time=generation_time,
                analyst=args.analyst,
                shared_css=shared_css,
                nav_scroll_js=nav_scroll_js,
                compare_html=compare_html,
                returns_html=returns_html,
                ai_brief_html=ai_brief_html,
                ai_events_html=ai_events_html,
                ai_deep_html=ai_deep_html,
            )
            recommendation = "多股对比"

    # stock 模板（默认）或 compare 回退
    if args.template == 'stock':
        # ----- 个股分析模板（原有逻辑） -----
        logger.info("使用个股分析模板（stock）")

        realtime_data = load_realtime_data(args.data_dir)
        history_df = load_history_data(args.data_dir)
        indicators_df = load_indicators(args.data_dir)
        risk_data = load_risk_metrics(args.data_dir)
        fundamental_data = load_fundamental_data(args.data_dir)

        data_source = args.data_source.strip() if args.data_source else detect_data_source(args.data_dir)
        logger.info(f"数据来源: {data_source}")

        realtime_html, realtime_metrics = analyze_realtime(realtime_data, fundamental_data)
        history_html, history_metrics = analyze_history(history_df)
        indicators_html, indicators_metrics = analyze_indicators(indicators_df)
        risk_html, risk_metrics = analyze_risk(risk_data)

        all_metrics = {
            'realtime': realtime_metrics,
            'history': history_metrics,
            'indicators': indicators_metrics,
            'risk': risk_metrics
        }
        conclusion_html, recommendation = generate_conclusion(all_metrics)
        echarts_html = build_echarts_kline(history_df)

        valuation_data = load_valuation_data(args.valuation_json) if args.valuation_json else None
        comps_raw = load_comps_data(args.comps_json) if args.comps_json else None
        if not comps_raw and valuation_data and 'comps' in valuation_data:
            comps_raw = valuation_data
        dcf_html = render_dcf_section(valuation_data) if valuation_data else ""
        comps_html = render_comps_section(comps_raw) if comps_raw else ""
        statements_html = render_statements_section(valuation_data) if valuation_data else ""

        data_cutoff_time = ""
        if realtime_data and realtime_data.get('获取时间'):
            data_cutoff_time = str(realtime_data['获取时间'])
        elif history_df is not None and not history_df.empty:
            date_col = 'Date' if 'Date' in history_df.columns else '日期'
            if date_col in history_df.columns:
                data_cutoff_time = str(history_df[date_col].iloc[-1])
        if not data_cutoff_time:
            data_cutoff_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        summary_html = build_summary_html(realtime_data, history_df, risk_data)
        recent_days_html = build_recent_days_table(history_df)

        template = Template(str(HTML_TEMPLATE))
        html_content = template.render(
            title=args.title,
            date=date_str,
            analyst=args.analyst,
            data_source=data_source,
            data_cutoff_time=data_cutoff_time,
            generation_time=generation_time,
            shared_css=shared_css,
            nav_scroll_js=nav_scroll_js,
            summary_html=summary_html,
            conclusion_html=conclusion_html,
            realtime_html=realtime_html,
            history_html=history_html,
            recent_days_html=recent_days_html,
            echarts_html=echarts_html,
            indicators_html=indicators_html,
            risk_html=risk_html,
            dcf_html=dcf_html,
            comps_html=comps_html,
            statements_html=statements_html,
            macro_html=macro_html,
            ai_brief_html=ai_brief_html,
            ai_events_html=ai_events_html,
            ai_deep_html=ai_deep_html,
        )

    # 保存HTML文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    logger.info("=" * 60)
    logger.info(f"✅ HTML报告已生成: {output_path}")
    logger.info(f"模板: {args.template} | 建议: {recommendation}")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
