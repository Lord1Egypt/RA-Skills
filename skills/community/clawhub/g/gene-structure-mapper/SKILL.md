---
name: gene-structure-mapper
description: Visualize gene structure with exon-intron diagrams, domain annotations, and mutation position markers. Produces SVG, PNG, or PDF figures suitable for publication from a gene symbol input.
license: MIT
skill-author: AIPOCH
status: beta
---
# Gene Structure Mapper

Generate exon-intron structure diagrams for any gene symbol using the Ensembl REST API. Optionally overlay protein domain annotations (UniProt) and mark mutation hotspot positions. Outputs publication-ready SVG, PNG, or PDF figures.

> ✅ **IMPLEMENTED** — `scripts/main.py` is fully functional. Ensembl REST API, caching, matplotlib visualization, `--domains`, `--mutations`, and `--demo` are all implemented.

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --demo --output demo.png
```

## When to Use

- Creating gene structure figures for manuscripts or presentations
- Visualizing splice variants and isoform differences
- Marking mutation positions on a gene diagram for functional annotation
- Overlaying domain boundaries on exon-intron maps

## Workflow

1. Confirm the user objective, required inputs, and non-negotiable constraints before doing detailed work.
2. Validate that the request matches the documented scope and stop early if the task would require unsupported assumptions.
3. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

**Fallback template:** If `scripts/main.py` fails or the gene symbol is unrecognized, report: (a) the failure point, (b) whether a manual Ensembl/UCSC lookup can substitute, (c) which output formats are still generatable.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--gene`, `-g` | string | Yes* | Gene symbol or Ensembl ID (e.g., `TP53`, `BRCA1`, `ENSG00000141510`) |
| `--species` | string | No | Species name for Ensembl lookup (default: `homo_sapiens`) |
| `--format` | string | No | Output format: `png`, `svg`, `pdf` (default: `png`) |
| `--output`, `-o` | string | No | Output file path (default: `<gene>_structure.<format>`) |
| `--domains` | flag | No | Fetch and overlay UniProt protein domain annotations |
| `--mutations` | string | No | Comma-separated codon positions to mark (e.g., `248,273`) |
| `--demo` | flag | No | Use hardcoded TP53 GRCh38 data — no internet required |

*Required unless `--demo` is used.

## Usage

```text
python scripts/main.py --gene TP53 --format png
python scripts/main.py --gene BRCA1 --format png --domains --output brca1_structure.png
python scripts/main.py --gene KRAS --mutations 12,13,61 --format pdf
python scripts/main.py --demo
python scripts/main.py --demo --output demo.png --format svg
```

## Implementation Notes (for script developer)

The script must implement:

1. **Gene lookup** — `GET https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}?expand=1` to fetch exon coordinates. Cache response to `.cache/{gene}_ensembl.json` to avoid repeated API calls. Add a 0.1 s delay between requests for batch lookups. The unauthenticated rate limit is 15 requests/second.
2. **Unknown gene handling** — catch HTTP 400/404 from Ensembl and exit with code 1: `Error: Gene not found: {gene_name}. Check the gene symbol and try again.`
3. **SVG/PNG/PDF output** — use `matplotlib` or `svgwrite` to draw exon blocks (filled rectangles) and intron lines scaled to genomic coordinates.
4. **`--domains` flag** — fetch UniProt domain annotations and overlay colored domain blocks on the gene structure.
5. **`--mutations` flag** — accept comma-separated codon positions; map to exon coordinates and draw vertical markers.
6. **`--demo` flag** — use hardcoded TP53 GRCh38 exon coordinates (no internet required) to generate a demo visualization.

## Known Limitations

- For genes with multiple isoforms, the script uses the canonical transcript (Ensembl `is_canonical` flag). Other isoforms are not visualized.
- Domain overlay (`--domains`) maps UniProt amino acid positions to genomic coordinates using CDS length; accuracy may vary for genes with complex splicing.
- Ensembl API responses are cached to `.cache/{gene}_ensembl.json`. Delete the cache file to force a fresh lookup.
- The unauthenticated Ensembl REST API rate limit is 15 requests/second; a 0.1 s delay is applied between batch requests.

## Features

- Exon-intron visualization scaled to genomic coordinates
- Protein domain annotation overlay via UniProt (optional, `--domains`)
- Mutation position markers with configurable labels (`--mutations`)
- Publication-ready output in SVG, PNG, or PDF
- Demo mode for offline testing (`--demo`)
- Ensembl API response caching to avoid rate-limit issues

## Output Requirements

Every response must make these explicit:

- Objective and deliverable
- Inputs used and assumptions introduced (e.g., genome build, transcript isoform selected)
- Workflow or decision path taken
- Core result: gene structure figure file path
- Constraints, risks, caveats (e.g., multi-isoform genes, annotation version)
- Unresolved items and next-step checks

## Input Validation

This skill accepts: gene symbol inputs for structure visualization, with optional domain and mutation overlays.

If the request does not involve gene structure visualization — for example, asking to perform sequence alignment, predict protein structure, or analyze expression data — do not proceed. Instead respond:

> "`gene-structure-mapper` is designed to visualize gene exon-intron structure. Your request appears to be outside this scope. Please provide a gene symbol and desired output format, or use a more appropriate tool for your task."

## Error Handling

- If `--gene` is missing, state that the gene symbol is required and provide an example.
- If the gene symbol is not found in Ensembl (HTTP 400/404), print: `Error: Gene not found: {gene_name}. Check the gene symbol and try again.` and exit with code 1.
- If `--mutations` contains non-numeric values, reject with: `Error: --mutations must be comma-separated integers (codon positions).`
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks
