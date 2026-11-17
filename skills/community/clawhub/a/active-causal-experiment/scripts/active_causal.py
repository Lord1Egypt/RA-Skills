#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
active_causal.py — 因果世界模型主动实验（Active Causal Experiment Design）

核心机制：面对多个候选因果结构（competing causal DAGs），不被动观察，
而是**主动设计干预（do-operations）**，用「期望信息增益 / 最优实验设计」
挑选最能区分候选结构的那次实验，Bayesian 更新后验，以最少实验辨识真实因果结构。

一线大模型薄弱点：会「读懂」因果图，但缺少「为了辨别因果结构，
下一步该做哪个干预实验最划算」的主动实验设计闭环。本技能把它工程化：

    候选结构族 H  →  对每个候选预测 do(X=x) 下的结果分布
    →  期望信息增益 EIG(a)=I(H;O|a)=H(prior)-E_o[H(post|o)]
    →  选 argmax EIG 的干预（最优实验设计）
    →  对真实世界执行该干预、观测、Bayesian 更新后验
    →  重复直到某结构后验≥阈值（辨识收敛）

纯标准库（stdlib）实现，自带 --selftest。
"""
import sys
import math
import argparse
import itertools
from collections import defaultdict


# --------------------------------------------------------------------------
# 因果假设（候选结构）：每个假设知道在 do(var=val) 干预下各变量的预测取值。
# 变量取值域为 {0,1}；baseline（无干预时）全 0。
# 一个假设 = 一组有向边 edges: {parent: [children...]}（线性传播 val=1 沿边扩散）。
# --------------------------------------------------------------------------
class CausalHypothesis:
    def __init__(self, name, edges, variables):
        self.name = name
        self.edges = {k: list(v) for k, v in edges.items()}  # parent -> children
        self.variables = list(variables)

    def predict(self, do_var, do_val):
        """
        在 do(do_var=do_val) 干预下，返回所有变量的预测取值 dict。
        语义：被干预变量固定为 do_val（切断其入边）；其余变量从 baseline=0
        出发，沿有向边做前向传播（若某父节点=1 则子节点=1）。
        干预会传给下游，但不会回传给上游（do 切断入边）。
        """
        val = {v: 0 for v in self.variables}
        val[do_var] = do_val
        # 前向传播：反复松弛直到不动点（DAG 保证有限步收敛）
        changed = True
        guard = 0
        while changed and guard < len(self.variables) + 2:
            changed = False
            guard += 1
            for parent, children in self.edges.items():
                if val.get(parent, 0) == 1:
                    for c in children:
                        # do_var 被固定，入边被切断，不受父节点影响
                        if c == do_var:
                            continue
                        if val.get(c, 0) != 1:
                            val[c] = 1
                            changed = True
        return val


# --------------------------------------------------------------------------
# 信息论工具
# --------------------------------------------------------------------------
def entropy(probs):
    """probs: iterable of probabilities. 返回香农熵（bit）。"""
    h = 0.0
    for p in probs:
        if p > 0:
            h -= p * math.log2(p)
    return h


def belief_entropy(belief):
    """belief: dict name->prob"""
    return entropy(belief.values())


# --------------------------------------------------------------------------
# 似然：观测 o（其它变量取值）在假设 h、干预 a 下的似然，带观测噪声 eps。
# --------------------------------------------------------------------------
def likelihood(hyp, do_var, do_val, observation, eps=0.05):
    """
    observation: dict var->observed_val（不含被干预变量）。
    对每个被观测变量：预测==观测 → (1-eps)，否则 → eps。取乘积。
    带 eps 噪声地板，避免后验塌缩为精确 0，保证鲁棒。
    """
    pred = hyp.predict(do_var, do_val)
    lk = 1.0
    for var, obs_val in observation.items():
        if var == do_var:
            continue
        lk *= (1.0 - eps) if pred.get(var, 0) == obs_val else eps
    return lk


def possible_observations(variables, do_var):
    """列出除被干预变量外所有变量的 0/1 组合（作为可能观测）。"""
    obs_vars = [v for v in variables if v != do_var]
    for combo in itertools.product([0, 1], repeat=len(obs_vars)):
        yield dict(zip(obs_vars, combo))


# --------------------------------------------------------------------------
# 期望信息增益 EIG(a) = I(H;O|a) = H(prior) - E_o[ H(posterior|o) ]
# --------------------------------------------------------------------------
def expected_information_gain(hyps, belief, do_var, do_val, eps=0.05):
    variables = hyps[0].variables
    prior_H = belief_entropy(belief)
    exp_post_H = 0.0
    for obs in possible_observations(variables, do_var):
        # 边缘 P(o|a) 与 联合 P(h,o|a)
        joint = {}
        p_o = 0.0
        for h in hyps:
            lk = likelihood(h, do_var, do_val, obs, eps)
            j = belief[h.name] * lk
            joint[h.name] = j
            p_o += j
        if p_o <= 0:
            continue
        # 后验 P(h|o)
        post = {name: j / p_o for name, j in joint.items()}
        exp_post_H += p_o * entropy(post.values())
    return prior_H - exp_post_H


def rank_interventions(hyps, belief, candidate_do_values=(1,), eps=0.05):
    """对每个 (变量, 干预值) 计算 EIG，降序返回。"""
    variables = hyps[0].variables
    scored = []
    for v in variables:
        for dv in candidate_do_values:
            eig = expected_information_gain(hyps, belief, v, dv, eps)
            scored.append(((v, dv), eig))
    scored.sort(key=lambda x: (-x[1], str(x[0])))
    return scored


# --------------------------------------------------------------------------
# 主动实验闭环：选最优干预 → 对真实世界执行观测 → Bayesian 更新 → 收敛
# --------------------------------------------------------------------------
def bayesian_update(hyps, belief, do_var, do_val, observation, eps=0.05):
    new = {}
    total = 0.0
    for h in hyps:
        lk = likelihood(h, do_var, do_val, observation, eps)
        new[h.name] = belief[h.name] * lk
        total += new[h.name]
    if total <= 0:
        return dict(belief)
    return {k: v / total for k, v in new.items()}


def active_experiment_loop(hyps, true_hyp, threshold=0.85, max_experiments=None,
                           eps=0.05, candidate_do_values=(1,)):
    """
    主动实验设计闭环。true_hyp 为真实世界结构（selftest/仿真用）。
    返回 trace（每步选的干预/观测/后验/信息增益）。
    """
    names = [h.name for h in hyps]
    belief = {n: 1.0 / len(names) for n in names}
    if max_experiments is None:
        max_experiments = len(hyps[0].variables) * len(candidate_do_values) + 1
    trace = []
    used = set()
    for step in range(max_experiments):
        ranking = rank_interventions(hyps, belief, candidate_do_values, eps)
        # 跳过已做过的干预（避免重复无新信息）
        choice = None
        for (act, eig) in ranking:
            if act not in used:
                choice = (act, eig)
                break
        if choice is None:
            break
        (do_var, do_val), eig = choice
        used.add((do_var, do_val))
        # 对真实世界执行该干预并观测（真实结构预测 + 无噪声理想观测）
        real = true_hyp.predict(do_var, do_val)
        observation = {v: real[v] for v in true_hyp.variables if v != do_var}
        belief = bayesian_update(hyps, belief, do_var, do_val, observation, eps)
        best_name = max(belief, key=belief.get)
        trace.append({
            "step": step + 1,
            "intervention": f"do({do_var}={do_val})",
            "eig": round(eig, 4),
            "observation": observation,
            "posterior": {k: round(v, 4) for k, v in belief.items()},
            "map": best_name,
            "map_prob": round(belief[best_name], 4),
        })
        if belief[best_name] >= threshold:
            break
    return trace


# --------------------------------------------------------------------------
# 标准 3 变量场景族：X, Y, Z
#   H_chain_XYZ : X -> Y -> Z
#   H_chain_XZY : X -> Z -> Y
#   H_fork_X    : X -> Y, X -> Z
# 关键性质：do(X) 对三者预测完全相同（Y=1,Z=1）→ 零信息，主动设计必须避开。
#   do(Y) 区分 {chain_XYZ} vs {chain_XZY, fork_X}
#   do(Z) 区分 {chain_XZY} vs {chain_XYZ, fork_X}
# --------------------------------------------------------------------------
def build_standard_scenario():
    variables = ["X", "Y", "Z"]
    hyps = [
        CausalHypothesis("chain_XYZ", {"X": ["Y"], "Y": ["Z"]}, variables),
        CausalHypothesis("chain_XZY", {"X": ["Z"], "Z": ["Y"]}, variables),
        CausalHypothesis("fork_X",    {"X": ["Y", "Z"]},         variables),
    ]
    return hyps


def naive_experiment_loop(hyps, true_hyp, order, threshold=0.85, eps=0.05):
    """朴素基线：按固定顺序 order 依次做干预（不看信息增益），做对比。"""
    names = [h.name for h in hyps]
    belief = {n: 1.0 / len(names) for n in names}
    trace = []
    for i, do_var in enumerate(order):
        real = true_hyp.predict(do_var, 1)
        observation = {v: real[v] for v in true_hyp.variables if v != do_var}
        belief = bayesian_update(hyps, belief, do_var, 1, observation, eps)
        best = max(belief, key=belief.get)
        trace.append({"step": i + 1, "intervention": f"do({do_var}=1)",
                      "map": best, "map_prob": round(belief[best], 4)})
        if belief[best] >= threshold:
            break
    return trace


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------
def selftest():
    print("=" * 60)
    print("active_causal.py --selftest：因果世界模型主动实验")
    print("=" * 60)
    ok = True
    hyps = build_standard_scenario()
    belief0 = {h.name: 1.0 / len(hyps) for h in hyps}

    # 场景1：do(X) 为零信息干预（三候选预测相同），EIG 必须≈0
    eig_X = expected_information_gain(hyps, belief0, "X", 1)
    eig_Y = expected_information_gain(hyps, belief0, "Y", 1)
    eig_Z = expected_information_gain(hyps, belief0, "Z", 1)
    print(f"\n[1] 初始信息增益: do(X)={eig_X:.4f}  do(Y)={eig_Y:.4f}  do(Z)={eig_Z:.4f}")
    cond1 = eig_X < 1e-9 and eig_Y > 0.5 and eig_Z > 0.5
    print(f"    do(X)零信息 & do(Y)/do(Z)高信息: {'PASS' if cond1 else 'FAIL'}")
    ok &= cond1

    # 场景2：最优实验设计首选 do(Y) 或 do(Z)，绝不选 do(X)
    ranking = rank_interventions(hyps, belief0)
    top_act = ranking[0][0][0]
    print(f"\n[2] 最优实验排序 top1 = do({top_act}=1)（应为 Y 或 Z，绝非 X）")
    cond2 = top_act in ("Y", "Z") and ranking[-1][0][0] == "X"
    print(f"    首选非X且X垫底: {'PASS' if cond2 else 'FAIL'}")
    ok &= cond2

    # 场景3：真实=chain_XZY，主动闭环应收敛到 chain_XZY 且不选 do(X)
    true_h = hyps[1]  # chain_XZY
    trace = active_experiment_loop(hyps, true_h, threshold=0.85)
    used_vars = [t["intervention"] for t in trace]
    final = trace[-1]
    print(f"\n[3] 真实结构=chain_XZY 主动辨识：")
    for t in trace:
        print(f"    step{t['step']} {t['intervention']} EIG={t['eig']} "
              f"→ MAP={t['map']}({t['map_prob']})")
    cond3 = (final["map"] == "chain_XZY" and final["map_prob"] >= 0.85
             and all("do(X" not in iv for iv in used_vars))
    print(f"    收敛到真实结构 & 全程未浪费在 do(X): {'PASS' if cond3 else 'FAIL'}")
    ok &= cond3

    # 场景4：主动 vs 朴素（朴素从 X 开始）——主动实验数 ≤ 朴素
    true_h2 = hyps[0]  # chain_XYZ
    active_tr = active_experiment_loop(hyps, true_h2, threshold=0.85)
    naive_tr = naive_experiment_loop(hyps, true_h2, order=["X", "Y", "Z"], threshold=0.85)
    n_active = len(active_tr)
    n_naive = len(naive_tr)
    print(f"\n[4] 真实=chain_XYZ：主动实验数={n_active}  朴素(X先)实验数={n_naive}")
    cond4 = (active_tr[-1]["map"] == "chain_XYZ" and n_active <= n_naive
             and naive_tr[0]["intervention"] == "do(X=1)")
    print(f"    主动收敛真结构 & 实验数不劣于朴素: {'PASS' if cond4 else 'FAIL'}")
    ok &= cond4

    # 场景5：信息增益单调性——做完一次决定性实验后，剩余干预 EIG 应下降
    b_after = active_tr[-1]["posterior"] if active_tr else belief0
    # 归一化保险
    s = sum(b_after.values())
    b_after = {k: v / s for k, v in b_after.items()}
    eig_before = ranking[0][1]
    ranking_after = rank_interventions(hyps, b_after)
    eig_after = ranking_after[0][1]
    print(f"\n[5] 信息增益递减: 收敛前 top EIG={eig_before:.4f} → 收敛后 top EIG={eig_after:.4f}")
    cond5 = eig_after <= eig_before + 1e-9
    print(f"    实验后不确定性下降(EIG 不增): {'PASS' if cond5 else 'FAIL'}")
    ok &= cond5

    print("\n" + "=" * 60)
    print(f"selftest 总结: {'✅ ALL PASS' if ok else '❌ FAIL'}")
    print("=" * 60)
    return ok


def demo():
    hyps = build_standard_scenario()
    print("候选因果结构：")
    for h in hyps:
        print(f"  {h.name}: {h.edges}")
    print("\n真实世界=chain_XZY，启动主动实验设计辨识：\n")
    trace = active_experiment_loop(hyps, hyps[1])
    for t in trace:
        print(f"  step{t['step']}: {t['intervention']} "
              f"(EIG={t['eig']}) 观测={t['observation']} "
              f"→ 后验={t['posterior']} MAP={t['map']}")
    print(f"\n辨识结论：{trace[-1]['map']}（置信 {trace[-1]['map_prob']}），"
          f"共 {len(trace)} 次实验。")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="因果世界模型主动实验（最优实验设计/信息增益）")
    ap.add_argument("--selftest", action="store_true", help="运行自检")
    ap.add_argument("--demo", action="store_true", help="运行演示")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(0 if selftest() else 1)
    elif args.demo:
        demo()
    else:
        demo()
