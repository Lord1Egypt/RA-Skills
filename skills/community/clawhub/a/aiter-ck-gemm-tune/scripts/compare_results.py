#!/usr/bin/env python3
"""Compare before/after benchmark results from aiter GEMM or MoE test logs.

Parses two log files (bench_before and bench_after) and produces a
comparison table showing performance changes and speedup percentages.

Auto-detects log format:
  - GEMM logs (test_gemm_*.py): keys on (m, n, k), default metric "ck TFLOPS" (higher=better)
  - MoE logs (test_moe_2stage.py): keys on (token, model_dim, inter_dim, E, topk), default metric "us" (lower=better)

Usage:
  python3 compare_results.py <before_log> <after_log>
  python3 compare_results.py <before_log> <after_log> --metric "ck us"
  python3 compare_results.py <before_log> <after_log> --metric us
"""

import argparse
import sys
from collections import defaultdict


def parse_markdown_table(log_file):
    """Parse markdown tables from a benchmark log.

    Returns (headers, {row_key: {col: value}}, log_type).
    log_type is "gemm" or "moe" based on detected columns.
    """
    results = {}
    headers = None
    log_type = None

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue

            cells = [c.strip() for c in line.split("|")[1:-1]]

            if not cells:
                continue

            lower_cells = [c.lower() for c in cells]

            # Detect header row
            if "dtype" in lower_cells or "m" in lower_cells or "token" in lower_cells:
                headers = [c.strip() for c in cells]
                # Detect log type from headers
                if "token" in lower_cells:
                    log_type = "moe"
                elif "m" in lower_cells:
                    log_type = "gemm"
                continue

            # Skip separator rows
            if headers is None or all(
                set(c.strip()) <= set("-: ") for c in cells
            ):
                continue

            if len(cells) != len(headers):
                continue

            row = {}
            for h, v in zip(headers, cells):
                try:
                    row[h] = float(v)
                except ValueError:
                    row[h] = v

            # Extract key based on log type
            if log_type == "moe":
                token = row.get("token")
                if token is None:
                    continue
                model_dim = int(row.get("model_dim", 0))
                inter_dim = int(row.get("inter_dim", 0))
                E = int(row.get("E", 0))
                topk = int(row.get("topk", 0))
                key = (int(token), model_dim, inter_dim, E, topk)
                results[key] = row
            else:
                m = row.get("m")
                n = row.get("n")
                k = row.get("k")
                if m is None or n is None or k is None:
                    continue
                key = (int(m), int(n), int(k))
                preshuffle = row.get("ck_preshuffle", "")
                full_key = (key, str(preshuffle))
                results[full_key] = row

    return headers, results, log_type


def compare_gemm(before, after, metric, common):
    """Compare GEMM benchmark results."""
    has_preshuffle = any(k[1] != "" for k in common)

    if has_preshuffle:
        print(
            f"| {'M':>6} | {'N':>6} | {'K':>5} | {'preshuffle':>10} | "
            f"{'Before':>10} | {'After':>10} | {'Speedup':>8} |"
        )
        print(
            f"|{'-'*8}|{'-'*8}|{'-'*7}|{'-'*12}|"
            f"{'-'*12}|{'-'*12}|{'-'*10}|"
        )
    else:
        print(
            f"| {'M':>6} | {'N':>6} | {'K':>5} | "
            f"{'Before':>10} | {'After':>10} | {'Speedup':>8} |"
        )
        print(
            f"|{'-'*8}|{'-'*8}|{'-'*7}|"
            f"{'-'*12}|{'-'*12}|{'-'*10}|"
        )

    M_CATEGORIES = [
        ("small M (1-63, decode)", lambda m: m <= 63),
        ("medium M (64-512)", lambda m: 64 <= m <= 512),
        ("large M (>512, prefill)", lambda m: m > 512),
    ]

    speedups = []
    by_nk = defaultdict(list)
    by_nk_mcat = defaultdict(lambda: defaultdict(list))

    for key in common:
        (m, n, k), preshuffle = key
        bval = before[key].get(metric)
        aval = after[key].get(metric)

        if bval is None or aval is None:
            continue
        if not isinstance(bval, (int, float)) or not isinstance(aval, (int, float)):
            continue
        if bval == 0:
            continue

        speedup = (aval - bval) / bval * 100
        speedups.append(speedup)
        by_nk[(n, k)].append(speedup)

        for cat_name, cat_fn in M_CATEGORIES:
            if cat_fn(m):
                by_nk_mcat[(n, k)][cat_name].append(speedup)
                break

        sign = "+" if speedup >= 0 else ""

        if has_preshuffle:
            print(
                f"| {m:>6} | {n:>6} | {k:>5} | {preshuffle:>10} | "
                f"{bval:>10.1f} | {aval:>10.1f} | {sign}{speedup:>6.1f}% |"
            )
        else:
            print(
                f"| {m:>6} | {n:>6} | {k:>5} | "
                f"{bval:>10.1f} | {aval:>10.1f} | {sign}{speedup:>6.1f}% |"
            )

    if not speedups:
        return None

    print_summary(speedups, metric)

    print(f"\n--- Per (N, K) breakdown ---")
    for (n, k), sps in sorted(by_nk.items()):
        avg_nk = sum(sps) / len(sps)
        print(
            f"  N={n}, K={k}: avg {'+' if avg_nk >= 0 else ''}{avg_nk:.1f}%, "
            f"min {'+' if min(sps) >= 0 else ''}{min(sps):.1f}%, "
            f"max {'+' if max(sps) >= 0 else ''}{max(sps):.1f}%"
        )

    print(f"\n--- Per (N, K) by M category ---")
    for cat_name, _ in M_CATEGORIES:
        print(f"\n  [{cat_name}]")
        for (n, k) in sorted(by_nk_mcat.keys()):
            sps = by_nk_mcat[(n, k)].get(cat_name)
            if not sps:
                continue
            avg_c = sum(sps) / len(sps)
            print(
                f"    N={n}, K={k}: avg {'+' if avg_c >= 0 else ''}{avg_c:.1f}%, "
                f"min {'+' if min(sps) >= 0 else ''}{min(sps):.1f}%, "
                f"max {'+' if max(sps) >= 0 else ''}{max(sps):.1f}%"
            )

    return speedups


def compare_moe(before, after, metric, common):
    """Compare MoE benchmark results."""
    # For latency (us), lower is better
    lower_is_better = metric == "us"

    print(
        f"| {'token':>6} | {'model_dim':>9} | {'inter_dim':>9} | {'E':>5} | {'topk':>4} | "
        f"{'Before':>10} | {'After':>10} | {'Speedup':>8} |"
    )
    print(
        f"|{'-'*8}|{'-'*11}|{'-'*11}|{'-'*7}|{'-'*6}|"
        f"{'-'*12}|{'-'*12}|{'-'*10}|"
    )

    TOKEN_CATEGORIES = [
        ("small token (1-63, decode)", lambda t: t <= 63),
        ("medium token (64-512)", lambda t: 64 <= t <= 512),
        ("large token (>512, prefill)", lambda t: t > 512),
    ]

    speedups = []
    by_config = defaultdict(list)
    by_config_tcat = defaultdict(lambda: defaultdict(list))

    for key in common:
        token, model_dim, inter_dim, E, topk = key
        bval = before[key].get(metric)
        aval = after[key].get(metric)

        if bval is None or aval is None:
            continue
        if not isinstance(bval, (int, float)) or not isinstance(aval, (int, float)):
            continue
        if bval == 0:
            continue

        if lower_is_better:
            speedup = (bval - aval) / bval * 100
        else:
            speedup = (aval - bval) / bval * 100

        speedups.append(speedup)
        config_key = (model_dim, inter_dim, E, topk)
        by_config[config_key].append(speedup)

        for cat_name, cat_fn in TOKEN_CATEGORIES:
            if cat_fn(token):
                by_config_tcat[config_key][cat_name].append(speedup)
                break

        sign = "+" if speedup >= 0 else ""
        print(
            f"| {token:>6} | {model_dim:>9} | {inter_dim:>9} | {E:>5} | {topk:>4} | "
            f"{bval:>10.1f} | {aval:>10.1f} | {sign}{speedup:>6.1f}% |"
        )

    if not speedups:
        return None

    qualifier = ", lower is better" if lower_is_better else ""
    print_summary(speedups, f"{metric}{qualifier}")

    print(f"\n--- Per config breakdown ---")
    for (model_dim, inter_dim, E, topk), sps in sorted(by_config.items()):
        avg_c = sum(sps) / len(sps)
        print(
            f"  model_dim={model_dim}, inter_dim={inter_dim}, E={E}, topk={topk}: "
            f"avg {'+' if avg_c >= 0 else ''}{avg_c:.1f}%, "
            f"min {'+' if min(sps) >= 0 else ''}{min(sps):.1f}%, "
            f"max {'+' if max(sps) >= 0 else ''}{max(sps):.1f}%"
        )

    print(f"\n--- Per config by token category ---")
    for cat_name, _ in TOKEN_CATEGORIES:
        print(f"\n  [{cat_name}]")
        for config_key in sorted(by_config_tcat.keys()):
            sps = by_config_tcat[config_key].get(cat_name)
            if not sps:
                continue
            model_dim, inter_dim, E, topk = config_key
            avg_c = sum(sps) / len(sps)
            print(
                f"    model_dim={model_dim}, inter_dim={inter_dim}, E={E}, topk={topk}: "
                f"avg {'+' if avg_c >= 0 else ''}{avg_c:.1f}%, "
                f"min {'+' if min(sps) >= 0 else ''}{min(sps):.1f}%, "
                f"max {'+' if max(sps) >= 0 else ''}{max(sps):.1f}%"
            )

    return speedups


def print_summary(speedups, metric_label):
    """Print summary statistics."""
    avg = sum(speedups) / len(speedups)
    improved = sum(1 for s in speedups if s > 1)
    regressed = sum(1 for s in speedups if s < -1)

    print(f"\n--- Summary ({metric_label}) ---")
    print(f"Shapes compared: {len(speedups)}")
    print(f"Average speedup: {'+' if avg >= 0 else ''}{avg:.1f}%")
    print(f"Min speedup:     {'+' if min(speedups) >= 0 else ''}{min(speedups):.1f}%")
    print(f"Max speedup:     {'+' if max(speedups) >= 0 else ''}{max(speedups):.1f}%")
    print(f"Improved (>1%):  {improved}/{len(speedups)}")
    print(f"Regressed (<-1%): {regressed}/{len(speedups)}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare before/after benchmark results (GEMM or MoE)"
    )
    parser.add_argument("before_log", help="Path to bench_before log file")
    parser.add_argument("after_log", help="Path to bench_after log file")
    parser.add_argument(
        "--metric",
        default=None,
        help='Metric column to compare. Auto-detected if not specified: '
             '"ck TFLOPS" for GEMM, "us" for MoE.',
    )
    args = parser.parse_args()

    _, before, type_b = parse_markdown_table(args.before_log)
    _, after, type_a = parse_markdown_table(args.after_log)

    if not before:
        print(f"ERROR: No results parsed from {args.before_log}", file=sys.stderr)
        sys.exit(1)
    if not after:
        print(f"ERROR: No results parsed from {args.after_log}", file=sys.stderr)
        sys.exit(1)

    # Determine log type
    log_type = type_b or type_a
    if type_b and type_a and type_b != type_a:
        print(
            f"ERROR: Log format mismatch — before is {type_b}, after is {type_a}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Auto-detect metric
    metric = args.metric
    if metric is None:
        metric = "us" if log_type == "moe" else "ck TFLOPS"

    common = sorted(set(before.keys()) & set(after.keys()))

    if not common:
        print("ERROR: No common shapes found between the two logs.", file=sys.stderr)
        print(f"  Before log has {len(before)} shapes", file=sys.stderr)
        print(f"  After log has {len(after)} shapes", file=sys.stderr)
        sys.exit(1)

    if log_type == "moe":
        speedups = compare_moe(before, after, metric, common)
    else:
        speedups = compare_gemm(before, after, metric, common)

    if speedups is None:
        print(f"\nNo comparable {metric} values found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
