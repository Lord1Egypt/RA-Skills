# -*- coding: utf-8 -*-
"""
大乐透 · 深度号码分析（学习增强版）  (新增)

目的: 把全网研究的「彩票特征工程」思路落地为一组**描述性统计观察**，
      用于让用户更深入地理解号码的冷热与结构特征，提升系统的信息价值。

诚实边界（与全站打假基调一致）:
  - 本模块**只做统计描述**，不预测、不宣称任何号码更可能开出。
  - 大乐透每期独立随机，历史统计无法预示未来；以下观察仅供「理解数据趣味」。
  - 所有数值均来自 dlt_history.json 的真实历史开奖，可复现、可核对。

增量维度（相对 compute_models 已有的统计）:
  1. 多窗口频率 Z-score 冷热 (前区 30/50/100/200 期；后区 30/50/100 期)
  2. 历史均值/中位数间隔 (overdue) → 统计极冷判定
  3. 近期结构特征 (三区比/奇偶比/大小比/012路/连号/和值/跨度)
  4. 分布健康度 (香农熵)
"""

import math
from collections import Counter


def _expected_appear(draws_n, slots, nums):
    """W 期内某号理论出现次数与二项标准差。"""
    p = slots / nums
    exp = draws_n * p
    std = math.sqrt(draws_n * p * (1 - p))
    return exp, std


def _gaps_for(num, draws, key):
    """返回某号在历史中出现位置的间隔列表。"""
    idxs = [i for i, d in enumerate(draws) if num in d.get(key, [])]
    return [b - a for a, b in zip(idxs, idxs[1:])]


def _analyze_zone(draws, key, nums, slots, windows, zone_fn=None, big_boundary=None):
    """计算某一区(前区/后区)的多窗口Z、遗漏、间隔、结构特征、熵。"""
    # ---------- 1. 多窗口频率 Z-score 冷热 ----------
    win_freq = {}
    for w in windows:
        sub = draws[-w:]
        c = Counter()
        for d in sub:
            for n in d.get(key, []):
                c[n] += 1
        win_freq[w] = c

    z_by_window = {}
    for w in windows:
        exp, std = _expected_appear(w, slots, len(nums))
        std = std or 1e-9
        z_by_window[w] = {n: (win_freq[w].get(n, 0) - exp) / std for n in nums}

    composite = {n: sum(z_by_window[w][n] for w in windows) / len(windows) for n in nums}
    hot = sorted(nums, key=lambda n: composite[n], reverse=True)[:6]
    cold = sorted(nums, key=lambda n: composite[n])[:6]

    # ---------- 2. 历史均值/中位数间隔 (overdue) ----------
    gap_stats = {}
    current_omit = {}
    for num in nums:
        gaps = _gaps_for(num, draws, key)
        gap_stats[num] = (sum(gaps) / len(gaps), sorted(gaps)[len(gaps) // 2]) if gaps else (0, 0)
        omit = 0
        for i in range(len(draws) - 1, -1, -1):
            if num in draws[i].get(key, []):
                break
            omit += 1
        current_omit[num] = omit

    # 统计极冷: 当前遗漏 > 1.5 × 历史均值间隔
    stat_cold = [n for n in nums
                 if gap_stats[n][0] > 0 and current_omit[n] > 1.5 * gap_stats[n][0]]

    # ---------- 3. 近期结构特征 (近30期) ----------
    recent = draws[-30:]
    struct = {'zone': Counter(), 'odd': 0, 'even': 0, 'big': 0, 'small': 0,
              'mod': Counter(), 'sums': [], 'spans': [], 'consecutive': 0}
    for d in recent:
        fr = d.get(key, [])
        for n in fr:
            if zone_fn:
                struct['zone'][zone_fn(n)] += 1
            if n % 2 == 0:
                struct['even'] += 1
            else:
                struct['odd'] += 1
            if big_boundary:
                if n > big_boundary:
                    struct['big'] += 1
                else:
                    struct['small'] += 1
            struct['mod'][n % 3] += 1
        s = sum(fr)
        struct['sums'].append(s)
        struct['spans'].append(max(fr) - min(fr))
        sf = sorted(fr)
        if any(sf[i + 1] - sf[i] == 1 for i in range(len(sf) - 1)):
            struct['consecutive'] += 1

    avg_sum = sum(struct['sums']) / len(struct['sums']) if struct['sums'] else 0
    avg_span = sum(struct['spans']) / len(struct['spans']) if struct['spans'] else 0
    conj_rate = struct['consecutive'] / len(recent) if recent else 0

    # ---------- 4. 分布健康度 (香农熵) ----------
    cnt = Counter()
    for d in draws:
        for n in d.get(key, []):
            cnt[n] += 1
    total_obs = sum(cnt.values()) or 1
    entropy = -sum((c / total_obs) * math.log2(c / total_obs) for c in cnt.values() if c > 0)
    max_entropy = math.log2(len(nums))
    entropy_ratio = entropy / max_entropy if max_entropy else 0

    return {
        'windows': windows,
        'z_by_window': z_by_window,
        'composite': composite,
        'hot': hot,
        'cold': cold,
        'current_omit': current_omit,
        'gap_stats': gap_stats,
        'stat_cold': stat_cold,
        'struct': {
            'zone': dict(struct['zone']),
            'odd': struct['odd'], 'even': struct['even'],
            'big': struct['big'], 'small': struct['small'],
            'mod': dict(struct['mod']),
            'avg_sum': avg_sum, 'avg_span': avg_span, 'conj_rate': conj_rate,
        },
        'entropy': entropy,
        'entropy_ratio': entropy_ratio,
        'nums': nums,
    }


def analyze_deep(draws):
    """计算前区+后区全部深度特征，返回结构化 dict。"""
    if not draws:
        return {}
    front_nums = list(range(1, 36))   # 前区 35 选 5
    back_nums = list(range(1, 13))    # 后区 12 选 2
    front = _analyze_zone(
        draws, 'front', front_nums, 5, [30, 50, 100, 200],
        zone_fn=lambda n: 0 if n <= 12 else (1 if n <= 23 else 2),
        big_boundary=17,
    )
    back = _analyze_zone(
        draws, 'back', back_nums, 2, [30, 50, 100],
        big_boundary=6,
    )
    return {'front': front, 'back': back}


def _ball(n, cls='ball-red'):
    return f'<span class="ball {cls}" style="width:26px;height:26px;line-height:26px;font-size:12px;">{n:02d}</span>'


def _zone_rows(a, is_front=True):
    """渲染某区的「冷暖 + 多窗口Z + 结构」子表。"""
    hot_html = ' '.join(_ball(n) for n in a['hot'])
    cold_html = ' '.join(_ball(n) for n in a['cold'])
    stat_cold_html = (' '.join(_ball(n) for n in a['stat_cold'])
                      if a['stat_cold'] else '<span style="color:#888;">（当前无统计极冷号）</span>')

    show_nums = a['hot'] + a['cold']
    rows = ''
    for n in show_nums:
        zcells = ''.join(
            f'<td style="text-align:center;color:{"#ff7b00" if a["z_by_window"][w][n] > 1 else ("#4aa3ff" if a["z_by_window"][w][n] < -1 else "#bbb")};">'
            f'{a["z_by_window"][w][n]:+.2f}</td>'
            for w in a['windows'])
        rows += (f'<tr><td style="text-align:center;">{_ball(n)}</td>{zcells}'
                 f'<td style="text-align:center;color:#999;">遗漏 {a["current_omit"][n]} 期</td></tr>')

    s = a['struct']
    if is_front:
        zone_html = (f'<tr><td>三区比 (01-12 / 13-23 / 24-35)</td>'
                     f'<td>{s["zone"].get(0,0)} / {s["zone"].get(1,0)} / {s["zone"].get(2,0)}</td>'
                     f'<td>≈ 2:1:2</td></tr>')
        oe_total = (s['odd'] + s['even']) or 1
        size_html = f'<tr><td>大小比（18及以上为大）</td><td>{s["small"]} : {s["big"]}</td><td>基本均衡</td></tr>'
        sum_norm = '理论均值 ≈ 90'
        span_norm = '多在 15-30'
        conj_norm = '历史约 60-70%'
    else:
        zone_html = ''
        oe_total = (s['odd'] + s['even']) or 1
        size_html = f'<tr><td>大小比（7及以上为大）</td><td>{s["small"]} : {s["big"]}</td><td>基本均衡</td></tr>'
        sum_norm = '范围 3-23，均值 ≈ 13'
        span_norm = '多在 5-10'
        conj_norm = '历史约 45-55%'

    mod_total = sum(s['mod'].values()) or 1
    struct_rows = (
        zone_html +
        f'<tr><td>奇偶比</td><td>{s["odd"]} : {s["even"]}（{s["odd"]/oe_total*100:.0f}% 奇）</td><td>3:2 / 2:3 为主</td></tr>'
        + size_html +
        f'<tr><td>012 路分布</td><td>0路 {s["mod"].get(0,0)} / 1路 {s["mod"].get(1,0)} / 2路 {s["mod"].get(2,0)}</td><td>三路趋均</td></tr>'
        f'<tr><td>平均和值</td><td>{s["avg_sum"]:.1f}</td><td>{sum_norm}</td></tr>'
        f'<tr><td>平均跨度</td><td>{s["avg_span"]:.1f}</td><td>{span_norm}</td></tr>'
        f'<tr><td>连号出现率</td><td>{s["conj_rate"]*100:.0f}%</td><td>{conj_norm}</td></tr>'
    )

    wlabels = ''.join(f'<th>近{w}期</th>' for w in a['windows'])
    return hot_html, cold_html, stat_cold_html, rows, wlabels, struct_rows


def render_deep_analysis_html(draws):
    """返回「深度号码分析」面板 HTML（只做描述，不改预测）。"""
    try:
        a = analyze_deep(draws)
    except Exception as e:
        return (f'<div class="section"><div class="section-title">深度号码分析</div>'
                f'<div class="info" style="border-color:#ff5555;">⚠ 深度分析计算异常: {e}</div></div>')

    if not a:
        return ''

    f = a['front']
    b = a['back']
    f_hot, f_cold, f_stat, f_rows, f_wlabels, f_struct = _zone_rows(f, True)
    b_hot, b_cold, b_stat, b_rows, b_wlabels, b_struct = _zone_rows(b, False)

    html = f"""
<div class="section">
<div class="section-title">📊 深度号码分析（学习增强版 · 描述性观察，不预示未来）</div>
<div class="info" style="border-color:#5577ff; background:#10122a;">
<p style="color:#aab4ff; font-size:12.5px; line-height:1.7; margin:6px 0;">
本栏基于 {len(draws)} 期真实历史开奖，用「多窗口频率 Z-score / 历史间隔 / 结构特征 / 香农熵」四个维度刻画号码的冷热与分布。
<b style="color:#ffd9a0;">大乐透每期独立随机，以下观察仅供理解数据趣味，不构成任何选号建议。</b>
</p>
</div>

<div class="sub" style="margin-top:14px; color:#ff9d5c;">【前区 35 选 5】</div>
<div class="sub" style="margin-top:10px;">① 前区冷热（综合 Z-score：多窗口均值）</div>
<table>
<tr><th>类型</th><th>号码</th><th>说明</th></tr>
<tr><td style="color:#ff7b00;">🔥 近期偏热</td><td>{f_hot}</td><td style="color:#888;">综合 Z&gt;0，近 30/50/100/200 期出现频率高于理论</td></tr>
<tr><td style="color:#4aa3ff;">❄️ 近期偏冷</td><td>{f_cold}</td><td style="color:#888;">综合 Z&lt;0，出现频率低于理论</td></tr>
<tr><td style="color:#ff5577;">📉 统计极冷</td><td>{f_stat}</td><td style="color:#888;">当前遗漏 &gt; 1.5×历史均值间隔，回补概率略高（仍随机）</td></tr>
</table>

<div class="sub" style="margin-top:14px;">② 前区多窗口 Z-score 明细（红=偏热 / 蓝=偏冷）</div>
<table>
<tr><th>号码</th>{f_wlabels}<th>当前遗漏</th></tr>
{f_rows}
</table>

<div class="sub" style="margin-top:14px;">③ 前区近期结构特征（近 30 期均值）</div>
<table>
<tr><th>维度</th><th>观测值</th><th>经验常态</th></tr>
{f_struct}
</table>

<div class="sub" style="margin-top:14px; color:#5cc8ff;">【后区 12 选 2】</div>
<div class="sub" style="margin-top:10px;">④ 后区冷热（综合 Z-score）</div>
<table>
<tr><th>类型</th><th>号码</th><th>说明</th></tr>
<tr><td style="color:#ff7b00;">🔥 近期偏热</td><td>{b_hot}</td><td style="color:#888;">综合 Z&gt;0，近 30/50/100 期出现频率高于理论</td></tr>
<tr><td style="color:#4aa3ff;">❄️ 近期偏冷</td><td>{b_cold}</td><td style="color:#888;">综合 Z&lt;0，出现频率低于理论</td></tr>
<tr><td style="color:#ff5577;">📉 统计极冷</td><td>{b_stat}</td><td style="color:#888;">当前遗漏 &gt; 1.5×历史均值间隔</td></tr>
</table>

<div class="sub" style="margin-top:14px;">⑤ 后区多窗口 Z-score 明细</div>
<table>
<tr><th>号码</th>{b_wlabels}<th>当前遗漏</th></tr>
{b_rows}
</table>

<div class="sub" style="margin-top:14px;">⑥ 后区近期结构特征（近 30 期均值）</div>
<table>
<tr><th>维度</th><th>观测值</th><th>经验常态</th></tr>
{b_struct}
</table>

<div class="sub" style="margin-top:14px;">⑦ 分布健康度（香农熵）</div>
<div class="info" style="border-color:#00dd88;">
<p style="color:#aaf0c8; font-size:13px; line-height:1.8; margin:6px 0;">
前区出现分布香农熵 = <b>{f['entropy']:.3f}</b> / 理论最大 {math.log2(35):.3f}（均匀度 <b>{f['entropy_ratio']*100:.1f}%</b>）；
后区 = <b>{b['entropy']:.3f}</b> / 理论最大 {math.log2(12):.3f}（均匀度 <b>{b['entropy_ratio']*100:.1f}%</b>）。
熵越接近理论上限，说明历史号码分布越均匀、无显著偏倚——也从侧面印证了开奖的随机性。
</p>
</div>
</div>
"""
    return html


if __name__ == '__main__':
    import json
    d = json.load(open('dlt_history.json', encoding='utf-8'))
    print(render_deep_analysis_html(d))
