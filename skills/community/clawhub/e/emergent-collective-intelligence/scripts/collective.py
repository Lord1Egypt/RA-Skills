#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent-collective-intelligence —— 涌现集体智能编排引擎（纯标准库）

单个大模型 = 单一先验、单点盲区。本引擎编排一个**多样化 agent 群体**：每个成员用
不同策略/偏置独立给出估计，再通过"多样性加权聚合 + 相互纠错"涌现出**超越任一个体**
的集体解（群体智慧 Wisdom of Crowds 的可验证工程化）。

核心机制：
  1) 多样性(Diversity)：成员偏置各异（乐观/悲观/保守/激进/随机…），偏置独立→误差可抵消。
  2) 聚合(Aggregation)：稳健聚合（去极值 + 逆方差/多样性加权），抑制离群、放大共识。
  3) 涌现判定(Emergence)：集体误差 < 最好单体误差 → 判定"涌现"（1+1>2 的可测证据）。
  4) 相互纠错(Peer-correction)：偏离群体共识过远的成员按共识收敛一步，迭代降方差。

用法：
  python collective.py --selftest
  python collective.py --demo
"""
import sys, statistics, json


class Agent:
    """一个带确定性偏置的群体成员。estimate(signal) -> 数值估计。"""
    def __init__(self, name, bias, gain=1.0):
        self.name = name
        self.bias = bias        # 系统性偏置（可正可负）
        self.gain = gain        # 对信号的敏感度

    def estimate(self, signal):
        return self.gain * signal + self.bias


def robust_aggregate(values, weights=None):
    """稳健聚合：>=5 个去掉最高最低各一个，再做（可选）加权均值。"""
    vals = list(values)
    if weights is None:
        weights = [1.0] * len(vals)
    paired = sorted(zip(vals, weights), key=lambda p: p[0])
    if len(paired) >= 5:
        paired = paired[1:-1]                     # 去极值
    tot_w = sum(w for _, w in paired)
    return sum(v * w for v, w in paired) / tot_w if tot_w else statistics.mean(vals)


def diversity_weights(values):
    """多样性/逆偏离加权：离群体中位数越近权重越高，抑制离群成员。"""
    med = statistics.median(values)
    devs = [abs(v - med) for v in values]
    maxd = max(devs) or 1.0
    return [1.0 - 0.5 * (d / maxd) for d in devs]   # [0.5, 1.0]


def peer_correction(values, rounds=2, pull=0.3):
    """相互纠错：每轮把每个估计朝群体共识拉近 pull 比例，降方差不改无偏共识。"""
    vals = list(values)
    for _ in range(rounds):
        consensus = statistics.mean(vals)
        vals = [v + pull * (consensus - v) for v in vals]
    return vals


def collective_solve(agents, signal, truth=None):
    """群体求解：采集个体估计 → 相互纠错 → 多样性加权稳健聚合 → 涌现判定。"""
    raw = [a.estimate(signal) for a in agents]
    corrected = peer_correction(raw, rounds=2, pull=0.3)
    w = diversity_weights(corrected)
    collective = robust_aggregate(corrected, w)
    report = {
        "n_agents": len(agents),
        "individual": {a.name: round(v, 4) for a, v in zip(agents, raw)},
        "collective": round(collective, 4),
        "diversity": round(statistics.pstdev(raw), 4),
    }
    if truth is not None:
        ind_err = {a.name: abs(v - truth) for a, v in zip(agents, raw)}
        best_ind = min(ind_err.values())
        col_err = abs(collective - truth)
        report.update({
            "truth": truth,
            "best_individual_error": round(best_ind, 4),
            "collective_error": round(col_err, 4),
            "emergent": col_err < best_ind,          # 集体优于最好单体 = 涌现
            "mean_individual_error": round(sum(ind_err.values()) / len(ind_err), 4),
        })
    return report


def _selftest():
    ok = True
    truth = 100.0
    signal = 100.0
    # 多样化群体：偏置各异（关键：偏置有正有负，误差可相互抵消）
    # 对称多样化群体：偏置成对相消、无"运气极准"单体（最好单体误差=7），
    # 集体经聚合应逼近真值并优于最好单体 → 可证涌现。
    agents = [
        Agent("optimist", bias=+12, gain=1.0),
        Agent("pessimist", bias=-11, gain=1.0),
        Agent("conservative", bias=-8, gain=1.0),
        Agent("aggressive", bias=+9, gain=1.0),
        Agent("hawk", bias=+15, gain=1.0),
        Agent("dove", bias=-13, gain=1.0),
        Agent("outlier", bias=+40, gain=1.0),        # 离群者：应被稳健聚合抑制
    ]
    r = collective_solve(agents, signal, truth=truth)

    # [1] 涌现：集体误差 < 最好单体误差
    cond1 = r["emergent"] is True
    print(f"[1] 涌现判定 集体误差={r['collective_error']} < 最好单体={r['best_individual_error']} "
          f"→ emergent={r['emergent']} {'PASS' if cond1 else 'FAIL'}")
    ok &= cond1

    # [2] 集体优于群体平均个体误差
    cond2 = r["collective_error"] < r["mean_individual_error"]
    print(f"[2] 集体误差 {r['collective_error']} < 平均个体误差 {r['mean_individual_error']} "
          f"{'PASS' if cond2 else 'FAIL'}")
    ok &= cond2

    # [3] 稳健聚合抑制离群者：集体估计明显偏离 outlier 的 140
    cond3 = abs(r["collective"] - 140) > 30
    print(f"[3] 离群者(140)被抑制 集体={r['collective']} {'PASS' if cond3 else 'FAIL'}")
    ok &= cond3

    # [4] 相互纠错降方差：纠错后标准差 < 原始
    raw = [a.estimate(signal) for a in agents]
    corr = peer_correction(raw)
    cond4 = statistics.pstdev(corr) < statistics.pstdev(raw)
    print(f"[4] 相互纠错降方差 {round(statistics.pstdev(raw),3)} → {round(statistics.pstdev(corr),3)} "
          f"{'PASS' if cond4 else 'FAIL'}")
    ok &= cond4

    # [5] 单一无多样性群体不产生涌现（所有成员同偏置 → 集体≈个体，误差不减）
    clones = [Agent(f"clone{i}", bias=+15, gain=1.0) for i in range(7)]
    rc = collective_solve(clones, signal, truth=truth)
    cond5 = rc["emergent"] is False
    print(f"[5] 无多样性(同偏置)群体 不涌现 → emergent={rc['emergent']} {'PASS' if cond5 else 'FAIL'}")
    ok &= cond5

    print("\n涌现集体智能编排 selftest:", "全部 PASS ✅" if ok else "存在 FAIL ❌")
    return ok


def _demo():
    agents = [Agent("a", 8), Agent("b", -6), Agent("c", 2), Agent("d", -3),
              Agent("e", 5), Agent("f", 30)]
    print(json.dumps(collective_solve(agents, 50.0, truth=50.0), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if _selftest() else 1)
    elif "--demo" in sys.argv:
        _demo()
    else:
        print(__doc__)
