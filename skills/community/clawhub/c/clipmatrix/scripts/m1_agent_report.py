#!/usr/bin/env python3
"""
M1 Agent Report — 精简版
核心：角色判定 + M1风格卡优化建议 + 独立站 + 异常标记

设计原则：
- 不对账号做"该停/该加"的决策（盼哥定）
- 只提供"这个方向表现好/差"的信号
- 所有建议都是"供参考"，不是自动执行
"""

import json, os, logging
from datetime import datetime

logger = logging.getLogger(__name__)

ACCOUNT_TRACK = {
    '00': 'brand_statement', '01': 'first_timer', '02': 'city_intro',
    '03': 'couple', '04': 'city_intro', '05': 'family', '06': 'slow_travel',
    '07': 'city_lifestyle', '08': 'hidden_gems', '09': 'business_travel',
    '10': 'food', '11': 'scenic_routes', '12': 'hidden_cities',
    '13': 'premium_routes', '14': 'budget_routes', '15': 'city_discovery',
    '16': 'travel_checklist', '17': 'first_timer_tips',
    '18': 'trip_secrets', '19': 'trip_planner',
    '20': 'comparison', '21': 'comparison',
}


def build_agent_report(today: dict, baseline: dict, insights_data: dict,
                       site_data: dict = None) -> dict:
    now = datetime.now()

    # ═══════════════════════════
    # Part 1: KPI总览
    # ═══════════════════════════
    tv = sum(d['views'] for d in today.values())
    tp = sum(d['posts'] for d in today.values())
    tl = sum(d['likes'] for d in today.values())
    bv = sum(b.get('views', 0) for b in baseline.values())

    kpi = {
        "total_views": tv, "total_likes": tl, "total_posts": tp,
        "avg_per_post": tv // max(tp, 1),
        "baseline_views": bv,
        "growth_vs_baseline": tv - bv,
        "platforms": {"tiktok": 22, "instagram": 11},
    }

    # ═══════════════════════════
    # Part 2: 账号角色 + 关键信号
    # ═══════════════════════════
    ig_accounts = {'00','01','03','04','05','06','07','09','10','14','17'}
    accounts = {}

    for aid in sorted(today.keys(), key=int):
        td = today[aid]
        bl = baseline.get(aid, {})
        p = td['posts']
        v = td['views']
        avg = v // max(p, 1)
        growth = (v - bl.get('views', 0)) / max(bl.get('views', 0), 1) * 100

        # 角色
        role = _classify(p, avg)

        # 平台
        plats = ['tiktok']
        if aid in ig_accounts:
            plats.append('instagram')

        # 异常检测
        alerts = []
        if p > 10 and avg < 30:
            alerts.append({"type": "ultra_low_engagement", "detail": f"avg={avg}/post across {p} posts"})
        if growth < -30 and bv > 0:
            alerts.append({"type": "sharp_decline", "detail": f"views {growth:+.0f}% vs baseline"})

        # IG被封
        if aid in ('02', '08'):
            alerts.append({"type": "ig_banned", "detail": "Instagram account suspended"})

        accounts[aid] = {
            "name": _name(aid),
            "track": ACCOUNT_TRACK.get(aid, 'unknown'),
            "role": role,
            "platforms": plats,
            "kpi": {"posts": p, "views": v, "likes": td['likes'], "avg_per_post": avg,
                    "growth_pct": round(growth, 1)},
            "alerts": alerts,
            "ai_insight": _extract_key_insight(aid, insights_data),
        }

    # ═══════════════════════════
    # Part 3: M1风格卡优化建议
    # ═══════════════════════════
    style_suggestions = _build_style_suggestions(accounts, insights_data)

    # ═══════════════════════════
    # Part 4: 独立站
    # ═══════════════════════════
    if site_data:
        s = site_data.get('summary', {})
        daily = site_data.get('daily', [])
        top_pages = site_data.get('top_pages', [])
        waf = site_data.get('waf', {})
        site = {
            "summary": {"total_pv": s.get('total_pv', 0),
                       "daily_avg_pv": s.get('daily_avg_pv', 0),
                       "days": s.get('days', 0)},
            "recent_daily": [{"date": d['date'], "pv": d['pv']} for d in daily[-3:]],
            "top_pages_real": [{"path": p['path'], "hits": p['requests']}
                              for p in top_pages[:5]
                              if not any(x in p['path'] for x in ('wp-', 'llms', 'lander', '.env'))],
            "waf_blocked_24h": waf.get('total_blocked', 0),
        }
    else:
        site = {"summary": {"total_pv": 0}, "note": "独立站数据模块未加载"}

    # ═══════════════════════════
    # Part 5: 角色汇总
    # ═══════════════════════════
    roles = {}
    for aid, acc in accounts.items():
        r = acc['role']
        if r not in roles:
            roles[r] = []
        roles[r].append(aid)

    # ═══════════════════════════
    # 组装
    # ═══════════════════════════
    return {
        "meta": {
            "generated_at": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "baseline": now.strftime("%Y-%m-%d"),  # 基线日期（当日首次运行=当日，后续为baseline.csv日期）
            "accounts": len(accounts),
        },
        "kpi": kpi,
        "role_summary": {r: {"count": len(aids), "accounts": aids}
                        for r, aids in sorted(roles.items())},
        "accounts": accounts,
        "style_suggestions": style_suggestions,
        "independent_site": site,
    }


def _classify(posts: int, avg: int) -> str:
    if posts == 0:
        return 'dormant'
    if avg >= 200 and posts >= 10:
        return 'winner'
    if avg >= 100 and posts >= 5:
        return 'emerging'
    if posts <= 10:
        return 'validation'
    if posts <= 20:
        return 'exploration'
    return 'saturated'


def _name(aid: str) -> str:
    names = {'00':'China Unbounded','01':'First Class China','02':'China Luxury Hotels',
        '03':'China For Couples','04':'China After Dark','05':'China Family Escape',
        '06':'China Slow Travel','07':'China With Kids','08':'China Multi-Gen Travel',
        '09':'China Family Adventure','10':'China City Routes','11':'China Scenic Routes',
        '12':'China Hidden Cities','13':'China Premium Routes','14':'China Budget Routes',
        '15':'China Urban Discovery','16':'China Travel Checklist','17':'China First-Timer Tips',
        '18':'China Trip Secrets','19':'China Trip Planner','20':'China vs The World','21':'China vs The World 2'}
    return names.get(aid, aid)


def _extract_key_insight(aid: str, insights_data: dict) -> dict:
    """从AI洞察中提取关键发现（容错版）"""
    info = insights_data.get(aid, {})
    if info.get('status') != 'COMPLETED':
        return {}
    if not info.get('insights'):
        # COMPLETED但无内容（内容太少，Metricool无法生成洞察）
        return {"note": "内容不足，Metricool未生成洞察"}

    content = info['insights']
    result = {}

    # 1. executive summary — 全量摘要（不只负面）
    exec_sum = content.get('executiveSummary', {}).get('summary', '')
    if exec_sum:
        result['executive_summary'] = exec_sum[:300]

    # 2. 按网络分类提取洞察
    all_insights = []
    for net, items in content.get('organicNetworks', {}).items():
        for item in items:
            title = item.get('title', '')
            text = item.get('text', '')
            if text:
                all_insights.append({'net': net, 'title': title, 'text': text[:200]})

    # 3. 优先提取 pattern/detect/recommend 类洞察（中英文关键词）
    pattern_kw = ('pattern', 'detect', 'recommend', 'strategy',
                  'performance', 'finding', 'analysis',
                  '模式', '发现', '趋势', '推荐', '策略', '分析', '表现')
    for item in all_insights:
        t = item['title'].lower()
        if any(kw in t for kw in pattern_kw):
            result['pattern'] = item['text'][:250]
            break

    # 4. 如果没找到特定类型，取第一条非trivial洞察
    if 'pattern' not in result and all_insights:
        result['key_insight'] = all_insights[0]['text'][:250]

    # 5. 最佳帖子
    for bp in (content.get('bestPosts') or [])[:1]:
        result['best_practice'] = bp.get('text', '')[:200]

    # 6. 机会/建议类（中英文关键词）
    opp_kw = ('opportunity', 'improve', 'growth', 'action',
              '机会', '改进', '增长', '行动', '优化', '建议')
    for item in all_insights:
        t = item['title'].lower()
        if any(kw in t for kw in opp_kw):
            result['opportunity'] = item['text'][:200]
            break

    # 7. 负面信号（中英文关键词）
    neg_kw = ('fail', 'low', 'negligible', 'zero', 'weak', 'poor',
              '失败', '低', '零', '弱', '差', '忽略不计', '无')
    if exec_sum and any(kw in exec_sum.lower() for kw in neg_kw):
        result['issue'] = exec_sum[:200]

    return result


def _build_style_suggestions(accounts: dict, insights_data: dict) -> dict:
    """
    M1风格卡优化建议 — 核心产出

    按5种风格分组，基于winner账号的pattern，
    给出M1.5 prompt调整建议。
    """
    style_groups = {
        'Velvet': ['00','01','02','03','04'],
        'Soft Signal': ['05','06','07','08','09'],
        'Shadow Cut': ['10','11','12','13','14'],
        'Swiss Pulse': ['15','16','17','18','19'],
        'Comparison': ['20','21'],
    }

    suggestions = {}

    for style, aids in style_groups.items():
        group_accounts = {}
        winners = []
        alerts = 0

        for a in aids:
            acc = accounts.get(a, {})
            group_accounts[a] = {
                "name": acc.get('name', ''),
                "role": acc.get('role', ''),
                "avg": acc.get('kpi', {}).get('avg_per_post', 0),
                "growth": acc.get('kpi', {}).get('growth_pct', 0),
            }
            if acc.get('role') == 'winner':
                winners.append(a)
            if acc.get('alerts'):
                alerts += len(acc['alerts'])

        # 计算风格组平均值
        avgs = [acc.get('kpi', {}).get('avg_per_post', 0) for acc in
                [accounts.get(a, {}) for a in aids]]
        style_avg = sum(avgs) / max(len(avgs), 1)

        # 从winner账号提取pattern
        winning_hooks = []
        winning_cta = []
        winning_themes = []

        for w in winners:
            info = insights_data.get(w, {})
            content = (info.get('insights') or {}) if info.get('status') == 'COMPLETED' else {}
            for net, items in content.get('organicNetworks', {}).items():
                for item in items:
                    text = (item.get('text', '') or '').lower()
                    t = item.get('title', '').lower()

                    # 中英文关键词匹配
                    title_kw = ('recommend', 'pattern', 'detect', '推荐', '模式', '发现', '趋势', '分析')
                    if any(kw in t for kw in title_kw):
                        for kw in ['discovery', 'narrative', 'storytelling', 'personal',
                                  'surprise', 'hidden', 'secret',
                                  '发现', '叙事', '故事', '个性化', '惊喜', '隐藏', '秘密']:
                            if kw in text and kw not in winning_hooks:
                                winning_hooks.append(kw)
                        for kw in ['comment', 'save', 'dm', 'map', 'itinerary', 'bookmark',
                                  '互动', '保存', '私信', '地图', '行程', '收藏']:
                            if kw in text and kw not in winning_cta:
                                winning_cta.append(kw)
                        for kw in ['family', 'couple', 'luxury', 'food', 'culture',
                                  'adventure', 'nature', 'city', 'hidden', 'local',
                                  '家庭', '情侣', '奢华', '美食', '文化',
                                  '冒险', '自然', '城市', '隐藏', '本地']:
                            if kw in text and kw not in winning_themes:
                                winning_themes.append(kw)

        # 生成M1.5优化建议
        optimization = []

        if style_avg < 100 and alerts > 0:
            optimization.append({
                "priority": "high",
                "target": "hook_direction",
                "suggestion": f"风格组帖均{style_avg:.0f}偏低。如果winner账号有明确pattern，在M1.5 prompt中强化该方向；如果没有winner，放开M1.5自由度尝试新方向。",
            })

        if winning_hooks:
            optimization.append({
                "priority": "medium",
                "target": "hook_style",
                "suggestion": f"强化hook风格: {', '.join(winning_hooks[:3])}。在M1.5 prompt中提及这些方向但不要求每条都必须用。",
            })

        if winning_cta and len(winners) >= 2:
            optimization.append({
                "priority": "low",
                "target": "cta_pattern",
                "suggestion": f"CTA倾向: {', '.join(winning_cta[:3])}。可在M1.5 prompt中保持当前CTA自由度，仅作为倾向参考。",
            })

        suggestions[style] = {
            "avg_views": round(style_avg),
            "winner_count": len(winners),
            "alert_count": alerts,
            "winning_hooks": winning_hooks[:5],
            "winning_cta": winning_cta[:5],
            "winning_themes": winning_themes[:5],
            "m15_optimization": optimization,
        }

    return suggestions


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "clipmatrix", "scripts"))

    from m1_report import fetch_analytics, fetch_baseline

    print("Loading...")
    today = fetch_analytics()
    baseline = fetch_baseline()
    insights_data = {}

    report = build_agent_report(today, baseline, insights_data)

    now = datetime.now()
    path = os.path.expanduser(f"~/Desktop/工作日志/Pandajourneys_agent_report_{now.strftime('%m%d')}.json")
    with open(path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"✅ {path}")
    print(f"KPI: {report['kpi']['total_views']:,}播放 {report['kpi']['total_posts']}帖")
    print(f"角色: {json.dumps(report['role_summary'], indent=2)}")
    print(f"风格建议: {len(report['style_suggestions'])}组")
    for s, info in report['style_suggestions'].items():
        print(f"  {s}: avg={info['avg_views']} winner={info['winner_count']} alerts={info['alert_count']}")
        for o in info['m15_optimization']:
            print(f"    [{o['priority']}] {o['target']}: {o['suggestion'][:80]}")
