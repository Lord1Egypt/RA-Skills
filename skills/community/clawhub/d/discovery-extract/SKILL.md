---
name: discovery-extract
description: Cross-domain scientific discovery through structured extraction of scientific publications. What one paper solves, another needs — this skill extracts provides/requires relationships to surface hidden connections between fields.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - gh
    emoji: "🔬"
    homepage: https://github.com/pcdeni/discovery-engine
---

# Discovery Engine — Paper Extraction Skill

## Why This Exists

A nanofiltration paper **provides** selective passage below a size threshold.
A drug delivery paper **requires** selective transport to a target.
Neither team knows the other exists — they publish in different journals, use different vocabulary, and will never cite each other.

This skill extracts structured **provides/requires** relationships from scientific papers, building a knowledge graph that surfaces these hidden cross-domain connections. Each paper you extract adds a node. The graph finds the bridges.

## When to Use

| Trigger | Action |
|---------|--------|
| `/discovery-extract` | Discover papers, extract, and save results |
| "Extract some papers" | Run the full pipeline (discover → extract → save) |
| "Submit my extractions" | Create a PR with your batch results |
| "Find papers from arXiv" | Discover from a specific source |

## Core Concept

Every paper is decomposed into:
- **Part A (Facts)**: entities, properties, relations — what the paper reports
- **Part B (Cross-domain)**: core friction, mechanism, bridge tags, provides/requires interface, unsolved tensions — what connects it to other fields

The `cross_domain` section is where discovery happens. The `provides` and `requires` fields use abstract functional language (not domain jargon) so a materials science paper can match a biology paper.

## You Are the Extractor

No external API keys or LLM calls needed — you read the paper text and produce the structured JSON yourself. The bundled prompt (`references/prompt.txt`) is your extraction specification.

## How It Works

1. Run `python scripts/extract.py discover` to find new papers with abstracts
2. Read `references/prompt.txt` — the full extraction format specification
3. For each paper: read its abstract and produce the extraction JSON following the prompt
4. Save each result via `python scripts/extract.py save`
5. Optionally submit results as a PR via `gh`

## Step 1: Discover Papers

```bash
python scripts/extract.py discover --count 5
```

This outputs a JSON array of papers (id, source, title, abstract) to stdout.
Already-processed papers are automatically excluded.

To target a specific source:
```bash
python scripts/extract.py discover --source arxiv --count 5
python scripts/extract.py discover --source pmc --count 5
```

## Step 2: Read the Extraction Prompt

Read `references/prompt.txt` to understand the output format. It specifies:
- **Part A (Facts)**: entities, properties, relations
- **Part B (Cross-domain)**: core_friction, mechanism, bridge_tags, provides/requires interface, unsolved_tensions

The prompt contains detailed rules, examples, and a self-check procedure.

## Step 3: Extract

For each paper from Step 1, produce a JSON object following the schema in
`references/prompt.txt`. The paper's abstract is your input text.

Write the JSON to a temporary file (e.g., `/tmp/result.json` or any local path).

**Key requirements:**
- Output ONLY valid JSON (no markdown wrapping, no commentary)
- The top-level key must be `paper_analysis` (not `analysis`)
- `unsolved_tensions` entries must be objects with `{tension, constraint_class, why_it_matters, source_quote}`
- `provides` entries must be objects with `{operation, description, performance, conditions}`
- `requires` entries must be objects with `{operation, description, reason}`
- `bridge_tags` must be abstract functional descriptors, not domain nouns
- The `cross_domain` section is where discovery happens — invest effort here

## Step 4: Save Results

```bash
python scripts/extract.py save /tmp/result.json \
  --paper-id "arxiv:2401.00001" \
  --source arxiv \
  --title "Paper Title Here"
```

The save command normalizes format issues, validates, adds metadata, and saves
to `~/.discovery/data/batch/`. It will report any validation warnings.

## Step 5: Validate (optional)

```bash
python scripts/extract.py validate ~/.discovery/data/batch/
```

## Step 6: Submit Results (optional)

After extracting a batch, submit results as a PR:

```bash
# Fork (first time only)
gh repo fork pcdeni/discovery-engine --clone=false

# Clone your fork
gh repo clone pcdeni/discovery-engine discovery-engine-submit
cd discovery-engine-submit

# Create branch and copy results
BRANCH="contrib/$(gh api user --jq .login)/$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"
cp ~/.discovery/data/batch/*.json submissions/
git add submissions/
git commit -m "Add extraction results"
git push -u origin "$BRANCH"

# Create PR
gh pr create --title "extraction: $(ls submissions/*.json | wc -l) papers" \
  --body "Extraction results from discovery-extract skill" \
  --repo pcdeni/discovery-engine
```

GitHub Actions CI validates submissions and auto-merges passing PRs.

## Bundled Files

| File | Purpose |
|------|---------|
| `scripts/extract.py` | Paper discovery, normalization, validation, saving (Python stdlib only) |
| `references/prompt.txt` | The extraction format specification (444 lines) |
| `references/schema.json` | JSON schema for validation |
