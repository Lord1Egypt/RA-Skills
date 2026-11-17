#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mult_alloc.py — 图形化多重性 α 分配（Maurer-Bretz / Bretz et al. 2009）

纯标准库实现，不引入 numpy，不注册为 ComputeBackend，不改动
scripts/compute_backend.py 的 select_backend 单后端路由。本模块只做
「多重终点的 α 分配 / 逐步回收」，不做样本量计算，不触碰数值真相源。

核心 API：
  - parse_graph(hypotheses, alpha_weights, transitions) -> dict
  - graphical_test(graph, alpha=0.05, pvalues=None, tol=1e-12) -> dict

参考：
  Bretz, Maurer, Brannath, Posch (2009). "A graphical approach to
  sequentially rejective multiple test procedures." Stat Med 28:585-602.
"""

import argparse
import json
import sys


def parse_graph(hypotheses, alpha_weights, transitions):
    """构造并校验加权图（转移矩阵）。

    Parameters
    ----------
    hypotheses : list[str]
        假设节点 id 列表，顺序即矩阵行/列顺序。
    alpha_weights : dict[str, float] | list[float]
        每个假设的初始权重 w_i（行和应为 1）。
    transitions : dict[str, dict[str, float]] | list[list[float]]
        转移矩阵 G：g_ij 表示被拒假设 i 的权重中有多少比例转给 j。
        g_ii 必须为 0，每行和为 1，0 <= g_ij <= 1。

    Returns
    -------
    dict with keys: nodes, weights, G, n
    """
    nodes = list(hypotheses)
    n = len(nodes)
    if n == 0:
        raise ValueError("hypotheses 不能为空")
    if len(set(nodes)) != n:
        raise ValueError("hypotheses 含重复 id：%s" % nodes)

    # ── 归一化权重 ──
    if isinstance(alpha_weights, dict):
        weights = [float(alpha_weights[h]) for h in nodes]
    else:
        weights = [float(x) for x in alpha_weights]
    if len(weights) != n:
        raise ValueError("alpha_weights 长度(%d)与 hypotheses 长度(%d)不一致" % (len(weights), n))
    wsum = sum(weights)
    if abs(wsum - 1.0) > 1e-9:
        raise ValueError("alpha_weights 之和必须为 1，实际为 %.10f" % wsum)
    for w in weights:
        if w < -1e-12 or w > 1 + 1e-12:
            raise ValueError("权重越界：%r" % w)

    # ── 归一化转移矩阵 ──
    if isinstance(transitions, dict):
        G = [[0.0] * n for _ in range(n)]
        for i, hi in enumerate(nodes):
            row = transitions.get(hi, {})
            for j, hj in enumerate(nodes):
                G[i][j] = float(row.get(hj, 0.0))
    else:
        G = [[float(x) for x in row] for row in transitions]
    if len(G) != n or any(len(r) != n for r in G):
        raise ValueError("transitions 必须是 %dx%d 方阵" % (n, n))

    for i in range(n):
        if abs(G[i][i]) > 1e-12:
            raise ValueError("转移矩阵对角线 g_%d%d 必须为 0（权重不可转给自己）" % (i + 1, i + 1))
        rowsum = sum(G[i])
        if abs(rowsum - 1.0) > 1e-9:
            raise ValueError("转移矩阵第 %d 行之和必须为 1，实际为 %.10f" % (i + 1, rowsum))
        for j in range(n):
            if G[i][j] < -1e-12 or G[i][j] > 1 + 1e-12:
                raise ValueError("转移矩阵元素 g_%d%d=%.6f 越界[0,1]" % (i + 1, j + 1, G[i][j]))

    return {"nodes": nodes, "weights": weights, "G": G, "n": n}


def graphical_test(graph, alpha=0.05, pvalues=None, tol=1e-12):
    """执行图形化逐步拒绝 / 或仅返回初始 α 分配。

    Parameters
    ----------
    graph : dict
        parse_graph 的产出。
    alpha : float
        总体 family-wise error rate（默认 0.05）。
    pvalues : dict[str, float] | None
        各假设 p 值。为 None 时只返回初始 α 分配（不做逐步拒绝）。
    tol : float
        数值容差。

    Returns
    -------
    dict:
      - alpha (总体)
      - initial_alpha: {node: 初始局部 α}
      - rejected: [node, ...]（仅当给定 pvalues）
      - local_alpha_final: {node: 最终局部 α}（仅当给定 pvalues）
      - stopped_at: 首次无法继续拒绝的节点（调试用）
      - note
    """
    nodes = graph["nodes"]
    weights = graph["weights"]
    G = graph["G"]
    n = graph["n"]

    if not (0 < alpha < 1):
        raise ValueError("alpha 必须落在 (0,1)，实际 %r" % alpha)

    # 初始局部 α
    local = [alpha * w for w in weights]
    initial_alpha = {nodes[i]: local[i] for i in range(n)}

    if pvalues is None:
        return {
            "alpha": alpha,
            "initial_alpha": initial_alpha,
            "rejected": [],
            "local_alpha_final": {},
            "stopped_at": None,
            "note": "未提供 pvalues，仅返回初始 α 分配（各终点边际 α = alpha * w_i）。"
        }

    if not isinstance(pvalues, dict):
        raise ValueError("pvalues 必须是 {node: p} 字典")
    pv = []
    for h in nodes:
        if h not in pvalues:
            raise ValueError("pvalues 缺假设 %s" % h)
        v = float(pvalues[h])
        if not (0.0 <= v <= 1.0):
            raise ValueError("pvalue(%s)=%r 越界[0,1]" % (h, v))
        pv.append(v)

    rejected = [False] * n
    order = []
    stopped_at = None

    while True:
        # 在尚未拒绝的集合里找 p_i <= local_i
        candidate = -1
        for i in range(n):
            if rejected[i]:
                continue
            if pv[i] <= local[i] + tol:
                candidate = i
                break
        if candidate == -1:
            # 没有可拒绝的，停止
            for i in range(n):
                if not rejected[i]:
                    stopped_at = nodes[i]
                    break
            break
        # 拒绝 candidate
        rejected[candidate] = True
        order.append(nodes[candidate])
        freed = local[candidate]
        local[candidate] = 0.0
        # 把 freed 权重按转移矩阵分发给其余未拒绝节点
        for j in range(n):
            if rejected[j]:
                continue
            local[j] += freed * G[candidate][j]

    rejected_nodes = list(order)  # 按实际逐步拒绝顺序，而非节点序
    local_final = {nodes[i]: local[i] for i in range(n)}

    return {
        "alpha": alpha,
        "initial_alpha": initial_alpha,
        "rejected": rejected_nodes,
        "reject_order": order,
        "local_alpha_final": local_final,
        "stopped_at": stopped_at,
        "note": "逐步拒绝完成。"
    }


def _main():
    ap = argparse.ArgumentParser(description="图形化多重性 α 分配（Maurer-Bretz）")
    ap.add_argument("--graph-json", required=True,
                    help="图定义 JSON 文件：{hypotheses:[...], weights:{...}|[...], transitions:{...}|[[...]]}")
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--pvalues-json", default=None,
                    help="可选，p 值 JSON 文件：{H1:0.01, H2:0.04, ...}。不给则只输出初始 α 分配")
    ap.add_argument("--out", default=None, help="输出 JSON 路径")
    args = ap.parse_args()

    with open(args.graph_json, "r", encoding="utf-8") as f:
        gdef = json.load(f)
    graph = parse_graph(gdef["hypotheses"], gdef["weights"], gdef["transitions"])

    pvalues = None
    if args.pvalues_json:
        with open(args.pvalues_json, "r", encoding="utf-8") as f:
            pvalues = json.load(f)

    result = graphical_test(graph, alpha=args.alpha, pvalues=pvalues)

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(_main())
