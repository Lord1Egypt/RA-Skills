# -*- coding: utf-8 -*-
"""
ebgm.py / FDA MGPS 贝叶斯收缩法 (Empirical Bayes Geometric Mean)

实现 DuMouchel (1999) 的多层 gamma-Poisson 收缩模型（openEBGM R 包的等价纯
Python 实现，无 scipy 依赖）：

  相对报告率 lambda = (N*a) / ((a+b)(a+c)) 的先验为两个 gamma 的混合；
  给定 2x2 列联表计数后，lambda 的后验为两个 gamma 的混合：
      w1 * Gamma(alpha1 + a, beta1 + e)  +  w2 * Gamma(alpha2 + a, beta2 + e)
  其中 e = (a+b)(a+c)/N 为独立性下的期望计数（Poisson-gamma 共轭）。

  - EBGM (theta-hat) = 后验均值 = w1*m1 + w2*m2
  - EB05 / EB95      = 后验 2.5% / 97.5% 分位数（可信区间）
  - 信号判定          = EB05 >= 2   (FDA MGPS 标准，保守下界)

a == 0 时估计收缩至先验均值 (~1)，正确避免 ROR/PRR 在零共现时的发散。
纯本地统计，不联网。
"""
import math


def _gammap(a, x):
    """Regularized lower incomplete gamma P(a, x) = gamma(a, x) / Gamma(a).

    Standard Numerical Recipes series / continued-fraction evaluation (pure
    stdlib, no scipy). Used for the gamma CDF and Beta-ratio mixture weights in
    the MGPS posterior.
    """
    if x <= 0.0:
        return 0.0
    if x < a + 1.0:
        gln = math.lgamma(a)
        ap = a
        summ = 1.0 / a
        delta = summ
        for _ in range(300):
            ap += 1.0
            delta *= x / ap
            summ += delta
            if abs(delta) < abs(summ) * 1e-12:
                break
        return summ * math.exp(-x + a * math.log(x) - gln)
    gln = math.lgamma(a)
    b = x + 1.0 - a
    c = 1e30
    d = 1.0 / b
    h = d
    for i in range(1, 300):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-30:
            d = 1e-30
        c = b + an / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-12:
            break
    q = math.exp(-x + a * math.log(x) - gln) * h
    return 1.0 - q


# Default MGPS prior (DuMouchel & Pregibon 2001; also openEBGM's `duMouchel_prior`).
# Mixture of two gammas for the relative reporting rate lambda; configurable so a
# prior fitted from a full FAERS quarter can be supplied later.
DEFAULT_MGPS_PRIOR = {"alpha1": 2.22, "beta1": 4.96, "alpha2": 2.38, "beta2": 3.10, "pi": 0.9084}


def ebgm(a, b, c, d, prior=None):
    """FDA MGPS empirical-Bayes shrinkage (EBGM) for a drug-event 2x2 table.

    Returns dict {value, eb05, eb95, signal, prior, weights}.
    See module docstring for the model and signal rule (EB05 >= 2).
    """
    if prior is None:
        prior = DEFAULT_MGPS_PRIOR
    a1, b1, a2, b2, pi = (prior["alpha1"], prior["beta1"],
                           prior["alpha2"], prior["beta2"], prior["pi"])
    a = float(a); b = float(b); c = float(c); d = float(d)
    N = a + b + c + d
    if N <= 0:
        return {"value": 1.0, "eb05": 1.0, "eb95": 1.0, "signal": False,
                "prior": prior, "weights": {"w1": pi, "w2": 1 - pi}}
    e = (a + b) * (a + c) / N  # expected count under independence
    # mixture weights via log-Beta ratios (avoids overflow)
    la = math.lgamma(a1 + a) + math.lgamma(a2 + b + c) - math.lgamma(a1 + a2 + a + b + c)
    lb = math.lgamma(a2 + a) + math.lgamma(a1 + b + c) - math.lgamma(a1 + a2 + a + b + c)
    num = pi * math.exp(la)
    den = (1 - pi) * math.exp(lb)
    w1 = num / (num + den) if (num + den) > 0 else pi
    w2 = 1.0 - w1
    s1, r1 = a1 + a, b1 + e
    s2, r2 = a2 + a, b2 + e
    m1 = s1 / r1
    m2 = s2 / r2
    theta = w1 * m1 + w2 * m2  # EBGM

    def _mix_cdf(x):
        return w1 * _gammap(s1, r1 * x) + w2 * _gammap(s2, r2 * x)

    def _quantile(p):
        lo, hi = 1e-6, 1e4
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if _mix_cdf(mid) < p:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    eb05 = _quantile(0.025)
    eb95 = _quantile(0.975)
    return {
        "value": round(theta, 3),
        "eb05": round(eb05, 3),
        "eb95": round(eb95, 3),
        "signal": eb05 >= 2.0,
        "prior": prior,
        "weights": {"w1": round(w1, 4), "w2": round(w2, 4)},
    }
