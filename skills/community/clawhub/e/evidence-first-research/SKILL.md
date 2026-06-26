---
name: evidence-first-research
description: Evidence-first workflow for scientific research, literature review, method selection, study planning, biomedical analysis, and research writing. Use when Codex should pause before acting to search for prior papers, datasets, protocols, software, libraries, reporting standards, or methodological patterns, then decide whether to adopt, adapt, benchmark, or design a new approach. Especially useful for medicine, public health, biology, translational research, clinical questions, and any task where evidence quality, safety, or reproducibility matters.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/ZackZ2025/evidence-first-research
---

# Evidence First Research

## Overview

Use a research-before-starting workflow. Search existing evidence, tools, datasets, and established patterns before drafting an analysis plan, recommending a method, or producing scientific content.

Default to reuse or adaptation of validated approaches. Only introduce a novel method, pipeline, or claim of novelty after establishing that the gap is real.

## Core Workflow

1. Define the task precisely.
- Restate the objective, target deliverable, domain, and decision stakes.
- Identify whether the task is literature synthesis, study design, data analysis, protocol drafting, manuscript support, tool selection, or interpretation.
- For medical work, identify the population, setting, intervention or exposure, comparator, outcomes, and time horizon when applicable.

2. Search before acting.
- Search for prior papers, systematic reviews, guidelines, benchmark datasets, existing tools, libraries, protocols, ontologies, and reporting standards before proposing work.
- Prefer primary and authoritative sources over tertiary summaries when accuracy matters.
- Search for negative results, contradictory evidence, failure modes, and replication attempts instead of only supportive results.
- Inspect local project artifacts before suggesting a new workflow when the task depends on an existing codebase, dataset, or protocol.

3. Evaluate evidence quality.
- Rank sources by relevance, rigor, recency, and direct applicability to the question.
- Distinguish peer-reviewed papers, preprints, guidelines, textbooks, package documentation, and informal discussion.
- Prioritize strong syntheses and well-matched study designs over isolated or weakly related findings.
- Flag uncertainty explicitly when evidence is indirect, outdated, conflicting, underpowered, or drawn from a mismatched population.

4. Choose the action mode deliberately.
- Adopt an established method when a strong, well-matched pattern already exists.
- Adapt a validated method when the problem is similar but not identical.
- Benchmark multiple credible approaches when the field lacks a dominant standard.
- Design a new approach only after documenting what was searched, what already exists, and why it is insufficient.

5. Execute with traceability.
- State the chosen approach and why it was selected over alternatives.
- Cite the papers, tools, libraries, datasets, or standards that informed the decision.
- Separate evidence, inference, and speculation.
- Preserve assumptions, inclusion criteria, exclusion criteria, and unresolved questions.

6. Re-check before finalizing.
- Verify that the strength of the final claims matches the strength of the underlying sources.
- Re-open the search if a key assumption is unsupported or if a stronger source is likely to exist.
- Perform an extra review for harms, contraindications, bias, and guideline consistency when the output is medically relevant or otherwise high stakes.

## Search Targets

- Search for literature first:
  systematic reviews, meta-analyses, guidelines, seminal papers, recent high-quality studies, protocols, replication studies.
- Search for research infrastructure:
  benchmark datasets, registries, ontologies, reference implementations, software packages, analysis pipelines, laboratory or clinical standards.
- Search for methodological patterns:
  study designs, statistical approaches, outcome definitions, preprocessing conventions, validation schemes, reporting frameworks.
- Search for practical constraints:
  data availability, licensing, regulatory context, ethical constraints, reporting expectations, reproducibility requirements.

## Decision Heuristics

- Prefer "adopt" when the question is standard and the field already has a stable method.
- Prefer "adapt" when the method exists but the data, population, or setting differs.
- Prefer "benchmark" when several plausible methods compete and no clear winner exists.
- Prefer "invent" only after showing that existing methods, tools, or study patterns do not adequately solve the problem.

## Medical Emphasis

- Give extra weight to clinical practice guidelines, systematic reviews, meta-analyses, and pivotal trials when the task involves patient care, diagnostics, treatment, prognosis, or safety.
- Treat preprints, conference abstracts, animal models, in vitro studies, single-center retrospective studies, case reports, and expert opinion as lower-certainty evidence unless the task specifically requires them.
- Avoid patient-specific recommendations without current sources, clear scope limits, and explicit uncertainty.
- Flag when geography, formulary availability, regulatory status, standard of care, or population differences may change the answer.
- Distinguish mechanistic plausibility from clinical effectiveness, and surrogate outcomes from patient-important outcomes.

## Output Pattern

Before doing deep work, produce a concise research checkpoint when useful:

- Objective.
- Search targets.
- Best existing papers, tools, or patterns found so far.
- Evidence strength and important gaps.
- Chosen path: adopt, adapt, benchmark, or invent.
- Main risks, assumptions, and next step.

## Anti-Patterns

- Do not start building, analyzing, or writing as if the problem were novel without checking the literature and existing tools.
- Do not equate "published" with "reliable" or "recent" with "best."
- Do not overgeneralize from weak evidence, surrogate endpoints, or mechanistic arguments.
- Do not rely on abstracts alone when methods or limitations matter.
- Do not ignore population mismatch, confounding, missing comparators, or sample size limitations.
- Do not present speculation as consensus.
- Do not skip contradictory evidence just because it complicates the answer.

## References

- Read [references/evidence-evaluation.md](references/evidence-evaluation.md) when prioritizing sources, appraising medical evidence, or checking for common biomedical failure modes.
