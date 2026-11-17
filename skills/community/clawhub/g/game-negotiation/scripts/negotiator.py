#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""game-negotiation: 可计算博弈与协商引擎。

实体化"前沿认知·博弈谈判"：多方可计算博弈/协商，求最优/纳什策略。
能力：
  1. Nash 议价(广义权重)：威胁点 + 剩余分配，闭式解。
  2. Rubinstein 轮流出价：贴现因子下的子博弈完美均衡份额。
  3. Shapley 值：合作博弈的公平贡献分配。
  4. 零和 minimax：离散化网格求最大最小均衡值(近似)。
纯标准库，零依赖；--selftest 内置实测。
"""
import sys, json, itertools, argparse

# ---------- 1. Nash 议价（广义权重） ----------
def nash_bargain(disagree, surplus, weights):
    """disagree=(d1,d2) 威胁点；surplus 可分配剩余总额；weights=(w1,w2) 议价力。
    广义 Nash：u_i = d_i + w_i/Σw * surplus。"""
    s = sum(weights)
    return [disagree[0] + weights[0] / s * surplus,
            disagree[1] + weights[1] / s * surplus]

# ---------- 2. Rubinstein 轮流出价 ----------
def rubinstein(p_discount, r_discount):
    """提议方(玩家1)份额 = (1-r)/(1-p*r)，应答方份额 = 1-前者。
    p=提议方贴现, r=应答方贴现。"""
    p1 = (1 - r_discount) / (1 - p_discount * r_discount)
    return [p1, 1 - p1]

# ---------- 3. Shapley 值 ----------
def shapley(players, char_func):
    """char_func(subset frozenset)->实数贡献值。返回每玩家平均边际贡献。"""
    n = len(players)
    vals = {p: 0.0 for p in players}
    for perm in itertools.permutations(players):
        seen = frozenset()
        for i, p in enumerate(perm):
            contrib = char_func(seen | {p}) - char_func(seen)
            vals[p] += contrib
            seen = seen | {p}
    fact = _factorial(n)
    return {p: vals[p] / fact for p in players}

def _factorial(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r

# ---------- 4. 零和 minimax（离散网格近似） ----------
def minimax(payoff_matrix, steps=21):
    """payoff_matrix[i][j] = 玩家1 在(纯策略i, 纯策略j)的收益。
    离散化玩家1混合策略 p，对每个 p 取对手最优反应的最小收益，再取最大。"""
    m = len(payoff_matrix); n = len(payoff_matrix[0])
    grid = [k / (steps - 1) for k in range(steps)]
    best = -1e18
    for a in grid:
        p = [a, 1 - a] if m == 2 else _simplex_point(grid, m, a)
        # 对手最优反应：对每个 j，算 E[payoff|j]，取最小
        worst = min(
            sum(p[i] * payoff_matrix[i][j] for i in range(m)) for j in range(n)
        )
        if worst > best:
            best = worst
    return round(best, 4)

def _simplex_point(grid, m, a):
    # 仅用于 m==2；更高维退化为等权（近似）
    return [1.0 / m] * m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["nash", "rubinstein", "shapley", "minimax"])
    ap.add_argument("--json", help="参数 json：依 mode 不同")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    kw = json.loads(a.json) if a.json else {}
    if a.mode == "nash":
        print(json.dumps(nash_bargain(tuple(kw["disagree"]), kw["surplus"], tuple(kw["weights"]))))
    elif a.mode == "rubinstein":
        print(json.dumps(rubinstein(kw["p"], kw["r"])))
    elif a.mode == "shapley":
        players = kw["players"]
        cf = lambda s: (kw["char"][",".join(sorted(s))] if s else 0.0)
        print(json.dumps(shapley(players, cf), ensure_ascii=False))
    elif a.mode == "minimax":
        print(json.dumps(minimax(kw["matrix"])))

def selftest():
    # Nash：威胁(0,0)，剩余 100，等权 -> 各 50
    nv = nash_bargain((0, 0), 100, (1, 1))
    assert abs(nv[0] - 50) < 1e-9 and abs(nv[1] - 50) < 1e-9, nv
    # 权重 3:1 -> 75 / 25
    nv2 = nash_bargain((0, 0), 100, (3, 1))
    assert abs(nv2[0] - 75) < 1e-9, nv2
    # Rubinstein δ=0.9/0.9：先手占优 -> 提议方≈0.526
    rb = rubinstein(0.9, 0.9)
    assert abs(rb[0] - 0.5263) < 1e-3 and abs(rb[1] - 0.4737) < 1e-3, rb
    # Rubinstein δ=0(无贴现) -> 提议方全拿 1.0
    rb2 = rubinstein(0.0, 0.0)
    assert abs(rb2[0] - 1.0) < 1e-9, rb2
    # Shapley：3 玩家投票博弈(多数=2票才赢)
    players = ["A", "B", "C"]
    char = {"A": 0, "B": 0, "C": 0, "A,B": 1, "A,C": 1, "B,C": 1, "A,B,C": 1}
    sv = shapley(players, lambda s: (char[",".join(sorted(s))] if s else 0.0))
    assert abs(sv["A"] - 1 / 3) < 1e-9, sv
    assert abs(sum(sv.values()) - 1.0) < 1e-9, sv
    # minimax：匹配 pennies 型 2x2，值应为 0（在 p=0.5）
    mm = minimax([[1, -1], [-1, 1]])
    assert abs(mm - 0.0) < 0.05, mm
    print("✅ selftest PASS：Nash/Rubinstein/Shapley/minimax 全部符合闭式/理论值")
    print(json.dumps({"nash_even": nv, "nash_3_1": nv2, "rubi_09": rb,
                     "shapley_voting": sv, "minimax_pennies": mm}, ensure_ascii=False, indent=2))
    return True

if __name__ == "__main__":
    main()
