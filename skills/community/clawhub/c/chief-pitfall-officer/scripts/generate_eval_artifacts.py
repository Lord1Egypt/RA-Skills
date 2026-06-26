#!/usr/bin/env python3
"""
Generate evaluation artifacts (review.html + report.html) from real regression-baseline.json data.
Reads the baseline JSON as the sole data source — no hardcoded mock data.
"""

import json
import os
from datetime import datetime


def load_baseline(baseline_path: str) -> dict:
    """Load regression-baseline.json and return parsed data."""
    with open(baseline_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_review_html(baseline: dict) -> str:
    """Generate evidence workbench HTML from baseline test results."""
    cases_html = ""
    for tc in baseline["test_results"]:
        findings_html = "".join(
            f"<li class='text-green-700 text-sm'>✅ {f}</li>" for f in tc["findings"]
        )
        misses_html = "".join(
            f"<li class='text-red-600 text-sm'>❌ {m}</li>" for m in tc.get("misses", [])
        ) or "<li class='text-slate-400 text-sm'>— 无遗漏</li>"

        dim_scores = tc["dimension_scores"]
        scores_grid = "".join(
            f'<div class="bg-slate-50 p-3 rounded-lg text-center">'
            f'<span class="block text-xs uppercase text-slate-400">{k}</span>'
            f'<span class="text-2xl font-bold">{v}</span></div>'
            for k, v in dim_scores.items()
        )

        cases_html += f"""
        <div class="bg-white p-8 rounded-2xl shadow-sm border">
            <h2 class="text-xl font-bold mb-2">{tc['id']}: <span class="text-slate-500">{tc['industry']}</span></h2>
            <p class="text-sm text-slate-400 mb-4">总分: <span class="font-bold text-2xl text-slate-900">{tc['score']}</span></p>
            <div class="grid grid-cols-5 gap-3 mb-6">{scores_grid}</div>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <h3 class="font-mono text-xs uppercase text-slate-400 mb-2">✅ Findings</h3>
                    <ul class="space-y-1">{findings_html}</ul>
                </div>
                <div>
                    <h3 class="font-mono text-xs uppercase text-slate-400 mb-2">❌ Misses</h3>
                    <ul class="space-y-1">{misses_html}</ul>
                </div>
            </div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Evidence Workbench - {baseline['skill_name']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 p-10 font-sans">
    <h1 class="text-3xl font-bold mb-2">Evidence Workbench: {baseline['skill_name']}</h1>
    <p class="text-slate-400 mb-10">Baseline v{baseline['baseline_version']} | {baseline['updated_at']} | {len(baseline['test_results'])} test cases</p>
    <div class="space-y-8">{cases_html}</div>
</body>
</html>"""


def generate_report_html(baseline: dict) -> str:
    """Generate evaluation report HTML with aggregated scores."""
    agg = baseline["aggregate"]
    dim_avgs = agg["dimension_averages"]

    # Score cards for all dimensions
    score_cards = "".join(
        f'<div class="bg-slate-50 p-4 rounded-xl text-center">'
        f'<span class="block text-xs uppercase text-slate-400">{k}</span>'
        f'<span class="text-3xl font-bold">{v}</span></div>'
        for k, v in dim_avgs.items()
    )

    # PRO / CON findings from all test cases
    all_findings = []
    all_misses = []
    for tc in baseline["test_results"]:
        for f in tc["findings"]:
            all_findings.append((tc["industry"], f))
        for m in tc.get("misses", []):
            all_misses.append((tc["industry"], m))

    findings_list = "".join(
        f'<li class="flex gap-4"><span class="bg-emerald-100 text-emerald-700 px-2 py-1 rounded text-xs font-bold h-fit">PRO</span>'
        f'<p class="text-slate-700"><b>[{industry}]</b> {finding}</p></li>'
        for industry, finding in all_findings[:8]
    )

    misses_list = "".join(
        f'<li class="flex gap-4"><span class="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-bold h-fit">CON</span>'
        f'<p class="text-slate-700"><b>[{industry}]</b> {miss}</p></li>'
        for industry, miss in all_misses[:5]
    ) or '<li class="text-slate-400">无遗漏项</li>'

    score_color = "text-emerald-600" if agg["mean_score"] >= 90 else ("text-amber-600" if agg["mean_score"] >= 80 else "text-red-600")

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Evaluation Report - {baseline['skill_name']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white p-10 font-sans">
    <div class="max-w-4xl mx-auto">
        <header class="border-b-4 border-slate-900 pb-6 mb-10">
            <h1 class="text-5xl font-black uppercase">Evaluation Report</h1>
            <p class="text-slate-500 mt-2">
                Skill: {baseline['skill_name']} v{baseline['baseline_version']} |
                Status: <span class="{score_color} font-bold">{'PRODUCTION READY' if agg['mean_score'] >= 90 else 'NEEDS IMPROVEMENT'}</span>
            </p>
        </header>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-6">Aggregate Scores</h2>
            <div class="mb-4 text-center">
                <span class="text-sm uppercase text-slate-400">Mean Score</span>
                <span class="block text-6xl font-black {score_color}">{agg['mean_score']}</span>
                <span class="text-slate-400 text-sm">std: ±{agg.get('score_std', '—')}</span>
            </div>
            <div class="grid grid-cols-5 gap-4">{score_cards}</div>
        </section>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-4">Key Findings</h2>
            <ul class="space-y-4">{findings_list}</ul>
        </section>

        <section class="mb-12">
            <h2 class="text-2xl font-bold mb-4">Improvement Areas</h2>
            <ul class="space-y-4">{misses_list}</ul>
        </section>

        <section class="mb-12 bg-slate-50 p-6 rounded-xl">
            <h2 class="text-xl font-bold mb-4">Test Coverage</h2>
            <table class="w-full text-sm">
                <thead><tr class="text-left text-slate-400"><th class="pb-2">ID</th><th class="pb-2">Industry</th><th class="pb-2">Score</th><th class="pb-2">Misses</th></tr></thead>
                <tbody>{"".join(
                    f'<tr class="border-t border-slate-200"><td class="py-2 font-mono">{tc["id"]}</td>'
                    f'<td class="py-2">{tc["industry"]}</td>'
                    f'<td class="py-2 font-bold">{tc["score"]}</td>'
                    f'<td class="py-2 text-red-500">{len(tc.get("misses", []))}</td></tr>'
                    for tc in baseline["test_results"]
                )}</tbody>
            </table>
        </section>

        <footer class="mt-20 border-t pt-6 text-slate-400 text-sm flex justify-between">
            <span>Generated by generate_eval_artifacts.py</span>
            <span>{datetime.now().strftime("%Y-%m-%d %H:%M")}</span>
        </footer>
    </div>
</body>
</html>"""


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(script_dir, "..", "evals", "artifacts")
    baseline_path = os.path.join(script_dir, "..", "evals", "regression-baseline.json")

    os.makedirs(base_path, exist_ok=True)

    baseline = load_baseline(baseline_path)

    # Generate review.html
    review_html = generate_review_html(baseline)
    with open(os.path.join(base_path, "review.html"), "w", encoding="utf-8") as f:
        f.write(review_html)
    print(f"✅ review.html generated — {len(baseline['test_results'])} test cases from regression-baseline.json")

    # Generate report.html
    report_html = generate_report_html(baseline)
    with open(os.path.join(base_path, "report.html"), "w", encoding="utf-8") as f:
        f.write(report_html)
    print(f"✅ report.html generated — mean score: {baseline['aggregate']['mean_score']}")

    print("Artifacts generated successfully from real data source.")


if __name__ == "__main__":
    main()
