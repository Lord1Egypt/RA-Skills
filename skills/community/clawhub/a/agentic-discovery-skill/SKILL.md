---
name: agentic-discovery-skill
description: >-
  Create CompleteTech LLC discovery and scoping artifacts for agentic development opportunities, including intake questionnaires, workflow discovery scripts, stakeholder interview guides, current/future-state workflow maps, systems/data readiness checklists, approval gate reviews, risk/excluded-use checks, success criteria, evaluation examples, pilot readiness scorecards, and proposal/SOW handoff briefs. Use before proposal, contract, invoice, or delivery work when Codex needs to gather verified facts for bounded agentic workflow services.
version: 1.0.3
metadata:
  openclaw:
    skillKey: agentic-discovery-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-discovery-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: pypdfium2==5.8.0
      - kind: uv
        package: pillow==12.2.0
      - kind: uv
        package: pyyaml==6.0.3
---

# Agentic Discovery Skill

## Purpose

Create discovery and scoping artifacts that turn an agentic development opportunity into verified facts for proposal/SOW, contract, invoice, and delivery work.

## System Boundary

This skill owns pre-sale fact-finding and scoping. Hand off to `agentic-proposal-skill` for buyer-facing scope and SOW documents, `agentic-security-review-skill` for formal security or launch risk review, `agentic-delivery-skill` after approval, and `agentic-customer-success-skill` for ongoing relationship management. Do not use discovery artifacts as final proposals, contracts, invoices, launch signoffs, or public proof.

## Core Workflow

1. Identify the discovery need: qualification, intake, stakeholder interview, workflow map, readiness check, risk review, success criteria, evaluation examples, prioritization, recap, or proposal handoff.
2. Gather verified facts only: repeated workflow, inputs, systems, tools, retrieval sources, decision points, approval gates, risks, exclusions, logging, monitoring, documentation, support, and handoff needs.
3. Use `references/use-case-decision-table.md` to choose the right artifact.
4. Use `references/discovery-positioning.md` for CompleteTech LLC framing and guardrails.
5. Use `references/discovery-catalog.md` for near-exhaustive artifact templates.
6. Keep discovery practical and bounded. Do not fabricate client facts, proof, savings metrics, regulated-use assurances, legal claims, or implementation feasibility.

## Artifact Selection Guide

- First-pass lead fit: use `quick-qualification-checklist`.
- New opportunity intake: use `client-intake-questionnaire`.
- Live discovery call: use `workflow-discovery-script`.
- Multiple roles or departments: use `stakeholder-interview-guide`.
- Existing process documentation: use `current-state-workflow-map`.
- Proposed reviewed-agent process: use `future-state-agentic-workflow-map`.
- System, document, data, or access review: use `systems-and-data-access-checklist`.
- API/tool feasibility: use `tool-api-readiness-checklist`.
- Approval and escalation design: use `human-approval-gate-checklist`.
- Regulated, sensitive, or risky workflow: use `risk-and-excluded-use-checklist`.
- Buyer asks what success looks like: use `success-criteria-worksheet`.
- Need test examples: use `evaluation-example-worksheet`.
- Decide whether to propose a pilot: use `pilot-readiness-scorecard`.
- After discovery call: use `discovery-recap-memo`.
- Handoff into proposal/SOW: use `requirements-brief-for-proposal-sow-handoff`.
- Missing facts or assumptions: use `assumptions-and-unknowns-log`.
- Ownership unclear: use `stakeholder-responsibility-matrix`.
- Dependencies unclear: use `implementation-dependency-checklist`.
- Sensitive data or retention concerns: use `data-sensitivity-and-retention-worksheet`.
- Several possible workflows: use `workflow-prioritization-matrix`.
- Need logging/monitoring requirements: use `logging-and-monitoring-needs-worksheet`.
- Need support/handoff expectations: use `support-and-handoff-discovery-worksheet`.
- Need production-readiness check: use `pilot-to-production-readiness-checklist`.

When several artifacts fit, choose the earliest artifact that resolves the biggest unknown. Do not draft proposal/SOW scope until the workflow, owners, approval points, success criteria, dependencies, and exclusions are clear enough to avoid vague scope.

## Quality Rules

- Frame discovery as bounded workflow scoping, not AI brainstorming.
- Always identify human approval points for external communication, production changes, purchases, data export, and material business decisions.
- Capture risks, excluded uses, data sensitivity, and assumptions explicitly.
- Make outputs easy to hand to `agentic-proposal-skill`.
- Use `TBD` or open questions for unknowns.

## Resource Guide

- `references/discovery-positioning.md`: load for CompleteTech LLC discovery language and boundaries.
- `references/use-case-decision-table.md`: load when choosing an artifact.
- `references/discovery-lifecycle.md`: load for flow from lead qualification through proposal handoff.
- `references/discovery-catalog.md`: load for the near-exhaustive artifact library.
- `references/template-index.json`: machine-readable template metadata used by the renderer.
- `scripts/render_discovery.py`: list discovery artifacts or render a draft with placeholders.

## Renderer

```bash
python3 scripts/render_discovery.py --list
python3 scripts/render_discovery.py --stage readiness --list
python3 scripts/render_discovery.py --template client-intake-questionnaire --var client_name=Acme --var workflow="support triage"
```

Rendered artifacts are drafts. Replace placeholders with verified client facts and refine questions for the meeting context.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. The renderer emits the PDF (and prints the Markdown) in **one command**, using the same reportlab branding engine as the contract skill:

```bash
pip install -r requirements.txt
python3 scripts/render_discovery.py --template requirements-brief-for-proposal-sow-handoff \
  --out artifact.pdf --png artifact.png \
  --title "Requirements Brief — Proposal / SOW Handoff" --doc-type "DISCOVERY HANDOFF" \
  --subtitle "Prepared for <b>Northwind Trading Co.</b>" --meta "DOCUMENT NO.=DISC-2026-0117" --meta "DATE=2026-05-15" \
  --var client_name="Client Name" --var workflow="support triage"
```

- `--no-pdf` emits Markdown only (the original behavior); `--no-cover` drops the cover page.
- Already drafted the Markdown yourself? Render it directly: `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."`.
- The PDF supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. PDF requires `reportlab`; the optional `--png` preview requires `pypdfium2` and `pillow`. See `assets/examples/` for a rendered example.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts discovery run metadata to an external service.
