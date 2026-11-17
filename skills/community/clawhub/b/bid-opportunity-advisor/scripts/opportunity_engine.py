#!/usr/bin/env python3
"""
Bid Opportunity Engine (draft)

Aligns public bid data to "my company profile" and produces a trustworthy
Go/No-Go with confidence, plus a self-contained HTML report (inline SVG,
no external CDN).

Design principles:
  - regional_access is computed from the real profile province vs the
    procurement-region distribution (no hardcoded placeholder).
  - confidence is derived from sample size; decisions are labeled accordingly.
  - fit scoring aligns opportunities to MY company (products/region/scale/qual).

Usage:
    python opportunity_engine.py <input_json> --profile <profile_json> \
        --output <out.html>

Input record schema (one dict per record):
    title, type, buyer, agency, budget_amount, win_amount, win_company,
    region, publish_date, project_name, content_summary,
    source_platform, source_url, project_type.
Profile schema: {"company","province","qualifications":[],"products":[],
                 "capacity_tier":"micro|small|medium|large|mega"}
"""

import json
import sys
import os
import re
import argparse
import statistics
from datetime import datetime
from collections import Counter, defaultdict
from pathlib import Path


# ---------- loaders ----------

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict) and 'records' in data:
        data = data['records']
    elif not isinstance(data, list):
        data = [data]
    return data


def load_profile(path):
    if not path or not Path(path).exists():
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ---------- cross-source dedup ----------

def _norm(s):
    return re.sub(r'\s+', '', s or '').strip()


def dedup_key(r):
    """跨源同一项目判定：项目名 + 采购人 + 发布日（任一为空则用其余两项）。"""
    name = _norm(r.get('project_name') or r.get('title') or '')
    buyer = _norm(r.get('buyer') or '')
    date = _norm(r.get('publish_date') or '')
    return (name, buyer, date)


def dedup_records(records):
    """按 (项目名+采购人+日期) 去重；重复项合并字段，保留信息更全者。

    返回 (deduped_list, removed_count)。无足够标识(名/采购人均空)的记录不判重、原样保留。
    """
    seen = {}
    kept = []
    removed = 0
    merge_fields = ('budget_amount', 'win_amount', 'win_company',
                    'project_name', 'project_type', 'agency', 'region')
    for r in records:
        k = dedup_key(r)
        if not k[0] and not k[1]:      # 无项目名也无采购人，无法判重
            kept.append(r)
            continue
        if k in seen:
            removed += 1
            existing = seen[k]
            for f in merge_fields:
                if r.get(f) is not None and existing.get(f) is None:
                    existing[f] = r[f]
            continue
        seen[k] = r
        kept.append(r)
    return kept, removed


# ---------- parsing helpers (reuse) ----------

def parse_date(s):
    if not s or s == 'null':
        return None
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(s[:19] if len(s) > 19 else s, fmt)
        except (ValueError, TypeError):
            continue
    return None


def parse_amount(v):
    if v is None or v == 'null' or v == '':
        return None
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, str):
        v = v.strip().replace(',', '').replace(' ', '')
        try:
            return int(float(v))
        except ValueError:
            return None
    return None


def extract_province(region):
    if not region:
        return 'unknown'
    region = region.strip()
    for prefix in ['北京', '上海', '天津', '重庆', '香港', '澳门', '台湾']:
        if region.startswith(prefix):
            return prefix + '市' if prefix in ('北京', '上海', '天津', '重庆') else prefix
    for prov in ['广东', '江苏', '浙江', '山东', '四川', '河南', '湖北', '湖南',
                 '河北', '福建', '安徽', '辽宁', '陕西', '江西', '广西', '云南',
                 '贵州', '山西', '吉林', '黑龙江', '甘肃', '内蒙古', '新疆',
                 '宁夏', '青海', '西藏', '海南']:
        if prov in region:
            return prov + ('省' if prov not in ('广西', '内蒙古', '新疆', '宁夏', '西藏') else '')
    return region[:6]


def budget_tier(amount):
    if amount is None:
        return 'unknown'
    if amount < 100000:
        return 'micro'
    elif amount < 1000000:
        return 'small'
    elif amount < 10000000:
        return 'medium'
    elif amount < 100000000:
        return 'large'
    return 'mega'


TIER_ORDER = ['micro', 'small', 'medium', 'large', 'mega', 'unknown']


# ---------- analyses (reuse + extend) ----------

def analyze_trends(records):
    monthly = defaultdict(lambda: {'total': 0, 'bid': 0, 'win': 0})
    regional = Counter()
    method = Counter()
    budget = Counter()
    for r in records:
        dt = parse_date(r.get('publish_date'))
        if dt:
            k = dt.strftime('%Y-%m')
            monthly[k]['total'] += 1
            t = r.get('type', '')
            if '招标' in t:
                monthly[k]['bid'] += 1
            elif '中标' in t:
                monthly[k]['win'] += 1
        regional[extract_province(r.get('region'))] += 1
        method[r.get('project_type') or 'unknown'] += 1
        budget[budget_tier(parse_amount(r.get('budget_amount')))] += 1
    return {
        'monthly': dict(sorted(monthly.items())),
        'regional': dict(regional.most_common(15)),
        'procurement_methods': dict(method.most_common()),
        'budget_distribution': {k: budget.get(k, 0) for k in TIER_ORDER if budget.get(k, 0) > 0},
    }


def analyze_winners(records):
    wins = [r for r in records if r.get('type') and '中标' in r.get('type', '')]
    stats = defaultdict(lambda: {'wins': 0, 'total': 0, 'amounts': [], 'regions': set()})
    for r in wins:
        c = (r.get('win_company') or '').strip()
        if not c:
            continue
        stats[c]['wins'] += 1
        a = parse_amount(r.get('win_amount'))
        if a:
            stats[c]['total'] += a
            stats[c]['amounts'].append(a)
        if r.get('region'):
            stats[c]['regions'].add(r.get('region'))
    ranked = sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)
    total = sum(s['total'] for _, s in ranked)
    shares = [s['total'] / total for c, s in ranked] if total else []
    hhi = sum(x * x for x in shares) * 10000
    cr5 = sum(shares[:5]) * 100 if len(shares) >= 5 else sum(shares) * 100
    conc = 'low' if hhi < 1500 else ('medium' if hhi < 2500 else 'high')
    return {'ranked': [(c, s) for c, s in ranked[:15]], 'total_winners': len(stats),
            'hhi': round(hhi, 1), 'cr5': round(cr5, 1), 'concentration': conc,
            'win_records': len(wins)}


def analyze_prices(records):
    amounts, discs = [], []
    for r in records:
        if r.get('type') and '中标' in r.get('type', ''):
            w = parse_amount(r.get('win_amount'))
            if w and w > 0:
                amounts.append(w)
            b = parse_amount(r.get('budget_amount'))
            if b and w and b > 0:
                discs.append((b - w) / b * 100)
    ps = {}
    if amounts:
        ps = {'count': len(amounts), 'min': min(amounts), 'max': max(amounts),
              'mean': statistics.mean(amounts), 'median': statistics.median(amounts),
              'q1': statistics.quantiles(amounts, n=4)[0] if len(amounts) >= 4 else min(amounts),
              'q3': statistics.quantiles(amounts, n=4)[2] if len(amounts) >= 4 else max(amounts),
              'stdev': statistics.stdev(amounts) if len(amounts) >= 2 else 0}
    ds = {}
    if discs:
        ds = {'count': len(discs), 'avg': statistics.mean(discs), 'median': statistics.median(discs),
              'min': min(discs), 'max': max(discs),
              'interpretation': ('low' if statistics.mean(discs) < 5 else 'medium' if statistics.mean(discs) < 15 else 'high')}
    return {'price_stats': ps, 'discount_stats': ds}


# ---------- NEW: profile alignment ----------

def compute_fit(records, profile):
    """Return (fit_score_or_None, breakdown) aligning opportunities to MY company."""
    if not profile:
        return None, {'note': 'no profile -> fit not computed'}
    prov = profile.get('province', '')
    products = [p.lower() for p in profile.get('products', [])]
    quals = profile.get('qualifications', [])
    cap = profile.get('capacity_tier', '')

    # product match: overlap of my products vs project text
    matched = 0
    for r in records:
        text = f"{r.get('project_name','')} {r.get('content_summary','')}".lower()
        if products and any(p in text for p in products):
            matched += 1
    product_score = (matched / len(records) * 100) if records else 0

    # region match: my province vs each record's region
    in_prov = sum(1 for r in records if prov and prov in (r.get('region') or ''))
    region_score = 100 if in_prov / max(len(records), 1) > 0.5 else (60 if in_prov else 50)

    # scale match: my capacity_tier vs budget tier distribution
    tiers = [budget_tier(parse_amount(r.get('budget_amount'))) for r in records]
    tiers = [t for t in tiers if t != 'unknown']
    common = Counter(tiers).most_common(1)[0][0] if tiers else ''
    order = {'micro': 0, 'small': 1, 'medium': 2, 'large': 3, 'mega': 4}
    diff = order.get(common, 2) - order.get(cap, 2)
    scale_score = {0: 100, 1: 70, -1: 70, 2: 40, -2: 40}.get(diff, 60)

    # qualification: cannot derive from data -> labeled heuristic, NOT a fake
    qual_score = 70 if quals else 50
    qual_unverified = bool(quals)

    fit = 0.30 * product_score + 0.20 * region_score + 0.25 * scale_score + 0.25 * qual_score
    return round(fit, 1), {
        'product': round(product_score, 1), 'region': region_score,
        'scale': scale_score, 'qualification': qual_score,
        'qual_unverified': qual_unverified,
        'matched_projects': matched, 'total': len(records),
    }


def compute_regional_access(records, profile):
    """REAL (not placeholder): openness of this market to a bidder from my province."""
    if not profile:
        return None, 'cannot evaluate without profile'
    prov = profile.get('province', '')
    with_region = [r for r in records if r.get('region')]
    if not with_region:
        return None, 'no region data'
    in_prov = sum(1 for r in with_region if prov and prov in r.get('region', ''))
    ratio = in_prov / len(with_region)
    # high local clustering => local incumbents dominate => low access for outsider
    if ratio > 0.4:
        score = 2
    elif ratio > 0.1:
        score = 3
    else:
        score = 5
    return score, f"local_share={ratio:.0%}"


def opportunity_score(trend, winner, price, regional_access):
    total = len(records_ref)
    mv = 5 if total >= 20 else 4 if total >= 10 else 3 if total >= 5 else 2 if total >= 2 else 1
    hhi = winner.get('hhi', 0)
    comp = 5 if hhi < 1000 else 4 if hhi < 1500 else 3 if hhi < 2500 else 2 if hhi < 5000 else 1
    avg_d = price.get('discount_stats', {}).get('avg', 10)
    pm = 5 if avg_d < 3 else 4 if avg_d < 8 else 3 if avg_d < 15 else 2 if avg_d < 25 else 1
    bd = trend.get('budget_distribution', {})
    small_r = (bd.get('micro', 0) + bd.get('small', 0)) / max(total, 1)
    eb = 5 if small_r > 0.5 else 4 if small_r > 0.3 else 3 if small_r > 0.15 else 2 if small_r > 0.05 else 1
    ra = regional_access[0] if regional_access and regional_access[0] is not None else None
    scores = {'market_volume': mv, 'competition': comp, 'price_margin': pm, 'entry_barrier': eb}
    if ra is not None:
        scores['regional_access'] = ra
    weights = {'market_volume': 0.25, 'competition': 0.25, 'price_margin': 0.20,
               'entry_barrier': 0.15, 'regional_access': 0.15}
    if ra is None:  # renormalize when unavailable
        wsum = sum(weights[k] for k in scores)
        total_w = sum(weights[k] for k in weights if k in scores)
        weights = {k: weights[k] / total_w for k in scores}
    tot = sum(scores[k] * weights[k] for k in scores)
    rating = 'excellent' if tot >= 4 else 'good' if tot >= 3 else 'fair' if tot >= 2 else 'poor'
    return {'scores': scores, 'weights': weights, 'total': round(tot, 2), 'rating': rating}


def confidence(total):
    return 'high' if total >= 10 else 'medium' if total >= 5 else 'low'


def go_no_go(fit, opp_total, conf, has_profile):
    if not has_profile:
        return '可跟(通用)' if opp_total >= 3.5 else '谨慎', '未对齐贵司画像，仅按市场面判断'
    if fit >= 75 and opp_total >= 4.0 and conf != 'low':
        return '强烈建议跟', 'fit高且市场面优'
    if fit >= 60 or opp_total >= 3.5:
        return '可跟', 'fit或市场面达标'
    if fit >= 40 or opp_total >= 2.5:
        return '谨慎', '部分维度偏弱'
    return '不建议', 'fit低或市场面差'


records_ref = []  # module-level ref for opportunity_score convenience


# ---------- self-contained SVG charts ----------

def svg_bar(labels, values, color='#1890ff', w=680, h=220):
    if not values:
        return ''
    maxv = max(values) or 1
    n = len(labels)
    gap = 12
    bw = (w - 40 - gap * (n - 1)) / max(n, 1)
    parts = [f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" width="100%">']
    for i, (lab, val) in enumerate(zip(labels, values)):
        x = 20 + i * (bw + gap)
        bh = (val / maxv) * (h - 50)
        y = h - 30 - bh
        parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{color}" rx="3"/>')
        parts.append(f'<text x="{x+bw/2:.0f}" y="{h-12}" font-size="11" text-anchor="middle" fill="#555">{lab}</text>')
        parts.append(f'<text x="{x+bw/2:.0f}" y="{y-4:.0f}" font-size="10" text-anchor="middle" fill="#333">{val}</text>')
    parts.append('</svg>')
    return ''.join(parts)


# ---------- HTML report ----------

def html_report(records, trend, winner, price, fit, ra, opp, conf, gng, profile):
    total = len(records)
    win = winner.get('win_records', 0)
    bid = total - win
    fit_html = f"<p>Fit: {fit[0]} / 100</p>" if fit[0] is not None else "<p>Fit: 未计算（无公司画像）</p>"
    reg_html = svg_bar(list(trend['regional'].keys())[:10], list(trend['regional'].values())[:10], '#1890ff')
    win_labels = [c[:18] for c, _ in winner['ranked'][:10]]
    win_vals = [s['total'] for _, s in winner['ranked'][:10]]
    win_html = svg_bar(win_labels, win_vals, '#52c41a')
    monthly_labels = list(trend['monthly'].keys())
    monthly_vals = [trend['monthly'][m]['total'] for m in monthly_labels]
    monthly_html = svg_bar(monthly_labels, monthly_vals, '#722ed1')
    ra_txt = ra[1] if ra else 'n/a'
    scores_txt = ' · '.join(f"{k}={v}" for k, v in opp['scores'].items())
    ds = price.get('discount_stats') or {}
    disc_avg = f"{ds.get('avg', 0):.1f}" if ds.get('avg') is not None else 'n/a'
    disc_intp = ds.get('interpretation', '-') or '-'
    if disc_avg == 'n/a':
        disc_line = '折扣率：n/a（无中标样本，无法计算）'
    else:
        disc_line = f'折扣率：{disc_avg}%（{disc_intp}）'
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="generator" content="bid-opportunity-advisor">
<style>body{{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;background:#f5f5f5;color:#333;line-height:1.6;margin:0;padding:20px}}
.container{{max-width:1000px;margin:0 auto;background:#fff;padding:24px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
h1{{font-size:24px}}h2{{font-size:18px;margin-top:28px;border-bottom:2px solid #e0e0e0;padding-bottom:6px}}
.card{{background:#e6f7ff;border-left:4px solid #1890ff;padding:12px 16px;margin:12px 0;border-radius:0 4px 4px 0}}
.flag{{color:#fa8c16;font-weight:600}}</style></head><body><div class="container">
<h1>投标机会分析报告</h1>
<p>生成：{datetime.now():%Y-%m-%d %H:%M} ｜ 记录：{total}（招标 {bid} / 中标 {win}）｜ 置信：<b>{conf}</b></p>
<div class="card"><b>Go/No-Go：{gng[0]}</b> — {gng[1]}</div>
{fit_html}
<h2>1. 趋势</h2>{monthly_html}
<h2>2. 地域分布</h2>{reg_html}
<h2>3. 中标方排名</h2>{win_html}
<h2>4. 机会评分</h2><p>{scores_txt}</p><p>总分：<b>{opp['total']}/5.0（{opp['rating']}）</b></p>
<p>地域可达性：{ra_txt}</p>
<h2>5. 价格</h2><p>{disc_line}</p>
<p class="flag">说明：资质匹配为启发式（数据未含标讯资质要求），需用户复核；样本薄时置信低，建议小范围试水。</p>
</div></body></html>"""


# ---------- main ----------

def main():
    global records_ref
    ap = argparse.ArgumentParser()
    ap.add_argument('input_json')
    ap.add_argument('--profile', default=None)
    ap.add_argument('--output', '-o', default=None)
    args = ap.parse_args()

    records = load_data(args.input_json)
    records_ref = records
    profile = load_profile(args.profile)
    if not records:
        print("Error: no records"); sys.exit(1)

    # 跨源去重（ccgp ↔ cebpubservice 同一项目只计一次）
    records, removed = dedup_records(records)
    records_ref = records
    if removed:
        print(f"[去重] 跨源/重复记录移除 {removed} 条，进入分析 {len(records)} 条")
    else:
        print(f"[去重] 无重复，进入分析 {len(records)} 条")

    trend = analyze_trends(records)
    winner = analyze_winners(records)
    price = analyze_prices(records)
    fit = compute_fit(records, profile)
    ra = compute_regional_access(records, profile)
    opp = opportunity_score(trend, winner, price, ra)
    conf = confidence(len(records))
    has_profile = profile is not None
    gng = go_no_go(fit[0] if fit[0] is not None else 0, opp['total'], conf, has_profile)

    summary = {
        'go_no_go': gng, 'confidence': conf,
        'fit': fit[0], 'fit_breakdown': fit[1],
        'opportunity': opp, 'regional_access': ra,
        'hhi': winner['hhi'], 'cr5': winner['cr5'],
        'price_discount_avg': price.get('discount_stats', {}).get('avg'),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    html = html_report(records, trend, winner, price, fit, ra, opp, conf, gng, profile)
    out = Path(args.output) if args.output else Path(args.input_json).parent / 'opportunity_report.html'
    out.write_text(html, encoding='utf-8')
    print(f"\nReport: {out}")


if __name__ == '__main__':
    main()
