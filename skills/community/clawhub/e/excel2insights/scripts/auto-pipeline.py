#!/usr/bin/env python3
"""
Excel2Insights — Auto Pipeline
One-command full analysis pipeline: load → analyze → chart → report.
"""

import argparse
import json
import sys
import subprocess
from pathlib import Path


def run_script(script_path, args_list):
    cmd = [sys.executable, str(script_path)] + args_list
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(script_path).parent.parent)
    if result.returncode != 0:
        return {"error": result.stderr}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"raw_output": result.stdout}


def main():
    parser = argparse.ArgumentParser(description="Excel2Insights — Auto Pipeline")
    parser.add_argument("--file", required=True, help="Path to data file")
    parser.add_argument("--sheet", help="Sheet name")
    parser.add_argument("--charts", default="histogram,boxplot,bar,correlation",
                        help="Chart types")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--format", default="html", choices=["html", "markdown"],
                        help="Report format")
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    chart_dir = out_dir / "charts"

    print("=" * 50)
    print("Excel2Insights — Auto Pipeline")
    print("=" * 50)

    # Step 1: Read & preview
    print("\n[1/4] Loading file...")
    reader = script_dir / "excel-reader.py"
    reader_args = ["--file", args.file]
    if args.sheet:
        reader_args += ["--sheet", args.sheet]
    result1 = run_script(reader, reader_args)
    if "error" in result1:
        print(f"  ERROR: {result1['error']}")
        sys.exit(1)
    meta = result1
    print(f"  Rows: {meta.get('rows', '?')} | Columns: {meta.get('columns', '?')}")
    print(f"  Numeric: {len(meta.get('column_types', {}).get('numeric', []))} | "
          f"Categorical: {len(meta.get('column_types', {}).get('categorical', []))}")
    quality = meta.get("quality_flags", [])
    if quality:
        for q in quality:
            print(f"  ⚠ {q}")

    # Step 2: Statistical analysis
    print("\n[2/4] Running statistical analysis...")
    analyzer = script_dir / "data-analyzer.py"
    analyzer_args = ["--file", args.file, "--correlation", "--outliers"]
    if args.sheet:
        analyzer_args += ["--sheet", args.sheet]
    analysis_out = str(out_dir / "analysis.json")
    analyzer_args += ["--output", analysis_out]
    result2 = run_script(analyzer, analyzer_args)
    print(f"  Analysis saved: {analysis_out}")

    # Step 3: Generate charts
    print(f"\n[3/4] Generating charts ({args.charts})...")
    chart_gen = script_dir / "chart-generator.py"
    chart_args = ["--file", args.file, "--charts", args.charts, "--output", str(chart_dir)]
    if args.sheet:
        chart_args += ["--sheet", args.sheet]
    result3 = run_script(chart_gen, chart_args)
    chart_count = result3.get("charts_generated", 0)
    print(f"  Charts generated: {chart_count}")

    # Step 4: Generate report
    print(f"\n[4/4] Generating {args.format.upper()} report...")
    report_gen = script_dir / "report-generator.py"
    report_path = out_dir / f"report.{args.format}"
    report_args = ["--file", args.file, "--charts", str(chart_dir),
                   "--output", str(report_path), "--format", args.format]
    if args.sheet:
        report_args += ["--sheet", args.sheet]
    result4 = run_script(report_gen, report_args)

    print(f"  Report saved: {report_path}")
    print("\n" + "=" * 50)
    print("Pipeline complete!")
    print(f"  Output directory: {out_dir.resolve()}")
    print(f"  Charts: {chart_count}")
    print(f"  Report: {report_path}")
    print("=" * 50)

    # Return structured output
    summary = {
        "status": "success",
        "file": args.file,
        "rows": meta.get("rows"),
        "columns": meta.get("columns"),
        "charts_generated": chart_count,
        "analysis_file": analysis_out,
        "report_file": str(report_path),
        "output_dir": str(out_dir.resolve()),
        "quality_flags": quality
    }
    print(f"\n{json.dumps(summary, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
