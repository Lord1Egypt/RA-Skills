#!/usr/bin/env python3
"""
Genome Report — Analyze 23andMe raw data and generate health/trait reports.
Pure Python, no external dependencies. Python 3.9+.

DISCLAIMER: This is NOT medical advice. Results are for educational/informational
purposes only. Consult a healthcare professional for medical decisions.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
SNP_DB_PATH = SCRIPT_DIR.parent / "references" / "snp_database.json"

CATEGORY_LABELS = {
    "cardiovascular": "❤️ Cardiovascular",
    "cognitive": "🧠 Cognitive",
    "metabolic": "🔥 Metabolic",
    "pharma": "💊 Pharmacogenomics",
    "athletic": "🏃 Athletic",
    "traits": "🧬 Traits",
}

CATEGORY_ALIASES = {
    "cardio": "cardiovascular",
    "pharma": "pharma",
    "cognitive": "cognitive",
    "metabolic": "metabolic",
    "athletic": "athletic",
    "traits": "traits",
    "cardiovascular": "cardiovascular",
}


def load_snp_database():
    with open(SNP_DB_PATH) as f:
        data = json.load(f)
    db = {}
    for snp in data["snps"]:
        db[snp["rsid"]] = snp
    return db


def parse_23andme(filepath):
    """Parse 23andMe raw data file. Returns dict of rsid -> genotype."""
    genotypes = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 4:
                rsid, _chrom, _pos, genotype = parts[0], parts[1], parts[2], parts[3]
                if rsid.startswith("rs") and genotype != "--":
                    genotypes[rsid] = genotype
    return genotypes


def analyze_genome(genotypes, snp_db, categories=None):
    """Analyze genotypes against SNP database. Returns results by category."""
    results = defaultdict(list)
    
    for rsid, snp_info in snp_db.items():
        cat = snp_info["category"]
        if categories and cat not in categories:
            continue
        genotype = genotypes.get(rsid)
        if not genotype:
            continue
        
        # Normalize genotype for lookup (try both orientations)
        gt = genotype
        effect = snp_info["genotypes"].get(gt)
        if effect is None and len(gt) == 2:
            gt_rev = gt[1] + gt[0]
            effect = snp_info["genotypes"].get(gt_rev)
            if effect:
                gt = gt_rev
        
        # Count risk alleles
        risk_allele = snp_info.get("risk_allele", "")
        risk_count = genotype.count(risk_allele) if risk_allele else 0
        
        results[cat].append({
            "rsid": rsid,
            "gene": snp_info["gene"],
            "trait": snp_info["trait"],
            "genotype": genotype,
            "risk_allele": risk_allele,
            "risk_count": risk_count,
            "effect": effect or "Genotype not in database",
        })
    
    return dict(results)


def calculate_scores(results):
    """Calculate risk score (0-100) per category."""
    scores = {}
    for cat, snps in results.items():
        if not snps:
            scores[cat] = 0
            continue
        total_possible = len(snps) * 2  # max 2 risk alleles per SNP
        total_risk = sum(s["risk_count"] for s in snps)
        scores[cat] = round((total_risk / total_possible) * 100) if total_possible else 0
    return scores


def risk_color(score):
    if score < 30:
        return "green"
    elif score < 60:
        return "orange"
    return "red"


def risk_label(score):
    if score < 30:
        return "Low"
    elif score < 60:
        return "Moderate"
    return "Elevated"


# ── Output formatters ──

def output_text(results, scores, filename):
    print(f"\n{'='*60}")
    print(f"  GENOME REPORT — {Path(filename).stem}")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print("\n⚠️  DISCLAIMER: This is NOT medical advice.\n")
    
    # Summary
    print("── RISK SCORE SUMMARY ──\n")
    for cat in sorted(scores, key=scores.get, reverse=True):
        label = CATEGORY_LABELS.get(cat, cat)
        score = scores[cat]
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        print(f"  {label:<30} {bar} {score:>3}% ({risk_label(score)})")
    
    # Details
    for cat, snps in sorted(results.items()):
        label = CATEGORY_LABELS.get(cat, cat)
        print(f"\n── {label} ──\n")
        for s in sorted(snps, key=lambda x: -x["risk_count"]):
            risk_indicator = "🔴" if s["risk_count"] == 2 else "🟡" if s["risk_count"] == 1 else "🟢"
            print(f"  {risk_indicator} {s['rsid']} ({s['gene']}) — {s['genotype']}")
            print(f"     {s['trait']}")
            print(f"     {s['effect']}")
            print()


def output_json(results, scores, filename):
    output = {
        "file": str(filename),
        "generated": datetime.now().isoformat(),
        "disclaimer": "This is NOT medical advice. For educational purposes only.",
        "scores": scores,
        "details": results,
    }
    print(json.dumps(output, indent=2))


def output_html(results, scores, filename, output_path=None):
    cats_html = ""
    for cat in sorted(scores, key=scores.get, reverse=True):
        label = CATEGORY_LABELS.get(cat, cat)
        score = scores[cat]
        color = risk_color(score)
        cats_html += f'<div class="score-card"><h3>{label}</h3><div class="score-bar"><div class="score-fill" style="width:{score}%;background:{color}"></div></div><span class="score-val">{score}% — {risk_label(score)}</span></div>\n'
    
    details_html = ""
    for cat, snps in sorted(results.items()):
        label = CATEGORY_LABELS.get(cat, cat)
        rows = ""
        for s in sorted(snps, key=lambda x: -x["risk_count"]):
            cls = "risk-high" if s["risk_count"] == 2 else "risk-med" if s["risk_count"] == 1 else "risk-low"
            rows += f'<tr class="{cls}"><td>{s["rsid"]}</td><td>{s["gene"]}</td><td>{s["genotype"]}</td><td>{s["trait"]}</td><td>{s["effect"]}</td></tr>\n'
        details_html += f'<h2>{label}</h2><table><tr><th>SNP</th><th>Gene</th><th>Genotype</th><th>Trait</th><th>Effect</th></tr>{rows}</table>\n'
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Genome Report — {Path(filename).stem}</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:960px;margin:0 auto;padding:20px;background:#f5f5f5;color:#333}}
h1{{color:#2c3e50}}
.disclaimer{{background:#fff3cd;border:1px solid #ffc107;padding:12px;border-radius:6px;margin:16px 0}}
.score-card{{background:white;padding:16px;border-radius:8px;margin:8px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
.score-bar{{background:#e0e0e0;border-radius:10px;height:20px;overflow:hidden;margin:8px 0}}
.score-fill{{height:100%;border-radius:10px;transition:width .3s}}
.score-val{{font-weight:600}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:8px;overflow:hidden;margin:12px 0;box-shadow:0 1px 3px rgba(0,0,0,.1)}}
th{{background:#2c3e50;color:white;padding:10px;text-align:left}}
td{{padding:8px 10px;border-bottom:1px solid #eee}}
.risk-high{{background:#ffebee}} .risk-med{{background:#fff8e1}} .risk-low{{background:#e8f5e9}}
</style></head><body>
<h1>🧬 Genome Report — {Path(filename).stem}</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<div class="disclaimer">⚠️ <strong>DISCLAIMER:</strong> This report is for educational and informational purposes only. It is NOT medical advice. Consult a healthcare professional before making any health decisions based on genetic data.</div>
<h2>Risk Score Summary</h2>
{cats_html}
{details_html}
</body></html>"""
    
    if output_path is None:
        output_path = Path(filename).stem + "_report.html"
    with open(output_path, "w") as f:
        f.write(html)
    print(f"HTML report saved to: {output_path}")


def family_comparison(genome_dir, snp_db, categories, output_format):
    """Compare multiple genome files in a directory."""
    genome_files = sorted(Path(genome_dir).glob("*.txt"))
    if not genome_files:
        print(f"No .txt genome files found in {genome_dir}")
        sys.exit(1)
    
    print(f"\nFound {len(genome_files)} genome file(s): {', '.join(f.stem for f in genome_files)}\n")
    
    all_results = {}
    all_scores = {}
    for gf in genome_files:
        genotypes = parse_23andme(gf)
        results = analyze_genome(genotypes, snp_db, categories)
        scores = calculate_scores(results)
        all_results[gf.stem] = results
        all_scores[gf.stem] = scores
    
    if output_format == "json":
        output = {
            "family_comparison": True,
            "generated": datetime.now().isoformat(),
            "disclaimer": "This is NOT medical advice.",
            "members": {name: {"scores": all_scores[name], "details": all_results[name]} for name in all_scores},
        }
        print(json.dumps(output, indent=2))
        return
    
    if output_format == "html":
        _family_html(all_results, all_scores, genome_dir)
        return
    
    # Text output
    print(f"{'='*60}")
    print("  FAMILY GENOME COMPARISON")
    print(f"{'='*60}\n")
    
    # Score comparison table
    members = list(all_scores.keys())
    all_cats = sorted(set(c for s in all_scores.values() for c in s))
    
    header = f"{'Category':<25}" + "".join(f"{m:<20}" for m in members)
    print(header)
    print("-" * len(header))
    for cat in all_cats:
        label = CATEGORY_LABELS.get(cat, cat)
        row = f"{label:<25}"
        for m in members:
            score = all_scores[m].get(cat, 0)
            row += f"{score:>3}% ({risk_label(score):<8})   "
        print(row)
    
    # Inheritance patterns
    if len(members) >= 2:
        print(f"\n── Shared Risk Alleles ──\n")
        # Find SNPs where all members share the same risk genotype
        snp_db_by_rsid = snp_db
        for rsid in snp_db_by_rsid:
            member_genotypes = {}
            for m in members:
                for cat_results in all_results[m].values():
                    for snp in cat_results:
                        if snp["rsid"] == rsid:
                            member_genotypes[m] = snp
            if len(member_genotypes) == len(members):
                risk_counts = [mg["risk_count"] for mg in member_genotypes.values()]
                if all(r >= 1 for r in risk_counts):
                    info = list(member_genotypes.values())[0]
                    gts = " / ".join(f"{m}:{member_genotypes[m]['genotype']}" for m in members)
                    print(f"  {info['rsid']} ({info['gene']}) — {info['trait']}")
                    print(f"    {gts}\n")


def _family_html(all_results, all_scores, genome_dir):
    members = list(all_scores.keys())
    all_cats = sorted(set(c for s in all_scores.values() for c in s))
    
    table_rows = ""
    for cat in all_cats:
        label = CATEGORY_LABELS.get(cat, cat)
        cells = f"<td><strong>{label}</strong></td>"
        for m in members:
            score = all_scores[m].get(cat, 0)
            color = risk_color(score)
            cells += f'<td><span style="color:{color};font-weight:600">{score}% ({risk_label(score)})</span></td>'
        table_rows += f"<tr>{cells}</tr>\n"
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Family Genome Comparison</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:20px;background:#f5f5f5}}
h1{{color:#2c3e50}}
.disclaimer{{background:#fff3cd;border:1px solid #ffc107;padding:12px;border-radius:6px;margin:16px 0}}
table{{width:100%;border-collapse:collapse;background:white;border-radius:8px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1);margin:16px 0}}
th{{background:#2c3e50;color:white;padding:10px}} td{{padding:10px;border-bottom:1px solid #eee}}
</style></head><body>
<h1>👨‍👩‍👧‍👦 Family Genome Comparison</h1>
<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<div class="disclaimer">⚠️ This report is for educational purposes only. NOT medical advice.</div>
<table><tr><th>Category</th>{"".join(f"<th>{m}</th>" for m in members)}</tr>
{table_rows}</table>
</body></html>"""
    
    out = Path(genome_dir) / "family_comparison.html"
    with open(out, "w") as f:
        f.write(html)
    print(f"Family comparison saved to: {out}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze 23andMe raw genome data and generate health/trait reports.",
        epilog="DISCLAIMER: This is NOT medical advice. For educational purposes only.",
    )
    parser.add_argument("genome_file", nargs="?", help="Path to 23andMe raw data file (.txt)")
    parser.add_argument("--family", metavar="DIR", help="Directory with multiple genome files for family comparison")
    parser.add_argument("--category", default="all",
                        choices=["all", "cardio", "cardiovascular", "cognitive", "metabolic", "pharma", "athletic", "traits"],
                        help="Category to analyze (default: all)")
    parser.add_argument("--output", default="text", choices=["text", "json", "html"],
                        help="Output format (default: text)")
    parser.add_argument("--output-path", help="Output file path (for html)")
    
    args = parser.parse_args()
    
    if not args.genome_file and not args.family:
        parser.print_help()
        sys.exit(1)
    
    snp_db = load_snp_database()
    
    # Resolve categories
    categories = None
    if args.category != "all":
        resolved = CATEGORY_ALIASES.get(args.category, args.category)
        categories = {resolved}
    
    if args.family:
        family_comparison(args.family, snp_db, categories, args.output)
        return
    
    if not os.path.exists(args.genome_file):
        print(f"Error: File not found: {args.genome_file}")
        sys.exit(1)
    
    genotypes = parse_23andme(args.genome_file)
    print(f"Parsed {len(genotypes)} SNPs from {args.genome_file}")
    
    results = analyze_genome(genotypes, snp_db, categories)
    scores = calculate_scores(results)
    
    if args.output == "json":
        output_json(results, scores, args.genome_file)
    elif args.output == "html":
        output_html(results, scores, args.genome_file, args.output_path)
    else:
        output_text(results, scores, args.genome_file)


if __name__ == "__main__":
    main()
