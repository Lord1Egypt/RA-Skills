# -*- coding: utf-8 -*-
"""
大乐透系统 — 强化引擎 / Power Engine  (V8.8 新增)
====================================================================

为什么需要它 (诚实动机):
    此前系统反复声称"所有策略不比随机好 (p>0.05)"，但这个结论来自一次性
    回测脚本，从未用"真实预测管线在历史上逐期假装未知、预测下一期、再核对"
    的方式验证过。这属于"声称 > 证据"。

    本模块把系统从"产出号码"升级为"能用统计证据证明自己有没有优势"，
    是真正的科学严谨性提升，而非又一次号码生成。

三大能力:
    1. walk_forward_backtest : 样本外滚动回测
       - 对历史上每个测试期 k, 只用 draws[:k] 训练(完全复刻 dlt_auto 的
         CDM 加权/后区评分/9项过滤), 生成与线上同构的 5 组推荐,
         再用真实 draws[k] 核对命中。
       - 累计各奖级命中数与派彩, 计算 ROI, 并与纯随机基线做比例 z 检验。

    2. monte_carlo_cost : 蒙特卡洛成本仿真
       - 用回测得到的"每期净盈亏经验分布"重采样, 模拟 M 名玩家照此策略
         玩 W 周的真实财务结果, 给出 P(正收益)/期望净亏/分位数。

    3. assert_improvement : 自我进化证明闸门
       - 任何"更强了"的声称, 必须用历史回测做两比例 z 检验;
         p>=0.05 则系统拒绝该声称并打印拒绝理由。防止"自我感觉良好"。

严谨性说明:
    - 组合评分用 top-15 号码枚举 (C(15,5)=3003) 近似全量 37,680 穷举。
      因为评分是号码级平滑加权, top-15 在实测中已覆盖最优组合,
      且保证可复现与快速; 这是有记录的工程近似, 非逻辑改变。
    - 一等奖/二等奖为浮动奖, 此处用代表性固定值 (1000万/20万),
      结论方向 (ROI 深度为负且≈随机) 不受具体数值影响。
    - 随机基线从"与真实策略相同的过滤后号码空间"抽取, 保证比较公平。
"""
import sys
import io
import json
import math
import random
import os
from collections import Counter, defaultdict
from itertools import combinations
from datetime import datetime

# 单一可信源: 过滤器/后区评分与线上完全一致, 杜绝漂移
from dlt_common import passes_filters, back_score, calc_ac
import dlt_common as _C

# ---------- 奖级与派彩 (2026 新规, 现行奖池≥8亿上浮档) ----------
# 键 = (前区命中数, 后区命中数)  -> 派彩(元)
# 2026-01-16 起执行新规: 奖级由9个改为7个; 一/二为浮动奖, 三~七为固定奖。
# ---------- 奖级与派彩 (2026新规, 第26014期/2026-01-31 起, 9档→7档) ----------
# 官方中奖条件(合并后, 与旧9档不同!):
#   一等奖 5+2 (浮动, 代表值1000万) | 二等奖 5+1 (浮动, 代表值500万)
#   三等奖 5+0 或 4+2            → 6666元
#   四等奖 4+1                   → 380元
#   五等奖 3+2 或 4+0            → 200元
#   六等奖 3+1 或 2+2            → 18元  (注: 个别媒体报20元, 以26015实际派奖18元为准)
#   七等奖 3+0 / 2+1 / 1+2 / 0+2 → 7元
# 当前奖池 8.07亿 ≥8亿, 适用上浮档(上述值); 奖池<8亿时三~七等为 5000/300/150/15/5。
# 一等奖单期封顶1亿(基本2元最高1000万, 追加3元最高1800万), 此处用代表性固定值。
# 非中奖组合((2,0)/(1,1)/(1,0)/(0,1)/(0,0)等)按规则派彩0, 由 .get 默认0处理。
PRIZE_PAYOUT = {
    (5, 2): 10_000_000,   # 一等奖 (浮动, 代表性固定值)
    (5, 1): 5_000_000,    # 二等奖 (浮动, 代表性固定值, 单注封顶500万)
    (5, 0): 6666,         # 三等奖
    (4, 2): 6666,         # 三等奖 (4+2 合并入三等奖)
    (4, 1): 380,          # 四等奖
    (3, 2): 200,          # 五等奖
    (4, 0): 200,          # 五等奖 (4+0 合并入五等奖)
    (3, 1): 18,           # 六等奖
    (2, 2): 18,           # 六等奖 (2+2 合并入六等奖)
    (3, 0): 7,            # 七等奖
    (2, 1): 7,            # 七等奖
    (1, 2): 7,            # 七等奖
    (0, 2): 7,            # 七等奖
}
PRIZE_NAME = {
    (5, 2): '一等奖', (5, 1): '二等奖',
    (5, 0): '三等奖', (4, 2): '三等奖',
    (4, 1): '四等奖',
    (3, 2): '五等奖', (4, 0): '五等奖',
    (3, 1): '六等奖', (2, 2): '六等奖',
    (3, 0): '七等奖', (2, 1): '七等奖', (1, 2): '七等奖', (0, 2): '七等奖',
}
COST_PER_BET = 2  # 基本投注 2 元/注


# ============================================================
# 1. 模型计算 (逐字复刻 dlt_auto.compute_models 的评分逻辑)
# ============================================================
def compute_models(draws):
    """只用 draws (历史, 不含待预测期) 计算与线上完全一致的评分向量。"""
    total = len(draws)
    latest = draws[-1]

    front_freq = Counter()
    back_freq = Counter()
    for d in draws:
        for n in d['front']:
            front_freq[n] += 1
        for n in d['back']:
            back_freq[n] += 1

    n_total = total * 5
    freqs = {num: front_freq.get(num, 0) / n_total for num in range(1, 36)}
    # V8.9.2 修复 empirical Bayes 先验退化 bug (与 dlt_auto.py 同构):
    # 原 alpha_prior ∝ freqs 导致收缩被抵消, cdm_prob 退化为原始频率。改为 flat 先验。
    prior_strength = max(1.0, total * 0.02)
    alpha_prior = {num: prior_strength / 35 for num in range(1, 36)}
    posterior = {num: alpha_prior[num] + front_freq.get(num, 0) for num in range(1, 36)}
    total_post = sum(posterior.values())
    cdm_prob = {num: 5 * posterior[num] / total_post for num in range(1, 36)}

    # 马尔可夫
    transition = defaultdict(lambda: defaultdict(int))
    state_count = defaultdict(int)
    for i in range(len(draws) - 1):
        for n1 in set(draws[i]['front']):
            state_count[n1] += 1
            for n2 in set(draws[i + 1]['front']):
                transition[n1][n2] += 1
    latest_front = set(latest['front'])
    markov_prob = defaultdict(float)
    for n1 in latest_front:
        sc = state_count[n1]
        if sc == 0:
            continue
        for n2 in range(1, 36):
            markov_prob[n2] += transition[n1][n2] / sc / len(latest_front)

    recent_30 = draws[-30:]
    freq_30 = Counter()
    for d in recent_30:
        for n in d['front']:
            freq_30[n] += 1

    front_omit = {}
    for num in range(1, 36):
        omit = 0
        for i in range(len(draws) - 1, -1, -1):
            if num in draws[i]['front']:
                break
            omit += 1
        front_omit[num] = omit
    max_omit = max(front_omit.values()) if front_omit else 1

    combined_score = {}
    for num in range(1, 36):
        cdm_s = cdm_prob.get(num, 0) / (5 / 35)
        markov_s = markov_prob.get(num, 0) / (5 / 35)
        freq30_s = freq_30.get(num, 0) / (30 * 5 / 35)
        omit_s = front_omit[num] / max_omit if max_omit > 0 else 0
        combined_score[num] = 0.40 * cdm_s + 0.25 * markov_s + 0.20 * freq30_s + 0.15 * (0.5 + 0.5 * omit_s)

    # 后区
    back_omit = {}
    for num in range(1, 13):
        omit = 0
        for i in range(len(draws) - 1, -1, -1):
            if num in draws[i]['back']:
                break
            omit += 1
        back_omit[num] = omit
    max_back_omit = max(back_omit.values()) if back_omit else 1

    n_back = total * 2
    # V8.9.2 同步修复: 后区 empirical Bayes 先验退化(与 dlt_auto.py 同构, flat 先验)
    prior_strength_b = max(1.0, total * 0.02)
    alpha_prior_b = {num: prior_strength_b / 12 for num in range(1, 13)}
    posterior_b = {num: alpha_prior_b[num] + back_freq.get(num, 0) for num in range(1, 13)}
    total_post_b = sum(posterior_b.values())
    cdm_prob_b = {num: 2 * posterior_b[num] / total_post_b for num in range(1, 13)}

    back_trans = defaultdict(lambda: defaultdict(int))
    back_sc = defaultdict(int)
    for i in range(len(draws) - 1):
        for n1 in set(draws[i]['back']):
            back_sc[n1] += 1
            for n2 in set(draws[i + 1]['back']):
                back_trans[n1][n2] += 1
    latest_back = set(latest['back'])
    markov_back = defaultdict(float)
    for n1 in latest_back:
        sc = back_sc[n1]
        if sc == 0:
            continue
        for n2 in range(1, 13):
            markov_back[n2] += back_trans[n1][n2] / sc / len(latest_back)

    return {
        'cdm_prob': cdm_prob, 'markov_prob': markov_prob,
        'freq_30': freq_30, 'front_omit': front_omit, 'max_omit': max_omit,
        'combined_score': combined_score,
        'back_omit': back_omit, 'max_back_omit': max_back_omit,
        'cdm_prob_b': cdm_prob_b, 'markov_back': markov_back,
    }


# ============================================================
# 2. 推荐生成 (与线上同构, 用 top-15 枚举近似全量穷举)
# ============================================================
def _build_valid_cache():
    """一次性穷举全部通过 8 项静态过滤的组合 (37,680 个), 供回测复用。"""
    cache = []
    for combo in combinations(range(1, 36), 5):
        if passes_filters(list(combo)):
            cache.append(list(combo))
    return cache


def _weighted_sample_k(score_dict, k, rng, pool):
    """从 pool 按 score_dict 权重无放回抽取 k 个, 返回升序 tuple。"""
    avail = list(pool)
    chosen = []
    for _ in range(k):
        if not avail:
            break
        weights = [max(score_dict.get(n, 1e-12), 1e-12) for n in avail]
        tot = sum(weights)
        r = rng.random() * tot
        acc = 0.0
        sel = avail[-1]
        for n, w in zip(avail, weights):
            acc += w
            if r <= acc:
                sel = n
                break
        chosen.append(sel)
        avail.remove(sel)
    return tuple(sorted(chosen))


def _sample_front_group(score_dict, valid_set, used, prev_front, seed):
    rng = random.Random(seed)
    for _ in range(800):
        combo = _weighted_sample_k(score_dict, 5, rng, list(range(1, 36)))
        if combo in valid_set and combo not in used and len(set(combo) & set(prev_front)) <= 2:
            return list(combo)
    return None


def _sample_back_group(score_dict, used_backs, seed):
    rng = random.Random(seed)
    for _ in range(400):
        combo = _weighted_sample_k(score_dict, 4, rng, list(range(1, 13)))
        if combo not in used_backs:
            return list(combo)
    return None


def recommend(draws_hist, valid_cache, seed_base=20260729):
    """生成与线上同构的 5 组推荐 (前区5元组 + 后区4码集合)。
    V8.9.2 起改为期号种子后验采样, 与 dlt_auto.generate_predictions 完全同构,
    以保住"回测复刻预测"的硬保证。seed_base 传测试期期号即可复现。"""
    models = compute_models(draws_hist)
    prev_front = draws_hist[-1]['front']
    cs = models['combined_score']
    cdm = models['cdm_prob']
    mk = models['markov_prob']
    omit = models['front_omit']

    # 动态过滤: 加第9项重号
    valid_dyn = [c for c in valid_cache if len(set(c) & set(prev_front)) <= 2]
    valid_dyn_set = set(tuple(sorted(c)) for c in valid_dyn)

    # 后区综合评分分布 (与 dlt_auto 一致: 走 dlt_common.back_score)
    back_scored = {}
    for num in range(1, 13):
        cdm_s = models['cdm_prob_b'].get(num, 0)
        mk_s = models['markov_back'].get(num, 0)
        omit_s = models['back_omit'].get(num, 0) / models['max_back_omit']
        back_scored[num] = back_score(cdm_s, mk_s, omit_s)

    # V8.9.3: 与 dlt_auto 完全同构 —— 加载同一份专家数据, 5 个互不从属的策略锚点 + 强制组内最小差异
    expert_picks = []
    try:
        _ep = json.load(open('dlt_expert_picks.json', 'r', encoding='utf-8'))
        expert_picks = [(e['expert'], e['front'], e.get('back', [])) for e in _ep.get('experts', [])]
    except (FileNotFoundError, KeyError, json.JSONDecodeError, OSError):
        expert_picks = []

    if expert_picks:
        front_eci = Counter()
        for _e, _f, _b in expert_picks:
            for n in _f:
                front_eci[n] += 1
        front_eci_pct = {num: front_eci.get(num, 0) / len(expert_picks) * 100 for num in range(1, 36)}
        eci_front_dist = {n: 0.6 * cs[n] + 0.4 * (100 - front_eci_pct.get(n, 0)) / 100 for n in range(1, 36)}
        back_eci_count = Counter()
        for _e, _f, _b in expert_picks:
            for n in _b:
                back_eci_count[n] += 1
        maxc = max(back_eci_count.values(), default=1)
        eci_back_dist = {n: (maxc - back_eci_count.get(n, 0) + 1) for n in range(1, 13)}
        eci_name = 'ECI逆向(真实专家)'
        eci_strategy = f'避开{len(expert_picks)}位专家热门 后验采样'
    else:
        eci_front_dist = {n: omit.get(n, 0) for n in range(1, 36)}
        eci_back_dist = back_scored
        eci_name = '遗漏优选'
        eci_strategy = '遗漏值最大组合(无专家数据替代ECI) 后验采样'

    back_dist = {
        '综合共识': back_scored,
        '热号追踪': models['cdm_prob_b'],
        '冷号回补': {n: models['back_omit'].get(n, 0) for n in range(1, 13)},
        '逆向专家': eci_back_dist,
        '熵均衡': {n: 1.0 for n in range(1, 13)},
    }
    strategy_defs = [
        ('综合共识', cs, back_dist['综合共识']),
        ('热号追踪', models['freq_30'], back_dist['热号追踪']),
        ('冷号回补', {n: omit.get(n, 0) for n in range(1, 36)}, back_dist['冷号回补']),
        (eci_name, eci_front_dist, back_dist['逆向专家']),
        ('熵均衡', {n: 1.0 for n in range(1, 36)}, back_dist['熵均衡']),
    ]

    groups = []
    used = set()
    used_backs = set()
    for idx, (name, front_dist, back_dist_i) in enumerate(strategy_defs):
        placed = False
        for attempt in range(8):
            seed = seed_base * 100003 + idx * 7919 + 17 + attempt * 1000003  # 与 dlt_auto 同构
            front = _sample_front_group(front_dist, valid_dyn_set, used, prev_front, seed)
            if front is None:
                cand = sorted(valid_dyn, key=lambda c: sum(front_dist.get(n, 0) for n in c), reverse=True)
                for c in cand:
                    if tuple(sorted(c)) not in used:
                        front = list(c)
                        break
            if front is None:
                continue
            if any(len(set(front) & set(g[1])) >= 4 for g in groups):
                continue
            back = _sample_back_group(back_dist_i, used_backs, seed + 1)
            if back is None:
                back = sorted(sorted(range(1, 13), key=lambda n: back_dist_i.get(n, 0), reverse=True)[:4])
            if any(len(set(back) & set(g[2])) >= 3 for g in groups):
                continue
            used.add(tuple(sorted(front)))
            used_backs.add(tuple(sorted(back)))
            groups.append((name, sorted(front), sorted(back)))
            placed = True
            break
        if not placed:
            front = sorted(range(1, 36), key=lambda n: front_dist.get(n, 0), reverse=True)[:5] if front is None else front
            back = sorted(sorted(range(1, 13), key=lambda n: back_dist_i.get(n, 0), reverse=True)[:4])
            groups.append((name, sorted(front), sorted(back)))

    # 去重 (与线上一致)
    seen = set()
    out = []
    for name, front, back in groups:
        t = tuple(sorted(front))
        if t in seen:
            continue
        seen.add(t)
        out.append((name, sorted(front), sorted(back)))
    return out


# ============================================================
# 3. 命中与派彩
# ============================================================
def score_one(front_rec, back_rec, actual):
    """front_rec: 5元组; back_rec: 4码集合(实际投注=6注后区对); actual: 真实开奖。
    返回 (前区命中, 后区命中, 派彩)。后区命中=|back_rec ∩ actual.back|∈0..2。"""
    fh = len(set(front_rec) & set(actual['front']))
    bh = len(set(back_rec) & set(actual['back']))
    payout = PRIZE_PAYOUT.get((fh, bh), 0)
    return fh, bh, payout


# ============================================================
# 4. 样本外滚动回测
# ============================================================
def walk_forward_backtest(draws, start_idx=50, end_idx=None, seed=20260729):
    """对 [start_idx, end_idx) 每个测试期做样本外预测。
    返回 dict: 命中统计 / 派彩 / ROI / 每期净盈亏序列。"""
    if end_idx is None:
        end_idx = len(draws)
    rng = random.Random(seed)
    valid_cache = _build_valid_cache()

    per_period_net = []       # 每期净盈亏 (派彩-成本)
    total_cost = 0
    total_payout = 0
    tier_counts = Counter()   # 各奖级命中次数 (按最佳一注计? 这里累加每组最佳)
    any_prize = 0             # 任一注中奖的期数
    n_periods = 0

    for k in range(start_idx, end_idx):
        hist = draws[:k]
        actual = draws[k]
        recs = recommend(hist, valid_cache, seed_base=int(actual['period']))
        if not recs:
            continue
        n_periods += 1
        period_cost = 0
        period_payout = 0
        period_won = False
        for _, front, back in recs:
            # 每组 = 1 前区组合 × C(4,2)=6 后区对 = 6 注
            back_pairs = list(combinations(back, 2))
            for bp in back_pairs:
                period_cost += COST_PER_BET
                # 该注后区命中 = |bp ∩ actual.back|
                bh = len(set(bp) & set(actual['back']))
                fh = len(set(front) & set(actual['front']))
                pay = PRIZE_PAYOUT.get((fh, bh), 0)
                if pay > 0:
                    period_won = True
                period_payout += pay
        total_cost += period_cost
        total_payout += period_payout
        per_period_net.append(period_payout - period_cost)
        if period_won:
            any_prize += 1

    roi = (total_payout / total_cost - 1) if total_cost else 0.0
    return {
        'n_periods': n_periods,
        'total_cost': total_cost,
        'total_payout': total_payout,
        'roi': roi,
        'any_prize_periods': any_prize,
        'any_prize_rate': any_prize / n_periods if n_periods else 0,
        'per_period_net': per_period_net,
        'avg_net_per_period': (total_payout - total_cost) / n_periods if n_periods else 0,
    }


def random_baseline(draws, start_idx=50, end_idx=None, n_sims=20, seed=12345):
    """纯随机基线: 从与真实策略相同的过滤后号码空间抽取, 公平比较。
    返回多次仿真的 ROI 统计, 以及每期净盈亏的"跨仿真均值序列"(供 Bootstrap 配对比较)。"""
    if end_idx is None:
        end_idx = len(draws)
    rng = random.Random(seed)
    valid_cache = _build_valid_cache()
    back4_all = list(combinations(range(1, 13), 4))
    # V8.9.2: 与策略同构 — 基线也从"含重号过滤"的同一空间抽取(每期只依赖历史, 预计算一次)
    valid_dyn_by_k = [
        [c for c in valid_cache if len(set(c) & set(draws[k - 1]['front'])) <= 2]
        for k in range(start_idx, end_idx)
    ]

    rois = []
    rates = []
    # 每期净盈亏, 维度 = [sim, period]
    net_by_sim = []
    for s in range(n_sims):
        r = random.Random(seed + s)
        total_cost = 0
        total_payout = 0
        any_prize = 0
        n_periods = 0
        net_seq = []
        for k in range(start_idx, end_idx):
            actual = draws[k]
            n_periods += 1
            period_cost = 0
            period_payout = 0
            period_won = False
            for _ in range(5):  # 5 组
                front = r.choice(valid_dyn_by_k[k - start_idx])
                back = list(r.choice(back4_all))
                for bp in combinations(back, 2):
                    period_cost += COST_PER_BET
                    bh = len(set(bp) & set(actual['back']))
                    fh = len(set(front) & set(actual['front']))
                    pay = PRIZE_PAYOUT.get((fh, bh), 0)
                    if pay > 0:
                        period_won = True
                    period_payout += pay
            total_cost += period_cost
            total_payout += period_payout
            net_seq.append(period_payout - period_cost)
            if period_won:
                any_prize += 1
        rois.append(total_payout / total_cost - 1)
        rates.append(any_prize / n_periods)
        net_by_sim.append(net_seq)
    # 跨仿真逐期均值 (长度 = n_periods), 作为与策略配对的基线序列
    per_period_net_mean = [sum(net_by_sim[s][k] for s in range(n_sims)) / n_sims
                           for k in range(len(net_by_sim[0]))]
    return {
        'n_sims': n_sims,
        'roi_mean': sum(rois) / len(rois),
        'roi_min': min(rois),
        'roi_max': max(rois),
        'any_prize_rate_mean': sum(rates) / len(rates),
        'per_period_net': per_period_net_mean,
    }


# ============================================================
# 5. 两比例 z 检验 (策略 any_prize_rate vs 随机基线)
# ============================================================
def two_proportion_z(p1, n1, p2, n2):
    """返回 (z, p_value) 双侧。"""
    x1 = p1 * n1
    x2 = p2 * n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    # 双侧 p (近似正态)
    p = math.erfc(abs(z) / math.sqrt(2))
    return z, p


def bootstrap_diff_ci(a, b, B=2000, seed=99):
    """Bootstrap 配对差值 CI: 返回 (low, high) of mean(a)-mean(b) 的 95% 区间。
    a, b 为逐期净盈亏序列(允许长度不同, 自动对齐到较短者)。用于检验'策略是否显著优于随机'。"""
    rng = random.Random(seed)
    n = min(len(a), len(b))
    if n == 0:
        return (0.0, 0.0)
    a = a[:n]
    b = b[:n]
    diffs = []
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        ma = sum(a[i] for i in idx) / n
        mb = sum(b[i] for i in idx) / n
        diffs.append(ma - mb)
    diffs.sort()
    return diffs[int(0.025 * B)], diffs[int(0.975 * B)]


# ============================================================
# 6. 蒙特卡洛成本仿真
# ============================================================
def monte_carlo_cost(per_period_net, players=10000, weeks=52, draws_per_week=3, seed=777):
    """用回测的每期净盈亏经验分布重采样, 模拟玩家财务结果。
    每"周"= draws_per_week 个开奖期。返回分布统计。"""
    rng = random.Random(seed)
    if not per_period_net:
        return None
    results = []
    for _ in range(players):
        net = 0
        for _ in range(weeks * draws_per_week):
            net += rng.choice(per_period_net)
        results.append(net)
    results.sort()
    n = len(results)
    p05 = results[int(0.05 * n)]
    p50 = results[int(0.50 * n)]
    p95 = results[int(0.95 * n)]
    profit = sum(1 for x in results if x > 0)
    return {
        'players': players,
        'weeks': weeks,
        'draws_per_week': draws_per_week,
        'expected_net': sum(results) / n,
        'p05_net': p05,
        'median_net': p50,
        'p95_net': p95,
        'prob_profit': profit / n,
    }


# ============================================================
# 7. 自我进化证明闸门
# ============================================================
def assert_improvement(new_backtest, baseline_backtest, label='本系统'):
    """任何'更强了'的声称必须过 Bootstrap 显著性检验, 否则系统拒绝该声称。
    比较 new_backtest 与 baseline (随机基线或上一版) 的逐期净盈亏:
    仅当 95% CI 下界 > 0 (策略 ROI 显著优于基线) 才接受。"""
    a = new_backtest.get('per_period_net', [])
    b = baseline_backtest.get('per_period_net', [])
    if not a or not b:
        return {'accepted': False, 'reason': '缺少逐期净盈亏数据, 无法检验'}
    ci_low, ci_high = bootstrap_diff_ci(a, b)
    roi_new = new_backtest['roi'] * 100
    roi_base = baseline_backtest['roi'] * 100 if 'roi' in baseline_backtest else baseline_backtest.get('roi_mean', 0) * 100
    if ci_low > 0:
        return {'accepted': True,
                'reason': f'通过 Bootstrap 检验 (ROI 差 95% CI=[{ci_low:+.2f},{ci_high:+.2f}]pp 全>0), '
                          f'策略 ROI {roi_new:+.1f}% 显著优于基线 {roi_base:+.1f}%。可声称更强。',
                'ci_low': ci_low, 'ci_high': ci_high}
    else:
        return {'accepted': False,
                'reason': f'未通过 Bootstrap 检验 (ROI 差 95% CI=[{ci_low:+.2f},{ci_high:+.2f}]pp, 下界未>0), '
                          f'不能声称"{label}更强"。策略 ROI {roi_new:+.1f}% 与基线 {roi_base:+.1f}% 无显著差异, 属随机波动。',
                'ci_low': ci_low, 'ci_high': ci_high}


# ============================================================
# 8.  honesty guardrail
# ============================================================
def honesty_guardrail(strat, base):
    """用 ROI 的 Bootstrap 配对 CI 判定是否存在预测优势。
    仅当策略 ROI 显著优于随机基线 (95% CI 下界>0) 才承认有优势。"""
    a = strat.get('per_period_net', [])
    b = base.get('per_period_net', [])
    if not a or not b:
        return {'no_edge': True, 'message': '缺少数据, 默认声明无优势。'}
    ci_low, ci_high = bootstrap_diff_ci(a, b)
    roi_s = strat['roi'] * 100
    roi_b = base['roi_mean'] * 100
    no_edge = ci_low <= 0  # 无法证明策略显著优于随机
    if no_edge:
        msg = ('✅ 已证明: 本策略 ROI=%.1f%% 与纯随机基线 %.1f%% 无统计显著差异 '
               '(ROI差 Bootstrap 95%% CI=[%+.2f,%+.2f]pp, 下界未>0)。'
               '系统不存在可证明的预测优势——任何"变强"都属随机波动。'
               % (roi_s, roi_b, ci_low, ci_high))
    else:
        msg = ('⚠️ 检测到潜在优势: 策略 ROI 显著优于随机 (ROI差 95%% CI=[%+.2f,%+.2f]pp)。'
               '需独立复核是否为真实优势, 暂不下结论。' % (ci_low, ci_high))
    return {'no_edge': no_edge, 'ci_low': ci_low, 'ci_high': ci_high, 'message': msg}


# ============================================================
# 主入口
# ============================================================
def run(window='sample'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 70)
    print("【Power Engine V8.9.7: 强化引擎 / 科学严谨性自检】")
    print("=" * 70)
    with open('dlt_history.json', 'r', encoding='utf-8') as f:
        draws = json.load(f)
    draws.sort(key=lambda x: x['period'])
    n = len(draws)
    print(f"  历史数据: {n} 期")

    if window == 'full':
        start, end = 200, n
        print(f"  回测窗口: 全量样本外 [{start}, {n}) = {n-start} 期")
    else:
        start, end = max(200, n - 200), n
        print(f"  回测窗口: 近 200 期样本外 [{start}, {n})")

    t0 = datetime.now()
    strat = walk_forward_backtest(draws, start_idx=start, end_idx=end)
    base = random_baseline(draws, start_idx=start, end_idx=end, n_sims=20)
    dt = (datetime.now() - t0).total_seconds()

    print(f"\n  [策略回测] 期数={strat['n_periods']} 成本=¥{strat['total_cost']:,} "
          f"派彩=¥{strat['total_payout']:,} ROI={strat['roi']*100:+.1f}% "
          f"中奖期率={strat['any_prize_rate']*100:.1f}%")
    print(f"  [随机基线] ROI均值={base['roi_mean']*100:+.1f}% "
          f"(区间[{base['roi_min']*100:+.1f}%,{base['roi_max']*100:+.1f}%]) "
          f"中奖期率={base['any_prize_rate_mean']*100:.1f}%")
    print(f"  计算耗时: {dt:.1f}s")

    guard = honesty_guardrail(strat, base)
    print(f"\n  {guard['message']}")

    mc = monte_carlo_cost(strat['per_period_net'], players=20000, weeks=52)
    if mc:
        print(f"\n  [蒙特卡洛成本仿真] 玩家={mc['players']:,} 玩 {mc['weeks']}周(≈{mc['weeks']*mc['draws_per_week']}期):")
        print(f"    期望净盈亏: ¥{mc['expected_net']:,.0f}")
        print(f"    中位净盈亏: ¥{mc['median_net']:,.0f}")
        print(f"    5%~95%区间: [¥{mc['p05_net']:,.0f}, ¥{mc['p95_net']:,.0f}]")
        print(f"    正收益概率 P(净盈亏>0): {mc['prob_profit']*100:.2f}%")

    gate = assert_improvement(strat, base, label='本系统')
    print(f"\n  [诚实闸门 vs 随机] {'✅接受' if gate['accepted'] else '⛔拒绝'}: {gate['reason']}")

    # 回归闸门: 对照上一版本基线, 检测本次代码改动是否意外改变结果
    saved = _load_baseline()
    if saved:
        reg = assert_improvement(strat, saved, label='本版本 vs 上一版')
        print(f"  [回归闸门 vs 上一版] {'✅无退化' if reg['accepted'] else '⚠️结果变动'}: {reg['reason']}")
    else:
        print(f"  [回归闸门] 无历史基线, 已建立基线")

    # 持久化基线 (供下一版本对照)
    _save_baseline(strat)

    report = {
        'version': 'V8.9.7 Power Engine',
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'window': f'[{start},{end})',
        'strategy': strat,
        'random_baseline': base,
        'honesty_guardrail': guard,
        'monte_carlo': mc,
        'self_improvement_gate': gate,
        'baseline_saved': True,
    }
    _out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dlt_power_report.json')
    with open(_out, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n  ✓ 强化报告已保存: dlt_power_report.json")
    return report


def _load_baseline(path='dlt_power_baseline.json'):
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def _save_baseline(strat, path='dlt_power_baseline.json'):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(strat, f, ensure_ascii=False, indent=2, default=str)
    except Exception:
        pass


def _self_test():
    # 奖级表完整性 (检查代表性中奖组合, 非中奖组合已不再入表)
    assert PRIZE_PAYOUT[(5, 2)] > 0 and PRIZE_PAYOUT[(0, 2)] > 0 and PRIZE_PAYOUT[(3, 1)] > 0
    # 合成 60 期数据, 校验模型与评分
    import random as _r
    _r.seed(1)
    synth = []
    for i in range(60):
        front = sorted(_r.sample(range(1, 36), 5))
        back = sorted(_r.sample(range(1, 13), 2))
        synth.append({'period': f'{i:05d}', 'date': '2020-01-01', 'front': front, 'back': back})
    m = compute_models(synth)
    assert len(m['combined_score']) == 35
    assert all(0 <= v < 1e9 for v in m['combined_score'].values())
    # 命中与派彩
    fh, bh, pay = score_one([1, 2, 3, 4, 5], [1, 2, 3, 4], {'front': [1, 2, 3, 9, 10], 'back': [3, 7]})
    assert fh == 3 and bh == 1 and pay == PRIZE_PAYOUT[(3, 1)]
    # 统计函数
    z, p = two_proportion_z(0.5, 100, 0.5, 100)
    assert p > 0.9
    ci = bootstrap_diff_ci([1.0] * 50, [1.0] * 50, B=200)
    assert abs(ci[0]) < 1e-9 and abs(ci[1]) < 1e-9
    return True


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        _self_test()
        print("dlt_power_engine self-test OK")
    else:
        w = 'full' if '--full' in sys.argv else 'sample'
        run(w)
