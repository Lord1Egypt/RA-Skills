#!/usr/bin/env python3
"""
为每个英雄计算百分位标记并更新 heroes_db.json
百分位分级：
  ⚠️  后10%（最差）
  ⚡  10-20%（较差）
  ✅  20-80%（正常）
  📈  前10%（最强/上升最多）
自动写入 heroes_db.json 的 warn_* 字段
"""
import json, statistics

SCRIPT_DIR = '/root/.openclaw/workspace/magi/skills/dota2-coach/scripts'
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'

def percentile_flag(value, all_values, invert=False):
    """返回百分位标记字符串
    invert=False: 值越大越好（用于变化率）→ rank = count > value（从顶计算位置）
    invert=True: 值越小越好（用于胜率/出场率）→ rank = count <= value（从底计算位置）
    """
    n = len(all_values)
    if invert:
        rank = sum(1 for v in all_values if v <= value)   # 位置从底部算
    else:
        rank = sum(1 for v in all_values if v > value)    # 位置从顶部算
    pct = rank / n
    if invert:
        # 小值=好，pct 越低越差，pct 越高越好
        if pct <= 0.1:
            return 'warn_bottom10'   # pct 极低 → 极差值（后10%）
        elif pct <= 0.2:
            return 'warn_bottom20'   # pct 低 → 较差值（后20%）
        elif pct >= 0.9:
            return 'warn_top10'      # pct 高 → 极好值（前10%）
        elif pct >= 0.8:
            return 'warn_top20'      # pct 较高 → 较好值（前20%）
    else:
        # 大值=好，pct 越低越好，pct 越高越差
        if pct <= 0.1:
            return 'warn_top10'      # pct 极低 → 极好值（前10%）
        elif pct <= 0.2:
            return 'warn_top20'      # pct 低 → 较好值（前20%）
        elif pct >= 0.9:
            return 'warn_bottom10'   # pct 高 → 极差值（后10%）
        elif pct >= 0.8:
            return 'warn_bottom20'   # pct 较高 → 较差值（后20%）
    return 'normal'

def warn_icon(warn_type):
    """将 warn_type 映射为显示符号"""
    return {
        'warn_bottom10': '⚠️',
        'warn_bottom20': '⚡',
        'warn_top20': '✅',
        'warn_top10': '✅',
        'normal': '',
        'unknown': '',
    }.get(warn_type, '')

def update_hero_warnings():
    with open(HEROES_FILE) as f:
        heroes = json.load(f)

    # 计算每周全英雄总出场
    weekly_totals = [0]*6
    for h in heroes:
        t = h.get('pub_pick_trend', [])
        for i in range(min(6, len(t))):
            weekly_totals[i] += t[i]

    # 计算四个指标
    records = []
    for h in heroes:
        t = h.get('pub_pick_trend', [])
        w = h.get('pub_win_trend', [])
        if not t or not w or len(t) < 6:
            h['warn_wr'] = 'unknown'
            h['warn_wr_change'] = 'unknown'
            h['warn_share'] = 'unknown'
            h['warn_share_change'] = 'unknown'
            continue

        total_pick = sum(t[:6])
        total_win = sum(w[:6])
        wr = total_win / total_pick * 100 if total_pick > 0 else 0

        # 胜率变化：最近3周 vs 之前3周（用市场胜率而非原始胜率）
        wr_old = sum(w[:3])/3 / (sum(t[:3])/3) * 100 if sum(t[:3]) > 0 else 0
        wr_new = sum(w[3:6])/3 / (sum(t[3:6])/3) * 100 if sum(t[3:6]) > 0 else 0
        wr_change = wr_new - wr_old

        # 出场率
        share = sum(t[:6]) / sum(weekly_totals) * 100

        # 出场率变化
        share_old = (sum(t[:3])/3) / (sum(weekly_totals[:3])/3) if sum(weekly_totals[:3]) > 0 else 0
        share_new = (sum(t[3:6])/3) / (sum(weekly_totals[3:6])/3) if sum(weekly_totals[3:6]) > 0 else 0
        share_change = (share_new - share_old) * 100

        h['wr'] = round(wr, 1)
        h['wr_change'] = round(wr_change, 1)
        h['share'] = round(share, 2)
        h['share_change'] = round(share_change, 2)

        records.append({
            'key': h.get('key', ''),
            'wr': wr,
            'wr_change': wr_change,
            'share': share,
            'share_change': share_change,
        })

    # 计算百分位
    wr_vals = [r['wr'] for r in records]
    wr_chg_vals = [r['wr_change'] for r in records]
    sh_vals = [r['share'] for r in records]
    sh_chg_vals = [r['share_change'] for r in records]

    for h in heroes:
        k = h.get('key', '')
        rec = next((r for r in records if r['key'] == k), None)
        if not rec:
            continue
        h['warn_wr'] = percentile_flag(rec['wr'], wr_vals, invert=True)
        h['warn_wr_change'] = percentile_flag(rec['wr_change'], wr_chg_vals, invert=False)
        h['warn_share'] = percentile_flag(rec['share'], sh_vals, invert=True)
        h['warn_share_change'] = percentile_flag(rec['share_change'], sh_chg_vals, invert=False)

    with open(HEROES_FILE, 'w') as f:
        json.dump(heroes, f, ensure_ascii=False, indent=2)

    # 统计
    for field in ['warn_wr', 'warn_wr_change', 'warn_share', 'warn_share_change']:
        cnt = sum(1 for h in heroes if h.get(field) == 'warn_bottom10')
        print(f'{field}: {cnt} 个在后10%')

if __name__ == '__main__':
    update_hero_warnings()
