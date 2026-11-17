# -*- coding: utf-8 -*-
"""
大乐透「最小成本 · 最大收益」覆盖优化器 (V8.9.8 新增)

用户需求(2026-09-07):
  "你至少预测出几个正确号码吧, 你预测几个三/四/五/六/七等奖, 总可以吧?
   加加油, 看看怎么能用最小的成本获取最大的收益"

核心思想(诚实):
  - 数学上任何选号法都不优于随机(no_edge), 一等奖概率恒 1/21,425,712 无法改变。
  - 但"中低等奖(六/七等, 需前区≤3 + 后区≤2)"是真实可捕获的奖级。
  - 单式只覆盖 1 个前区组合 + 1 个后区对, 几乎永远凑不出六/七等奖所需的对齐。
  - 本器在【固定预算】内, 用组合数学(复式/胆拖)选择最优"覆盖结构",
    使一张张票的 (前区子集, 后区对) 组合尽可能铺满号码空间,
    从而最大化"命中六/七等奖"的概率 —— 这是成本效率优化, 不是预测优势。
  - EV 仍为负(返奖率 51%), 本器是伤害减损(在娱乐预算内提高中奖体验), 绝非盈利。

方法:
  - 枚举候选结构(单式 / 复式前区 / 复式后区 / 胆拖), 在预算上限内。
  - 蒙特卡洛(N 次随机开奖)估计每张票集合命中各奖级的概率。
  - 选 P(命中≥目标奖级)/成本 最优者, 同分取更省成本。

与 dlt_dantuo_optimizer 的区别:
  - 那是"模型评分加权 MC"(依赖模型置信度, 仍无 edge)。
  - 本器是"纯组合覆盖"(与号码置信度无关), 直接回答"最小成本最大收益"。
"""
import itertools
import random
from dataclasses import dataclass, field

FRONT_N = 35
FRONT_PICK = 5
BACK_N = 12
BACK_PICK = 2
NOTE_COST = 2  # 基本投注每注 2 元

# 当前 7 奖级映射(财综〔2025〕51号, 自26014期起; 与 dlt_power_engine/dlt_draw_check 一致)
def tier_of(fh, bh):
    if fh == 5 and bh == 2:
        return 1
    if fh == 5 and bh == 1:
        return 2
    if (fh == 5 and bh == 0) or (fh == 4 and bh == 2):
        return 3
    if fh == 4 and bh == 1:
        return 4
    if (fh == 3 and bh == 2) or (fh == 4 and bh == 0):
        return 5
    if (fh == 3 and bh == 1) or (fh == 2 and bh == 2):
        return 6
    if (fh == 3 and bh == 0) or (fh == 2 and bh == 1) or (fh == 1 and bh == 2) or (fh == 0 and bh == 2):
        return 7
    return 0


def build_tickets(front_pool, back_pool, front_dan=None, back_dan=None):
    """构造票集合。front_pool/back_pool 为待组合号码全集(与置信度无关, 纯覆盖)。
    返回 [(frozenset(5前区), frozenset(2后区)), ...]"""
    front_pool = list(front_pool)
    back_pool = list(back_pool)
    if front_dan:
        dan = set(front_dan)
        need = FRONT_PICK - len(dan)
        drag = [x for x in front_pool if x not in dan]
        front_combos = [frozenset(dan | set(c)) for c in itertools.combinations(drag, need)]
    else:
        front_combos = [frozenset(c) for c in itertools.combinations(front_pool, FRONT_PICK)]
    if back_dan:
        dan = set(back_dan)
        need = BACK_PICK - len(dan)
        drag = [x for x in back_pool if x not in dan]
        back_combos = [frozenset(dan | set(c)) for c in itertools.combinations(drag, need)]
    else:
        back_combos = [frozenset(c) for c in itertools.combinations(back_pool, BACK_PICK)]
    return [(f, b) for f in front_combos for b in back_combos]


def monte_carlo(tickets, n_sims=120000, seed=20260907):
    """蒙特卡洛估计: 返回 {tier: P(至少中第 tier 等奖)} 与 P(任意奖)。

    语义(⚠️ 历史教训: 曾误用 max 取"最差奖级编号", 使 p_capture 语义颠倒,
    多票方案下会把"最差那张票的奖级"当成最好成绩, 导致 P(六等)>P(七等) 这类不可能结果):
      奖级编号 1=一等奖(最好) ... 7=七等奖(最低)。
      best = 本次开奖下所有票里的"最好奖级" = 最小编号(未中奖记 99)。
      p_capture[t] = P(best <= t) = P(至少中第 t 等奖)。
      故 p_capture[7] = P(任意奖), p_capture[6] = P(六等奖或更好)。
    """
    rng = random.Random(seed)
    cap = {t: 0 for t in range(1, 8)}
    any_prize = 0
    for _ in range(n_sims):
        df = frozenset(rng.sample(range(1, FRONT_N + 1), FRONT_PICK))
        db = frozenset(rng.sample(range(1, BACK_N + 1), BACK_PICK))
        best = 99  # 越小越好; 99 = 未中奖
        for f, b in tickets:
            fh = len(f & df)
            bh = len(b & db)
            t = tier_of(fh, bh)
            if 0 < t < best:
                best = t
                if best == 1:
                    break
        if best <= 7:
            any_prize += 1
        for t in range(1, 8):
            if best <= t:
                cap[t] += 1
    return {t: cap[t] / n_sims for t in cap}, any_prize / n_sims


@dataclass
class Plan:
    name: str
    tickets: list
    cost: int
    p_capture: dict = field(default_factory=dict)
    p_any: float = 0.0
    structure: str = ""


def enumerate_plans(front_pool, back_pool, budget, max_front_pool=12, max_back_pool=8):
    """枚举预算内所有候选结构, 返回 Plan 列表(未算 MC)。"""
    plans = []
    # 1) 单式
    if len(front_pool) >= 5 and len(back_pool) >= 2:
        t = build_tickets(front_pool[:5], back_pool[:2])
        plans.append(Plan("单式(1前区组合+1后区对)", t, len(t) * NOTE_COST, structure="single"))
    # 2) 复式前区 n 选 5 × 单式后区
    for n in range(6, min(max_front_pool, len(front_pool)) + 1):
        t = build_tickets(front_pool[:n], back_pool[:2])
        c = len(t) * NOTE_COST
        if c <= budget:
            plans.append(Plan(f"复式前区{n}选5 × 单式后区", t, c, structure=f"front{n}"))
    # 3) 复式前区 × 复式后区 m 选 2
    for n in range(6, min(max_front_pool, len(front_pool)) + 1):
        for m in range(3, min(max_back_pool, len(back_pool)) + 1):
            t = build_tickets(front_pool[:n], back_pool[:m])
            c = len(t) * NOTE_COST
            if c <= budget:
                plans.append(Plan(f"复式前区{n}选5 × 复式后区{m}选2", t, c, structure=f"front{n}back{m}"))
    # 4) 胆拖: 前区 2 胆 + 拖, 后区 0/1 胆
    for d in (2, 3):
        if len(front_pool) > d + (FRONT_PICK - d):
            for m in (2, 3, 4):
                t = build_tickets(front_pool[:d + (FRONT_PICK - d) + 2], back_pool[:m],
                                  front_dan=front_pool[:d])
                c = len(t) * NOTE_COST
                if c <= budget:
                    plans.append(Plan(f"胆拖前{d}胆 × 后区{m}选2", t, c, structure=f"dantu{d}back{m}"))
    return plans


def optimize(front_pool, back_pool, budget=30, target_tier=7, n_sims=120000, seed=20260907):
    """返回 (最优Plan, 所有候选Plan)。target_tier: 7=七等奖, 6=六等奖。"""
    plans = enumerate_plans(front_pool, back_pool, budget)
    for p in plans:
        p.p_capture, p.p_any = monte_carlo(p.tickets, n_sims=n_sims, seed=seed)
    # 评分: 优先 P(命中≥目标奖级); 同分取更省成本(更小 cost)
    def score(p):
        return (p.p_capture.get(target_tier, 0), -p.cost)
    plans.sort(key=score, reverse=True)
    return plans[0] if plans else None, plans


def honest_ev_note(plan, pool_mode="保底档(奖池<8亿)"):
    """诚实 EV 附注(伤害减损, 非盈利)。"""
    return (
        f"诚实声明: 本方案为纯组合覆盖优化, 不宣称任何预测优势(no_edge)。"
        f"返奖率约51%, 期望净收益为负 —— 长期必亏, 仅作娱乐预算内的中奖体验优化。"
        f"所选号码本身与随机机选等价; 优化的是'覆盖结构'而非'号码对错'。"
        f"奖金口径: {pool_mode}。"
    )


if __name__ == "__main__":
    # 自检: 用模型常用 top 号码作为覆盖池(仅作演示, 不暗示更可能中)
    front_pool = list(range(1, 13)) + [15, 17, 20, 22, 24, 26, 28, 30, 32, 34]
    back_pool = list(range(1, 13))
    best, allp = optimize(front_pool, back_pool, budget=30, target_tier=7, n_sims=120000)
    print("预算 ¥30 候选方案数:", len(allp))
    for p in allp[:8]:
        print(f"  {p.name:28s} 注数={len(p.tickets):4d} 成本=¥{p.cost:3d} "
              f"P(七等)={p.p_capture.get(7,0):.3f} P(六等)={p.p_capture.get(6,0):.4f} P(任意)={p.p_any:.3f}")
    print("\n最优(最小成本最大收益, 目标七等奖):")
    print(f"  {best.name}  成本=¥{best.cost}  注数={len(best.tickets)}")
    print(f"  P(七等奖)={best.p_capture.get(7,0):.3f}  P(六等奖)={best.p_capture.get(6,0):.4f}  P(任意奖)={best.p_any:.3f}")
    print("  ", honest_ev_note(best))
