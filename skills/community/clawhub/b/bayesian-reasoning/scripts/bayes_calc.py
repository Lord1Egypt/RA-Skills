#!/usr/bin/env python3
"""Bayesian reasoning calculation engine.

Subcommands:
    compute     - Compute posterior probability P(H|E) via Bayes' theorem
    sensitivity - Sensitivity analysis with grid sampling over probability ranges
"""

import argparse
import json
import sys
from datetime import datetime, timezone


# Bayes factor interpretation scale (Harold Jeffreys)
BF_THRESHOLDS = [
    (100, "decisive"),
    (30, "very strong"),
    (10, "strong"),
    (3, "moderate"),
    (1, "barely worth mentioning"),
    (0, "disconfirming"),
]

BAR_WIDTH = 20
BAR_FILLED = "█"
BAR_EMPTY = "░"


def interpret_bf(bf):
    for threshold, label in BF_THRESHOLDS:
        if bf >= threshold:
            return label
    return "disconfirming"


def make_bar(value):
    filled = round(value * BAR_WIDTH)
    filled = max(0, min(BAR_WIDTH, filled))
    return BAR_FILLED * filled + BAR_EMPTY * (BAR_WIDTH - filled)


def bayes_posterior(prior, likelihood, false_positive):
    numerator = likelihood * prior
    denominator = likelihood * prior + false_positive * (1 - prior)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def validate_prob(value, name, exclusive=False):
    if exclusive:
        if not (0 < value < 1):
            return f"{name} must be between 0 and 1 exclusive, got {value}"
    else:
        if not (0 <= value <= 1):
            return f"{name} must be between 0 and 1 inclusive, got {value}"
    return None


def cmd_compute(args):
    prior = args.prior
    likelihood = args.likelihood
    false_positive = args.false_positive

    err = validate_prob(prior, "prior", exclusive=True)
    if err:
        return {"error": "validation", "message": err}
    err = validate_prob(likelihood, "likelihood")
    if err:
        return {"error": "validation", "message": err}
    err = validate_prob(false_positive, "false-positive")
    if err:
        return {"error": "validation", "message": err}

    posterior = bayes_posterior(prior, likelihood, false_positive)
    if false_positive > 0:
        bf = likelihood / false_positive
    else:
        bf = float("inf") if likelihood > 0 else 0.0

    return {
        "command": "compute",
        "prior": prior,
        "likelihood": likelihood,
        "false_positive": false_positive,
        "posterior": round(posterior, 6),
        "bayes_factor": round(bf, 4) if bf != float("inf") else "inf",
        "bar": f"{make_bar(posterior)} {posterior:.1%}",
        "interpretation": interpret_bf(bf) if bf != float("inf") else "decisive",
    }


def parse_range(s, name):
    try:
        parts = s.split(",")
        if len(parts) != 2:
            return None, f"{name} must be two comma-separated numbers (min,max), got '{s}'"
        lo = float(parts[0].strip())
        hi = float(parts[1].strip())
        if lo > hi:
            lo, hi = hi, lo
        for v in (lo, hi):
            err = validate_prob(v, name)
            if err:
                return None, err
        return (lo, hi), None
    except ValueError:
        return None, f"{name} must be numeric, got '{s}'"


def cmd_sensitivity(args):
    prior = args.prior
    err = validate_prob(prior, "prior", exclusive=True)
    if err:
        return {"error": "validation", "message": err}

    l_range, err = parse_range(args.likelihood, "likelihood")
    if err:
        return {"error": "validation", "message": err}
    fp_range, err = parse_range(args.false_positive, "false-positive")
    if err:
        return {"error": "validation", "message": err}

    steps = max(2, args.steps)
    l_lo, l_hi = l_range
    fp_lo, fp_hi = fp_range

    l_points = [l_lo + i * (l_hi - l_lo) / (steps - 1) for i in range(steps)]
    fp_points = [fp_lo + i * (fp_hi - fp_lo) / (steps - 1) for i in range(steps)]

    grid = []
    for l in l_points:
        for fp in fp_points:
            post = bayes_posterior(prior, l, fp)
            bf = l / fp if fp > 0 else float("inf")
            grid.append({
                "likelihood": round(l, 6),
                "false_positive": round(fp, 6),
                "posterior": round(post, 6),
                "bayes_factor": round(bf, 4) if bf != float("inf") else "inf",
            })

    posteriors = [g["posterior"] for g in grid]
    bfs = [g["bayes_factor"] for g in grid if g["bayes_factor"] != "inf"]

    return {
        "command": "sensitivity",
        "prior": prior,
        "grid": grid,
        "posterior_range": [round(min(posteriors), 6), round(max(posteriors), 6)],
        "bayes_factor_range": [round(min(bfs), 4), round(max(bfs), 4)] if bfs else ["inf", "inf"],
    }


def main():
    parser = argparse.ArgumentParser(description="Bayesian reasoning calculator")
    sub = parser.add_subparsers(dest="command")

    p_compute = sub.add_parser("compute")
    p_compute.add_argument("--prior", type=float, required=True)
    p_compute.add_argument("--likelihood", type=float, required=True)
    p_compute.add_argument("--false-positive", type=float, required=True)

    p_sens = sub.add_parser("sensitivity")
    p_sens.add_argument("--prior", type=float, required=True)
    p_sens.add_argument("--likelihood", type=str, required=True)
    p_sens.add_argument("--false-positive", type=str, required=True)
    p_sens.add_argument("--steps", type=int, default=3)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    handlers = {"compute": cmd_compute, "sensitivity": cmd_sensitivity}
    result = handlers[args.command](args)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
