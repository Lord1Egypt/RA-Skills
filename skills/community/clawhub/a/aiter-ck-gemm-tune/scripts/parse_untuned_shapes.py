#!/usr/bin/env python3
"""Parse aiter logs to extract unique untuned GEMM and fused MoE shapes.

Scans log files for two patterns:

1. Regular GEMM (untuned):
   shape is M:<val>, N:<val>, K:<val>, not found tuned config in <path>_tuned_gemm.csv, will use default config!

2. Fused MoE (untuned — using default heuristics):
   [fused_moe] using 1stage default for (cu_num, token, model_dim, inter_dim, expert, topk, 'ActivationType.X', 'torch.dtype', 'torch.dtype', 'torch.dtype', 'QuantType.X', use_g1u1, doweight_stage1)

Outputs deduplicated shapes grouped by kernel variant.

Usage:
  python3 parse_untuned_shapes.py <log_file>
  python3 parse_untuned_shapes.py <log_file> --variant a8w8_blockscale --csv output.csv --m-sweep
  python3 parse_untuned_shapes.py <log_file> --variant moe_2stages --csv output.csv --token-sweep
  python3 parse_untuned_shapes.py <log_file> --variant all --csv output.csv --m-sweep

Options:
  --variant <name>     Filter to a specific variant, or "all" for all variants.
                       Use "moe_2stages" for fused MoE shapes.
                       If omitted, prints summary only (no CSV).
  --csv <file>         Write results to CSV file. Requires --variant.
                       GEMM variants: M,N,K format. moe_2stages: untuned_fmoe.csv format.
  --m-sweep            Generate M sweep (1,2,4,...,32768) for each (N,K) pair in CSV output.
  --token-sweep        Generate token sweep (1,2,4,...,32768) for each MoE config in CSV output.
"""

import argparse
import re
import sys
from collections import defaultdict


GEMM_PATTERN = re.compile(
    r"shape is M:(\d+), N:(\d+), K:(\d+).*not found tuned config in .*/(\w+)_tuned_gemm"
)

FMOE_PATTERN = re.compile(
    r"\[fused_moe\] using \d+stage default for "
    r"\((\d+), (\d+), (\d+), (\d+), (\d+), (\d+), "
    r"'([^']+)', '([^']+)', '([^']+)', '([^']+)', '([^']+)', "
    r"(True|False), (True|False)\)"
)

SWEEP = [2**i for i in range(16)]  # 1, 2, 4, ..., 32768

MOE_VARIANT = "moe_2stages"

FMOE_CSV_HEADER = "token,model_dim,inter_dim,expert,topk,act_type,dtype,q_dtype_a,q_dtype_w,q_type,use_g1u1,doweight_stage1"


def parse_log(log_file):
    """Parse a log file and return {variant: set of shapes}, fmoe_tokens.

    For regular GEMM variants: shapes are (N, K) tuples.
    For moe_2stages: shapes are tuples of (model_dim, inter_dim, expert, topk,
      act_type, dtype, q_dtype_a, q_dtype_w, q_type, use_g1u1, doweight_stage1).
    fmoe_tokens maps each MoE config to the set of token values seen in the log.
    """
    variants = defaultdict(set)
    fmoe_tokens = defaultdict(set)

    with open(log_file, "r") as f:
        for line in f:
            match = GEMM_PATTERN.search(line)
            if match:
                n, k = int(match.group(2)), int(match.group(3))
                variant = match.group(4)
                variants[variant].add((n, k))
                continue

            match = FMOE_PATTERN.search(line)
            if match:
                token = int(match.group(2))
                config = (
                    int(match.group(3)),   # model_dim
                    int(match.group(4)),   # inter_dim
                    int(match.group(5)),   # expert
                    int(match.group(6)),   # topk
                    match.group(7),        # act_type
                    match.group(8),        # dtype
                    match.group(9),        # q_dtype_a
                    match.group(10),       # q_dtype_w
                    match.group(11),       # q_type
                    match.group(12) == "True",   # use_g1u1
                    match.group(13) == "True",   # doweight_stage1
                )
                variants[MOE_VARIANT].add(config)
                fmoe_tokens[config].add(token)

    return variants, fmoe_tokens


def print_summary(variants, fmoe_tokens):
    """Print human-readable summary of all untuned shapes found."""
    print(f"Found {len(variants)} kernel variant(s) with untuned shapes:\n")
    for variant, shapes in sorted(variants.items()):
        if variant == MOE_VARIANT:
            print(f"  Variant: {variant} (fused MoE)")
            print(f"    Unique MoE configs: {len(shapes)}")
            for config in sorted(shapes, key=str):
                (model_dim, inter_dim, expert, topk,
                 act_type, dtype, q_dtype_a, q_dtype_w, q_type,
                 use_g1u1, doweight_stage1) = config
                tokens_seen = sorted(fmoe_tokens[config])
                print(f"      model_dim={model_dim}, inter_dim={inter_dim}, "
                      f"expert={expert}, topk={topk}")
                print(f"        act={act_type}, dtype={dtype}, "
                      f"q_a={q_dtype_a}, q_w={q_dtype_w}, q_type={q_type}")
                print(f"        use_g1u1={use_g1u1}, doweight_stage1={doweight_stage1}")
                print(f"        tokens seen: {tokens_seen}")
        else:
            print(f"  Variant: {variant}")
            print(f"    Unique (N, K) pairs: {len(shapes)}")
            for n, k in sorted(shapes):
                print(f"      N={n}, K={k}")
        print()

    if len(variants) > 1:
        print(
            "Multiple variants found. Use --variant <name> to select one, "
            "or --variant all to include all.",
        )


def write_csv(args, selected, fmoe_tokens):
    """Write the untuned shapes CSV in the appropriate format."""
    has_moe = MOE_VARIANT in selected
    has_gemm = any(v != MOE_VARIANT for v in selected)

    if has_moe and has_gemm:
        print(
            "ERROR: Cannot mix GEMM and MoE variants in the same CSV — "
            "they have different formats. Run separately for each.",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(args.csv, "w") as f:
        if has_moe:
            f.write(FMOE_CSV_HEADER + "\n")
            for config in sorted(selected[MOE_VARIANT], key=str):
                (model_dim, inter_dim, expert, topk,
                 act_type, dtype, q_dtype_a, q_dtype_w, q_type,
                 use_g1u1, doweight_stage1) = config

                tokens = SWEEP if args.token_sweep else sorted(fmoe_tokens[config])
                for token in tokens:
                    f.write(
                        f"{token},{model_dim},{inter_dim},{expert},{topk},"
                        f"{act_type},{dtype},{q_dtype_a},{q_dtype_w},{q_type},"
                        f"{int(use_g1u1)},{int(doweight_stage1)}\n"
                    )
        else:
            f.write("M,N,K\n")
            for variant, shapes in sorted(selected.items()):
                for n, k in sorted(shapes):
                    if args.m_sweep:
                        for m in SWEEP:
                            f.write(f"{m},{n},{k}\n")
                    else:
                        f.write(f"0,{n},{k}\n")

    # Print CSV summary
    print(f"CSV written to: {args.csv}")
    print(f"  Variant(s): {', '.join(sorted(selected.keys()))}")
    if has_moe:
        n_configs = len(selected[MOE_VARIANT])
        if args.token_sweep:
            total_rows = n_configs * len(SWEEP)
            print(f"  Unique MoE configs: {n_configs}")
            print(f"  Token sweep: {len(SWEEP)} values per config")
        else:
            total_rows = sum(len(fmoe_tokens[c]) for c in selected[MOE_VARIANT])
            print(f"  Unique MoE configs: {n_configs}")
            print(f"  Using tokens seen in log")
        print(f"  Total rows: {total_rows}")
    else:
        total_nk = sum(len(s) for s in selected.values())
        total_rows = total_nk * (len(SWEEP) if args.m_sweep else 1)
        print(f"  Unique (N,K) pairs: {total_nk}")
        print(f"  Total rows: {total_rows}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse aiter logs for untuned GEMM and fused MoE shapes"
    )
    parser.add_argument("log_file", help="Path to the log file to parse")
    parser.add_argument(
        "--variant",
        help='Filter to a specific kernel variant, or "all" for all variants',
    )
    parser.add_argument(
        "--csv", help="Output CSV file path (requires --variant)"
    )
    parser.add_argument(
        "--m-sweep",
        action="store_true",
        help="Generate M sweep (1,2,4,...,32768) for each (N,K) in CSV (GEMM only)",
    )
    parser.add_argument(
        "--token-sweep",
        action="store_true",
        help="Generate token sweep (1,2,4,...,32768) for each MoE config in CSV",
    )
    args = parser.parse_args()

    variants, fmoe_tokens = parse_log(args.log_file)

    if not variants:
        print("No untuned shapes found in log file.", file=sys.stderr)
        sys.exit(1)

    print_summary(variants, fmoe_tokens)

    if args.csv:
        if not args.variant:
            print(
                "ERROR: --csv requires --variant to specify which variant(s) to output.",
                file=sys.stderr,
            )
            sys.exit(1)

        if args.variant == "all":
            selected = variants
        elif args.variant in variants:
            selected = {args.variant: variants[args.variant]}
        else:
            print(
                f"ERROR: Variant '{args.variant}' not found in log. "
                f"Available: {', '.join(sorted(variants.keys()))}",
                file=sys.stderr,
            )
            sys.exit(1)

        write_csv(args, selected, fmoe_tokens)


if __name__ == "__main__":
    main()
