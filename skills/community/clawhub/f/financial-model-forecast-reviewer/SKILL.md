---
name: financial-model-forecast-reviewer
description: >-
  Help users with Validated demand: Founders, analysts, and operators need help reviewing financial models, checking assumptions, building revenue or expense forecasts, and turning spreadsheets into scenario plans. This requirement is supported by 11 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.. Use when a user asks for business-and-operations, financial model, forecast, scenario planning, runway, or needs a practical workflow, artifact, checklist, analysis, or implementation support for this requirement.
---

# Financial Model Forecast Reviewer

## Requirement

Use this skill to help startup founders, finance analysts, operators, consultants, and managers responsible for forecasts, runway planning, and spreadsheet models with:

> Validated demand: Founders, analysts, and operators need help reviewing financial models, checking assumptions, building revenue or expense forecasts, and turning spreadsheets into scenario plans. This requirement is supported by 11 separate online signals across 2 source families, so it represents broader demand rather than a single isolated request.

Demand score: 90/100 (`70/70` demand, `30/30` local feasibility).
Evidence: 11 signals across 2 source families.

Read `references/requirement-plan.md` when source evidence, planning details, or review criteria are needed.

## Workflow

1. Restate the user's outcome, constraints, available inputs, and success criteria.
2. Turn the operational problem into a repeatable process, checklist, template, or lightweight analysis.
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

Keywords: `business-and-operations`, `financial model`, `forecast`, `scenario planning`, `runway`, `assumptions`

Example trigger sentences:

- `Help me Founders, analysts, and operators need help reviewing financial models, checking assumptions, building revenue or expens.`
- `I need a practical workflow for Founders, analysts, and operators need help reviewing financial models, checking assumptions, building revenue or expens.`
- `Use $financial-model-forecast-reviewer to handle Founders, analysts, and operators need help reviewing financial models, checking assumptions, building revenue or expens.`
