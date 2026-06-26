---
name: genome-report
description: Analyze 23andMe raw genome data to generate comprehensive health, trait, and family comparison reports. Supports cardiovascular, cognitive, metabolic, pharmacogenomic, athletic, and ancestry analysis. Use when user asks to analyze genome data, 23andMe files, genetic reports, SNP analysis, health risk from DNA, or family genetic comparison.
---

# Genome Report

Analyze 23andMe v5 raw data files and generate health/trait reports with risk scoring.

## Usage

```bash
python3 skills/genome-report/scripts/genome_report.py <genome_file.txt> [options]
```

### Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--category` | `all\|cardio\|cognitive\|metabolic\|pharma\|athletic\|traits` | `all` | Category filter |
| `--output` | `text\|json\|html` | `text` | Output format |
| `--output-path` | filepath | auto | HTML output path |
| `--family DIR` | directory path | — | Family comparison mode |

### Examples

```bash
# Full report to console
python3 skills/genome-report/scripts/genome_report.py ~/my_genome.txt

# HTML report for one category
python3 skills/genome-report/scripts/genome_report.py ~/my_genome.txt --category cardio --output html

# Family comparison
python3 skills/genome-report/scripts/genome_report.py --family ~/genomes/ --output html
```

## Input Format

23andMe v5 raw data (tab-separated): `rsid  chromosome  position  genotype`

Lines starting with `#` are skipped. Genotypes marked `--` (no-call) are excluded.

## Output

- **Text**: Console output with risk bars and color-coded SNP details
- **JSON**: Structured data with scores and per-SNP results
- **HTML**: Styled report with risk score cards and color-coded tables

## Categories & Coverage

~55 curated SNPs across 6 categories:

- **Cardiovascular** — blood pressure, cholesterol, cardiac rhythm, CAD risk
- **Cognitive** — memory, dopamine, BDNF, social cognition, brain volume
- **Metabolic** — diabetes risk, MTHFR, lactose, alcohol, iron metabolism
- **Pharmacogenomics** — warfarin, clopidogrel, CYP2D6, CYP2C19 drug metabolism
- **Athletic** — muscle fiber type, endurance, recovery, injury risk
- **Traits** — eye color, hair color, earwax, bitter taste, asparagus smell

## SNP Database

The SNP reference data lives in `references/snp_database.json`. Edit this file to add/update SNPs without changing the script. Each entry has: rsid, gene, category, trait, risk_allele, and genotype-specific effect descriptions.

## Constraints

- Pure Python 3.9+ — no external dependencies
- **Not medical advice** — educational/informational only
