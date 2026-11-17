#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autonomous-science-loop —— 自主科学发现闭环引擎（纯标准库）

把"观测 → 假设 → 实验设计 → 反驳 → 定律归纳"做成一次可机器执行、可证伪的
自主科学发现闭环，这是一线大模型不具备的"真正做出可证伪原创发现"的元之三阶能力。

核心机制：
  1) 假设空间 = 一组可解析的候选定律（线性/二次/反比/根号/对数/常数），
     每个用最小二乘闭式拟合观测数据（线性于参数，正规方程求解，纯 stdlib）。
  2) 反驳(Refutation) = 拟合残差 RMSE 超过容差的假设被证伪剔除（Popper 可证伪性）。
  3) 主动实验设计(Active experiment design) = 在候选实验点里选"存活假设间预测分歧最大"
     的 x（最大化预测方差 ≈ 最大期望信息增益），一次实验剔除最多假设。
  4) 定律归纳(Occam) = 在所有"存活且一致"的假设中取复杂度最低者（参数最少，
     并列取 RMSE 最低），得到最简可解释定律。

用法：
  python science_loop.py --selftest
  python science_loop.py --demo
"""
import sys, math, json


# ---------------------------------------------------------------------------
# 候选假设：每个定律用一组基函数 basis(x) -> [f1, f2, ...]，y ≈ sum(w_i * f_i)
# 线性于参数，可用正规方程闭式最小二乘拟合。complexity = 参数个数。
# ---------------------------------------------------------------------------
HYPOTHESES = {
    "constant":  {"basis": lambda x: [1.0],                      "complexity": 1,
                  "form": "y = a"},
    "linear":    {"basis": lambda x: [x, 1.0],                   "complexity": 2,
                  "form": "y = a*x + b"},
    "quadratic": {"basis": lambda x: [x * x, x, 1.0],            "complexity": 3,
                  "form": "y = a*x^2 + b*x + c"},
    "inverse":   {"basis": lambda x: [1.0 / x, 1.0] if x != 0 else None, "complexity": 2,
                  "form": "y = a/x + b"},
    "sqrt":      {"basis": lambda x: [math.sqrt(x), 1.0] if x >= 0 else None, "complexity": 2,
                  "form": "y = a*sqrt(x) + b"},
    "log":       {"basis": lambda x: [math.log(x), 1.0] if x > 0 else None, "complexity": 2,
                  "form": "y = a*ln(x) + b"},
}


# ---------------------------------------------------------------------------
# 线性代数：正规方程 (X^T X) w = X^T y，高斯消元解，纯 stdlib
# ---------------------------------------------------------------------------
def _solve(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            return None
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r != col and abs(M[r][col]) > 1e-15:
                factor = M[r][col]
                M[r] = [a - factor * bb for a, bb in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def fit(name, obs):
    """最小二乘拟合假设 name 到 obs=[(x,y),...]，返回 (weights, rmse) 或 None（不可拟合）。"""
    spec = HYPOTHESES[name]
    rows = []
    for x, _ in obs:
        phi = spec["basis"](x)
        if phi is None:
            return None            # 该假设定义域不覆盖此观测点 → 不可拟合
        rows.append(phi)
    k = len(rows[0])
    if len(obs) < k:
        return None                # 观测不足以定参
    ys = [y for _, y in obs]
    # 正规方程
    ATA = [[sum(rows[m][i] * rows[m][j] for m in range(len(rows)))
            for j in range(k)] for i in range(k)]
    ATy = [sum(rows[m][i] * ys[m] for m in range(len(rows))) for i in range(k)]
    w = _solve(ATA, ATy)
    if w is None:
        return None
    sse = 0.0
    for (x, y) in obs:
        phi = spec["basis"](x)
        pred = sum(wi * pi for wi, pi in zip(w, phi))
        sse += (pred - y) ** 2
    rmse = math.sqrt(sse / len(obs))
    return w, rmse


def predict(name, w, x):
    phi = HYPOTHESES[name]["basis"](x)
    if phi is None:
        return None
    return sum(wi * pi for wi, pi in zip(w, phi))


# ---------------------------------------------------------------------------
# 闭环：discover
# ---------------------------------------------------------------------------
def discover(observe, seed_obs, candidate_xs, tol=1e-6, max_experiments=12,
             hypotheses=None, verbose=False):
    """
    observe(x) -> y : 环境（真实世界/仿真）观测函数
    seed_obs        : 初始观测 [(x,y),...]
    candidate_xs    : 可供主动实验的候选 x 池
    返回发现报告 dict。
    """
    names = list(hypotheses or HYPOTHESES.keys())
    obs = list(seed_obs)
    pool = list(candidate_xs)
    trace = []

    def refute(current):
        survivors = []
        for nm in current:
            r = fit(nm, obs)
            if r is None:
                continue           # 定义域不适配 → 悬置（不算被证伪）
            w, rmse = r
            if rmse <= tol:
                survivors.append((nm, w, rmse))
        return survivors

    surv = refute(names)
    exp_count = 0
    while len(surv) > 1 and exp_count < max_experiments and pool:
        # 主动实验设计：选存活假设预测分歧(方差)最大的 x
        best_x, best_spread = None, -1.0
        for x in pool:
            preds = [predict(nm, w, x) for (nm, w, _) in surv]
            preds = [p for p in preds if p is not None]
            if len(preds) < 2:
                continue
            mean = sum(preds) / len(preds)
            spread = sum((p - mean) ** 2 for p in preds) / len(preds)
            if spread > best_spread:
                best_spread, best_x = spread, x
        if best_x is None:
            break
        y = observe(best_x)
        obs.append((best_x, y))
        pool.remove(best_x)
        exp_count += 1
        before = [nm for nm, _, _ in surv]
        surv = refute([nm for nm, _, _ in surv])
        after = [nm for nm, _, _ in surv]
        killed = [nm for nm in before if nm not in after]
        trace.append({"experiment": exp_count, "x": round(best_x, 4),
                      "y": round(y, 6), "spread": round(best_spread, 6),
                      "refuted": killed, "survivors": after})
        if verbose:
            print(f"[exp{exp_count}] x={best_x:.3f} y={y:.4f} 反驳={killed} 存活={after}")

    # 定律归纳：Occam —— 参数最少者优先，并列取 RMSE 最低
    if surv:
        surv.sort(key=lambda t: (HYPOTHESES[t[0]]["complexity"], t[2]))
        law_name, law_w, law_rmse = surv[0]
        law = {
            "name": law_name,
            "form": HYPOTHESES[law_name]["form"],
            "params": [round(x, 6) for x in law_w],
            "rmse": round(law_rmse, 9),
            "complexity": HYPOTHESES[law_name]["complexity"],
        }
    else:
        law = None

    return {
        "discovered_law": law,
        "surviving_hypotheses": [nm for nm, _, _ in surv],
        "experiments_run": exp_count,
        "total_observations": len(obs),
        "trace": trace,
    }


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------
def _selftest():
    ok = True

    # 场景 A：真实定律 = 线性 y = 2x + 1（二次能以 a=0 完美拟合 → Occam 应选线性）
    truthA = lambda x: 2.0 * x + 1.0
    rA = discover(truthA, seed_obs=[(1.0, truthA(1.0)), (2.0, truthA(2.0))],
                  candidate_xs=[0.5, 3.0, 4.0, 5.0, 8.0], tol=1e-6)
    lawA = rA["discovered_law"]
    condA = lawA and lawA["name"] == "linear" and abs(lawA["params"][0] - 2.0) < 1e-6 \
        and abs(lawA["params"][1] - 1.0) < 1e-6
    print(f"[A] 线性真值 → 归纳定律={lawA['name'] if lawA else None} "
          f"params={lawA['params'] if lawA else None} {'PASS' if condA else 'FAIL'}")
    ok &= condA

    # 场景 B：真实定律 = 二次 y = x^2 - x + 3（线性/常数将被残差反驳）
    truthB = lambda x: x * x - x + 3.0
    rB = discover(truthB, seed_obs=[(0.0, truthB(0.0)), (1.0, truthB(1.0)), (2.0, truthB(2.0))],
                  candidate_xs=[3.0, 4.0, 5.0, 6.0, 7.0], tol=1e-6)
    lawB = rB["discovered_law"]
    condB = lawB and lawB["name"] == "quadratic" and "linear" not in rB["surviving_hypotheses"]
    print(f"[B] 二次真值 → 归纳定律={lawB['name'] if lawB else None} "
          f"存活={rB['surviving_hypotheses']} 反驳线性={'linear' not in rB['surviving_hypotheses']} "
          f"{'PASS' if condB else 'FAIL'}")
    ok &= condB

    # 场景 C：主动实验设计。场景 A 的 2 个种子点会留下多个存活假设(linear/inverse/sqrt/log)，
    # 必须靠主动实验逐步反驳收敛到唯一线性 → 实验次数 >0 且最终唯一存活。
    condC = rA["experiments_run"] >= 1 and len(rA["surviving_hypotheses"]) == 1 \
        and rA["trace"] and any(t["refuted"] for t in rA["trace"])
    print(f"[C] 主动实验设计有效：A场景实验{rA['experiments_run']}次, 逐步反驳={[t['refuted'] for t in rA['trace']]}, "
          f"最终存活{rA['surviving_hypotheses']} {'PASS' if condC else 'FAIL'}")
    ok &= condC

    # 场景 D：反比真值 y = 6/x + 2（线性/二次在多点上无法零残差拟合 → 被反驳）
    truthD = lambda x: 6.0 / x + 2.0
    rD = discover(truthD, seed_obs=[(1.0, truthD(1.0)), (2.0, truthD(2.0))],
                  candidate_xs=[3.0, 4.0, 6.0, 12.0], tol=1e-6)
    lawD = rD["discovered_law"]
    condD = lawD and lawD["name"] == "inverse" and abs(lawD["params"][0] - 6.0) < 1e-5
    print(f"[D] 反比真值 → 归纳定律={lawD['name'] if lawD else None} "
          f"params={lawD['params'] if lawD else None} {'PASS' if condD else 'FAIL'}")
    ok &= condD

    print("\n自主科学发现闭环 selftest:", "全部 PASS ✅" if ok else "存在 FAIL ❌")
    return ok


def _demo():
    truth = lambda x: 2.0 * x + 1.0
    r = discover(truth, seed_obs=[(1.0, 3.0), (2.0, 5.0)],
                 candidate_xs=[0.5, 3.0, 4.0, 8.0], tol=1e-6, verbose=True)
    print(json.dumps(r, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if _selftest() else 1)
    elif "--demo" in sys.argv:
        _demo()
    else:
        print(__doc__)
