# Evidence-First Research

A Codex skill for scientific work that enforces a research-before-starting workflow.

This skill tells the model to search for prior papers, tools, datasets, protocols, and methodological patterns before proposing a plan or producing output. It is designed to be broadly useful for scientific research, with extra emphasis on medicine, biomedicine, public health, and other evidence-sensitive domains.

## What It Tries To Prevent

- starting analysis as if the problem were novel without checking the literature
- reinventing methods that already have strong precedents
- overclaiming from weak, indirect, or mismatched evidence
- skipping safety, guideline, or reproducibility checks in biomedical work

## Included Files

- `SKILL.md`: core AI-facing workflow
- `agents/openai.yaml`: interface metadata
- `references/evidence-evaluation.md`: source-priority guidance, medical appraisal prompts, and biomedical red flags

## Core Principle

Adopt, adapt, benchmark, or invent only after a real search has established what already exists and how strong the evidence is.
