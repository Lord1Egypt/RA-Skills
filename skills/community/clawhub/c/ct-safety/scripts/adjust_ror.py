#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
adjust_ror.py / 多药比较 · 调整 ROR (aROR)

Answers: "for the same event / SOC, is drug A reported more often than drug B?"

FAERS reality check: the openFDA aggregate API only returns COUNTS, not
individual patient-level covariates (age / sex / comorbidities). A true
covariate-adjusted logistic regression therefore needs individual records
(which openFDA can serve via large `limit` pulls, but that is heavy and
out-of-scope for the default pipeline). So this module provides BOTH:

  (A) Aggregate aROR (default, no network beyond the counts already fetched):
      focal drug vs a pooled reference group, on the target event, as an
      adjusted reporting odds ratio with a Haldane-Anscombe fallback for
      sparse (zero-cell) tables. Optionally stratified via Mantel-Haenszel
      when year-stratified counts are supplied.

  (B) Individual-level logistic IRLS (`logistic_irls`, with optional Firth
      penalization) — a clean, testable hook for when the caller HAS
      patient-level rows (X, y). This is what "true aROR" reduces to.

All statistics are pure stdlib (math only). / 纯本地数学，不联网（除已抓取计数）。
"""
import math


# ---------------------------------------------------------------------------
# (A) Aggregate adjusted ROR: focal drug vs pooled reference group
# ---------------------------------------------------------------------------
def adjusted_ror_aggregate(focal_a, focal_n, ref_a, ref_n, continuity=True):
    """Adjusted ROR of the FOCAL drug vs a POOLED REFERENCE group on one event.

    Builds the 2x2:
        focal:  a1 = focal_a,  b1 = focal_n - focal_a
        ref:    a2 = ref_a,    b2 = ref_n   - ref_a
    OR = (a1/b1) / (a2/b2); log-OR SE via Woolf; 95% CI by exp(±1.96·SE).
    `continuity` applies Haldane-Anscombe (+0.5/cell) when any cell is 0 so a
    sparse table yields a finite, conservative estimate instead of inf/nan.

    Returns dict with or, ci_low, ci_high, se_log, sparse (bool), signal
    (True if OR>1 and lower CI>1, i.e. focal reports the event more than ref).
    """
    a1, n1 = focal_a, focal_n
    a2, n2 = ref_a, ref_n
    b1 = n1 - a1
    b2 = n2 - a2
    sparse = (a1 == 0 or b1 == 0 or a2 == 0 or b2 == 0)
    if continuity and sparse:
        a1 += 0.5; b1 += 0.5; a2 += 0.5; b2 += 0.5
    # guard against any residual zero after correction
    a1 = a1 or 1e-9; b1 = b1 or 1e-9; a2 = a2 or 1e-9; b2 = b2 or 1e-9
    or_val = (a1 * b2) / (b1 * a2)
    se_log = math.sqrt(1.0 / a1 + 1.0 / b1 + 1.0 / a2 + 1.0 / b2)
    lo = math.exp(math.log(or_val) - 1.96 * se_log)
    hi = math.exp(math.log(or_val) + 1.96 * se_log)
    signal = (or_val > 1.0) and (lo > 1.0)
    return {
        "or": round(or_val, 3), "ci_low": round(lo, 3), "ci_high": round(hi, 3),
        "se_log": round(se_log, 4), "sparse": bool(sparse and continuity),
        "signal": signal,
    }


# ---------------------------------------------------------------------------
# (A2) Mantel-Haenszel stratified OR (e.g. year-stratified to adjust time trend)
# ---------------------------------------------------------------------------
def mantel_haenszel_or(strata):
    """Mantel-Haenszel pooled OR across strata.

    `strata`: list of 2x2 dicts/tuples (a, b, c, d) per stratum.
    Returns {or_mh, se_log, ci_low, ci_high, n_strata}. Uses the
    Robins-Breslow-Greenland variance estimator. Returns None components if a
    stratum has n==0.
    """
    num = 0.0
    den = 0.0
    var_num = 0.0
    for s in strata:
        a, b, c, d = s[0], s[1], s[2], s[3]
        n = a + b + c + d
        if n == 0:
            continue
        num += a * d / n
        den += b * c / n
        var_num += (a * d * (a + d) / (n ** 2)) + (b * c * (b + c) / (n ** 2))
    if den == 0:
        return {"or_mh": None, "se_log": None, "ci_low": None,
                "ci_high": None, "n_strata": len(strata)}
    or_mh = num / den
    se = math.sqrt(var_num / (num * den)) if (num > 0 and den > 0) else None
    if se is None:
        return {"or_mh": round(or_mh, 3), "se_log": None, "ci_low": None,
                "ci_high": None, "n_strata": len(strata)}
    lo = math.exp(math.log(or_mh) - 1.96 * se)
    hi = math.exp(math.log(or_mh) + 1.96 * se)
    return {"or_mh": round(or_mh, 3), "se_log": round(se, 4),
            "ci_low": round(lo, 3), "ci_high": round(hi, 3),
            "n_strata": len(strata)}


# ---------------------------------------------------------------------------
# (B) Individual-level logistic regression (IRLS), optional Firth penalization
# ---------------------------------------------------------------------------
def logistic_irls(X, y, add_intercept=True, firth=False, max_iter=100, tol=1e-8):
    """Fit logistic regression by iteratively reweighted least squares.

    X: list of feature vectors (list of floats); y: list of 0/1 labels.
    Returns beta coefficients (list). With `firth=True`, applies Firth's
    penalized-likelihood bias reduction with the Jeffreys-prior invariant
    (Heinze 2002 exact Newton step on the penalized score) — the standard
    fix for separated / sparse data.

    Pure stdlib; intended as the individual-level engine for true covariate-
    adjusted ROR when patient rows are available. NOT used by the default
    aggregate pipeline (which has no individual covariates from openFDA counts).
    """
    if add_intercept:
        X = [[1.0] + list(row) for row in X]
    n = len(y)
    p = len(X[0])
    beta = [0.0] * p
    # mu clamp: under separation mu -> 0/1 and the Firth penalty h*w*(1-2mu)
    # underflows to exactly 0, which would silently degrade Firth into the
    # diverging plain MLE. Clamping keeps the penalty alive in saturation.
    MU_EPS = 1e-8

    for _ in range(max_iter):
        eta = [sum(beta[j] * X[i][j] for j in range(p)) for i in range(n)]
        mu = []
        for e in eta:
            if e > 18.0:
                mu.append(1.0 - MU_EPS)
            elif e < -18.0:
                mu.append(MU_EPS)
            else:
                mu.append(1.0 / (1.0 + math.exp(-e)))
        # weights w_i = mu(1-mu)
        W = []
        for i in range(n):
            m = mu[i]
            w = m * (1.0 - m)
            if w <= 1e-12:
                w = 1e-12
            W.append(w)
        # information matrix I = X'WX (+ ridge for numerical stability —
        # a pure ridge perturbation of a Newton step is standard practice
        # and does not change the converged root materially)
        XtWX = [[0.0] * p for _ in range(p)]
        for i in range(n):
            wi = W[i]
            xi = X[i]
            for j in range(p):
                for k in range(p):
                    XtWX[j][k] += wi * xi[j] * xi[k]
        for j in range(p):
            XtWX[j][j] += 1e-9
        try:
            inv = _invert(XtWX)
        except ZeroDivisionError:
            # still singular (collinear columns): stop, return current beta
            break
        if firth:
            # Exact Firth penalized-likelihood Newton step with Jeffreys
            # invariant prior (Firth 1993):
            #   l*(β) = l(β) + 0.5·log|I(β)|
            #   U*_j = Σ_i x_ij (y_i − μ_i) + 0.5 Σ_i x_ij h_i w_i (1 − 2μ_i)
            #   β_new = β + I⁻¹ U*,   h_i = leverage x_i' I⁻¹ x_i
            # (the second term is 0.5·∂ log|I|/∂β_j — derived, not guessed;
            # under complete separation it converges to −0.5·Σ_j-side while
            # the main score decays as e^(−β), so a finite root exists).
            # Yields bias reduction and a FINITE estimate even under complete
            # separation — the standard fix, replacing the earlier
            # diagonal-nudge approximation (upgrade D, 2026-09-29).
            h = []
            for i in range(n):
                xi = X[i]
                acc = 0.0
                for j in range(p):
                    s = 0.0
                    for k in range(p):
                        s += inv[j][k] * xi[k]
                    acc += xi[j] * s
                h.append(acc)
            U = [0.0] * p
            for i in range(n):
                resid = (y[i] - mu[i]) + 0.5 * h[i] * W[i] * (1.0 - 2.0 * mu[i])
                for j in range(p):
                    U[j] += X[i][j] * resid
            delta = [sum(inv[j][k] * U[k] for k in range(p)) for j in range(p)]
        else:
            # Classic IRLS: solve (X'WX) β_new = X'W z, z = η + (y−μ)/w
            XtWz = [0.0] * p
            for i in range(n):
                zi = eta[i] + (y[i] - mu[i]) / W[i]
                wi_zi = W[i] * zi
                for j in range(p):
                    XtWz[j] += X[i][j] * wi_zi
            delta = [sum(inv[j][k] * XtWz[k] for k in range(p)) - beta[j]
                     for j in range(p)]
        # Step bound (trust region): Newton without a bound can overshoot into
        # the saturated mu region where the penalty underflows; capping the
        # update norm keeps the iteration on the penalized-score path. The
        # fixed point is unchanged by bounding.
        dnorm = math.sqrt(sum(d * d for d in delta))
        if dnorm > 2.0:
            delta = [d * (2.0 / dnorm) for d in delta]
        diff = dnorm
        beta = [beta[j] + delta[j] for j in range(p)]
        if diff < tol:
            break
    return beta


def _invert(M):
    """Invert a small square matrix M via Gauss-Jordan (pure stdlib)."""
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for col in range(n):
        # pivot
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        if abs(A[piv][col]) < 1e-12:
            raise ZeroDivisionError("singular matrix")
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col:
                factor = A[r][col]
                if factor != 0.0:
                    A[r] = [A[r][k] - factor * A[col][k] for k in range(2 * n)]
    return [row[n:] for row in A]


def firth_logistic_irls(X, y, add_intercept=True, max_iter=100, tol=1e-8):
    """Named entry for a TRUE Firth-penalized logistic fit (Jeffreys prior).

    Thin wrapper over `logistic_irls(..., firth=True)` — kept as the explicit
    API used by upgrade D (稀疏数据 / 分离数据的 aROR 混杂调整)。Returns beta.
    """
    return logistic_irls(X, y, add_intercept=add_intercept,
                         firth=True, max_iter=max_iter, tol=tol)


def adjusted_ror_from_logistic(beta_drug, se_drug=None):
    """Convert a logistic drug-coefficient to an adjusted OR.

    `beta_drug` is the coefficient on the drug indicator in a logistic model
    (drug=1 vs 0), optionally with its SE. aROR = exp(beta); 95% CI uses SE if
    supplied, else None. This is the individual-level aROR.
    """
    aor = math.exp(beta_drug)
    if se_drug is not None:
        lo = math.exp(beta_drug - 1.96 * se_drug)
        hi = math.exp(beta_drug + 1.96 * se_drug)
        return {"aor": round(aor, 3), "ci_low": round(lo, 3),
                "ci_high": round(hi, 3), "beta": round(beta_drug, 4)}
    return {"aor": round(aor, 3), "beta": round(beta_drug, 4)}


if __name__ == "__main__":
    # quick self-test (no network)
    import json
    # aggregate: focal 150/10000 vs ref 300/50000 on same event
    agg = adjusted_ror_aggregate(150, 10000, 300, 50000)
    print("aggregate aROR:", json.dumps(agg))
    # MH across 2 strata
    mh = mantel_haenszel_or([(50, 4950, 100, 9900), (100, 9900, 200, 19800)])
    print("MH OR:", json.dumps(mh))
    # logistic: separable-ish toy (perfect separation -> Firth stabilizes)
    X = [[1.0], [1.0], [0.0], [0.0], [1.0], [0.0]]
    y = [1, 1, 0, 0, 1, 0]
    b = logistic_irls(X, y, add_intercept=False, firth=True)
    print("logistic beta (firth):", [round(v, 4) for v in b])
    assert all(abs(v) < 50.0 for v in b), "Firth must stay finite under separation"
    # unpenalized MLE under separation must diverge (much larger |beta|)
    b_plain = logistic_irls(X, y, add_intercept=False, firth=False, max_iter=200)
    print("logistic beta (plain):", [round(v, 4) for v in b_plain])
    assert abs(b_plain[0]) > abs(b[0]), "Firth shrinks the separated MLE"
    # named API check (upgrade D)
    b_named = firth_logistic_irls(X, y, add_intercept=False)
    assert b_named == b, "firth_logistic_irls must equal logistic_irls(firth=True)"
    # non-separated sanity: recover a known slope
    import random
    random.seed(7)
    Xr, yr = [], []
    for _ in range(4000):
        x = random.gauss(0, 1)
        pr = 1.0 / (1.0 + math.exp(-(0.5 + 1.2 * x)))
        Xr.append([x]); yr.append(1 if random.random() < pr else 0)
    bb = firth_logistic_irls(Xr, yr)
    print("recovered (intercept, slope):", [round(v, 3) for v in bb])
    assert abs(bb[0] - 0.5) < 0.15 and abs(bb[1] - 1.2) < 0.15, "Firth unbiased on truth"
    print("SELF-TEST PASS")
