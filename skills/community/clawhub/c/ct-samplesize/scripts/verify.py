#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify.py / 本地模拟验证闭环（power / TIE / events）— ct-samplesize P1-C

WHY / 动机
----------
样本量的解析解（pwr / gsDesign / rpact / coze 端点）一旦参数或公式用错，结果
"看起来仍然合理"，肉眼与单元测试都很难发现。本模块用**纯本地 Monte-Carlo**
把解析解**回代**到数据生成过程里，检验它实际达到的操作特性：

  - empirical power  vs 名义 power   —— 容差 ±2 pp
  - empirical TIE    vs 名义 alpha   —— 容差 ±0.5 pp
  - expected events  vs 解析事件数   —— 容差 ±5 %（生存设计）

独立性原则 / independence
-------------------------
验证器**不复用**被验证对象的样本量公式——否则同源错误会互相掩盖、验证退化为
自证。本模块只接收「解析解给出的 n（以及组序贯的检验边界）」作为**输入**，
其余（数据生成、检验统计量、判定）全部独立实现。因此：

  - 固定设计：n 来自 pwr/coze，本模块独立生成数据并做 t / z 检验。
  - 组序贯：**推荐传入 `--boundaries`**（rpact / gsDesign 输出的 z 边界），
    本模块独立模拟其真实 power 与 TIE。未传时会用内置 Lan-DeMets 递归积分
    自算边界，此时结果标注 `self_derived_boundaries`——只算 sanity check，
    **不构成独立验证**。

诚实性 / honesty
----------------
Monte-Carlo 自身有抽样误差。每项结果都同时给出经验值的 95% MC 置信区间；
若 MC 误差已接近或超过判定容差，会显式告警「nsim 不足，结论不可判」，
而不是给出一个看似确定的 PASS / FAIL。

依赖 / dependencies
-------------------
标准库即可运行（`statistics.NormalDist` 提供正态分位数）。若本机存在
numpy / scipy 则自动用于向量化与精确 t 分位数（更快更准），但**不是硬依赖**。
零联网、零患者数据。

用法 / usage
------------
    # 固定设计：pwr 给出每组 n=64（d=0.5, alpha=0.05, power=0.8）
    python scripts/verify.py --design ttest_ind --n 64 --effect_size 0.5

    # 两比例
    python scripts/verify.py --design proportion_two --n 100 --p1 0.6 --p2 0.4

    # 组序贯（独立验证：边界来自 rpact / gsDesign）
    python scripts/verify.py --design group_sequential --n 120 --effect_size 0.3 \
        --looks 2 --boundaries 2.797,1.977

    # 生存（log-rank）：同时校验 power 与期望事件数
    python scripts/verify.py --design survival --n 200 --hazard_ratio 0.6 \
        --median_control 12 --accrual 12 --followup 12 --expected_events 190

    # 适应性样本量再估计（promising zone）：重点看 TIE 是否被膨胀
    python scripts/verify.py --design adaptive_reestimate --n 100 --effect_size 0.3 \
        --interim_fraction 0.5 --target_cp 0.9 --max_inflation 2.0
"""
import argparse
import hashlib
import json
import math
import os
import random
import sys
import tempfile
import time
from statistics import NormalDist

_ND = NormalDist()

try:  # optional: vectorized simulation
    import numpy as _np
except Exception:  # pragma: no cover
    _np = None

try:  # optional: exact Student-t quantiles
    from scipy import stats as _sps
except Exception:  # pragma: no cover
    _sps = None

# Tolerances mandated by ct-update P1-C
TOL_POWER_PP = 2.0      # percentage points
TOL_TIE_PP = 0.5        # percentage points
TOL_EVENTS_REL = 0.05   # relative
NSIM_HARD_CAP = 500000  # guard against accidental multi-hour runs


# ─────────────────────────── distribution helpers ───────────────────────────
def _z(p):
    return _ND.inv_cdf(p)


def _t_ppf(p, df):
    """Student-t quantile. Exact via scipy when available, else the
    Abramowitz & Stegun 26.7.5 expansion (error < 1e-4 for df >= 10)."""
    if _sps is not None:
        return float(_sps.t.ppf(p, df))
    z = _z(p)
    z2, z3, z5, z7 = z * z, z ** 3, z ** 5, z ** 7
    g1 = (z3 + z) / 4.0
    g2 = (5 * z5 + 16 * z3 + 3 * z) / 96.0
    g3 = (3 * z7 + 19 * z5 + 17 * z3 - 15 * z) / 384.0
    return z + g1 / df + g2 / df ** 2 + g3 / df ** 3


def _mc_ci(k, n):
    """Wilson-free simple 95% MC CI for a proportion (k successes of n)."""
    if n <= 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    se = math.sqrt(max(p * (1 - p), 1e-12) / n)
    return (p, max(0.0, p - 1.96 * se), min(1.0, p + 1.96 * se))


# ─────────────────────── Lan-DeMets spending & boundaries ───────────────────
def _spend(t, alpha, kind):
    """Cumulative alpha spent by information fraction t (one-sided)."""
    t = min(max(t, 1e-9), 1.0)
    if kind == "pocock":
        return alpha * math.log(1.0 + (math.e - 1.0) * t)
    # O'Brien-Fleming (Lan-DeMets approximation)
    return 2.0 * (1.0 - _ND.cdf(_z(1.0 - alpha / 2.0) / math.sqrt(t)))


def _gs_boundaries(looks, alpha, kind, grid=801, span=8.0):
    """Solve sequential z boundaries by Armitage-McPherson recursive numerical
    integration over the Brownian-motion increments (one-sided, equal spacing).

    Independent of gsDesign/rpact -- used ONLY when the caller does not supply
    boundaries, and the result is then flagged as non-independent.
    """
    fracs = [(i + 1) / looks for i in range(looks)]
    bounds = []
    xs = [(-span + 2 * span * i / (grid - 1)) for i in range(grid)]
    h = xs[1] - xs[0]
    dens = None  # sub-density of the continuation region, on the B-scale
    prev_t = 0.0
    for k, t in enumerate(fracs):
        dt = t - prev_t
        sd = math.sqrt(dt)
        target = _spend(t, alpha, kind) - (_spend(prev_t, alpha, kind) if k else 0.0)
        target = max(target, 1e-12)

        if dens is None:
            def tail(b):
                return 1.0 - _ND.cdf(b / sd)
        else:
            def tail(b, _dens=dens, _sd=sd, _h=h, _xs=xs):
                s = 0.0
                for i, x in enumerate(_xs):
                    d = _dens[i]
                    if d <= 0.0:
                        continue
                    s += d * (1.0 - _ND.cdf((b - x) / _sd)) * _h
                return s

        lo, hi = 0.0, 12.0
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if tail(mid) > target:
                lo = mid
            else:
                hi = mid
        b = 0.5 * (lo + hi)
        bounds.append(b / math.sqrt(t))  # B-scale -> z-scale

        # propagate the continuation sub-density to the next look
        new = []
        for x in xs:
            if dens is None:
                v = _ND.pdf(x / sd) / sd if x < b else 0.0
            else:
                if x >= b:
                    v = 0.0
                else:
                    s = 0.0
                    for i, y in enumerate(xs):
                        d = dens[i]
                        if d <= 0.0:
                            continue
                        s += d * (_ND.pdf((x - y) / sd) / sd) * h
                    v = s
            new.append(v)
        dens = new
        prev_t = t
    return bounds


# ───────────────────────────── simulators ───────────────────────────────────
def _sim_fixed(design, n, alpha, side, params, nsim, delta_scale, rng, seed):
    """Fixed-design simulation. delta_scale=1 -> H1, 0 -> H0 (for TIE)."""
    d = float(params.get("effect_size") or 0.0) * delta_scale
    p1 = params.get("p1")
    p2 = params.get("p2")
    crit_p = 1.0 - (alpha / 2.0 if side == "two" else alpha)
    rej = 0

    if design in ("ttest_ind", "ttest_one", "ttest_paired"):
        if design == "ttest_ind":
            df = 2 * n - 2
            tcrit = _t_ppf(crit_p, df)
            if _np is not None:
                r = _np.random.default_rng(seed)
                for _ in range(0, nsim, 2000):
                    b = min(2000, nsim - _)
                    x = r.normal(d, 1.0, (b, n))
                    y = r.normal(0.0, 1.0, (b, n))
                    mx, my = x.mean(1), y.mean(1)
                    vx, vy = x.var(1, ddof=1), y.var(1, ddof=1)
                    sp = _np.sqrt(((n - 1) * vx + (n - 1) * vy) / df)
                    tstat = (mx - my) / (sp * math.sqrt(2.0 / n))
                    rej += int((_np.abs(tstat) > tcrit).sum()) if side == "two" \
                        else int((tstat > tcrit).sum())
            else:
                for _ in range(nsim):
                    x = [rng.gauss(d, 1.0) for _ in range(n)]
                    y = [rng.gauss(0.0, 1.0) for _ in range(n)]
                    mx, my = sum(x) / n, sum(y) / n
                    vx = sum((v - mx) ** 2 for v in x) / (n - 1)
                    vy = sum((v - my) ** 2 for v in y) / (n - 1)
                    sp = math.sqrt(((n - 1) * vx + (n - 1) * vy) / df)
                    tstat = (mx - my) / (sp * math.sqrt(2.0 / n))
                    if (abs(tstat) > tcrit) if side == "two" else (tstat > tcrit):
                        rej += 1
        else:  # one-sample / paired reduce to the same one-sample problem
            df = n - 1
            tcrit = _t_ppf(crit_p, df)
            if _np is not None:
                r = _np.random.default_rng(seed)
                for _ in range(0, nsim, 2000):
                    b = min(2000, nsim - _)
                    x = r.normal(d, 1.0, (b, n))
                    tstat = x.mean(1) / (x.std(1, ddof=1) / math.sqrt(n))
                    rej += int((_np.abs(tstat) > tcrit).sum()) if side == "two" \
                        else int((tstat > tcrit).sum())
            else:
                for _ in range(nsim):
                    x = [rng.gauss(d, 1.0) for _ in range(n)]
                    m = sum(x) / n
                    v = sum((q - m) ** 2 for q in x) / (n - 1)
                    tstat = m / (math.sqrt(v) / math.sqrt(n))
                    if (abs(tstat) > tcrit) if side == "two" else (tstat > tcrit):
                        rej += 1

    elif design == "proportion_two":
        if p1 is None or p2 is None:
            raise SystemExit("proportion_two 需要 --p1 与 --p2")
        pa = p1 if delta_scale else p2   # H0: both arms at p2
        zc = _z(crit_p)
        if _np is not None:
            r = _np.random.default_rng(seed)
            for _ in range(0, nsim, 20000):
                b = min(20000, nsim - _)
                x1 = r.binomial(n, pa, b)
                x2 = r.binomial(n, p2, b)
                ph1, ph2 = x1 / n, x2 / n
                pp = (x1 + x2) / (2.0 * n)
                se = _np.sqrt(_np.maximum(pp * (1 - pp) * 2.0 / n, 1e-12))
                zs = (ph1 - ph2) / se
                rej += int((_np.abs(zs) > zc).sum()) if side == "two" \
                    else int((zs > zc).sum())
        else:
            for _ in range(nsim):
                x1 = sum(1 for _ in range(n) if rng.random() < pa)
                x2 = sum(1 for _ in range(n) if rng.random() < p2)
                ph1, ph2 = x1 / n, x2 / n
                pp = (x1 + x2) / (2.0 * n)
                se = math.sqrt(max(pp * (1 - pp) * 2.0 / n, 1e-12))
                zs = (ph1 - ph2) / se
                if (abs(zs) > zc) if side == "two" else (zs > zc):
                    rej += 1
    else:
        raise SystemExit("unsupported fixed design: %s" % design)
    return rej


def _logrank_once(n_per_arm, lam1, lam2, accrual, followup, r):
    """One log-rank replication with uniform accrual + administrative censoring.
    Returns (z_statistic, n_events)."""
    tot = accrual + followup
    if _np is not None:
        t1 = r.exponential(1.0 / lam1, n_per_arm)
        t2 = r.exponential(1.0 / lam2, n_per_arm)
        e1 = r.uniform(0.0, accrual, n_per_arm) if accrual > 0 else _np.zeros(n_per_arm)
        e2 = r.uniform(0.0, accrual, n_per_arm) if accrual > 0 else _np.zeros(n_per_arm)
        c1, c2 = tot - e1, tot - e2
        o1 = _np.minimum(t1, c1)
        o2 = _np.minimum(t2, c2)
        d1 = (t1 <= c1)
        d2 = (t2 <= c2)
        obs = _np.concatenate([o1, o2])
        ev = _np.concatenate([d1, d2])
        grp = _np.concatenate([_np.ones(n_per_arm, dtype=int),
                               _np.zeros(n_per_arm, dtype=int)])
        order = _np.argsort(obs, kind="mergesort")
        obs, ev, grp = obs[order], ev[order], grp[order]
        N = obs.size
        at_risk1 = _np.concatenate([[grp.sum()], grp.sum() - _np.cumsum(grp)[:-1]])
        at_risk = _np.arange(N, 0, -1)
        O_E, V = 0.0, 0.0
        idx = _np.nonzero(ev)[0]
        for i in idx:                     # ties are rare with continuous times
            nr, nr1 = at_risk[i], at_risk1[i]
            if nr <= 1:
                continue
            e = nr1 / nr
            O_E += (1.0 if grp[i] == 1 else 0.0) - e
            V += e * (1.0 - e)
        nev = int(ev.sum())
    else:
        rows = []
        for g, lam in ((1, lam1), (0, lam2)):
            for _ in range(n_per_arm):
                t = r.expovariate(lam)
                entry = r.uniform(0.0, accrual) if accrual > 0 else 0.0
                c = tot - entry
                rows.append((min(t, c), 1 if t <= c else 0, g))
        rows.sort(key=lambda q: q[0])
        N = len(rows)
        nr1 = sum(1 for q in rows if q[2] == 1)
        O_E, V, nev = 0.0, 0.0, 0
        for i, (_tm, dd, g) in enumerate(rows):
            nr = N - i
            if dd:
                nev += 1
                if nr > 1:
                    e = nr1 / nr
                    O_E += (1.0 if g == 1 else 0.0) - e
                    V += e * (1.0 - e)
            if g == 1:
                nr1 -= 1
    zst = O_E / math.sqrt(V) if V > 0 else 0.0
    return zst, nev


def _sim_survival(n, alpha, side, params, nsim, under_h0, seed):
    med = float(params.get("median_control") or 12.0)
    hr = 1.0 if under_h0 else float(params.get("hazard_ratio") or 0.6)
    lam2 = math.log(2.0) / med
    lam1 = lam2 * hr
    accrual = float(params.get("accrual") or 0.0)
    followup = float(params.get("followup") or 12.0)
    zc = _z(1.0 - (alpha / 2.0 if side == "two" else alpha))
    r = _np.random.default_rng(seed) if _np is not None else random.Random(seed)
    rej, ev_tot = 0, 0
    for _ in range(nsim):
        zst, nev = _logrank_once(n, lam1, lam2, accrual, followup, r)
        ev_tot += nev
        if (abs(zst) > zc) if side == "two" else (zst < -zc):
            rej += 1
    return rej, ev_tot / float(nsim)


def _sim_group_sequential(n, alpha, params, bounds, nsim, under_h0, seed):
    """Continuous endpoint, equally spaced looks, one-sided efficacy stops.
    Uses the canonical joint distribution of sequential z statistics."""
    looks = len(bounds)
    d = 0.0 if under_h0 else float(params.get("effect_size") or 0.3)
    # information at look k: n_k per arm -> z drift = d / sqrt(2/n_k)
    r = _np.random.default_rng(seed) if _np is not None else random.Random(seed)
    rej, stop_at = 0, [0] * looks
    per = [int(round(n * (k + 1) / looks)) for k in range(looks)]
    incr_info = []
    prev = 0.0
    for k in range(looks):
        info = per[k] / 2.0            # Fisher information (unit variance)
        incr_info.append(info - prev)
        prev = info
    for _ in range(nsim):
        b = 0.0                        # Brownian score
        info = 0.0
        for k in range(looks):
            di = incr_info[k]
            step = (r.normal(0.0, 1.0) if _np is not None else r.gauss(0.0, 1.0)) \
                * math.sqrt(di) + d * di
            b += step
            info += di
            zk = b / math.sqrt(info)
            if zk > bounds[k]:
                rej += 1
                stop_at[k] += 1
                break
    return rej, stop_at


def _sim_adaptive_ssr(n, alpha, params, nsim, under_h0, seed):
    """Promising-zone sample-size re-estimation (Mehta-Pocock style), tested
    with the naive (unadjusted) final z. TIE inflation here is the whole point:
    if the analytic design claims TIE control, this simulation must confirm it.
    """
    d = 0.0 if under_h0 else float(params.get("effect_size") or 0.3)
    frac = float(params.get("interim_fraction") or 0.5)
    target_cp = float(params.get("target_cp") or 0.9)
    infl = float(params.get("max_inflation") or 2.0)
    zc = _z(1.0 - alpha)               # one-sided final test
    n1 = max(2, int(round(n * frac)))
    r = _np.random.default_rng(seed) if _np is not None else random.Random(seed)
    rej, resized = 0, 0
    for _ in range(nsim):
        g = (lambda: r.normal(0.0, 1.0)) if _np is not None else (lambda: r.gauss(0.0, 1.0))
        i1 = n1 / 2.0
        b1 = g() * math.sqrt(i1) + d * i1
        z1 = b1 / math.sqrt(i1)
        dhat = b1 / i1
        n2 = n - n1
        cp = 1.0 - _ND.cdf((zc * math.sqrt(n / 2.0) - dhat * (n / 2.0))
                           / math.sqrt(max(n2 / 2.0, 1e-9)))
        if 0.3 <= cp < target_cp:      # promising zone -> inflate stage 2
            need = ((zc + _z(target_cp)) / max(dhat, 1e-6)) ** 2 * 2.0 - n1
            n2 = int(min(max(n2, need), n * infl - n1))
            resized += 1
        i2 = max(n2, 1) / 2.0
        b2 = g() * math.sqrt(i2) + d * i2
        ztot = (b1 + b2) / math.sqrt(i1 + i2)
        if ztot > zc:
            rej += 1
    return rej, resized


# ───────────────────────────── verdict assembly ─────────────────────────────
def _verdict(label, emp, k, nsim, target, tol_pp, direction="two"):
    """Assemble a single check.

    direction="two"   -> |empirical - target| must be within tolerance.
    direction="lower" -> empirical must not fall BELOW target - tolerance;
                         exceeding the target is acceptable by design
                         (e.g. promising-zone SSR is meant to raise power).
    direction="upper" -> empirical must not EXCEED target + tolerance
                         (e.g. type-I error must be controlled, not matched).
    """
    p, lo, hi = _mc_ci(k, nsim)
    diff_pp = (emp - target) * 100.0
    mc_halfwidth_pp = (hi - lo) / 2.0 * 100.0
    conclusive = mc_halfwidth_pp < tol_pp
    if direction == "lower":
        ok = diff_pp >= -tol_pp
    elif direction == "upper":
        ok = diff_pp <= tol_pp
    else:
        ok = abs(diff_pp) <= tol_pp

    diag = ""
    if not ok:
        if label == "power" and diff_pp < 0:
            diag = ("经验功效低于名义值 → n 不足或解析公式/参数有误 "
                    "(underpowered: n too small or wrong formula/params)")
        elif label == "power" and diff_pp > 0:
            diag = ("经验功效高于名义值 → 设计过保守、n 传错，或该设计本就以"
                    "抬升功效为目的（此时应按 direction=lower 判定）"
                    " (overpowered: conservative design / mismatched n)")
        elif label == "type_I_error":
            diag = ("I 类错误未受控 → 检验统计量/边界/多重性校正需修正，"
                    "加大 n 无法解决 (TIE not controlled: fix the test, not n)")
    return {
        "metric": label,
        "empirical": round(emp, 5),
        "target": round(target, 5),
        "diff_pp": round(diff_pp, 3),
        "tolerance_pp": tol_pp,
        "direction": direction,
        "mc_ci95": [round(lo, 5), round(hi, 5)],
        "mc_halfwidth_pp": round(mc_halfwidth_pp, 3),
        "conclusive": conclusive,
        "verdict": ("PASS" if ok else "FAIL") if conclusive else "INCONCLUSIVE",
        "diagnosis": diag,
    }


def _cache_path(fp):
    return os.path.join(tempfile.gettempdir(), "ct_ss_verify_%s.json" % fp)


def run_verify(design, n, alpha=0.05, power=0.8, side="two", nsim=20000,
               seed=20260829, params=None, boundaries=None, looks=1,
               spending="obrien_fleming", expected_events=None,
               check_tie=True, use_cache=True):
    """Run the verification and return a structured report dict."""
    params = dict(params or {})
    if nsim > NSIM_HARD_CAP:
        raise SystemExit("--verify-nsim 超过硬上限 %d" % NSIM_HARD_CAP)
    # R 端求解的 n 常为 float（64.0），range 不接受 float → 强转 int
    n = int(round(float(n)))
    fp_src = json.dumps({"d": design, "n": n, "a": alpha, "pw": power, "s": side,
                         "ns": nsim, "sd": seed, "p": params, "b": boundaries,
                         "lk": looks, "sp": spending, "ee": expected_events,
                         "tie": check_tie}, sort_keys=True)
    fp = hashlib.sha1(fp_src.encode("utf-8")).hexdigest()[:16]
    cp = _cache_path(fp)
    if use_cache and os.path.exists(cp):
        try:
            with open(cp, encoding="utf-8") as f:
                cached = json.load(f)
            cached["cached"] = True
            return cached
        except Exception:
            pass

    t0 = time.time()
    rng = random.Random(seed)
    rep = {
        "design": design, "n_per_arm": n, "alpha": alpha, "nominal_power": power,
        "side": side, "nsim": nsim, "seed": seed, "params": params,
        "engine": "numpy" if _np is not None else "pure-python",
        "t_quantile": "scipy(exact)" if _sps is not None else "AS-26.7.5(approx)",
        "checks": [], "notes": [], "cached": False,
    }

    if design in ("ttest_ind", "ttest_one", "ttest_paired", "proportion_two"):
        k = _sim_fixed(design, n, alpha, side, params, nsim, 1.0, rng, seed)
        rep["checks"].append(_verdict("power", k / nsim, k, nsim, power, TOL_POWER_PP))
        if check_tie:
            k0 = _sim_fixed(design, n, alpha, side, params, nsim, 0.0, rng, seed + 1)
            rep["checks"].append(_verdict("type_I_error", k0 / nsim, k0, nsim,
                                          alpha, TOL_TIE_PP))

    elif design == "survival":
        k, ev = _sim_survival(n, alpha, side, params, nsim, False, seed)
        rep["checks"].append(_verdict("power", k / nsim, k, nsim, power, TOL_POWER_PP))
        rep["empirical_events_mean"] = round(ev, 2)
        if expected_events:
            rel = abs(ev - expected_events) / float(expected_events)
            rep["checks"].append({
                "metric": "expected_events", "empirical": round(ev, 2),
                "target": expected_events, "rel_diff": round(rel, 4),
                "tolerance_rel": TOL_EVENTS_REL, "conclusive": True,
                "verdict": "PASS" if rel <= TOL_EVENTS_REL else "FAIL",
            })
        if check_tie:
            k0, _ = _sim_survival(n, alpha, side, params, nsim, True, seed + 1)
            rep["checks"].append(_verdict("type_I_error", k0 / nsim, k0, nsim,
                                          alpha, TOL_TIE_PP))

    elif design == "group_sequential":
        if boundaries:
            bnds = list(boundaries)
            rep["boundary_source"] = "supplied (independent verification)"
        else:
            bnds = _gs_boundaries(looks, alpha if side == "one" else alpha / 2.0,
                                  spending)
            rep["boundary_source"] = "self_derived_boundaries (NOT independent)"
            rep["notes"].append(
                "未提供 --boundaries，已用内置 Lan-DeMets 递归积分自算边界；"
                "此模式只作 sanity check，不构成对 gsDesign/rpact 结果的独立验证。"
                " / Boundaries were self-derived; this is a sanity check, NOT an "
                "independent verification of the analytic design.")
        rep["boundaries"] = [round(b, 4) for b in bnds]
        k, stops = _sim_group_sequential(n, alpha, params, bnds, nsim, False, seed)
        rep["checks"].append(_verdict("power", k / nsim, k, nsim, power, TOL_POWER_PP))
        rep["stop_distribution"] = [round(s / nsim, 4) for s in stops]
        if check_tie:
            k0, _ = _sim_group_sequential(n, alpha, params, bnds, nsim, True, seed + 1)
            tgt = alpha if side == "one" else alpha / 2.0
            rep["checks"].append(_verdict("type_I_error", k0 / nsim, k0, nsim,
                                          tgt, TOL_TIE_PP))

    elif design == "adaptive_reestimate":
        k, rs = _sim_adaptive_ssr(n, alpha, params, nsim, False, seed)
        # Promising-zone SSR is DESIGNED to raise power above the nominal value
        # when the interim looks promising, so "power exceeds target" is the
        # intended behaviour, not a defect -> one-sided (lower-bound) verdict.
        rep["checks"].append(_verdict("power", k / nsim, k, nsim, power,
                                      TOL_POWER_PP, direction="lower"))
        rep["resize_rate"] = round(rs / nsim, 4)
        if check_tie:
            k0, _ = _sim_adaptive_ssr(n, alpha, params, nsim, True, seed + 1)
            # TIE only needs to be CONTROLLED (<= alpha + tol), not matched.
            rep["checks"].append(_verdict("type_I_error", k0 / nsim, k0, nsim,
                                          alpha, TOL_TIE_PP, direction="upper"))
            rep["notes"].append(
                "SSR 的 TIE 用未调整的合并 z 检验评估——若此处 FAIL，说明该设计"
                "必须改用加权/条件误差函数检验，而非样本量算错。"
                " / SSR TIE is assessed with the naive pooled z; a FAIL means the "
                "design needs a weighted / conditional-error test, not a bigger n.")
    else:
        raise SystemExit("unsupported --design: %s" % design)

    verdicts = [c["verdict"] for c in rep["checks"]]
    rep["overall"] = ("FAIL" if "FAIL" in verdicts else
                      ("INCONCLUSIVE" if "INCONCLUSIVE" in verdicts else "PASS"))
    rep["elapsed_sec"] = round(time.time() - t0, 2)
    rep["limitation"] = (
        "模拟按理想数据生成过程（正态/二项/指数、无脱落、无分层、无缺失）；"
        "PASS 只说明解析解在该理想模型下自洽，不代表真实试验条件下成立。"
        " / Simulation assumes an idealised data-generating process (no dropout, "
        "no stratification, no missingness); PASS means the analytic solution is "
        "self-consistent under that model only.")
    for c in rep["checks"]:
        if c.get("conclusive") is False:
            rep["notes"].append(
                "MC 误差(±%.2f pp) ≥ 容差(±%.2f pp)：nsim=%d 不足以判定 %s，"
                "请提高 --verify-nsim。 / MC error exceeds tolerance; raise nsim."
                % (c["mc_halfwidth_pp"], c["tolerance_pp"], nsim, c["metric"]))
    if use_cache:
        try:
            with open(cp, "w", encoding="utf-8") as f:
                json.dump(rep, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    return rep


def format_report(rep, lang="zh"):
    L = []
    head = ("## 本地模拟验证 / Local simulation verification (P1-C)"
            if lang == "zh" else "## Local simulation verification (P1-C)")
    L.append(head)
    L.append("")
    L.append("- design: `%s` | n/组 per-arm: **%s** | alpha: %s | side: %s"
             % (rep["design"], rep["n_per_arm"], rep["alpha"], rep["side"]))
    L.append("- nsim: **%d** | seed: %s | engine: %s | t-quantile: %s%s"
             % (rep["nsim"], rep["seed"], rep["engine"], rep["t_quantile"],
                "（缓存命中 cached）" if rep.get("cached") else ""))
    if rep.get("boundary_source"):
        L.append("- boundaries: %s — %s" % (rep.get("boundaries"), rep["boundary_source"]))
    L.append("")
    L.append("| 指标 Metric | 经验值 Empirical | 目标 Target | 差 Diff | 容差 Tol | MC 95% CI | 判定 |")
    L.append("|---|---|---|---|---|---|---|")
    for c in rep["checks"]:
        if "rel_diff" in c:
            L.append("| %s | %s | %s | %+.2f%% | ±%.0f%% | — | **%s** |" % (
                c["metric"], c["empirical"], c["target"], c["rel_diff"] * 100,
                c["tolerance_rel"] * 100, c["verdict"]))
        else:
            L.append("| %s | %.4f | %.4f | %+.2f pp | ±%.1f pp | [%.4f, %.4f] | **%s** |" % (
                c["metric"], c["empirical"], c["target"], c["diff_pp"],
                c["tolerance_pp"], c["mc_ci95"][0], c["mc_ci95"][1], c["verdict"]))
    L.append("")
    L.append("- **总判定 Overall: %s** （耗时 %.2fs）" % (rep["overall"], rep["elapsed_sec"]))
    if rep.get("stop_distribution"):
        L.append("- 各次分析停止概率 stop probability by look: %s" % rep["stop_distribution"])
    if rep.get("empirical_events_mean") is not None:
        L.append("- 平均事件数 mean events: %s" % rep["empirical_events_mean"])
    if rep.get("resize_rate") is not None:
        L.append("- 进入 promising zone 并扩样的比例 resize rate: %s" % rep["resize_rate"])
    for nt in rep.get("notes", []):
        L.append("- ⚠️ %s" % nt)
    L.append("")
    L.append("> **局限 Limitation**：%s" % rep["limitation"])
    return "\n".join(L)


def build_parser():
    p = argparse.ArgumentParser(
        description="ct-samplesize P1-C: local Monte-Carlo verification of an "
                    "analytic sample-size / power solution (power ±2pp, TIE ±0.5pp).")
    p.add_argument("--design", required=True,
                   choices=["ttest_ind", "ttest_one", "ttest_paired",
                            "proportion_two", "survival", "group_sequential",
                            "adaptive_reestimate"])
    p.add_argument("--n", type=int, required=True, help="每组样本量（解析解给出的 n）")
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--power", type=float, default=0.8, help="名义功效（待验证目标）")
    p.add_argument("--side", choices=["one", "two"], default="two")
    p.add_argument("--effect_size", type=float, default=None, help="Cohen's d")
    p.add_argument("--p1", type=float, default=None)
    p.add_argument("--p2", type=float, default=None)
    p.add_argument("--hazard_ratio", "--hr", dest="hazard_ratio", type=float, default=None)
    p.add_argument("--median_control", type=float, default=None, help="对照中位生存（月）")
    p.add_argument("--accrual", type=float, default=None, help="入组期（与中位数同单位）")
    p.add_argument("--followup", type=float, default=None, help="末例随访期")
    p.add_argument("--expected_events", type=float, default=None,
                   help="解析解给出的期望事件数（校验容差 ±5%%）")
    p.add_argument("--looks", type=int, default=2, help="组序贯分析次数（含最终）")
    p.add_argument("--boundaries", type=str, default=None,
                   help="rpact/gsDesign 给出的 z 边界，逗号分隔（强烈建议提供："
                        "这才是独立验证）")
    p.add_argument("--spending", default="obrien_fleming",
                   choices=["obrien_fleming", "pocock"])
    p.add_argument("--interim_fraction", type=float, default=None)
    p.add_argument("--target_cp", type=float, default=None)
    p.add_argument("--max_inflation", type=float, default=None)
    p.add_argument("--verify-nsim", dest="verify_nsim", type=int, default=20000,
                   help="Monte-Carlo 重复次数（默认 20000；上限 %d）" % NSIM_HARD_CAP)
    p.add_argument("--seed", type=int, default=20260829)
    p.add_argument("--no-tie", action="store_true", help="跳过 H0 下的 TIE 检验")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--json", dest="json_out", default=None, help="报告 JSON 输出路径")
    p.add_argument("--lang", default="zh", choices=["zh", "en"])
    return p


def main():
    a = build_parser().parse_args()
    bnds = None
    if a.boundaries:
        bnds = [float(x) for x in a.boundaries.replace(" ", "").split(",") if x]
    params = {k: v for k, v in {
        "effect_size": a.effect_size, "p1": a.p1, "p2": a.p2,
        "hazard_ratio": a.hazard_ratio, "median_control": a.median_control,
        "accrual": a.accrual, "followup": a.followup,
        "interim_fraction": a.interim_fraction, "target_cp": a.target_cp,
        "max_inflation": a.max_inflation,
    }.items() if v is not None}
    rep = run_verify(a.design, a.n, alpha=a.alpha, power=a.power, side=a.side,
                     nsim=a.verify_nsim, seed=a.seed, params=params,
                     boundaries=bnds, looks=(len(bnds) if bnds else a.looks),
                     spending=a.spending, expected_events=a.expected_events,
                     check_tie=not a.no_tie, use_cache=not a.no_cache)
    print(format_report(rep, lang=a.lang))
    if a.json_out:
        with open(a.json_out, "w", encoding="utf-8") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2)
        print("\n[OK] JSON -> %s" % a.json_out)
    sys.exit(0 if rep["overall"] == "PASS" else (2 if rep["overall"] == "FAIL" else 1))


if __name__ == "__main__":
    main()
