---
name: error-message-improver
description: >-
  Help users with Validated demand: Remote workers and technically curious households need local diagnostic workflows for network issues such as bufferbloat, router problems, and latency. This requirement is supported by 10 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.. Use when a user asks for general-help, bufferbloat, router, modem, latency, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Error Message Improver

## Requirement

Use this skill to help remote workers, gamers, home-office users, and small teams who need to diagnose internet quality with consumer networking hardware with:

> Validated demand: Remote workers and technically curious households need local diagnostic workflows for network issues such as bufferbloat, router problems, and latency. This requirement is supported by 10 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.

Demand score: 90/100 (`70/70` demand, `30/30` local feasibility).
Evidence: 10 signals across 2 source families.

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Convert the request into a practical plan and useful output.
3. Ask only for missing information that materially changes the output; otherwise make reasonable assumptions and continue.
4. Keep the implementation local-hardware friendly: prefer scripts, templates, checklists, and small-model or CPU-safe workflows over cloud-only or large-training approaches.
5. Produce the requested artifact, workflow, checklist, analysis, code change, or decision support.
6. Validate the output against the success criteria and list any remaining risks or follow-up work.

## Expected Outputs

- A tailored answer or artifact for the user's immediate situation.
- A reusable checklist or workflow when the task is repeatable.
- A verification note showing how the result was checked.

## Validation

- The output directly addresses the discovered requirement.
- The user can act on the result without reading the original source post.
- Assumptions, limits, and required inputs are visible.
- The final response includes a short usage or next-step note when helpful.

## Triggers

Keywords: `general-help`, `bufferbloat`, `router`, `modem`, `latency`, `network troubleshooting`

Example trigger sentences:

- `Help me Remote workers and technically curious households need local diagnostic workflows for network issues such as bufferbloat.`
- `I need a practical workflow for Remote workers and technically curious households need local diagnostic workflows for network issues such as bufferbloat.`
- `Use $error-message-improver to handle Remote workers and technically curious households need local diagnostic workflows for network issues such as bufferbloat.`
