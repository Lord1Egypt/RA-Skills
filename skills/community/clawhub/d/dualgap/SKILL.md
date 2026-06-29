---
name: dualgap
description: "Use DualGap for dual-domain research gap analysis: turn two paper collections, PDF folders, arXiv downloads, or research directions into reviewer-checked literature notes, direction-level syntheses, cross-domain comparison, research-gap analysis, and ranked improvement ideas. Use this skill when the user wants critical multi-paper research planning grounded in PDF evidence rather than generic summaries."
compatibility: Requires Python 3.10+ and an OpenAI-compatible chat completion API. PDF text extraction uses pypdf when available and can fall back to pdftotext if installed.
---

# DualGap

DualGap performs dual-domain research gap analysis over two PDF corpora. It produces per-paper notes, independent quality reviews, direction-level syntheses, cross-domain comparison, research gaps, ranked improvement ideas, and validation reports.

## When To Use

Use this skill when the user wants to:

- compare two research directions from PDF folders
- turn arXiv downloads or paper collections into critical literature notes
- identify research gaps and ranked follow-up ideas
- produce reviewer-checked outputs grounded in PDF evidence

Do not use it for single-paper summarization, casual bibliography formatting, or tasks that do not need LLM-based literature analysis.

## Required Inputs

Collect these before running the workflow:

- Direction A PDF directory
- Direction A name
- Direction B PDF directory
- Direction B name
- Output directory
- Research agenda, priorities, and exclusions
- LLM API access through either:
  - `--env-file` plus `--env-prefix`, such as `QWEN_API_KEY`, `QWEN_BASE_URL`, `QWEN_MODEL`
  - `--config` JSON with `base_url`, `api_key`, and `model`
  - already-set environment variables

Never ask the user to paste a real API key into generated notes, logs, examples, or committed files. Prefer a local env file outside output directories.

## Agent Workflow

1. Parse the user's two PDF directories, direction names, output directory, API configuration, and agenda.
2. Check that both PDF directories exist and contain PDFs.
3. If API configuration is missing, ask for an env file path, config file path, or existing environment-variable prefix before running.
4. Install dependencies if needed with `python -m pip install -r requirements.txt`.
5. Run `scripts/run_literature_workflow.py` from this skill directory.
6. Run `scripts/validate_outputs.py <out-dir>`.
7. Inspect the audit report and at least a small sample of generated notes.
8. Summarize output paths, validation status, failed notes if any, and the most useful synthesis files.

## Prompt Invocation Example

```text
Use $dualgap.

LLM API env file:
<workspace>\config\qwen.env

Env prefix:
QWEN

Direction A PDF directory:
<workspace>\papers\direction_a

Direction A name:
Graph Neural Networks

Direction B PDF directory:
<workspace>\papers\direction_b

Direction B name:
Federated Learning

Output directory:
<workspace>\outputs\dualgap

Agenda:
Find concrete research gaps at the intersection of both directions. Prioritize performance, scalability, communication cost, model quality, and realistic validation plans. Do not focus mainly on privacy, fairness, or poisoning.
```

## Recommended Command

```powershell
python scripts\run_literature_workflow.py `
  --dir-a <workspace>\papers\direction_a `
  --dir-b <workspace>\papers\direction_b `
  --name-a "Direction A" `
  --name-b "Direction B" `
  --out <workspace>\outputs\dualgap `
  --env-file <workspace>\config\qwen.env `
  --env-prefix QWEN `
  --agenda "Prioritize concrete cross-domain research gaps, mechanisms, validation plans, costs, scalability, and unrealistic assumptions." `
  --batch-size 10 `
  --api-retries 5 `
  --api-timeout 180
```

For a cheap smoke test, add:

```powershell
--limit-a 1 --limit-b 1 --batch-size 1
```

Then validate:

```powershell
python scripts\validate_outputs.py <workspace>\outputs\dualgap
```

## Output Contract

The workflow writes:

```text
out/
  extracted_texts/
  notes/
  reviews/
  synthesis_reviews/
  raw/
  syntheses/
    direction_a_synthesis.md
    direction_b_synthesis.md
    cross_direction_analysis.md
    research_gaps.md
    improvement_ideas_ranked.md
  audit_report.md
  workflow_manifest.json
```

## Quality Rules

- Notes must be critical, paper-specific, and grounded in extracted PDF evidence.
- Every note needs an independent reviewer pass record.
- Failed notes are rewritten once using reviewer feedback.
- Synthesis files also receive independent review.
- Research gaps must explain why adjacent papers do not already solve the gap.
- Separate author evidence, model inference, and uncertain hypotheses.
- If notes truncate, rerun with a larger `--max-tokens` value.

For detailed schemas and review criteria, load `references/note_schema.md` only when needed. For validation details, load `references/validation_protocol.md`.

## Validation

Use:

```powershell
python scripts\self_validate_skill.py
```

This checks skill metadata, Python compilation, eval schema, simulated output validation, and accidental key-leak patterns.
