# SKILL.md — Pipeline Pattern
# Pattern: Pipeline
# Use: Enforce strict sequential workflow with hard checkpoints

---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when the user asks to document a module, generate API docs, or create documentation from code.

metadata:
  pattern: pipeline
  steps: "4"
  version: 1.0
---

## Role
You are running a documentation generation pipeline.

## CRITICAL INSTRUCTION
**Execute each step in order. Do NOT skip steps or proceed if a step fails.**

## Step 1 — Parse & Inventory
Analyze the user's Python code to extract:
- All public classes
- All public functions
- All public constants

Present the inventory as a checklist.
Ask: "Is this the complete public API you want documented?"

**GATE:** Do NOT proceed until user confirms.

## Step 2 — Generate Docstrings
For each function lacking a docstring:
1. Load 'references/docstring-style.md' for the required format
2. Generate a docstring following the style guide exactly
3. Present each generated docstring for user approval

**GATE:** Do NOT proceed to Step 3 until user confirms ALL docstrings.

## Step 3 — Assemble Documentation
1. Load 'assets/api-doc-template.md' for the output structure
2. Compile all classes, functions, and docstrings into a single API reference document

## Step 4 — Quality Check
Review against 'references/quality-checklist.md':
- Every public symbol documented
- Every parameter has a type and description
- At least one usage example per function

Report results. Fix issues before presenting final document.

## Important
- Execute steps sequentially
- Honor all gates — wait for explicit user confirmation
- Do not proceed if any step fails
- Keep context clean by only loading references when needed
