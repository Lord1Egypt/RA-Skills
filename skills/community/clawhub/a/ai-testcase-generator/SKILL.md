---
name: ai-testcase-generator
description: Use when turning requirements, screenshots, or other QA inputs into structured test cases and review questions with an AI-assisted workflow.
tags: [testing, qa, testcases, ai, automation, review]
version: 1.0.1
---

# AI Test Case Generator

This ClawHub package is documentation-only. It does not embed runtime binaries, install scripts, or package manifests.

## When to use

- A user wants test cases from a PRD, specification, screenshot, or plain text brief.
- You need a structured review loop for QA coverage before implementation or release.
- You want a checklist for turning requirements into executable test work.

## Inputs to collect

- Requirement text or a file path
- Product stage: requirement review, implementation, or pre-release
- Preferred output language
- Any focus area such as security, edge cases, compatibility, or accessibility

## Recommended workflow

1. Extract the core flows.
   Identify user journeys, rules, dependencies, and constraints.
2. Group coverage by module.
   Organize cases by feature area, API, UI surface, or role.
3. Add negative and edge paths.
   Include invalid input, permission boundaries, failures, and concurrency where relevant.
4. Run a review pass.
   Check coverage, clarity, execution readiness, and security impact.

## Recommended outputs

- Test scope summary
- Test points grouped by module
- Detailed cases with steps and expected results
- Priority or severity labels
- Open questions for product or engineering

## Guardrails

- Keep uploaded requirements confidential.
- State clearly when a case depends on missing product detail.
- Do not claim that spreadsheet, XMind, or binary exports were produced unless an actual generator runtime was used outside this skill bundle.
