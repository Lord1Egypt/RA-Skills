---
name: agentic-browser-workflow-templates
description: Generate repeatable, audit-friendly browser-agent workflow templates for form filling, case routing, portal operations, research capture, and approval-gated web actions.
---

# Agentic Browser Workflow Templates

Use this skill when browser automation needs a reusable operating template rather than a one-off prompt.

## Workflow

1. Choose a use case such as `form-filling`, `case-routing`, `portal-operation`, or `research-capture`.
2. Provide optional steps as JSON, or let the script generate a safe starter workflow.
3. Review the generated controls before connecting to live browser/computer-use tools.
4. Pair with Browser Agent Trust Hub for runtime policy scoring.

## Parameters

- `--use-case`: Workflow type.
- `--portal`: Portal or website category.
- `--steps PATH`: Optional JSON list of workflow steps.
- `--output PATH`: Optional YAML-like markdown output path.
- `--json`: Emit JSON instead of markdown.
- `--approval-threshold {low,normal,high}`: Sets human approval strictness.

## Outputs

The script generates:

- Objective and assumptions.
- Step-by-step browser workflow.
- Approval gates.
- Evidence capture requirements.
- Error handling and rollback/degraded-mode notes.
- Handoff payload schema.

This skill does not execute browser actions.
