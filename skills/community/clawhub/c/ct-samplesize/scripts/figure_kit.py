#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ⚠️ 本文件是默认图形层（figure layer）的唯一真相源（v5.12.0 起）。coze 部署包内的
#    adapters/coze/scripts/figure_kit.py 由部署构建器（_build_deploy_new.py /
#    _build_deploy.py）在打包前从本文件复制同步生成——请勿手工编辑 coze 侧副本，
#    改这里后重新构建即可。coze 端 samplesize.py 按路径子进程执行包内副本。
"""
figure_kit.py — ct-samplesize v5.1 默认图形层（Default Figure Layer）

为什么需要这一层
-----------------
v5.0.2 之前：只有 5 种检验（ttest_ind / ttest_paired / ttest_one /
proportion_one / proportion_two）在契约里标了 `default_curve=true`，其余 44 种
算完只回一个数字，没有任何图形。原因不是"画不了"，而是**曲线必须由 R 端算**——
一旦要求 coze 为 65 种方法各画一张图，就要在云端 R 里塞进一大段绘图代码并
引入额外图形依赖。

本模块的取舍：**数值锚点来自 R（真相源），曲线形状交给本地的族级解析结构**。

    锚点 (n*, power*)  ──族级公式标定──▶  λ*  ──扫网格──▶  整条 power(N) 曲线

数学依据是严格的：几乎所有常用检验的检验统计量都落在四大族里，其非中心参数
对样本量只有两种缩放 ——

    族           非中心参数随 n 的缩放         参考分布
    ----------   -------------------------     ----------
    z  (正态)     λ(n) = λ*·√(n/n*)              N(0,1)
    t  (非中心t)  ncp(n) = ncp*·√(n/n*)           t(df(n))
    F  (非中心F)  λ(n) = λ*·(n/n*)                F(df1, df2(n))
    X  (非中心χ²) λ(n) = λ*·(n/n*)                χ²(df(n))

因此**只要有一个 R 算出的锚点，整条曲线的形状就在数学上被唯一确定**，
本地无需知道 coze 内部用的到底是 pwr、TrialSize 还是 rpact。
曲线必然精确穿过 R 给出的锚点，这不是近似。

代价与边界（必须在报告中如实标注）
----------------------------------
1. 曲线**穿过锚点是精确的**，锚点以外的点依赖"族级缩放"这一结构假设。
   对 z/t/F/χ² 四大族，该假设在大样本下误差可忽略；小样本（n<20）或
   含离散校正（Fisher 精确、Yates、exact binomial）的方法误差会变大。
2. 因此每张图都带「效应量 ±20% 敏感带」，把标定误差的可见后果显式画出来，
   而不是假装曲线是精确的。
3. 曲线只用于**呈现与沟通**（看趋势、选方案），**不用于二次求解样本量**。
   需要精确值一律以 R 返回的数值为准（图中红点即锚点）。

依赖：仅标准库（math）。coze 端零改动、零新增 R 包。

用法
----
    from figure_kit import render_default_figures
    paths = render_default_figures(test, meta, args, out_dir)
"""
from __future__ import annotations

import io
import math
import os

# 复用 alloc_curve 的数值内核与绘图框架（同一技能内，发布包同时含两文件）
try:
    from alloc_curve import (  # type: ignore
        Axes, _esc, _frame, _label, _legend, _nice_ticks, _polyline, _dot,
        _phi, _norm_ppf, _nct_cdf, _t_ppf,
        C_BAND, C_BLUE, C_GREEN, C_INK, C_MUTE, C_ORANGE, C_PURPLE, C_RED,
        PAD_B, PAD_L, PAD_R, PAD_T, W, H, PW, PH,
    )
    _ALLOC_AVAILABLE = True
except Exception:  # pragma: no cover - alloc_curve 缺失时降级为无图
    _ALLOC_AVAILABLE = False

__all__ = [
    "render_default_figures", "METHOD_FIGURES", "calibrate",
    "power_normal", "power_nct", "power_ncf", "power_ncchi2",
]


# ===========================================================================
# 1. 分布内核（零依赖；非中心 F / χ² 用泊松混合 + 正则化不完全 Γ/Β）
# ===========================================================================

def _log_gamma(x: float) -> float:
    return math.lgamma(x)


def _gser(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a,x) — series branch (x < a+1)."""
    ap, s, d = a, 1.0 / a, 1.0 / a
    for _ in range(1000):
        ap += 1.0
        d *= x / ap
        s += d
        if abs(d) < abs(s) * 1e-15:
            break
    return s * math.exp(-x + a * math.log(x) - _log_gamma(a))


def _gcf(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a,x) — continued fraction (x >= a+1)."""
    tiny = 1e-300
    b, c, d = x + 1.0 - a, 1.0 / tiny, 1.0 / (x + 1.0 - a)
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-15:
            break
    return math.exp(-x + a * math.log(x) - _log_gamma(a)) * h


def gamma_p(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a,x) = γ(a,x)/Γ(a)."""
    if x <= 0:
        return 0.0
    if x < a + 1.0:
        return _gser(a, x)
    return 1.0 - _gcf(a, x)


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction for the incomplete beta function (NR convention)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-15:
            break
    return h


def beta_i(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    lbeta = (_log_gamma(a + b) - _log_gamma(a) - _log_gamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    bt = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def chi2_cdf(x: float, df: float) -> float:
    """CDF of central chi-square(df)."""
    if x <= 0:
        return 0.0
    return gamma_p(0.5 * df, 0.5 * x)


def f_cdf(x: float, df1: float, df2: float) -> float:
    """CDF of central F(df1, df2)."""
    if x <= 0:
        return 0.0
    return beta_i(0.5 * df1, 0.5 * df2, df1 * x / (df1 * x + df2))


def _poisson_weights(lam: float, tol: float = 1e-12):
    """Poisson(lam/2) weights for the noncentral chi-square mixture.

    Yields (j, w) until the tail mass is negligible; guarantees the returned
    weights sum to ~1 (renormalised) so the mixture CDF stays in [0,1].
    """
    mu = 0.5 * lam
    # start near the mode to keep exp() well-conditioned for large lambda
    j0 = max(0, int(mu - 8.0 * math.sqrt(mu + 1.0)))
    logw = -mu + j0 * math.log(mu) - _log_gamma(j0 + 1.0) if mu > 0 else 0.0
    if mu <= 0:
        yield 0, 1.0
        return
    ws, js = [], []
    w = math.exp(logw)
    j = j0
    # walk up
    while True:
        ws.append(w)
        js.append(j)
        if j > mu and w < tol * max(ws):
            break
        j += 1
        w *= mu / j
        if j > mu + 400:
            break
    # walk down
    w = math.exp(logw)
    j = j0 - 1
    while j >= 0:
        w *= (j + 1.0) / mu
        if w < tol * max(ws):
            break
        ws.append(w)
        js.append(j)
        j -= 1
    tot = sum(ws)
    if tot <= 0:
        yield 0, 1.0
        return
    for jj, ww in zip(js, ws):
        yield jj, ww / tot


def ncchi2_cdf(x: float, df: float, lam: float) -> float:
    """CDF of noncentral chi-square(df, ncp=lambda) via Poisson mixture."""
    if lam <= 0:
        return chi2_cdf(x, df)
    if x <= 0:
        return 0.0
    s = 0.0
    for j, w in _poisson_weights(lam):
        s += w * chi2_cdf(x, df + 2.0 * j)
    return min(max(s, 0.0), 1.0)


def ncf_cdf(x: float, df1: float, df2: float, lam: float) -> float:
    """CDF of noncentral F(df1, df2, ncp=lambda) via Poisson mixture.

    F' = (X1/df1)/(X2/df2) with X1 ~ nc-chi2(df1, lam) independent of
    X2 ~ chi2(df2)  =>  P(F'<=f) = sum_j Poisson(j; lam/2) I_{z}(df1/2+j, df2/2).
    """
    if lam <= 0:
        return f_cdf(x, df1, df2)
    if x <= 0:
        return 0.0
    z = df1 * x / (df1 * x + df2)
    s = 0.0
    for j, w in _poisson_weights(lam):
        s += w * beta_i(0.5 * df1 + j, 0.5 * df2, z)
    return min(max(s, 0.0), 1.0)


# ===========================================================================
# 2. 四族的 power 函数（给定非中心参数 → power）
# ===========================================================================

def _zc(alpha: float, sides: int) -> float:
    """Critical value on the standard normal scale."""
    return _norm_ppf(1.0 - alpha / sides)


def power_normal(lam: float, alpha: float, sides: int) -> float:
    """Power of a z-test with noncentrality `lam` (|lam| on the z scale)."""
    z = _zc(alpha, sides)
    a = abs(lam)
    p = _phi(a - z)
    if sides == 2:
        p += _phi(-a - z)
    return min(max(p, 0.0), 1.0)


def power_nct(lam: float, df: float, alpha: float, sides: int) -> float:
    """Power of a t-test: |T'| > t_{1-alpha/sides}(df), T' ~ t(df, ncp=lam)."""
    if df <= 0:
        return 0.0
    tc = _t_ppf(1.0 - alpha / sides, df)
    a = abs(lam)
    p = 1.0 - _nct_cdf(tc, df, a)
    if sides == 2:
        p += _nct_cdf(-tc, df, a)
    return min(max(p, 0.0), 1.0)


def power_ncf(lam: float, df1: float, df2: float, alpha: float) -> float:
    """Power of an F-test (one-sided by construction): F' > F_{1-alpha}(df1,df2)."""
    if df1 <= 0 or df2 <= 0:
        return 0.0
    fc = _f_ppf(1.0 - alpha, df1, df2)
    return min(max(1.0 - ncf_cdf(fc, df1, df2, lam), 0.0), 1.0)


def power_ncchi2(lam: float, df: float, alpha: float) -> float:
    """Power of a chi-square test: X' > chi2_{1-alpha}(df)."""
    if df <= 0:
        return 0.0
    xc = _chi2_ppf(1.0 - alpha, df)
    return min(max(1.0 - ncchi2_cdf(xc, df, lam), 0.0), 1.0)


def _f_ppf(p: float, df1: float, df2: float) -> float:
    """Inverse CDF of central F by bisection on log-scale (robust, zero-dep)."""
    lo, hi = 1e-8, 1e6
    for _ in range(200):
        mid = math.sqrt(lo * hi)  # geometric bisection
        if f_cdf(mid, df1, df2) < p:
            lo = mid
        else:
            hi = mid
        if hi / lo < 1.0 + 1e-12:
            break
    return math.sqrt(lo * hi)


def _chi2_ppf(p: float, df: float) -> float:
    lo, hi = 1e-10, df + 40.0 * math.sqrt(2.0 * df) + 500.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if chi2_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-10 * max(1.0, hi):
            break
    return 0.5 * (lo + hi)


# ===========================================================================
# 3. 标定器：从 R 给出的锚点 (n*, power*) 反解非中心参数
# ===========================================================================

#: 族 → (缩放指数, 参考分布)
#:   scale : 非中心参数 λ(n) = λ* · (n/n*) ** scale
#:   dist  : "z" | "t" | "F" | "X"
FAMILY_SCALE = {
    "z": 0.5,
    "t": 0.5,
    "F": 1.0,
    "X": 1.0,
}


def _power_given_lam(fam, lam, df1, df2, alpha, sides):
    if fam == "z":
        return power_normal(lam, alpha, sides)
    if fam == "t":
        return power_nct(lam, df2, alpha, sides)      # df2 carries df
    if fam == "F":
        return power_ncf(lam, df1, df2, alpha)
    if fam == "X":
        return power_ncchi2(lam, df2, alpha)
    raise ValueError("unknown family %r" % fam)


def _solve_lam(fam, target, df1, df2, alpha, sides):
    """Invert power(lam) = target for the noncentrality, by monotone bisection.

    power is strictly increasing in |lam| for all four families, so bisection
    on [0, 200] is both safe and fast (60 iterations ~ 1e-16 resolution).
    """
    if not (0.0 < target < 1.0):
        return 0.0
    lo, hi = 0.0, 200.0
    while _power_given_lam(fam, hi, df1, df2, alpha, sides) < target:
        hi *= 2.0
        if hi > 1e6:
            break
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if _power_given_lam(fam, mid, df1, df2, alpha, sides) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def calibrate(test, n_star, power_star, alpha=0.05, sides=2, groups=2):
    """Return a closure `power(n)` anchored at the R-supplied point.

    Parameters
    ----------
    test        : method id (looked up in METHOD_FAMILY)
    n_star      : the N reported by R (interpretation per METHOD_N_UNIT)
    power_star  : the power reported by R at n_star
    alpha,sides : test size / sidedness
    groups      : number of groups (ANOVA / Dunnett / MAMS)

    The returned function satisfies  power(n_star) == power_star  (exactly, up
    to the 1e-12 bisection tolerance) — the curve is pinned to the R anchor.
    """
    fam, df1_of, df2_of = METHOD_FAMILY.get(
        test, METHOD_FAMILY["_default"])
    if not n_star or n_star <= 0:
        return None
    if not power_star or not (0.0 < power_star < 1.0):
        return None

    df1_0, df2_0 = df1_of(n_star, groups), df2_of(n_star, groups)
    lam_star = _solve_lam(fam, float(power_star), df1_0, df2_0, alpha, sides)
    scale = FAMILY_SCALE[fam]

    def power(n, _lam_scale=1.0):
        """power at sample size n; _lam_scale shrinks/inflates the effect size."""
        if n <= 0:
            return 0.0
        lam = lam_star * _lam_scale * (float(n) / float(n_star)) ** scale
        return _power_given_lam(fam, lam, df1_of(n, groups), df2_of(n, groups),
                                alpha, sides)

    power.lam_star = lam_star      # type: ignore[attr-defined]
    power.family = fam             # type: ignore[attr-defined]
    power.n_star = float(n_star)   # type: ignore[attr-defined]
    power.power_star = float(power_star)  # type: ignore[attr-defined]
    return power


# ===========================================================================
# 4. 方法 → 族 / 默认图型 / N 的单位
# ===========================================================================

#: 默认族：z（正态近似，绝大多数样本量公式的落点）
_DEFAULT_FAMILY = ("z", lambda n, g: 1.0, lambda n, g: 1e9)

#: test → (family, df1(n,groups), df2(n,groups))
#:   z 族：df 不参与，填占位
#:   t 族：df2 = 残余自由度
#:   F 族：df1 = 组间自由度，df2 = 组内自由度
#:   X 族：df2 = 自由度
METHOD_FAMILY = {
    # ── 连续均值 ──
    "ttest_ind":        ("t", lambda n, g: 1.0, lambda n, g: max(1.0, 2.0 * n - 2.0)),
    "ttest_paired":     ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "ttest_one":        ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "anova":            ("F", lambda n, g: max(1.0, g - 1.0),
                         lambda n, g: max(1.0, g * n - g)),
    "dunnett":          ("t", lambda n, g: 1.0, lambda n, g: max(1.0, g * n - g)),
    # ── 率 / 计数 ──
    "proportion_one":   ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "proportion_two":   ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "proportion_paired": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "odds_ratio":       ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "risk_ratio":       ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "poisson":          ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "vaccine_efficacy": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── 非劣 / 等效 / 优效 / TOST ──
    "non_inferiority":  ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "superiority_margin": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "equivalence":      ("t", lambda n, g: 1.0, lambda n, g: max(1.0, 2.0 * n - 2.0)),
    "be_tost":          ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    # ── 生存 ──
    "survival":         ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ni_survival":      ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "survival_equivalence": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "survival_superiority": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "survival_exact":   ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "cox_covariate":    ("X", lambda n, g: 1.0, lambda n, g: 1.0),
    "survival_one_sample": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "competing_risks":  ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "recurrent_events": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "survival_historical": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── 诊断 / 一致性 ──
    "roc":              ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "bland_altman":     ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    # ── 聚类 / 纵向 ──
    "cluster":          ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "mixed_model":      ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "mediation":        ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── 多重性 / 多臂 ──
    "multiple_endpoints": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "mams":             ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── Win ratio / 共同主要 / 历史对照 ──
    "win_ratio":        ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "must_win":         ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "historical_controls": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "dose_escalation":  ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── 成组序贯 / 适应性 ──
    "group_sequential": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_proportion":   ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_survival":     ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_hazard":       ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_poisson":      ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_survival_sim": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "gsd_hazard_sim":   ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "adaptive":         ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "adaptive_simulate": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "conditional_power": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── 贝叶斯 ──
    "bayesian":         ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "assurance":        ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    # ── PASS-coverage extension (v5.9 / v5.10) ──
    "correlation":        ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "variance_one":       ("X", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "variance_two":       ("F", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "cv_one":             ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_mean":            ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_prop":            ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_or":              ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_rr":              ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_cor":             ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "ci_icc":             ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "regression_linear":  ("F", lambda n, g: 1.0, lambda n, g: max(1.0, n - 2.0)),
    "meta_planning":      ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "regression_logistic":("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "regression_poisson": ("z", lambda n, g: 1.0, lambda n, g: 1e9),
    "cluster_ext":        ("t", lambda n, g: 1.0, lambda n, g: max(1.0, n - 1.0)),
    "rates_ext":          ("z", lambda n, g: 1.0, lambda n, g: 1e9),
}
METHOD_FAMILY["_default"] = _DEFAULT_FAMILY

#: N 的语义单位（决定 X 轴标签）
METHOD_N_UNIT = {
    "ttest_ind": "每组样本量 n per group",
    "ttest_paired": "配对数 n pairs",
    "ttest_one": "总样本量 N",
    "anova": "每组样本量 n per group",
    "proportion_one": "总样本量 N",
    "proportion_two": "每组样本量 n per group",
    "proportion_paired": "配对数 n pairs",
    "odds_ratio": "每组样本量 n per group",
    "risk_ratio": "每组样本量 n per group",
    "non_inferiority": "每组样本量 n per group",
    "superiority_margin": "每组样本量 n per group",
    "equivalence": "每组样本量 n per group",
    "be_tost": "每序列样本量 n per sequence",
    "survival": "每组样本量 n per arm",
    "ni_survival": "每组样本量 n per arm",
    "survival_equivalence": "每组样本量 n per arm",
    "survival_superiority": "每组样本量 n per arm",
    "survival_exact": "每组样本量 n per arm",
    "cox_covariate": "总样本量 N",
    "survival_one_sample": "总样本量 N",
    "competing_risks": "每组样本量 n per group",
    "recurrent_events": "每组样本量 n per group",
    "survival_historical": "总样本量 N",
    "poisson": "每组样本量 n per group",
    "roc": "总样本量 N",
    "bland_altman": "总样本量 N",
    "cluster": "总样本量 N",
    "vaccine_efficacy": "每组样本量 n per group",
    "multiple_endpoints": "每组样本量 n per group",
    "bayesian": "每组样本量 n per group",
    "dose_escalation": "每剂量组样本量 n per dose",
    "win_ratio": "总样本量 N",
    "must_win": "每组样本量 n per group",
    "historical_controls": "试验组样本量 n treatment",
    "mams": "每臂样本量 n per arm",
    "dunnett": "每组样本量 n per group",
    "mediation": "总样本量 N",
    "mixed_model": "受试者数 n subjects",
    "group_sequential": "每组样本量 n per arm",
    "gsd_proportion": "每组样本量 n per arm",
    "gsd_survival": "每组样本量 n per arm",
    "gsd_hazard": "每组样本量 n per arm",
    "gsd_poisson": "每组样本量 n per arm",
    "gsd_survival_sim": "每组样本量 n per arm",
    "gsd_hazard_sim": "每组样本量 n per arm",
    "adaptive": "每组样本量 n per arm",
    "adaptive_simulate": "每组样本量 n per arm",
    "conditional_power": "每组样本量 n per arm",
    "assurance": "每组样本量 n per group",
    # ── PASS-coverage extension (v5.9 / v5.10) ──
    "correlation": "总样本量 N",
    "variance_one": "总样本量 N",
    "variance_two": "每组样本量 n per group",
    "cv_one": "总样本量 N",
    "ci_mean": "总样本量 N",
    "ci_prop": "总样本量 N",
    "ci_or": "每组样本量 n per group",
    "ci_rr": "每组样本量 n per group",
    "ci_cor": "总样本量 N",
    "ci_icc": "总样本量 N",
    "regression_linear": "总样本量 N",
    "meta_planning": "总样本量 N",
    "regression_logistic": "总样本量 N",
    "regression_poisson": "总样本量 N",
    "cluster_ext": "总样本量 N",
    "rates_ext": "每组样本量 n per group",
}

#: test → (主图, 副图 or None)
#:   主图一定出；副图需要额外参数（如两组分配比）时才可能出
METHOD_FIGURES = {
    # 两独立组 → 主图 + 分配比四图（v5.1 新增能力，见 alloc_curve.py）
    "ttest_ind":        ("power_n", "alloc_suite"),
    "proportion_two":   ("power_n", "alloc_suite"),
    "odds_ratio":       ("power_n", "alloc_suite"),
    "risk_ratio":       ("power_n", "alloc_suite"),
    "survival":         ("power_events", "alloc_suite"),
    "ni_survival":      ("power_events", "alloc_suite"),
    "survival_superiority": ("power_events", "alloc_suite"),
    "survival_equivalence": ("power_events", "alloc_suite"),
    "competing_risks":  ("power_events", "alloc_suite"),
    "recurrent_events": ("power_events", "alloc_suite"),
    "poisson":          ("power_n", "alloc_suite"),
    "vaccine_efficacy": ("power_n", "alloc_suite"),
    "win_ratio":        ("power_n", "alloc_suite"),
    "non_inferiority":  ("margin_tradeoff", "power_n"),
    "superiority_margin": ("margin_tradeoff", "power_n"),
    "equivalence":      ("margin_tradeoff", "power_n"),
    "be_tost":          ("margin_tradeoff", "power_n"),
    "anova":            ("power_n_multi", None),
    "dunnett":          ("power_n_multi", None),
    "mams":             ("power_n_multi", None),
    "multiple_endpoints": ("power_n_multi", None),
    "dose_escalation":  ("power_n_multi", None),
    "cluster":          ("icc_sens", "power_n"),
    "mixed_model":      ("icc_sens", "power_n"),
    "bland_altman":     ("power_n", None),
    "group_sequential": ("gs_boundary", "power_n"),
    "gsd_proportion":   ("gs_boundary", "power_n"),
    "gsd_survival":     ("gs_boundary", "power_n"),
    "gsd_hazard":       ("gs_boundary", "power_n"),
    "gsd_poisson":      ("gs_boundary", "power_n"),
    "gsd_survival_sim": ("gs_boundary", "power_n"),
    "gsd_hazard_sim":   ("gs_boundary", "power_n"),
    "adaptive":         ("gs_boundary", "power_n"),
    "adaptive_simulate": ("gs_boundary", "power_n"),
    "conditional_power": ("gs_boundary", None),
    "bayesian":         ("assurance_n", None),
    "assurance":        ("assurance_n", None),
    # ── PASS-coverage extension (v5.9 / v5.10) ──
    "correlation":        ("power_n", None),
    "variance_one":       ("power_n", None),
    "variance_two":       ("power_n", None),
    "cv_one":             ("power_n", None),
    "ci_mean":            ("power_n", None),
    "ci_prop":            ("power_n", None),
    "ci_or":              ("power_n", None),
    "ci_rr":              ("power_n", None),
    "ci_cor":             ("power_n", None),
    "ci_icc":             ("power_n", None),
    "regression_linear":  ("power_n", None),
    "meta_planning":      ("meta_hetero", None),
    "regression_logistic":("power_n", None),
    "regression_poisson": ("power_n", None),
    "cluster_ext":        ("icc_sens", "power_n"),
    "rates_ext":          ("power_n", None),
}

#: 兜底：未登记的方法一律出 power_n
_DEFAULT_FIGURE = ("power_n", None)


def figure_plan(test: str):
    """Return (primary_kind, secondary_kind) for a method."""
    return METHOD_FIGURES.get(test, _DEFAULT_FIGURE)


# ===========================================================================
# 5. 图模板
# ===========================================================================

def _band_poly(ax, xs, lo, hi, color="#2980b9", opacity=0.13):
    """Shaded band between two series (effect-size sensitivity)."""
    up = " ".join("%.1f,%.1f" % (ax.sx(x), ax.sy(h)) for x, h in zip(xs, hi))
    dn = " ".join("%.1f,%.1f" % (ax.sx(x), ax.sy(l)) for x, l in reversed(
        list(zip(xs, lo))))
    return ('<polygon points="%s %s" fill="%s" opacity="%s" stroke="none"/>'
            % (up, dn, color, opacity))


def _n_grid(n_star, fam_scale, lo_f=0.35, hi_f=2.6, npts=61):
    """Sample-size grid, log-spaced around the anchor."""
    lo = max(4.0, n_star * lo_f)
    hi = max(lo + 8.0, n_star * hi_f)
    step = (math.log(hi) - math.log(lo)) / (npts - 1)
    return [math.exp(math.log(lo) + i * step) for i in range(npts)]


def fig_power_n(test, power_fn, n_star, power_star, alpha, sides,
                target_power=None, ref_n=None, unit=None, ylab="Power",
                title_note=""):
    """通用主图：power vs N，带效应量 ±20% 敏感带。"""
    scale = FAMILY_SCALE[power_fn.family]
    xs = _n_grid(n_star, scale)
    ys = [power_fn(x) for x in xs]
    lo = [power_fn(x, 0.8) for x in xs]
    hi = [power_fn(x, 1.2) for x in xs]

    ymin = max(0.0, min(min(ys), min(lo)) - 0.04)
    ymax = min(1.0, max(max(ys), max(hi)) + 0.05)
    if ymax - ymin < 0.15:
        ymax = min(1.0, ymin + 0.15)
    ax = Axes(min(xs), max(xs), ymin, ymax)

    extra = []
    # 目标 power 水平参考线
    tp = target_power if target_power is not None else power_star
    if ymin <= tp <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(tp), W - PAD_R, ax.sy(tp), C_RED))
        extra.append(_label(ax, min(xs), tp, "power = %g" % tp, C_RED,
                            dx=PAD_L - ax.sx(min(xs)) + 4, dy=-5,
                            anchor="start", size=10, weight="600"))
    # 锚点竖线
    if min(xs) <= n_star <= max(xs):
        extra.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                     'stroke-width="1.1" stroke-dasharray="3,4"/>'
                     % (ax.sx(n_star), PAD_T, ax.sx(n_star), H - PAD_B, C_GREEN))

    body = [_band_poly(ax, xs, lo, hi)]
    body.append(_polyline(ax, list(zip(xs, ys)), C_BLUE))
    body.append(_dot(ax, n_star, power_star, C_RED, 4.6))
    body.append(_label(ax, n_star, power_star,
                       "R 结果  n=%s, power=%.3f" % (_fmt(n_star), power_star),
                       C_RED, dy=-11, size=10.5, weight="600"))
    body.append(_legend([("power(N)", C_BLUE, None),
                         ("效应量 ±20%", C_BLUE, "3,3")], y0=PAD_T + 4))

    xt = _nice_ticks(min(xs), max(xs), 6, "%g")
    yt = _nice_ticks(ymin, ymax, 5, "%g")
    title = "%s  |  power vs N%s  |  alpha=%g (%s)" % (
        test, ("  ·  " + title_note) if title_note else "",
        alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title, unit or METHOD_N_UNIT.get(test, "样本量 N"),
                  ylab, xt, yt, "".join(extra) + "".join(body))


def _fmt(v):
    if v is None:
        return "-"
    if abs(v - round(v)) < 1e-9:
        return "%d" % int(round(v))
    return "%.1f" % v


def fig_power_n_multi(test, power_fn, n_star, power_star, alpha, sides,
                      groups=2, target_power=None, unit=None):
    """多系列：power vs N，每条线一个组数（ANOVA / Dunnett / MAMS）。"""
    scale = FAMILY_SCALE[power_fn.family]
    xs = _n_grid(n_star, scale)
    glist = sorted({max(2, groups + d) for d in (-1, 0, 1, 2)})
    cols = [C_BLUE, C_ORANGE, C_GREEN, C_PURPLE]
    series = []
    ymax = 0.0
    ymin = 1.0
    for g in glist:
        pg = calibrate(test, n_star, power_star, alpha, sides, groups=g)
        if pg is None:
            continue
        ys = [pg(x) for x in xs]
        series.append((g, ys))
        ymax = max(ymax, max(ys))
        ymin = min(ymin, min(ys))
    if not series:
        return ""
    ymin = max(0.0, ymin - 0.04)
    ymax = min(1.0, ymax + 0.06)
    ax = Axes(min(xs), max(xs), ymin, ymax)

    extra = []
    tp = target_power if target_power is not None else power_star
    if ymin <= tp <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(tp), W - PAD_R, ax.sy(tp), C_RED))

    body = []
    legend = []
    for i, (g, ys) in enumerate(series):
        col = cols[i % len(cols)]
        body.append(_polyline(ax, list(zip(xs, ys)), col,
                              width=2.6 if g == groups else 1.9,
                              dash=None if g == groups else "5,4"))
        legend.append(("%d 组%s" % (int(g), "（当前）" if g == groups else ""),
                       col, None if g == groups else "5,4"))
    body.append(_dot(ax, n_star, power_star, C_RED, 4.6))
    body.append(_legend(legend, y0=PAD_T + 4))

    xt = _nice_ticks(min(xs), max(xs), 6, "%g")
    yt = _nice_ticks(ymin, ymax, 5, "%g")
    title = "%s  |  power vs N（按组数分层）  |  alpha=%g (%s)" % (
        test, alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title,
                  unit or METHOD_N_UNIT.get(test, "每组样本量 n per group"),
                  "Power", xt, yt, "".join(extra) + "".join(body))


def fig_margin_tradeoff(test, power_fn, n_star, power_star, alpha, sides,
                        margin, target_power=None, unit=None):
    """非劣 / 等效 / 优效：power vs margin（界值放宽的代价与收益）。

    数学：非中心参数对 margin 是**线性**的——
        λ(margin) = (Δ − margin)/SE = λ* − (margin − margin*)/SE*
    而 (Δ − margin*) / SE* = λ*，故 SE* = (Δ − margin*)/λ*。Δ 未知，但可用
    用户给定的 margin* 与锚点共同消去：以「相对余量」r = margin/Δ 为横轴，
        λ(r) = Δ(1 − r)/SE* = λ* · (1 − r)/(1 − r*)
    横轴直接用 margin/Δ 的比值刻度，Y 轴 power。这样无需知道 Δ 与 SE 的绝对值。
    """
    if not margin or margin <= 0:
        return ""
    r_star = float(margin) / (float(margin) + 1.0)  # 保守占位：无 Δ 时无法定位
    # 用锚点 λ* 反推 r*：Δ/SE* = λ*/(1−r*) 无法闭合 → 改用「margin 相对缩放」刻度
    # 横轴 = margin / margin*（1.0 即当前方案），λ 随 (1 − r·s) 线性衰减，
    # s = margin*/Δ 为未知常数 → 取图中性假设 s=0.5（即当前界值占效应量一半），
    # 并在图注中显式声明该假设。
    s = 0.5
    ratios = [0.2 + (1.8 * i / 60.0) for i in range(61)]
    fam = power_fn.family
    lam_star = power_fn.lam_star

    def power_at_ratio(rr):
        lam = lam_star * (1.0 - s * rr) / max(1e-9, (1.0 - s * 1.0))
        if lam <= 0:
            # margin 超过真实效应 → power 衰减到 alpha 附近
            return max(alpha / sides, min(1.0, math.exp(-lam * lam / 2.0)))
        if fam == "z":
            return power_normal(lam, alpha, sides)
        if fam == "t":
            return power_nct(lam, max(1.0, 2.0 * n_star - 2.0), alpha, sides)
        return power_normal(lam, alpha, sides)

    ys = [power_at_ratio(r) for r in ratios]
    ymin, ymax = max(0.0, min(ys) - 0.04), min(1.0, max(ys) + 0.05)
    ax = Axes(min(ratios), max(ratios), ymin, ymax)

    extra = []
    tp = target_power if target_power is not None else power_star
    if ymin <= tp <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(tp), W - PAD_R, ax.sy(tp), C_RED))
    extra.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                 'stroke-width="1.1" stroke-dasharray="3,4"/>'
                 % (ax.sx(1.0), PAD_T, ax.sx(1.0), H - PAD_B, C_GREEN))

    body = [_polyline(ax, list(zip(ratios, ys)), C_BLUE)]
    body.append(_dot(ax, 1.0, power_star, C_RED, 4.6))
    body.append(_label(ax, 1.0, power_star, "当前界值 margin=%g" % margin,
                       C_RED, dy=-11, size=10.5, weight="600"))
    body.append(_label(
        ax, 0.62, ymin + 0.035,
        "假设：当前界值 ≈ 真实效应量的 50%（Δ 未由 R 回传，仅作形状示意）",
        C_MUTE, dy=0, size=9.5, anchor="start"))
    body.append(_legend([("power(margin)", C_BLUE, None)], y0=PAD_T + 4))

    xt = {0.2: "0.2×", 0.6: "0.6×", 1.0: "1.0×（当前）", 1.4: "1.4×",
          1.8: "1.8×", 2.0: "2.0×"}
    yt = _nice_ticks(ymin, ymax, 5, "%g")
    title = "%s  |  power vs 界值 margin  |  alpha=%g (%s)" % (
        test, alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title, "margin 相对当前界值的倍数", "Power", xt, yt,
                  "".join(extra) + "".join(body))


def fig_icc_sens(test, power_fn, n_star, power_star, alpha, sides,
                 icc=0.05, m=20, target_power=None, unit=None):
    """聚类 / 混合模型：power vs ICC（设计效应的直观来源）。

    设计效应 DEFF = 1 + (m−1)·ICC，样本量与 DEFF 成正比 →
        λ(ICC) = λ* · sqrt( DEFF* / DEFF(ICC) )
    这是聚类随机试验的标准结果（Donner & Klar），本地可精确外推。
    """
    m = float(m) if m else 20.0
    icc = float(icc) if icc else 0.05
    deff_star = 1.0 + (m - 1.0) * icc
    iccs = [0.001 + (0.30 * i / 60.0) for i in range(61)]
    fam = power_fn.family
    lam_star = power_fn.lam_star
    df_at = max(1.0, 2.0 * n_star - 2.0) if fam == "t" else 1e9

    def power_at_icc(v):
        deff = 1.0 + (m - 1.0) * v
        lam = lam_star * math.sqrt(deff_star / max(deff, 1e-9))
        if fam == "z":
            return power_normal(lam, alpha, sides)
        return power_nct(lam, df_at, alpha, sides)

    ys = [power_at_icc(v) for v in iccs]
    ymin, ymax = max(0.0, min(ys) - 0.04), min(1.0, max(ys) + 0.05)
    ax = Axes(min(iccs), max(iccs), ymin, ymax)

    extra = []
    tp = target_power if target_power is not None else power_star
    if ymin <= tp <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(tp), W - PAD_R, ax.sy(tp), C_RED))
    extra.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                 'stroke-width="1.1" stroke-dasharray="3,4"/>'
                 % (ax.sx(icc), PAD_T, ax.sx(icc), H - PAD_B, C_GREEN))

    body = [_polyline(ax, list(zip(iccs, ys)), C_BLUE)]
    body.append(_dot(ax, icc, power_star, C_RED, 4.6))
    body.append(_label(ax, icc, power_star,
                       "ICC=%.3g, m=%g → DEFF=%.2f" % (icc, m, deff_star),
                       C_RED, dy=-11, size=10.5, weight="600"))
    body.append(_legend([("power(ICC)", C_BLUE, None)], y0=PAD_T + 4))

    xt = {0.0: "0", 0.05: "0.05", 0.10: "0.10", 0.15: "0.15",
          0.20: "0.20", 0.25: "0.25", 0.30: "0.30"}
    yt = _nice_ticks(ymin, ymax, 5, "%g")
    title = "%s  |  power vs 组内相关系数 ICC（m=%g）  |  alpha=%g (%s)" % (
        test, m, alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title, "ICC（组内相关系数）", "Power", xt, yt,
                  "".join(extra) + "".join(body))


# ── Meta 规划：不同异质性水平下所需研究数 K（PASS「Plots」栏目对标）─────────
# 数学核心与 R 引擎 ss_meta_planning 一致（Hedges & Pigott 2001）：
#   V_W 按效应族闭式；R = I²/(1−I²)；λ = (T−T0)/SE，SE = sqrt(V_W(1+R)/K)

def _meta_vw(effect_type, effect, n, p0, m=20.0, icc=0.05, cv=0.0):
    """研究内（族内）方差 V_W。cluster 需 m/icc/cv（设计效应放大）。"""
    if effect_type in ("smd", "cluster"):
        vw = (2.0 + effect ** 2 / 4.0) / n
        if effect_type == "cluster":
            vw *= 1.0 + (((cv or 0.0) ** 2 + 1.0) * m - 1.0) * icc
        return vw
    if effect_type == "paired":
        return (2.0 + effect ** 2 / 2.0) / n
    if effect_type == "or":
        p1 = effect * p0 / ((1.0 - p0) + effect * p0)
        return 1.0 / (n * p0) + 1.0 / (n * (1.0 - p0)) + 1.0 / (n * p1) + 1.0 / (n * (1.0 - p1))
    if effect_type == "rr":
        p1 = effect * p0
        return (1.0 - p0) / (n * p0) + (1.0 - p1) / (n * p1)
    if effect_type == "cor":
        return 1.0 / (n - 3.0)
    return None


def _meta_K_required(effect_type, effect, n, i2, alpha, sides, p0,
                     power, m=20.0, icc=0.05, cv=0.0):
    """达到目标功效所需最少研究数 K（递增整数搜索，与 R 端一致）。"""
    vw = _meta_vw(effect_type, effect, n, p0, m, icc, cv)
    if not vw or vw <= 0:
        return None
    R = 1e6 if i2 >= 1 else i2 / (1.0 - i2)
    if effect_type in ("or", "rr"):
        core_eff, core0 = math.log(effect), math.log(1.0)
    elif effect_type == "cor":
        core_eff, core0 = math.atanh(effect), 0.0
    else:
        core_eff, core0 = float(effect), 0.0
    for k in range(1, 200001):
        lam = (core_eff - core0) / math.sqrt(vw * (1.0 + R) / k)
        if power_normal(lam, alpha, sides) >= power:
            return k
    return None


def fig_meta_hetero(test, alpha=0.05, sides=2, target_power=0.8,
                    effect_type="smd", effect=0.3, n_per_study=100, p0=0.3,
                    m=20, icc=0.05, cluster_cv=0.0, i2_given=None, **kw):
    """meta_planning 主图：所需研究数 K 随异质性 I² 的变化曲线。"""
    power = float(target_power or 0.8)
    grid = [i / 40.0 for i in range(0, 39)]          # I² ∈ [0, 0.95]
    ys = []
    for x in grid:
        k = _meta_K_required(effect_type, float(effect), float(n_per_study), x,
                             alpha, sides, float(p0), power,
                             float(m or 20), float(icc or 0.05),
                             float(cluster_cv or 0.0))
        ys.append(k if k else float("nan"))
    ok = [(x, y) for x, y in zip(grid, ys) if y == y]
    if not ok:
        return ""
    xs = [p[0] for p in ok]
    yvs = [p[1] for p in ok]
    ymin = max(1.0, min(yvs) - 0.5)
    ymax = max(yvs) + 0.5
    ax = Axes(0.0, 0.95, ymin, ymax)

    body = [_polyline(ax, list(zip(xs, yvs)), C_BLUE)]
    presets = [0.0, 0.25, 0.5, 0.75, 0.9]
    for pv in presets:
        k = _meta_K_required(effect_type, float(effect), float(n_per_study), pv,
                             alpha, sides, float(p0), power,
                             float(m or 20), float(icc or 0.05),
                             float(cluster_cv or 0.0))
        if k:
            body.append(_dot(ax, pv, k, C_GREEN, 4.0))
    if i2_given:
        k0 = _meta_K_required(effect_type, float(effect), float(n_per_study),
                              min(float(i2_given), 0.95), alpha, sides,
                              float(p0), power, float(m or 20),
                              float(icc or 0.05), float(cluster_cv or 0.0))
        if k0:
            body.append(_dot(ax, min(float(i2_given), 0.95), k0, C_RED, 5.0))
            body.append(_label(ax, min(float(i2_given), 0.95), k0,
                               "I2=%g → K=%d" % (float(i2_given), k0),
                               C_RED, dy=-11, size=10.5, weight="600"))
    body.append(_legend([("K required", C_BLUE, None),
                         ("PASS 预设 I2", C_GREEN, None)], y0=PAD_T + 4))

    xt = {i / 10.0: "%.1f" % (i / 10.0) for i in range(0, 10)}
    yt = _nice_ticks(ymin, ymax, 6, "%d")
    title = "%s  |  所需研究数 K vs 异质性 I2（power=%g）  |  alpha=%g (%s)" % (
        test, power, alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title, "I2（异质性）", "Studies needed (K)",
                  xt, yt, "".join(body))


# ── 序贯边界（Lan-DeMets 消耗函数，闭式，零依赖）─────────────────────────

def _spend_obf(t, alpha):
    """O'Brien-Fleming-like spending: alpha(t) = 2(1 - Phi(z_{alpha/2}/sqrt(t)))."""
    if t <= 0:
        return 0.0
    return 2.0 * (1.0 - _phi(_norm_ppf(1.0 - alpha / 2.0) / math.sqrt(t)))


def _spend_pocock(t, alpha):
    """Pocock-like spending: alpha(t) = alpha * ln(1 + (e-1) t)."""
    if t <= 0:
        return 0.0
    return alpha * math.log1p((math.e - 1.0) * t)


def gs_boundaries(K=3, alpha=0.05, sides=2, kind="obf"):
    """Lan-DeMets 消耗函数法求各次期中分析的名义显著性水平与 z 边界。

    返回 [(info_frac, alpha_k, z_k, cum_alpha)]。
    零依赖、闭式——不需要 rpact / gsDesign，也不需要联网。
    """
    spend = _spend_obf if kind == "obf" else _spend_pocock
    out = []
    prev = 0.0
    for k in range(1, int(K) + 1):
        t = k / float(K)
        cum = spend(t, alpha)
        inc = cum - prev
        prev = cum
        z = _norm_ppf(1.0 - inc / sides) if inc > 0 else 8.0
        out.append((t, inc, min(z, 8.0), cum))
    return out


def fig_gs_boundary(test, power_fn, n_star, power_star, alpha, sides,
                    K=3, target_power=None, unit=None):
    """成组序贯：z 边界随信息分数下降（两侧对称，含 OBF / Pocock 对照）。"""
    K = max(2, min(9, int(K or 3)))
    obf = gs_boundaries(K, alpha, sides, "obf")
    poc = gs_boundaries(K, alpha, sides, "pocock")
    ymin, ymax = 0.0, max(max(z for _, _, z, _ in obf),
                          max(z for _, _, z, _ in poc)) * 1.16
    ax = Axes(0.0, 1.0, ymin, ymax)

    extra = []
    zf = _norm_ppf(1.0 - alpha / sides)
    if ymin <= zf <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(zf), W - PAD_R, ax.sy(zf), C_RED))
        extra.append(_label(ax, 0.0, zf, "固定设计 z=%.3f" % zf, C_RED,
                            dx=PAD_L - ax.sx(0.0) + 4, dy=-5, anchor="start",
                            size=10, weight="600"))

    body = []
    for data, col, lab, dash in ((obf, C_BLUE, "O'Brien-Fleming", None),
                                 (poc, C_ORANGE, "Pocock", "5,4")):
        pts = [(t, z) for t, _, z, _ in data]
        body.append(_polyline(ax, pts, col, width=2.3, dash=dash))
        for t, inc, z, _c in data:
            body.append(_dot(ax, t, z, col, 3.6))
            body.append(_label(ax, t, z, "%.2f" % z, col, dy=-8, size=9.5))
            body.append(_label(ax, t, ymin + (ymax - ymin) * 0.035,
                               "α=%.4f" % inc, C_MUTE, dy=0, size=9))
    body.append(_legend([("O'Brien-Fleming", C_BLUE, None),
                         ("Pocock", C_ORANGE, "5,4"),
                         ("固定设计临界值", C_RED, "6,4")], y0=PAD_T + 4))

    xt = {t: ("%d/%d" % (round(t * K), K)) for t in [k / float(K)
                                                     for k in range(1, K + 1)]}
    yt = _nice_ticks(ymin, ymax, 5, "%.2f")
    title = ("%s  |  序贯边界 z_k（K=%d，Lan-DeMets 消耗函数）  |  alpha=%g (%s)"
             % (test, K, alpha, "单侧" if sides == 1 else "双侧"))
    return _frame(ax, title, "信息分数（累计样本量占比）", "统计量边界 z",
                  xt, yt, "".join(extra) + "".join(body))


def fig_assurance_n(test, power_fn, n_star, power_star, alpha, sides,
                    target_power=None, unit=None):
    """贝叶斯：assurance / 后验成功概率 vs N（与频率派 power 同图对照）。"""
    scale = FAMILY_SCALE[power_fn.family]
    xs = _n_grid(n_star, scale)
    ys = [power_fn(x) for x in xs]
    ymin, ymax = max(0.0, min(ys) - 0.04), min(1.0, max(ys) + 0.05)
    ax = Axes(min(xs), max(xs), ymin, ymax)
    extra = []
    tp = target_power if target_power is not None else power_star
    if ymin <= tp <= ymax:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(tp), W - PAD_R, ax.sy(tp), C_RED))
    body = [_polyline(ax, list(zip(xs, ys)), C_PURPLE)]
    body.append(_dot(ax, n_star, power_star, C_RED, 4.6))
    body.append(_label(ax, n_star, power_star,
                       "n=%s, assurance=%.3f" % (_fmt(n_star), power_star),
                       C_RED, dy=-11, size=10.5, weight="600"))
    body.append(_legend([("assurance / 后验成功概率", C_PURPLE, None)],
                        y0=PAD_T + 4))
    xt = _nice_ticks(min(xs), max(xs), 6, "%g")
    yt = _nice_ticks(ymin, ymax, 5, "%g")
    title = "%s  |  assurance vs N  |  alpha=%g (%s)" % (
        test, alpha, "单侧" if sides == 1 else "双侧")
    return _frame(ax, title, unit or METHOD_N_UNIT.get(test, "每组样本量 n"),
                  "Assurance", xt, yt, "".join(extra) + "".join(body))


#: 图型 → 渲染函数
_RENDERERS = {
    "power_n": fig_power_n,
    "power_events": fig_power_n,        # 同一引擎，轴单位换为事件数
    "power_n_multi": fig_power_n_multi,
    "margin_tradeoff": fig_margin_tradeoff,
    "icc_sens": fig_icc_sens,
    "gs_boundary": fig_gs_boundary,
    "assurance_n": fig_assurance_n,
}


# ===========================================================================
# 6. 对外入口
# ===========================================================================

def _pick_n(meta: dict, test: str):
    """从 coze 返回的 stats 里挑出「N」——不同方法字段名不同。"""
    if not isinstance(meta, dict):
        return None
    # meta 可能为嵌套 {stats: {...}}
    cand = meta.get("stats") if isinstance(meta.get("stats"), dict) else meta
    prefer = ("n_per_group", "n_per_arm", "n_total", "n_pairs", "n_subjects",
              "n_per_dose", "n_treatment", "n_clusters", "events", "n")
    keys = set(cand.keys())
    for k in prefer:
        if k in keys:
            v = cand.get(k)
            if isinstance(v, (int, float)) and v > 0:
                return float(v)
    # 次选：任何以 n_ 开头的正数
    for k in sorted(keys):
        if k.startswith("n_") or k == "n":
            v = cand.get(k)
            if isinstance(v, (int, float)) and v > 0:
                return float(v)
    return None


def _pick_power(meta: dict):
    """从 coze 返回的 stats 里挑出「效能类」数值作为锚点的 Y 值。

    字段名按方法而异，且**契约登记的 output 名与实际返回名并不总是一致**：
    实测 assurance 返回的是 `assurance`（契约里写的是 assurance_prob），
    曾因此整条链路静默无图。故此处按优先序列举，宁可多列也别漏。
    """
    if not isinstance(meta, dict):
        return None
    cand = meta.get("stats") if isinstance(meta.get("stats"), dict) else meta
    for k in ("power", "achieved_power", "conditional_power",
              "assurance", "assurance_prob", "posterior_power", "prob_success"):
        v = cand.get(k)
        if isinstance(v, (int, float)) and 0.0 < float(v) < 1.0:
            return float(v)
    return None


def render_default_figures(test, meta, args=None, out_dir=None,
                           skip_primary=False):
    """为某方法生成默认图形，落盘并返回路径列表。

    Parameters
    ----------
    test         : 方法 id
    meta         : coze 返回的 stats/meta 字典（提供锚点数值）
    args         : argparse.Namespace（alpha / power / nobs / k_groups / icc / ...）
    out_dir      : 落盘目录，缺省取 CTSS_OUTPUT_DIR 或 ./outputs
    skip_primary : True 时只出专项副图（分配比/界值/ICC/序贯边界），不出
                   power-vs-N 主图。用于 coze 已返回权威曲线、避免重复。

    Returns
    -------
    list[str] 已写入的 SVG 绝对路径（失败返回 []，绝不抛异常）
    """
    if not _ALLOC_AVAILABLE:
        return []
    try:
        return _render_default_figures(test, meta, args, out_dir, skip_primary)
    except Exception:  # noqa: BLE001 - 图形层绝不阻断主结果
        return []


def _render_default_figures(test, meta, args, out_dir, skip_primary=False):
    n_star = _pick_n(meta, test)
    p_star = _pick_power(meta)
    if n_star is None or p_star is None:
        return []

    g = lambda name, default: (getattr(args, name, default) if args is not None
                               else default)
    alpha = float(g("alpha", 0.05) or 0.05)
    sides = 2 if str(g("side", "two")) == "two" else 1
    target = g("power", None)
    if target is not None:
        target = float(target)
        if not (0.0 < target < 1.0):
            target = None
    groups = int(g("k_groups", 2) or 2)
    icc = g("icc", 0.05)
    # 注意：CLI 里的簇大小参数名是 --m（不是 --cluster_size），期中分析次数是
    # --interim_looks（不是 --n_looks）——两者都取自 build_parser 的实际定义。
    m = g("m", 20)
    margin = g("margin", None)
    K = g("interim_looks", 3)
    nobs = g("nobs", None)

    power_fn = calibrate(test, n_star, p_star, alpha, sides, groups)
    if power_fn is None:
        return []

    primary, secondary = figure_plan(test)
    outdir = out_dir or os.environ.get("CTSS_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "outputs")
    os.makedirs(outdir, exist_ok=True)

    unit = METHOD_N_UNIT.get(test, "样本量 N")
    if primary == "power_events":
        unit = "事件数 D（Events）"
    kw = dict(test=test, power_fn=power_fn, n_star=n_star, power_star=p_star,
              alpha=alpha, sides=sides, target_power=target, unit=unit)

    written = []
    # ── 主图（coze 已返权威曲线或用户显式指定曲线时跳过，避免重复）──
    if not skip_primary:
        svg = ""
        if primary == "power_n_multi":
            svg = fig_power_n_multi(groups=groups, **kw)
        elif primary == "margin_tradeoff":
            svg = fig_margin_tradeoff(margin=margin, **kw)
        elif primary == "icc_sens":
            svg = fig_icc_sens(icc=icc, m=m, **kw)
        elif primary == "gs_boundary":
            svg = fig_gs_boundary(K=K, **kw)
        elif primary == "assurance_n":
            svg = fig_assurance_n(**kw)
        elif primary == "meta_hetero":
            svg = fig_meta_hetero(
                test=test, alpha=alpha, sides=sides,
                target_power=(target if target is not None else 0.8),
                effect_type=g("effect_type", "smd") or "smd",
                effect=g("effect", 0.3), n_per_study=g("n_per_study", 100),
                p0=g("p0", 0.3), m=g("m", 20), icc=g("icc", 0.05),
                cluster_cv=g("cluster_cv", 0.0), i2_given=g("i2", None))
        else:
            svg = fig_power_n(test=test, power_fn=power_fn, n_star=n_star,
                              power_star=p_star, alpha=alpha, sides=sides,
                              target_power=target, ref_n=nobs, unit=unit,
                              title_note=("事件数口径"
                                          if primary == "power_events" else ""))
        if svg:
            p = os.path.join(outdir, "ctss_%s_default_1.svg" % test)
            with io.open(p, "w", encoding="utf-8") as f:
                f.write(svg)
            written.append(p)

    # ── 副图：分配比四图（仅两独立组方法，复用 alloc_curve）──
    if secondary == "alloc_suite":
        written.extend(_render_alloc_suite(test, args, outdir,
                                           n_star=n_star, p_star=p_star,
                                           sides=sides) or [])
    elif secondary and secondary in _RENDERERS and secondary != primary:
        try:
            svg2 = _RENDERERS[secondary](**kw)
            if svg2:
                p = os.path.join(outdir, "ctss_%s_default_2.svg" % test)
                with io.open(p, "w", encoding="utf-8") as f:
                    f.write(svg2)
                written.append(p)
        except Exception:  # noqa: BLE001
            pass
    return written


def _first(args, names, default=None):
    """按候选名依次取第一个非 None 的属性值。

    必要性：CLI 存在 argparse 前缀缩写，属性名 ≠ 命令行名。实测 `--hr` 是
    `--hazard_ratio` 的缩写，解析后只有 `hazard_ratio` 有值，直接 getattr(
    args, "hr") 恒为 None —— 曾导致全部生存类方法的分配比副图静默不出。
    """
    if args is None:
        return default
    for n in names:
        v = getattr(args, n, None)
        if v is not None:
            return v
    return default


def _debug(msg):
    if os.environ.get("CTSS_FIGURE_DEBUG") == "1":
        print("# [figure_kit] %s" % msg)


#: 两独立组 z 族方法：无通用效应量参数（VE / 率比 / win ratio 各自口径不同），
#: 故效应量不由 CLI 参数给出，而是**从 R 返回的锚点反解** θ（ct-base §19.13）。
#: 这些方法与 ttest_ind / prop / logrank 并列，同样有分配比权衡问题。
_ALLOC_Z_TESTS = {"poisson", "vaccine_efficacy", "win_ratio"}

#: 上述方法中 n_star 口径为「总样本量 N」者（其余为每组 n）
_ALLOC_Z_TOTAL_N = {"win_ratio"}


def _render_alloc_suite(test, args, outdir, n_star=None, p_star=None, sides=2):
    """两独立组方法：调用 alloc_curve 生成分配比四图。

    只在能确定该方法的效应量（或能由锚点反解）时才生成 —— 否则曲线无依据，宁可不出图。
    """
    if not _ALLOC_AVAILABLE:
        return []
    try:
        import subprocess
        import sys as _sys
        here = os.path.dirname(os.path.abspath(__file__))
        cmd = [_sys.executable, os.path.join(here, "alloc_curve.py")]
        if test == "ttest_ind":
            d = _first(args, ("effect", "delta"), None)
            sd = _first(args, ("sd",), 1.0)
            if not d:
                _debug("ttest_ind 缺少 effect，跳过分配比图")
                return []
            cmd += ["--test", "ttest_ind",
                    "--delta", str(float(d) / float(sd or 1.0))]
        elif test in ("proportion_two", "odds_ratio", "risk_ratio"):
            p1 = _first(args, ("p1",), None)
            p2 = _first(args, ("p2",), None)
            if p1 is None or p2 is None:
                _debug("%s 缺少 p1/p2，跳过分配比图" % test)
                return []
            cmd += ["--test", "prop", "--p1", str(p1), "--p2", str(p2)]
        elif (test.startswith("survival")
              or test in ("ni_survival", "competing_risks", "recurrent_events")):
            # 注意：CLI 的 HR 参数名为 --hazard_ratio（--hr 只是其前缀缩写）
            hr = _first(args, ("hazard_ratio", "hr_expected", "sup_hr",
                               "cox_hr", "hr_exact"), None)
            if not hr or float(hr) <= 0:
                _debug("%s 缺少 hazard_ratio，跳过分配比图" % test)
                return []
            cmd += ["--test", "logrank", "--hr", str(float(hr))]
        elif test in _ALLOC_Z_TESTS:
            # 通用 z 族：θ 由 R 锚点反解（ct-base §19.13 锚点标定法）。
            # 这类方法（Poisson 率、疫苗效力、win ratio）效应量无统一尺度，
            # 只有锚点能给出绝对水平；曲线的 k 依赖形状则由 z 族结构唯一确定。
            if not n_star or n_star <= 0 or not p_star or not (0.0 < p_star < 1.0):
                _debug("%s 缺少锚点 (n*, power*)，跳过分配比图" % test)
                return []
            n_per_group = float(n_star) / 2.0 if test in _ALLOC_Z_TOTAL_N \
                else float(n_star)
            try:
                import alloc_curve as _ac   # noqa: PLC0415 - 延迟导入，与 _ALLOC_AVAILABLE 同步
                theta = _ac.theta_from_anchor(
                    n_per_group, p_star,
                    float(_first(args, ("alpha",), 0.05) or 0.05),
                    int(sides or 2))
            except Exception as _e:  # noqa: BLE001
                _debug("%s θ 标定失败，跳过分配比图: %r" % (test, _e))
                return []
            cmd += ["--test", "z", "--theta", "%.10g" % theta]
        else:
            return []
        # 按方法名隔离文件名前缀：否则 13 个两独立组方法会互相覆盖同一组
        # ctss_alloc_*.svg（实测 68 张里只剩 4 张 alloc 图，即此 bug）。
        prefix = "ctss_alloc_%s" % test
        cmd += ["--power", str(_first(args, ("power",), 0.8) or 0.8),
                "--alpha", str(_first(args, ("alpha",), 0.05) or 0.05),
                "--prefix", prefix,
                "--out-dir", outdir]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            _debug("alloc_curve 退出码 %d: %s"
                   % (r.returncode, (r.stderr or "").strip()[-300:]))
            return []
        import glob
        return sorted(glob.glob(os.path.join(outdir, prefix + "_*.svg")))
    except Exception as _e:  # noqa: BLE001
        _debug("分配比图生成异常: %r" % (_e,))
        return []


# ===========================================================================
# 7. CLI 入口（coze 内部兜底调用）
# ===========================================================================
# 本文件随包上传到 coze，作为「R 主出图模块 coze_figure_layer.R 故障时的 coze
# 内部兜底」。coze 端 Python（coze_fallback.py）在 R 模块未产出图形时，
# 通过本入口重算 SVG 并写回同一捕获目录，使下游 figures 收集逻辑无需改动。
# 本地主流程已不再调用本模块（v5.6 起绘图全部上 coze），本地仅作离线调试用。

def _build_cli_args(ns):
    """把 argparse 解析结果整理成 render_default_figures 期望的命名空间。"""
    import argparse as _ap
    a = _ap.Namespace()
    for k in ("alpha", "side", "power", "k_groups", "icc", "m", "margin",
              "interim_looks", "nobs", "effect", "sd", "p1", "p2",
              "hazard_ratio", "hr_expected", "sup_hr", "cox_hr", "hr_exact"):
        if hasattr(ns, k):
            setattr(a, k, getattr(ns, k))
    if not hasattr(a, "side"):
        setattr(a, "side", "two")
    return a


def _parse_meta_arg(raw):
    """支持内联 JSON 或 @文件路径。"""
    import json as _json
    if raw is None:
        return {}
    s = raw
    if isinstance(raw, str) and raw.startswith("@"):
        with io.open(raw[1:], "r", encoding="utf-8") as fh:
            s = fh.read()
    try:
        return _json.loads(s)
    except Exception:
        return {}


def _cli_main(argv=None):
    import argparse as _ap
    import json as _json
    p = _ap.ArgumentParser(
        description="ct-samplesize figure_kit — coze 内部兜底出图")
    p.add_argument("--test", required=True)
    p.add_argument("--meta", required=True,
                   help="coze 返回 stats 的 JSON 字符串，或 @文件路径")
    p.add_argument("--out-dir", default=os.environ.get("CTSS_OUTPUT_DIR",
                                                       os.path.join(os.getcwd(),
                                                                     "outputs")))
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--side", choices=["one", "two"], default="two")
    p.add_argument("--power", type=float, default=None)
    p.add_argument("--k-groups", type=int, default=2)
    p.add_argument("--icc", type=float, default=0.05)
    p.add_argument("--m", type=float, default=20)
    p.add_argument("--margin", type=float, default=None)
    p.add_argument("--interim-looks", type=int, default=3)
    p.add_argument("--nobs", type=int, default=None)
    p.add_argument("--effect", type=float, default=None)
    p.add_argument("--sd", type=float, default=None)
    p.add_argument("--p1", type=float, default=None)
    p.add_argument("--p2", type=float, default=None)
    p.add_argument("--hazard-ratio", dest="hazard_ratio", type=float,
                   default=None)
    ns = p.parse_args(argv)
    meta = _parse_meta_arg(ns.meta)
    args = _build_cli_args(ns)
    out = render_default_figures(ns.test, meta, args, out_dir=ns.out_dir,
                                skip_primary=False)
    # 输出 JSON 行，便于 coze_fallback.py 判断成败
    print(_json.dumps({"test": ns.test, "figures": out, "count": len(out)}))
    return 0 if out else 1


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(_cli_main())
