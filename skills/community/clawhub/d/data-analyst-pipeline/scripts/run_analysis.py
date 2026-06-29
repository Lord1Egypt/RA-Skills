#!/usr/bin/env python
"""
Main entry point for the data-analyst skill.
Orchestrates the full pipeline: Load → Audit → Clean → EDA → Visualize → Report.

Usage:
    python run_analysis.py <data_file> [--output report.html] [--target TARGET_COL] [--rules business_rules.yaml]
"""
import os
import sys
import json
import argparse
from pathlib import Path

# Ensure scripts directory is on path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from data_loader import load_data
from data_auditor import audit_data
from data_cleaner import clean_data
from eda_runner import run_eda
from visualizer import generate_all_charts
from report_builder import build_report


def parse_args():
    parser = argparse.ArgumentParser(
        description='Data Analyst — full pipeline from raw data to HTML report'
    )
    parser.add_argument('data_file', help='Path to data file (CSV, Excel, JSON, SQLite)')
    parser.add_argument('--output', '-o', default=None,
                        help='Output HTML report path (default: reports/report_<timestamp>.html)')
    parser.add_argument('--target', '-t', default=None,
                        help='Target column for bivariate analysis')
    parser.add_argument('--rules', '-r', default=None,
                        help='Path to business rules YAML file')
    parser.add_argument('--skip-clean', action='store_true',
                        help='Skip data cleaning step')
    parser.add_argument('--sample', '-s', type=int, default=None,
                        help='Sample N rows (for large datasets)')
    parser.add_argument('--name', '-n', default=None,
                        help='Dataset name for report title')
    return parser.parse_args()


def load_business_rules(rule_path: str) -> dict:
    """Load business rules from YAML file."""
    if not rule_path:
        return None
    try:
        import yaml
        with open(rule_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"[Warning] Could not load business rules: {e}")
        return None


def main():
    args = parse_args()

    data_file = args.data_file
    dataset_name = args.name or Path(data_file).stem
    output_dir = os.path.dirname(args.output) if args.output else os.path.join(os.getcwd(), 'reports')
    charts_dir = os.path.join(output_dir, 'charts')

    if not args.output:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = os.path.join(output_dir, f'report_{timestamp}.html')

    print("=" * 60)
    print(f"  Data Analyst Pipeline")
    print(f"  Dataset: {data_file}")
    print(f"  Output:  {args.output}")
    if args.target:
        print(f"  Target:  {args.target}")
    print("=" * 60)

    # ========== Step 1: Load Data ==========
    print("\n[1/6] Loading data...")
    df = load_data(data_file)

    if args.sample and len(df) > args.sample:
        df = df.sample(n=args.sample, random_state=42)
        print(f"  Sampled {args.sample:,} rows")

    # ========== Step 2: Audit ==========
    print("\n[2/6] Auditing data quality...")
    rules = load_business_rules(args.rules)
    audit_results = audit_data(df, business_rules=rules, target_col=args.target)

    score = audit_results['summary']['score']
    print(f"  Quality Score: {score['score']}/100 (Grade {score['grade']})")
    print(f"  Issues found:  {audit_results['summary']['total_issues']}")

    # ========== Step 3: Clean ==========
    if args.skip_clean:
        print("\n[3/6] Skipping data cleaning (--skip-clean)")
        df_clean = df
    else:
        print("\n[3/6] Cleaning data...")
        df_clean = clean_data(df)

    # ========== Step 4: EDA ==========
    print("\n[4/6] Running EDA...")
    eda_results = run_eda(df_clean, target_col=args.target)
    print(f"  Numeric features: {eda_results['overview']['numeric_columns']}")
    print(f"  Categorical features: {eda_results['overview']['categorical_columns']}")

    # ========== Step 5: Visualize ==========
    print("\n[5/6] Generating charts...")
    charts = generate_all_charts(df_clean, eda_results, charts_dir, target_col=args.target)

    # ========== Step 6: Report ==========
    print("\n[6/6] Building report...")
    report_path = build_report(df_clean, audit_results, eda_results, charts,
                               args.output, dataset_name=dataset_name)

    print("\n" + "=" * 60)
    print(f"  ✅ Analysis complete!")
    print(f"  📊 Report: {report_path}")
    print(f"  📈 Charts: {charts_dir}")
    print("=" * 60)

    # Print quick summary
    print(f"\nQuick Summary:")
    print(f"  Rows: {eda_results['overview']['rows']:,}")
    print(f"  Columns: {eda_results['overview']['columns']} ({eda_results['overview']['numeric_columns']} numeric, {eda_results['overview']['categorical_columns']} categorical)")
    print(f"  Missing: {eda_results['overview']['missing_pct']}%")
    print(f"  Quality: {score['score']}/100 ({score['grade']})")

    if eda_results['correlation'].get('top_correlations'):
        top_corr = eda_results['correlation']['top_correlations'][:3]
        print(f"\n  Top Correlations:")
        for c in top_corr:
            print(f"    {c['feature1']} ↔ {c['feature2']}: {c['correlation']:+.3f} ({c['strength']} {c['direction']})")

    # Save summary JSON for programmatic consumption
    summary_path = os.path.join(output_dir, 'summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'quality_score': score,
            'overview': eda_results['overview'],
            'issues_count': audit_results['summary']['total_issues'],
            'top_correlations': eda_results['correlation'].get('top_correlations', [])[:10],
        }, f, indent=2, ensure_ascii=False)
    print(f"\n  Summary JSON: {summary_path}")

    return report_path


if __name__ == '__main__':
    main()
