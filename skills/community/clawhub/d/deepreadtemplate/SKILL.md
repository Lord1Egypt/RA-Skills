---
name: literature-deep-read-report
description: This skill should be used when a user provides an academic paper (PDF file, DOI, arXiv link, or title) and asks for a structured deep-read report or literature summary. It extracts the full paper text, quotes exact numbers from the original, and produces a deep, visually structured report with a mechanism diagram, covering background, variables, paradigm/method, task flow, design details, statistical analysis, and main results. Trigger on phrases such as 精读这篇论文, 做一份文献精读报告, 分析这篇文章的方法与设计, 总结这篇研究, summarize this paper, or deep-read report.
version: 1.1.0
---

# Literature Deep-Read Report

## Overview

This skill converts a research paper into a deep, reusable report that a graduate student, reviewer, or researcher can file and cite. It enforces a consistent scaffold — background, variables, paradigm/method, task flow, design details, statistical analysis, main results — and goes further by quoting exact numbers from the full text, drawing a mechanism/method diagram, and adding an "implications for the reader's research" section. The skill reads the actual paper text (downloading and extracting the PDF when possible); it does not invent findings.

## When to Use

Activate this skill when the user:

- Attaches or links a paper (PDF, DOI, arXiv, PubMed, or journal URL) and asks for a "精读", "文献报告", "深度总结", or "deep-read".
- Asks to extract a study's method, variables, design, or results for a literature review.
- Says "分析这篇论文的设计/统计/范式" or "帮我整理这篇文献".
- Wants a comparable one-page-per-paper note for a reading list.

Do not activate for: pure citation formatting, plagiarism checks, or non-academic documents. If the user only wants a one-line summary, still deliver the full scaffold but keep each section brief.

## Execution Logic

### Step 1 — Acquire the FULL text (not just the abstract)

Resolve the input in this priority order:

1. Local PDF path → extract text with a PDF text library (e.g., Python `pypdf` or `pdfplumber`). Do not settle for the abstract when the full text is obtainable.
2. DOI or arXiv/PubMed link → download the PDF (open access or preprint) and extract text. If paywalled, fetch the abstract plus any public preprint from an author repository (OSF, ResearchGate, or university repositories such as WRAP).
3. Title only → search the web for the PDF/preprint and confirm with the user before proceeding.

Only if the full text is truly unobtainable, build the report from abstract + available sections and mark it "全文未获取，以下基于摘要与公开信息".

### Step 2 — Parse the structure

Map the paper's real sections (Introduction, Methods, Results, Discussion) onto the required components. Do not force a mismatch — if a component is genuinely absent, say so.

### Step 3 — Extract each component with exact numbers

Use the scaffold in `references/deep-read-template.md` and fill:

- **背景 (Background):** the gap, research question, and why it matters.
- **变量 (Variables):** independent, dependent, moderators/mediators, control variables, and how each was measured. For computational papers, include the parameter-to-mechanism mapping table (e.g., DDM drift rate vs starting point).
- **范式方法 (Paradigm / Method):** the overarching paradigm (e.g., RL + DDM computational modeling, fMRI, survey, experiment) and the modeling or analytical approach.
- **任务流程 (Task Flow):** the participant's step-by-step experience or the analysis pipeline.
- **设计细节 (Design Details):** design type, sample size (N), stimuli, trials, counterbalancing, software, parameters.
- **统计分析 (Statistical Analysis):** tests, models, corrections, and model-comparison criteria (e.g., DIC/ΔDIC, BIC, BF).
- **主要结果 (Main Results):** key findings with exact estimates, effect sizes, CIs, and p-values.

Copy numbers verbatim from the paper. Record section/page where possible.

### Step 4 — Render a DEEP, VISUAL report

Produce two artifacts:

1. A markdown report (archival / citable).
2. A polished, self-contained HTML report (no external libraries) as the primary deliverable, containing:
   - A header with the full citation, DOI, and a one-line contribution.
   - A mechanism/method diagram (inline SVG) illustrating the core paradigm (e.g., a DDM with starting-point bias and drift rate, an RL update loop, or a task timeline).
   - The seven sections with exact numbers quoted.
   - A model-comparison or key-result chart/table (e.g., ΔDIC bar chart, parameter table, or condition comparison table).
   - A "对本研究者的启示 (Implications)" section with 3-5 concrete, actionable points for the reader's own work.
   - Limitations and a sources/method footer.

## Output Structure

The report must contain these headings (in this order):

0. **一句话贡献 (One-line Contribution)**
1. **背景 (Background)**
2. **变量 (Variables)**
3. **范式方法 (Paradigm / Method)**
4. **任务流程 (Task Flow)**
5. **设计细节 (Design Details)**
6. **统计分析 (Statistical Analysis)**
7. **主要结果 (Main Results)**
8. **局限与可复现性 (Limitations & Reproducibility)**
9. **对本研究者的启示 (Implications for the Reader's Research)**

A filled template and a worked computational-modeling example are in `references/deep-read-template.md`.

## Depth Requirements

Before finishing, verify the report satisfies ALL of the following:

- [ ] Full text acquired and extracted (not abstract-only) whenever the PDF is obtainable.
- [ ] Exact numbers quoted from the paper: N, trials, parameter estimates, effect sizes, p-values, model-fit indices.
- [ ] A mechanism/method diagram (inline SVG) illustrating the core paradigm.
- [ ] A model-comparison or key-result table/chart.
- [ ] An "Implications for the reader's research" section with 3-5 concrete points.
- [ ] Nothing fabricated; every inferred claim marked "推断".

If any item is unchecked, retrieve more of the paper text and re-render before delivering.

## Reliability Rules

- Quote the paper; never hallucinate statistics, p-values, or sample sizes.
- Mark every inferred (non-explicit) claim as "推断".
- If the text is unavailable, state it and degrade gracefully to an abstract-based report.
- Preserve the authors' original terminology for variables and methods; add Chinese glosses in parentheses.
- The HTML report must be self-contained (no CDN / external JS), so it renders offline.

## Resources

- `references/deep-read-template.md` — the deep-read scaffold, per-section extraction prompts, mechanism-diagram guidance, and a worked DDM example.
