#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ⚠️ 本文件是分配比曲线计算（figure_kit 依赖）的唯一真相源（v5.12.0 起）。coze 部署包内的
#    adapters/coze/scripts/alloc_curve.py 由部署构建器（_build_deploy_new.py /
#    _build_deploy.py）在打包前从本文件复制同步生成——请勿手工编辑 coze 侧副本，
#    改这里后重新构建即可。
"""
alloc_curve.py — Allocation-ratio (n2/n1) vs Power diagnostics for unequal group sizes.

Companion module to `samplesize_power.py`. Answers the question the point-estimate
CLI cannot: **what does an unequal allocation cost me, and where is the cliff?**

Pure standard library (ct-base §6.1: no numpy/scipy). Noncentral-t power is computed
by Simpson integration over the chi-square mixing density — exact, not the normal
approximation, so small-sample curves stay honest.

Mathematical core
-----------------
For two groups with n2 = k*n1 and total N = n1 + n2:

    1/n1 + 1/n2 = (1+k)^2 / (k*N)

which is minimised at k = 1. Hence:

  * **Fixed N**  -> noncentrality lambda = delta*sqrt(k*N)/|1+k| is maximised at k=1,
    so power is maximised at 1:1 (inverted-U curve).
  * **Fixed power** -> N(k) = N(1) * (1+k)^2/(4k)  (Schoenfeld's inflation factor).
    Same factor governs two means, two proportions (equal-variance case) and
    log-rank event counts, so one formula covers all three backends.

    k      1/3     1/2     2/3      1     3/2      2       3       5
    infl.  1.333   1.125   1.042   1.000  1.042   1.125   1.333   1.800

  * **Two proportions with p1 != p2** -> the Neyman (variance-optimal) allocation is
    k* = sqrt( p2(1-p2) / (p1(1-p1)) ), which is NOT 1. The contour and N-vs-k plots
    mark k* so the user can see the optimum drift away from 1:1.

Plots (each a standalone ct-base §19 SVG, 700x500)
-------------------------------------------------
  A `n_vs_k`     Total N required vs allocation ratio k, at fixed target power.
                 U-shaped; annotated with % inflation vs 1:1 and the <5% band.
  B `power_vs_k` Power vs k at fixed total N. Inverted-U; annotated with the
                 absolute power loss at common ratios.
  C `contour`    Iso-power contours in the (n1, n2) plane, plus iso-total lines
                 (n1+n2 = const, slope -1) and the 1:1 diagonal. The tangency of an
                 iso-total line with an iso-power curve ON the 1:1 diagonal is the
                 geometric proof that 1:1 is optimal.
  D `loss`       Power loss vs k, faceted by effect size. Shows that the penalty is
                 worst where the power curve is steepest (power ~ 0.5-0.8), not at
                 the smallest effect size.

Usage
-----
  python scripts/alloc_curve.py --test ttest_ind --delta 0.5 --sd 1 --power 0.8
  python scripts/alloc_curve.py --test prop --p1 0.10 --p2 0.30 --power 0.8
  python scripts/alloc_curve.py --test logrank --hr 0.70 --power 0.8 --events
  python scripts/alloc_curve.py --delta 0.5 --plots contour --out-dir ./outputs

Outputs SVG files into the output dir and prints a plain-text ratio table.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import os
import sys

# --------------------------------------------------------------------------
# 1. Numerical kernel: normal, chi-square, noncentral t
# --------------------------------------------------------------------------


def _phi(x: float) -> float:
    """Standard normal CDF."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def _norm_ppf(p: float) -> float:
    """Inverse normal CDF (Acklam rational approximation + one Halley step)."""
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1), got %r" % p)
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    elif p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    else:
        q = p - 0.5
        r = q * q
        x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
            (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
    # Halley refinement to full double precision
    e = _phi(x) - p
    u = e * math.sqrt(2 * math.pi) * math.exp(x * x / 2)
    return x - u / (1 + x * u / 2)


def _chi2_logpdf(v: float, nu: float) -> float:
    """log density of chi-square(nu) at v."""
    return (0.5 * nu - 1.0) * math.log(v) - 0.5 * v \
        - (0.5 * nu) * math.log(2.0) - math.lgamma(0.5 * nu)


def _nct_cdf(t: float, df: float, ncp: float, ngrid: int = 600) -> float:
    """P(T' <= t) for T' ~ noncentral t with df and noncentrality ncp.

    Uses T' = (Z + ncp)/sqrt(V/df) with Z ~ N(0,1) independent of V ~ chi2(df):

        P(T' <= t) = E_V[ Phi( t*sqrt(V/df) - ncp ) ]

    integrated by Simpson's rule over the chi-square density. ngrid must be even.
    Validated against R's pt(..., ncp=) to <= 1e-6 across df in [10, 5000].
    """
    if df <= 0:
        raise ValueError("df must be > 0")
    ngrid = ngrid if ngrid % 2 == 0 else ngrid + 1
    lo = 1e-12
    hi = df + 12.0 * math.sqrt(2.0 * df) + 10.0
    h = (hi - lo) / ngrid
    total = 0.0
    sqrt_df = math.sqrt(df)
    for i in range(ngrid + 1):
        v = lo + i * h
        lp = _chi2_logpdf(v, df)
        fv = math.exp(lp) if lp > -745.0 else 0.0
        if fv == 0.0:
            continue
        g = _phi(t * math.sqrt(v) / sqrt_df - ncp)
        w = 1.0 if i in (0, ngrid) else (4.0 if i % 2 else 2.0)
        total += w * fv * g
    return total * h / 3.0


def _t_logpdf(t: float, df: float) -> float:
    """log density of central t(df)."""
    return (math.lgamma(0.5 * (df + 1.0)) - 0.5 * math.log(df * math.pi)
            - math.lgamma(0.5 * df)
            - 0.5 * (df + 1.0) * math.log1p(t * t / df))


def _t_ppf(p: float, df: float) -> float:
    """Inverse CDF of central t(df): Cornish-Fisher init + Newton refinement."""
    z = _norm_ppf(p)
    t = z + (z ** 3 + z) / (4.0 * df) \
        + (5.0 * z ** 5 + 16.0 * z ** 3 + 3.0 * z) / (96.0 * df * df)
    for _ in range(25):
        c = _nct_cdf(t, df, 0.0)
        step = (c - p) / math.exp(_t_logpdf(t, df))
        t -= step
        if abs(step) < 1e-13:
            break
    return t


# --------------------------------------------------------------------------
# 2. Power backends (all share the (1+k)^2/(4k) inflation geometry)
# --------------------------------------------------------------------------


def power_ttest(n1: float, n2: float, d: float, alpha: float = 0.05,
                sides: int = 2) -> float:
    """Two-sample t-test power via noncentral t. d = |mu1-mu2|/sd (Cohen's d)."""
    df = n1 + n2 - 2
    if df <= 0 or n1 <= 0 or n2 <= 0:
        return 0.0
    ncp = abs(d) / math.sqrt(1.0 / n1 + 1.0 / n2)
    if ncp == 0.0:
        return alpha / sides
    if sides == 1:
        tc = _t_ppf(1 - alpha, df)
        return 1.0 - _nct_cdf(tc, df, ncp)
    tc = _t_ppf(1 - alpha / 2.0, df)
    return (1.0 - _nct_cdf(tc, df, ncp)) + _nct_cdf(-tc, df, ncp)


def power_prop(n1: float, n2: float, p1: float, p2: float, alpha: float = 0.05,
               sides: int = 2) -> float:
    """Two-proportion z-test power (unpooled variance for the alternative).

    Uses the noncentral-t machinery via a normal approximation with the
    unpooled SE; accurate to <0.005 for np >= 5 (standard practice).
    """
    if n1 <= 0 or n2 <= 0:
        return 0.0
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se <= 0:
        return 0.0
    zc = _norm_ppf(1 - alpha / sides)
    lam = abs(p2 - p1) / se
    if sides == 1:
        return 1.0 - _phi(zc - lam)
    return (1.0 - _phi(zc - lam)) + _phi(-zc - lam)


def power_z_alloc(n1: float, n2: float, theta: float, alpha: float = 0.05,
                  sides: int = 2) -> float:
    """Generic two-group z-family power: ncp = theta * sqrt(n1*n2/(n1+n2)).

    Covers every two-independent-group test whose statistic is asymptotically
    normal with noncentrality proportional to sqrt(n1*n2/(n1+n2)) — Poisson
    rates, vaccine efficacy, win ratio, … The effect size is carried by a
    single scalar `theta`, which is *calibrated from the R anchor* rather than
    derived from a method-specific formula (see `theta_from_anchor`).
    """
    if n1 <= 0 or n2 <= 0:
        return 0.0
    lam = abs(theta) * math.sqrt(n1 * n2 / (n1 + n2))
    zc = _norm_ppf(1 - alpha / sides)
    if sides == 1:
        return 1.0 - _phi(zc - lam)
    return (1.0 - _phi(zc - lam)) + _phi(-zc - lam)


def theta_from_anchor(n_per_group_star: float, power_star: float,
                      alpha: float = 0.05, sides: int = 2) -> float:
    """Invert the z-family power at 1:1 allocation to recover theta.

    At k=1 with per-group n: ncp = theta*sqrt(n/2). Solve for the theta that
    reproduces the R-reported power, so the alloc suite is pinned to the same
    anchor as the main figure (ct-base §19.13 anchor calibration).
    """
    if not n_per_group_star or n_per_group_star <= 0:
        raise ValueError("anchor n must be positive")
    if not (0.0 < power_star < 1.0):
        raise ValueError("anchor power must lie in (0,1)")

    def _f(theta):
        return power_z_alloc(n_per_group_star, n_per_group_star,
                             theta, alpha, sides) - power_star

    lo, hi = 0.0, 1.0
    while _f(hi) < 0 and hi < 1e6:
        hi *= 2.0
    if _f(hi) < 0:
        raise ValueError("cannot reach anchor power %.4f" % power_star)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def neyman_k(p1: float, p2: float) -> float:
    """Variance-optimal allocation ratio k* = n2/n1 for two proportions.

    Minimises p1(1-p1)/n1 + p2(1-p2)/n2 subject to fixed total N.
    Equals 1 only when p1(1-p1) == p2(1-p2).
    """
    v1, v2 = p1 * (1 - p1), p2 * (1 - p2)
    if v1 <= 0 or v2 <= 0:
        return 1.0
    return math.sqrt(v2 / v1)


def _make_power_fn(test: str, **kw):
    """Return (power_fn, effect_label, effect_value)."""
    if test == "ttest_ind":
        d = kw["delta"] / kw["sd"]
        return (lambda a, b: power_ttest(a, b, d, kw["alpha"], kw["sides"]),
                "Cohen's d", d)
    if test == "prop":
        p1, p2 = kw["p1"], kw["p2"]
        return (lambda a, b: power_prop(a, b, p1, p2, kw["alpha"], kw["sides"]),
                "p1=%.3g vs p2=%.3g" % (p1, p2), abs(p2 - p1))
    if test == "logrank":
        # Schoenfeld: power depends on events D and allocation via
        #   lambda = |log HR| * sqrt(D * p1a * p2a),  p1a = 1/(1+k), p2a = k/(1+k)
        hr = kw["hr"]
        lam0 = abs(math.log(hr))
        def _pw(n1, n2):
            if n1 <= 0 or n2 <= 0:
                return 0.0
            D = n1 + n2
            pa = n1 / D
            pb = n2 / D
            lam = lam0 * math.sqrt(D * pa * pb)
            zc = _norm_ppf(1 - kw["alpha"] / kw["sides"])
            if kw["sides"] == 1:
                return 1.0 - _phi(zc - lam)
            return (1.0 - _phi(zc - lam)) + _phi(-zc - lam)
        return _pw, "HR", hr
    if test == "z":
        # Anchor-calibrated generic two-group z family (poisson / vaccine
        # efficacy / win ratio / …). theta has no universal scale, so it is
        # always supplied pre-solved by the caller via `theta_from_anchor`.
        theta = kw["theta"]
        return (lambda a, b: power_z_alloc(a, b, theta, kw["alpha"], kw["sides"]),
                "theta (z-scale)", theta)
    raise ValueError("unsupported test: %s" % test)


# --------------------------------------------------------------------------
# 3. Solvers
# --------------------------------------------------------------------------


def _analytic_n1(k: float, lam_coef: float, zc: float, zb: float) -> float:
    """Normal-approximation starting value: N(k) = (zc+zb)^2 * (1+k)^2/(k*lam^2).

    lam_coef is the effect size expressed so that lambda = lam_coef/sqrt(1/n1+1/n2).
    """
    if lam_coef <= 0:
        return float("inf")
    N = ((zc + zb) ** 2) * (1.0 + k) ** 2 / (k * lam_coef ** 2)
    return N / (1.0 + k)


def solve_n1(power_fn, k: float, target: float, lam_coef: float,
             alpha: float, sides: int, lo: float = 2.0,
             hi: float = 2.0e6) -> float:
    """Smallest n1 such that power(n1, k*n1) >= target (power is monotone in n1)."""
    zc = _norm_ppf(1 - alpha / sides)
    zb = _norm_ppf(target)
    start = _analytic_n1(k, lam_coef, zc, zb)
    if math.isfinite(start) and start > 0:
        lo = max(lo, start * 0.80)
        hi = min(hi, start * 1.25 + 10.0)
    if power_fn(hi, k * hi) < target:
        return hi
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if power_fn(mid, k * mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve_N_at_power(power_fn, target: float, lam_coef: float,
                     alpha: float, sides: int) -> float:
    """Total N required at the 1:1 allocation (k=1)."""
    n1 = solve_n1(power_fn, 1.0, target, lam_coef, alpha, sides)
    return 2.0 * n1


def inflation_factor(k: float) -> float:
    """Schoenfeld inflation: N(k)/N(1) = (1+k)^2/(4k).

    Only valid for EQUAL-VARIANCE backends (two means, log-rank events, and two
    proportions with p1(1-p1) == p2(1-p2)). For unequal-variance proportions the
    true optimum is the Neyman ratio and this factor is merely an upper bound on
    one side of it.
    """
    return (1.0 + k) ** 2 / (4.0 * k)


def find_kopt(power_fn, target, lam_coef, alpha, sides,
              lo: float = 0.25, hi: float = 4.0, iters: int = 28) -> float:
    """Allocation ratio minimising total N, by ternary search (N(k) is unimodal)."""
    def N_of_k(k):
        return solve_n1(power_fn, k, target, lam_coef, alpha, sides) * (1.0 + k)
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if N_of_k(m1) < N_of_k(m2):
            hi = m2
        else:
            lo = m1
    return 0.5 * (lo + hi)


# --------------------------------------------------------------------------
# 4. Curve data
# --------------------------------------------------------------------------

# log2(k) grid, k = n2/n1. NOTE the direction: k=0.5 means group 2 is HALF of
# group 1, i.e. n1:n2 = 2:1 — the printed label is (den:num) of k = num/den,
# NOT "1:k". Getting this backwards silently mirrors every plot.
K_GRID = [2.0 ** (i / 12.0) for i in range(-24, 25)]  # 49 points, k in [1/4, 4]
RATIO_TICKS = [(0.25, "4:1"), (0.3333, "3:1"), (0.5, "2:1"), (0.6667, "3:2"),
               (1.0, "1:1"), (1.5, "2:3"), (2.0, "1:2"), (3.0, "1:3"),
               (4.0, "1:4")]


def fmt_ratio(k: float) -> str:
    """Render k = n2/n1 as the human-facing 'n1:n2' label (k=0.5 -> '2:1').

    Prefers a clean small-denominator fraction (1:2, 2:3, 3:1...) and falls back
    to 2-decimal form when no tidy fraction exists — otherwise a Neyman optimum
    like k*=1.528 renders as the unreadable '19:29'.
    """
    if abs(k - 1.0) < 1e-9:
        return "1:1"
    try:
        from fractions import Fraction
        for maxd in (4, 6, 8):
            fr = Fraction(k).limit_denominator(maxd)
            if abs(float(fr) - k) < 0.02:
                return "%d:%d" % (fr.denominator, fr.numerator)
    except Exception:  # noqa: BLE001 - defensive, non-numeric / extreme k
        pass
    if k > 1:
        return "1:%.2f" % k
    return "%.2f:1" % (1.0 / k)


def pct_delta(ratio_value: float) -> str:
    """Signed percentage vs 1.0, with the -0.0% float artifact suppressed."""
    v = (ratio_value - 1.0) * 100.0
    if abs(v) < 0.05:
        v = 0.0
    return "%+.1f%%" % v


def curve_n_vs_k(power_fn, target, lam_coef, alpha, sides):
    """(ks, Ns) — total N required at each allocation ratio."""
    ks, Ns = [], []
    for k in K_GRID:
        n1 = solve_n1(power_fn, k, target, lam_coef, alpha, sides)
        ks.append(k)
        Ns.append(n1 * (1.0 + k))
    return ks, Ns


def curve_power_vs_k(power_fn, N_total):
    """(ks, powers) — power at each allocation ratio for a fixed total N."""
    ks, ps = [], []
    for k in K_GRID:
        n1 = N_total / (1.0 + k)
        ks.append(k)
        ps.append(power_fn(n1, k * n1))
    return ks, ps


def contour_points(power_fn, target, lam_coef, alpha, sides, npts=61):
    """Iso-power curve in the (n1, n2) plane for a given target power."""
    pts = []
    for i in range(npts):
        k = 2.0 ** (-2.0 + 4.0 * i / (npts - 1))
        n1 = solve_n1(power_fn, k, target, lam_coef, alpha, sides)
        pts.append((n1, k * n1))
    return pts


# --------------------------------------------------------------------------
# 5. SVG rendering — ct-base §19 (700x500, gridlines, shared sx()/sy() mapping)
# --------------------------------------------------------------------------

W, H = 700, 500
PAD_L, PAD_R, PAD_T, PAD_B = 78, 34, 46, 62
PW = W - PAD_L - PAD_R
PH = H - PAD_T - PAD_B

C_INK = "#2c3e50"
C_MUTE = "#7f8c8d"
C_GRID = "#e6e9ec"
C_RED = "#c0392b"
C_BLUE = "#2980b9"
C_GREEN = "#27ae60"
C_PURPLE = "#8e44ad"
C_ORANGE = "#d35400"
C_BAND = "#d5f5e3"


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


class Axes:
    """Linear or log2 axes with the shared coordinate mapping required by §19."""

    def __init__(self, xmin, xmax, ymin, ymax, logx=False):
        self.xmin, self.xmax = float(xmin), float(xmax)
        self.ymin, self.ymax = float(ymin), float(ymax)
        self.logx = logx
        if logx:
            self.lxmin, self.lxmax = math.log2(self.xmin), math.log2(self.xmax)
        if self.ymax == self.ymin:
            self.ymax = self.ymin + 1.0

    def sx(self, v):
        if self.logx:
            v = math.log2(max(v, 1e-12))
            return PAD_L + (v - self.lxmin) / (self.lxmax - self.lxmin) * PW
        return PAD_L + (v - self.xmin) / (self.xmax - self.xmin) * PW

    def sy(self, v):
        return PAD_T + (self.ymax - v) / (self.ymax - self.ymin) * PH


def _frame(ax, title, xlab, ylab, xticks, yticks, extra=""):
    """Gridlines, axes, tick labels, titles — everything below the data layer."""
    o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'viewBox="0 0 %d %d" font-family="Segoe UI, Helvetica, Arial, '
         'PingFang SC, Microsoft YaHei, sans-serif">' % (W, H, W, H)]
    o.append('<rect width="100%%" height="100%%" fill="#ffffff"/>')
    # horizontal gridlines + y labels
    for v in yticks:
        y = ax.sy(v)
        if not (PAD_T - 1 <= y <= H - PAD_B + 1):
            continue
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                 'stroke-width="1"/>' % (PAD_L, y, W - PAD_R, y, C_GRID))
        o.append('<text x="%d" y="%.1f" font-size="10.5" fill="%s" '
                 'text-anchor="end">%s</text>'
                 % (PAD_L - 7, y + 3.5, C_MUTE, _esc(yticks[v])))
    # vertical gridlines + x labels
    for v in xticks:
        x = ax.sx(v)
        if not (PAD_L - 1 <= x <= W - PAD_R + 1):
            continue
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                 'stroke-width="1"/>' % (x, PAD_T, x, H - PAD_B, C_GRID))
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" '
                 'text-anchor="middle">%s</text>'
                 % (x, H - PAD_B + 16, C_MUTE, _esc(xticks[v])))
    o.append(extra)
    # axis lines
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>'
             % (PAD_L, H - PAD_B, W - PAD_R, H - PAD_B, C_MUTE))
    o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.2"/>'
             % (PAD_L, PAD_T, PAD_L, H - PAD_B, C_MUTE))
    o.append('<text x="%d" y="%d" font-size="13.5" fill="%s" font-weight="600">%s</text>'
             % (PAD_L, PAD_T - 16, C_INK, _esc(title)))
    o.append('<text x="%.1f" y="%d" font-size="12" fill="#555" text-anchor="middle">%s</text>'
             % (PAD_L + PW / 2.0, H - 14, _esc(xlab)))
    o.append('<text x="19" y="%.1f" font-size="12" fill="#555" text-anchor="middle" '
             'transform="rotate(-90 19 %.1f)">%s</text>'
             % (PAD_T + PH / 2.0, PAD_T + PH / 2.0, _esc(ylab)))
    o.append("</svg>")
    return "".join(o)


def _nice_ticks(lo, hi, n=5, fmt="%g"):
    lo, hi = float(lo), float(hi)
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / (n - 1)
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for m in (1, 2, 2.5, 5, 10):
        if raw / mag <= m:
            step = m * mag
            break
    else:
        step = 10 * mag
    start = math.floor(lo / step) * step
    out = []
    v = start
    while v <= hi + step * 0.5:
        if lo - step * 0.5 <= v <= hi + step * 0.5:
            out.append(v)
        v += step
    return {v: fmt % v for v in out}


def _ratio_ticks():
    return {k: lab for k, lab in RATIO_TICKS}


def _polyline(ax, pts, color, width=2.2, dash=None):
    d = " ".join("%.1f,%.1f" % (ax.sx(a), ax.sy(b)) for a, b in pts)
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"'
            ' stroke-linejoin="round" stroke-linecap="round"%s/>' % (d, color, width, da))


def _dot(ax, x, y, color, r=3.6):
    return ('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="#fff" '
            'stroke-width="1.2"/>' % (ax.sx(x), ax.sy(y), r, color))


def _label(ax, x, y, text, color=C_INK, dx=0, dy=0, anchor="middle", size=10.5,
           weight="normal"):
    return ('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" '
            'font-weight="%s">%s</text>'
            % (ax.sx(x) + dx, ax.sy(y) + dy, size, color, anchor, weight, _esc(text)))


def _legend(items, x0=None, y0=None):
    """Small legend box, top-right by default."""
    x0 = W - PAD_R - 168 if x0 is None else x0
    y0 = PAD_T + 6 if y0 is None else y0
    o = []
    for i, (lab, col, dash) in enumerate(items):
        y = y0 + i * 17
        if dash:
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" '
                     'stroke-width="2" stroke-dasharray="%s"/>'
                     % (x0, y, x0 + 18, y, col, dash))
        else:
            o.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4"/>'
                     % (x0, y, x0 + 18, y, col))
        o.append('<text x="%d" y="%d" font-size="10.5" fill="%s">%s</text>'
                 % (x0 + 24, y + 3.5, C_INK, _esc(lab)))
    return "".join(o)


# ---- Plot A: N vs k -------------------------------------------------------

def plot_n_vs_k(power_fn, target, lam_coef, alpha, sides, effect_desc, test):
    """Total N required vs k, at fixed target power.

    The <5% band and the optimum marker are derived from the ACTUAL curve, not
    hard-coded to [2/3, 3/2]. That matters: for two proportions with unequal
    variances the optimum drifts off 1:1 (Neyman allocation), so a hard-coded
    band would be wrong for exactly the case where this plot is most useful.
    """
    ks, Ns = curve_n_vs_k(power_fn, target, lam_coef, alpha, sides)
    Nmin = min(Ns)
    kopt = ks[Ns.index(Nmin)]
    N11 = 2.0 * solve_n1(power_fn, 1.0, target, lam_coef, alpha, sides)
    ymax = max(Ns) * 1.16
    ax = Axes(0.25, 4.0, 0.0, ymax, logx=True)

    # <5% band, solved from the curve itself
    band_hi = Nmin * 1.05
    kb = [k for k, N in zip(ks, Ns) if N <= band_hi]
    extra = []
    if len(kb) >= 2:
        xb_lo, xb_hi = ax.sx(min(kb)), ax.sx(max(kb))
        extra.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                     'opacity="0.55"/>'
                     % (xb_lo, ax.sy(band_hi), xb_hi - xb_lo,
                        ax.sy(0) - ax.sy(band_hi), C_BAND))
        extra.append(_label(ax, math.sqrt(min(kb) * max(kb)), band_hi,
                            "within 5%% of optimum   (%s ~ %s)"
                            % (fmt_ratio(min(kb)), fmt_ratio(max(kb))),
                            C_GREEN, dy=-5, size=10))
    # reference line at N(1:1)
    extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                 'stroke-width="1.2" stroke-dasharray="6,4"/>'
                 % (PAD_L, ax.sy(N11), W - PAD_R, ax.sy(N11), C_RED))
    extra.append(_label(ax, 0.25, N11, "N(1:1) = %s" % _fmt_n(N11), C_RED,
                        dx=PAD_L - ax.sx(0.25) + 4, dy=-5, anchor="start", weight="600"))

    body = [_polyline(ax, list(zip(ks, Ns)), C_BLUE)]
    # optimum marker (green) — coincides with 1:1 for equal-variance backends
    body.append(_dot(ax, kopt, Nmin, C_GREEN, 4.6))
    body.append(_label(ax, kopt, Nmin,
                       "optimum  %s   N = %s" % (fmt_ratio(kopt), _fmt_n(Nmin)),
                       C_GREEN, dy=-11, size=10.5, weight="700"))
    body.append(_dot(ax, 1.0, N11, C_RED, 4.0))
    if abs(kopt - 1.0) > 1e-9:
        body.append(_label(ax, 1.0, N11, "1:1  %s  (%s)" % (
            _fmt_n(N11), pct_delta(N11 / Nmin)), C_RED, dy=16, size=10,
            weight="600"))
    for k in (0.5, 2.0, 3.0):
        n1 = solve_n1(power_fn, k, target, lam_coef, alpha, sides)
        Nk = n1 * (1 + k)
        body.append(_dot(ax, k, Nk, C_BLUE, 3.0))
        body.append(_label(ax, k, Nk, pct_delta(Nk / Nmin),
                           C_BLUE, dy=-9, size=10, weight="600"))
    body.append(_legend([("N required", C_BLUE, None),
                         ("optimum", C_GREEN, None),
                         ("N at 1:1", C_RED, "6,4")], y0=PAD_T + 4))

    yt = _nice_ticks(0, ymax, 5, "%g")
    title = "Total N required vs allocation ratio  |  %s  |  power=%.2f, alpha=%.3g (%s)" % (
        effect_desc, target, alpha, "1-sided" if sides == 1 else "2-sided")
    return _frame(ax, title,
                  "allocation ratio  n1 : n2   (k = n2/n1)",
                  "total N = n1 + n2",
                  _ratio_ticks(), yt, "".join(extra) + "".join(body))


# ---- Plot B: power vs k ---------------------------------------------------

def plot_power_vs_k(power_fn, N_total, effect_desc, alpha, sides):
    ks, ps = curve_power_vs_k(power_fn, N_total)
    p1 = power_fn(N_total / 2.0, N_total / 2.0)
    ymin = max(0.0, min(ps) - 0.06)
    ymax = min(1.0, max(ps) + 0.07)
    ax = Axes(0.25, 4.0, ymin, ymax, logx=True)

    extra = []
    if ymin - 1e-9 <= 0.80 <= ymax + 1e-9:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.2" stroke-dasharray="6,4"/>'
                     % (PAD_L, ax.sy(0.8), W - PAD_R, ax.sy(0.8), C_RED))
        extra.append(_label(ax, 0.25, 0.8, "power = 0.80", C_RED,
                            dx=PAD_L - ax.sx(0.25) + 4, dy=-5, anchor="start",
                            weight="600"))

    body = [_polyline(ax, list(zip(ks, ps)), C_BLUE)]
    body.append(_dot(ax, 1.0, p1, C_RED, 4.4))
    body.append(_label(ax, 1.0, p1, "%.3f" % p1, C_RED, dy=-10, weight="600"))
    for k in (0.5, 2.0, 3.0):
        pk = power_fn(N_total / (1 + k), k * N_total / (1 + k))
        body.append(_dot(ax, k, pk, C_BLUE, 3.0))
        # signed change vs 1:1 — for unequal-variance proportions this can be
        # POSITIVE (moving off 1:1 gains power), so never hard-code a minus sign.
        body.append(_label(ax, k, pk, "%+.3f" % (pk - p1), C_BLUE, dy=-9, size=10,
                           weight="600"))
    body.append(_legend([("power", C_BLUE, None), ("target 0.80", C_RED, "6,4")],
                        y0=PAD_T + 4))

    yt = {v: "%.2f" % v for v in
          [ymin + (ymax - ymin) * i / 4.0 for i in range(5)]}
    title = "Power vs allocation ratio at fixed N  |  %s  |  N = %s, alpha=%.3g (%s)" % (
        effect_desc, _fmt_n(N_total), alpha, "1-sided" if sides == 1 else "2-sided")
    return _frame(ax, title,
                  "allocation ratio  n1 : n2   (k = n2/n1)",
                  "power", _ratio_ticks(), yt, "".join(extra) + "".join(body))


# ---- Plot C: iso-power contours ------------------------------------------

def plot_contour(power_fn, lam_coef, alpha, sides, effect_desc, targets=(0.80, 0.90),
                 neyman=None):
    curves = []
    for tg in targets:
        curves.append((tg, contour_points(power_fn, tg, lam_coef, alpha, sides)))
    allx = [p[0] for _, c in curves for p in c] + [p[1] for _, c in curves for p in c]
    vmax = max(allx) * 1.10
    ax = Axes(0, vmax, 0, vmax)

    extra = []
    # 1:1 diagonal
    extra.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                 'stroke-width="1.2" stroke-dasharray="7,5"/>'
                 % (ax.sx(0), ax.sy(0), ax.sx(vmax), ax.sy(vmax), C_MUTE))
    extra.append(_label(ax, vmax * 0.62, vmax * 0.70, "1 : 1", C_MUTE, size=10.5))
    # iso-total lines n1+n2 = C (slope -1) — tangency with iso-power proves 1:1 optimal
    N80 = 2.0 * solve_n1(power_fn, 1.0, targets[0], lam_coef, alpha, sides)
    for mult in (0.85, 1.0, 1.25):
        C = N80 * mult
        x1, y1 = (0.0, C)
        x2, y2 = (C, 0.0)
        extra.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="1" stroke-dasharray="2,4" opacity="0.75"/>'
                     % (ax.sx(x1), ax.sy(y1), ax.sx(x2), ax.sy(y2), C_MUTE))
    extra.append(_label(ax, N80 * 0.10, N80 * 0.86,
                        "iso-total  n1+n2 = const", C_MUTE, size=10, anchor="start"))

    body = []
    cols = [C_BLUE, C_RED, C_GREEN]
    for i, (tg, c) in enumerate(curves):
        body.append(_polyline(ax, c, cols[i % len(cols)]))
        # tangency point on the 1:1 diagonal
        n1eq = solve_n1(power_fn, 1.0, tg, lam_coef, alpha, sides)
        body.append(_dot(ax, n1eq, n1eq, cols[i % len(cols)], 4.0))
        body.append(_label(ax, n1eq, n1eq, "power=%.2f  (n=%s/group)" % (tg, _fmt_n(n1eq)),
                           cols[i % len(cols)], dx=10, dy=-8, anchor="start",
                           size=10, weight="600"))
    if neyman and abs(neyman - 1.0) > 1e-9:
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="1.4" stroke-dasharray="5,3"/>'
                    % (ax.sx(0), ax.sy(0), ax.sx(vmax), ax.sy(vmax * neyman), C_PURPLE))
        body.append(_label(ax, vmax * 0.16, vmax * neyman * 0.60,
                           "Neyman optimum  k* = %.2f" % neyman, C_PURPLE,
                           anchor="start", size=10.5, weight="600"))

    legend = [(("power = %.2f" % tg), cols[i % len(cols)], None)
              for i, (tg, _) in enumerate(curves)]
    legend.append(("iso-total line", C_MUTE, "2,4"))
    legend.append(("1:1 diagonal", C_MUTE, "7,5"))
    body.append(_legend(legend, x0=W - PAD_R - 158, y0=PAD_T + 4))

    xt = _nice_ticks(0, vmax, 5, "%g")
    title = "Iso-power contours in the (n1, n2) plane  |  %s  |  alpha=%.3g (%s)" % (
        effect_desc, alpha, "1-sided" if sides == 1 else "2-sided")
    return _frame(ax, title, "n1  (group 1)", "n2  (group 2)",
                  xt, dict(xt), "".join(extra) + "".join(body))


# ---- Plot D: power loss faceted by effect size ---------------------------

def plot_loss(test, kw, N_total, effect_grid, alpha, sides):
    body = []
    cols = [C_ORANGE, C_BLUE, C_RED, C_GREEN, C_PURPLE]
    ymax = 0.0
    ymin = 0.0
    series = []
    for d in effect_grid:
        kw2 = dict(kw)
        if test == "ttest_ind":
            kw2["delta"] = d * kw2["sd"]
        elif test == "prop":
            kw2["p2"] = kw2["p1"] + d
        else:
            kw2["hr"] = math.exp(-d)
        fn, lab, _ = _make_power_fn(test, **kw2)
        base = fn(N_total / 2.0, N_total / 2.0)
        ks = K_GRID
        losses = [base - fn(N_total / (1 + k), k * N_total / (1 + k)) for k in ks]
        series.append((lab, d, base, ks, losses))
        ymax = max(ymax, max(losses))
        ymin = min(ymin, min(losses))
    ymax = max(ymax * 1.20, 0.02)
    # ymin must follow the data below zero: for unequal-variance proportions the
    # "loss" goes NEGATIVE off 1:1 (moving away from 1:1 actually gains power),
    # and a hard floor at 0 would push those points outside the plot area.
    ymin = min(ymin * 1.25, 0.0)
    ax = Axes(0.25, 4.0, ymin, ymax, logx=True)

    extra = ['<rect x="0" y="0" width="0" height="0" fill="none"/>']
    extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                 'stroke-width="1.1" stroke-dasharray="5,4"/>'
                 % (PAD_L, ax.sy(0.05), W - PAD_R, ax.sy(0.05), C_MUTE))
    extra.append(_label(ax, 0.25, 0.05, "5 pp loss", C_MUTE,
                        dx=PAD_L - ax.sx(0.25) + 4, dy=-4, anchor="start", size=9.5))
    if ymin < -1e-9:
        extra.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.3"/>'
                     % (PAD_L, ax.sy(0.0), W - PAD_R, ax.sy(0.0), C_INK))
        extra.append(_label(ax, 0.25, 0.0, "0 = 1:1 baseline", C_INK,
                            dx=PAD_L - ax.sx(0.25) + 4, dy=12, anchor="start",
                            size=9.5))

    legend = []
    for i, (lab, d, base, ks, losses) in enumerate(series):
        col = cols[i % len(cols)]
        body.append(_polyline(ax, list(zip(ks, losses)), col, 2.0))
        kmax = max(zip(losses, ks))[1]
        lmax = max(losses)
        body.append(_dot(ax, kmax, lmax, col, 3.2))
        body.append(_label(ax, kmax, lmax, "%.3f" % lmax, col, dy=-8, size=9.5,
                           weight="600"))
        legend.append(("%s  (power 1:1 = %.2f)" % (lab, base), col, None))

    body.append(_legend(legend, x0=W - PAD_R - 205, y0=PAD_T + 4))
    yt = _nice_ticks(0, ymax, 5, "%.2f")
    title = ("Power loss vs allocation ratio, by effect size  |  fixed N = %s  "
             "|  alpha=%.3g (%s)" % (_fmt_n(N_total), alpha,
                                     "1-sided" if sides == 1 else "2-sided"))
    return _frame(ax, title,
                  "allocation ratio  n1 : n2   (k = n2/n1)",
                  "power loss  =  power(1:1) - power(k)",
                  _ratio_ticks(), yt, "".join(extra) + "".join(body))


# --------------------------------------------------------------------------
# 6. Text table + HTML report
# --------------------------------------------------------------------------


def _fmt_n(v):
    v = float(v)
    if abs(v - round(v)) < 0.5:
        return "%d" % int(round(v))
    return "%.1f" % v


def ratio_table(power_fn, target, lam_coef, alpha, sides, N_fixed=None):
    """Plain-text summary table: what each common ratio costs.

    Inflation is measured against the COST-MINIMISING ratio, not against 1:1 —
    for equal-variance backends these coincide, but for two proportions with
    p1(1-p1) != p2(1-p2) the 1:1 column should read as a positive penalty.
    """
    rows = []
    N1 = None
    Nbase = None
    if lam_coef and lam_coef > 0:
        N1 = 2.0 * solve_n1(power_fn, 1.0, target, lam_coef, alpha, sides)
        kopt = find_kopt(power_fn, target, lam_coef, alpha, sides)
        Nbase = solve_n1(power_fn, kopt, target, lam_coef, alpha, sides) * (1.0 + kopt)
    for k, lab in RATIO_TICKS:
        row = {"ratio": fmt_ratio(k), "k": k, "label_raw": lab}
        if N1:
            n1 = solve_n1(power_fn, k, target, lam_coef, alpha, sides)
            Nk = n1 * (1 + k)
            row["n1"] = n1
            row["n2"] = k * n1
            row["N"] = Nk
            row["infl_emp"] = Nk / Nbase
            row["infl_theor"] = inflation_factor(k)
        if N_fixed:
            p1 = power_fn(N_fixed / 2.0, N_fixed / 2.0)
            pk = power_fn(N_fixed / (1 + k), k * N_fixed / (1 + k))
            row["power"] = pk
            row["loss"] = p1 - pk
        rows.append(row)
    return rows, N1


def render_html(figs, meta):
    """Wrap generated SVGs into one self-contained light-theme HTML page."""
    parts = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">',
             '<meta name="viewport" content="width=device-width, initial-scale=1">',
             '<title>Allocation ratio vs Power — ct-samplesize</title>',
             '<style>',
             ':root{--ink:#2c3e50;--mute:#7f8c8d;--line:#e6e9ec;--bg:#f7f9fa;}',
             '*{box-sizing:border-box}',
             'body{margin:0;padding:28px 20px 60px;background:var(--bg);color:var(--ink);',
             'font-family:"Segoe UI",Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;',
             'line-height:1.6}',
             '.wrap{max-width:900px;margin:0 auto}',
             'h1{font-size:21px;margin:0 0 6px;font-weight:650}',
             '.sub{color:var(--mute);font-size:13px;margin-bottom:22px}',
             '.card{background:#fff;border:1px solid var(--line);border-radius:10px;',
             'padding:16px 18px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,.04)}',
             '.card h2{font-size:14.5px;margin:0 0 12px;font-weight:620;color:var(--ink)}',
             '.card svg{display:block;width:100%;height:auto}',
             'table{border-collapse:collapse;width:100%;font-size:12.5px;margin-top:4px}',
             'th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:right}',
             'th{background:#f2f5f7;font-weight:600;text-align:right;color:#34495e}',
             'td:first-child,th:first-child{text-align:left;font-weight:600}',
             'tr.hi td{background:#eafaf1}',
             '.note{font-size:12px;color:var(--mute);margin-top:10px}',
             'code{background:#f2f5f7;padding:1px 5px;border-radius:3px;font-size:12px}',
             '</style></head><body><div class="wrap">',
             '<h1>分配比 vs 检验效能（两组样本量不等）</h1>',
             '<div class="sub">ct-samplesize · alloc_curve · 生成于 %s</div>' % meta.get("ts", "")]
    for cap, svg in figs:
        parts.append('<div class="card"><h2>%s</h2>%s</div>' % (_esc(cap), svg))
    tbl = meta.get("table_html")
    if tbl:
        parts.append('<div class="card"><h2>关键分配比的代价（速查表）</h2>%s</div>' % tbl)
    parts.append('<div class="note">核心公式：固定总 N 时 <code>1/n1 + 1/n2 = (1+k)²/(kN)</code>'
                 ' 在 k=1 处取极小值，故 1:1 分配的效能最高；固定效能时'
                 ' <code>N(k) = N(1) · (1+k)²/(4k)</code>（Schoenfeld 膨胀因子），'
                 '两均数、两率、log-rank 事件数通用。</div>')
    parts.append('</div></body></html>')
    return "".join(parts)


def table_to_html(rows, N1, N_fixed):
    o = ['<table><thead><tr><th>n1 : n2</th>']
    if N1:
        o.append('<th>n1</th><th>n2</th><th>总 N</th><th>vs 最优</th><th>等方差理论值</th>')
    if N_fixed:
        o.append('<th>power @N=%s</th><th>效能损失</th>' % _fmt_n(N_fixed))
    o.append('</tr></thead><tbody>')
    for r in rows:
        cls = ' class="hi"' if abs(r["k"] - 1.0) < 1e-9 else ''
        o.append('<tr%s><td>%s</td>' % (cls, r["ratio"]))
        if N1:
            o.append('<td>%s</td><td>%s</td><td><b>%s</b></td><td>%s</td><td>%s</td>'
                     % (_fmt_n(r["n1"]), _fmt_n(r["n2"]), _fmt_n(r["N"]),
                        pct_delta(r["infl_emp"]), pct_delta(r["infl_theor"])))
        if N_fixed:
            o.append('<td>%.4f</td><td>-%.4f</td>' % (r["power"], r["loss"]))
        o.append('</tr>')
    o.append('</tbody></table>')
    return "".join(o)


# --------------------------------------------------------------------------
# 7. CLI
# --------------------------------------------------------------------------


def build_parser():
    p = argparse.ArgumentParser(
        description="Allocation-ratio (n2/n1) vs power diagnostics (unequal group sizes)")
    p.add_argument("--test", default="ttest_ind",
                   choices=["ttest_ind", "prop", "logrank", "z"],
                   help="comparison backend (default ttest_ind); "
                        "'z' = generic two-group z family, effect given by --theta")
    p.add_argument("--delta", type=float, default=0.5, help="mean difference (ttest_ind)")
    p.add_argument("--sd", type=float, default=1.0, help="common SD (ttest_ind)")
    p.add_argument("--p1", type=float, default=0.10, help="proportion group 1 (prop)")
    p.add_argument("--p2", type=float, default=0.30, help="proportion group 2 (prop)")
    p.add_argument("--hr", type=float, default=0.70, help="hazard ratio (logrank)")
    p.add_argument("--theta", type=float, default=None,
                   help="z-scale effect for --test z: ncp = theta*sqrt(n1*n2/(n1+n2)). "
                        "Caller solves it from the R anchor via theta_from_anchor().")
    p.add_argument("--power", type=float, default=0.80, help="target power (default 0.80)")
    p.add_argument("--alpha", type=float, default=0.05, help="two/one-sided alpha (default 0.05)")
    p.add_argument("--sides", type=int, default=2, choices=[1, 2], help="1 or 2 sided")
    p.add_argument("--n-fixed", type=float, default=None,
                   help="total N for the fixed-N plots (default: N required at 1:1)")
    p.add_argument("--plots", default="all",
                   help="comma list of n_vs_k,power_vs_k,contour,loss (default all)")
    p.add_argument("--effect-grid", default=None,
                   help="comma list of effect sizes for the loss plot "
                        "(default: auto around the given effect)")
    p.add_argument("--out-dir", default=None, help="output directory (default ./outputs)")
    p.add_argument("--prefix", default="ctss_alloc",
                   help="输出文件名前缀（默认 ctss_alloc；"
                        "由 figure_kit 按方法名传入，避免多方法互相覆盖）")
    p.add_argument("--no-html", action="store_true", help="skip the HTML report")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    kw = {"alpha": args.alpha, "sides": args.sides,
          "delta": args.delta, "sd": args.sd,
          "p1": args.p1, "p2": args.p2, "hr": args.hr,
          "theta": args.theta}
    power_fn, effect_desc, _ = _make_power_fn(args.test, **kw)

    if args.test == "ttest_ind":
        lam_coef = abs(args.delta) / args.sd
    elif args.test == "prop":
        pbar = 0.5 * (args.p1 + args.p2)
        lam_coef = abs(args.p2 - args.p1) / math.sqrt(pbar * (1 - pbar))
    elif args.test == "z":
        # 通用 z 族：ncp = theta*sqrt(n1*n2/N)，与 t / logrank 同形，故 lam_coef = theta
        lam_coef = abs(args.theta or 0.0)
    else:
        lam_coef = abs(math.log(args.hr))

    if lam_coef <= 0:
        print("ERROR: effect size must be non-zero", file=sys.stderr)
        return 2

    N1 = 2.0 * solve_n1(power_fn, 1.0, args.power, lam_coef, args.alpha, args.sides)
    # Default the fixed-N plots to the N that achieves the target power at 1:1 —
    # that puts the whole curve in the steep, informative region instead of
    # saturating near power=1 where every allocation looks alike.
    N_fixed = args.n_fixed if args.n_fixed else N1

    plots = [s.strip() for s in args.plots.split(",")]
    if "all" in plots:
        plots = ["n_vs_k", "power_vs_k", "contour", "loss"]

    outdir = args.out_dir or os.path.join(os.getcwd(), "outputs")
    try:
        os.makedirs(outdir, exist_ok=True)
    except OSError:
        outdir = os.getcwd()

    figs = []
    if "n_vs_k" in plots:
        figs.append(("A. 所需总样本量 N vs 分配比（固定目标 power）",
                     plot_n_vs_k(power_fn, args.power, lam_coef,
                                 args.alpha, args.sides, effect_desc, args.test)))
    if "power_vs_k" in plots:
        figs.append(("B. 检验效能 vs 分配比（固定总样本量）",
                     plot_power_vs_k(power_fn, N_fixed, effect_desc,
                                     args.alpha, args.sides)))
    if "contour" in plots:
        nk = neyman_k(args.p1, args.p2) if args.test == "prop" else None
        figs.append(("C. 等效能等高线（n1 × n2 平面）",
                     plot_contour(power_fn, lam_coef, args.alpha, args.sides,
                                  effect_desc, neyman=nk)))
    if "loss" in plots:
        if args.effect_grid:
            grid = [float(x) for x in args.effect_grid.split(",")]
        elif args.test == "ttest_ind":
            d0 = abs(args.delta) / args.sd
            grid = [d0 * 0.6, d0 * 0.8, d0, d0 * 1.3]
        elif args.test == "prop":
            d0 = abs(args.p2 - args.p1)
            grid = [d0 * 0.6, d0 * 0.8, d0, d0 * 1.4]
        else:
            l0 = abs(math.log(args.hr))
            grid = [l0 * 0.6, l0 * 0.8, l0, l0 * 1.3]
        figs.append(("D. 效能损失 vs 分配比（效应量分层）",
                     plot_loss(args.test, kw, N_fixed, grid, args.alpha, args.sides)))

    written = []
    for i, (cap, svg) in enumerate(figs, 1):
        path = os.path.join(outdir, "%s_%d.svg" % (args.prefix, i))
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        written.append((cap, path))

    rows, _ = ratio_table(power_fn, args.power, lam_coef, args.alpha, args.sides,
                          N_fixed=N_fixed)
    tbl_html = table_to_html(rows, N1, N_fixed)

    # ---- plain-text summary ----
    print("# ct-samplesize · allocation-ratio diagnostics  (%s)" % args.test)
    print("# effect: %s   alpha=%.3g (%s-sided)   target power=%.2f"
          % (effect_desc, args.alpha, args.sides, args.power))
    print("# N required at 1:1 = %s total (%s per group)"
          % (_fmt_n(N1), _fmt_n(N1 / 2.0)))
    if args.test != "logrank":
        kopt = find_kopt(power_fn, args.power, lam_coef, args.alpha, args.sides)
        Nopt = solve_n1(power_fn, kopt, args.power, lam_coef,
                        args.alpha, args.sides) * (1.0 + kopt)
        if abs(kopt - 1.0) > 0.02:
            print("# >> OPTIMUM IS NOT 1:1 <<  k* = %.3f  (n1:n2 = %s),  N = %s "
                  "(%+.1f%% vs 1:1)" % (kopt, fmt_ratio(kopt), _fmt_n(Nopt),
                                        (Nopt / N1 - 1.0) * 100))
        else:
            print("# cost-minimising ratio k* = %.3f (n1:n2 = %s) -> N = %s (1:1 is optimal)"
                  % (kopt, fmt_ratio(kopt), _fmt_n(Nopt)))
    print("# fixed-N plots use N = %s\n" % _fmt_n(N_fixed))
    print("%-9s %8s %8s %9s %11s %13s %10s %9s"
          % ("n1:n2", "n1", "n2", "total N", "vs optimum", "equal-var theor",
             "power@N", "loss"))
    print("-" * 82)
    print("# columns n1/n2/total N = required at target power; "
          "power@N/loss = at fixed N = %s" % _fmt_n(N_fixed))
    for r in rows:
        print("%-9s %8s %8s %9s %11s %14s %10.4f %9.4f"
              % (r["ratio"], _fmt_n(r["n1"]), _fmt_n(r["n2"]), _fmt_n(r["N"]),
                 pct_delta(r["infl_emp"]), pct_delta(r["infl_theor"]),
                 r["power"], r["loss"]))
    print()

    if not args.no_html:
        import datetime
        meta = {"ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "table_html": tbl_html}
        html = render_html(figs, meta)
        hpath = os.path.join(outdir, "%s_report.html" % args.prefix)
        with io.open(hpath, "w", encoding="utf-8") as f:
            f.write(html)
        print("# HTML report: %s" % hpath)
    for cap, path in written:
        print("# SVG: %s  <- %s" % (path, cap))
    return 0


if __name__ == "__main__":
    sys.exit(main())
