---
name: agentic-delivery-skill
description: >-
  Create CompleteTech LLC delivery execution artifacts for approved agentic development engagements, including kickoff agendas, access checklists, project plans, milestone trackers, status updates, decision logs, risk/issue logs, change request intake, prototype review, evaluation reports, acceptance packets, launch readiness, monitoring, support, handoff, runbooks, quickstarts, closeout, post-launch review, and escalation procedures. Use after proposal/SOW or contract approval when Codex needs to run bounded agentic workflow delivery cleanly.
version: 1.0.9
metadata:
  openclaw:
    skillKey: agentic-delivery-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-delivery-skill
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

# Agentic Delivery Skill

## Purpose

| Use | Scope |
|---|---|
| Delivery artifact generation | Create execution artifacts for approved CompleteTech LLC agentic development engagements. |
| Starting point | Use after proposal/SOW or contract approval is current. |
| Operating boundary | Keep outputs inside approved scope; route new or unapproved work to proposal/change control. |

## System Boundary

| Boundary | Use |
|---|---|
| This skill | Kickoff, project control, evaluation, launch preparation, handoff, support, and closeout artifacts after approval. |
| `agentic-proposal-skill` | Unapproved commercial scope, change requests, or new workflow expansion. |
| `agentic-contract-skill` | Legal agreement artifacts and signature-authority questions. |
| `agentic-security-review-skill` | Security-sensitive work, production readiness, credentials, permissions, data handling, or launch risk. |
| `agentic-invoice-skill` | Billing, payment requests, credits, receipts, and invoice events. |
| `agentic-customer-success-skill` | Relationship health, renewal, expansion planning, and account state. |
| `agentic-case-study-skill` | Proof only after outcomes are verified and approved. |

## Core Workflow

| Step | Action |
|---|---|
| 1 | Identify the delivery need: kickoff, access, planning, status, decisions, risk/issue, change request, prototype review, evaluation, acceptance, launch, monitoring, support, handoff, closeout, or escalation. |
| 2 | Gather verified delivery facts. |
| 3 | Use `references/use-case-decision-table.md` to choose the right delivery artifact. |
| 4 | Use `references/delivery-positioning.md` for CompleteTech LLC delivery framing and guardrails. |
| 5 | Use `references/delivery-catalog.md` for the near-exhaustive delivery artifact library. |
| 6 | Keep delivery practical and bounded; do not fabricate approvals, test results, metrics, legal claims, or production readiness. |

| Required Fact | Examples |
|---|---|
| Approved work | Approved scope, workflow, milestone, change request, or acceptance criteria. |
| Ownership | Client owner, delivery owner, reviewers, approvers, and escalation contacts. |
| Execution context | Timeline, systems, dependencies, risks, support expectations, and handoff needs. |
| Evidence | Evaluation examples, test results, logs, approvals, acceptance notes, and launch gates. |

## Artifact Selection Guide

Choose by the current operational event first.

| Event Group | Use These Artifacts |
|---|---|
| Kickoff and access | `kickoff-agenda`, `client-access-checklist`, `project-plan`, `stakeholder-communication-plan` |
| Project control | `milestone-tracker`, `weekly-status-update`, `decision-log`, `risk-and-issue-log`, `dependency-tracker` |
| Change and remediation | `change-request-intake`, `defect-remediation-plan`, `escalation-procedure` |
| Prototype and evaluation | `prototype-review-checklist`, `evaluation-run-report`, `test-results-summary` |
| Acceptance and launch | `acceptance-review-packet`, `launch-readiness-checklist`, `deployment-runbook`, `monitoring-plan` |
| Handoff and support | `support-plan`, `handoff-checklist`, `administrator-runbook`, `user-reviewer-quickstart`, `support-ticket-intake` |
| Closeout and learning | `post-launch-review`, `lessons-learned`, `closeout-summary`, `training-session-plan` |

| Selection Rule | Guidance |
|---|---|
| Several artifacts fit | Choose the one closest to the operational event. |
| Launch, acceptance, or complete status | Do not mark ready, accepted, launched, or complete unless verified evidence supports it. |
| New or changed scope | Use `change-request-intake` and route commercial approval before delivery expands. |

## Quality Rules

| Rule | Requirement |
|---|---|
| Approved scope | Execute only the approved scope; route new scope into change request intake. |
| Approval gates | Protect human approval gates for external communications, production changes, purchases, data export, and material business decisions. |
| Project controls | Track decisions, risks, issues, dependencies, and acceptance evidence explicitly. |
| Evaluation | Verify evaluation examples before acceptance. |
| Operations | Document logs, monitoring, runbooks, quickstarts, support, and handoff. |
| Unknowns | Use `TBD` or open questions for unknowns. |

## Resource Guide

| Resource | Role |
|---|---|
| `references/delivery-positioning.md` | CompleteTech LLC delivery language and boundaries. |
| `references/use-case-decision-table.md` | Delivery artifact selection for the current operational event. |
| `references/delivery-lifecycle.md` | Flow from kickoff through support and closeout. |
| `references/delivery-catalog.md` | Near-exhaustive delivery template library. |
| `references/template-index.json` | Machine-readable template metadata used by the renderer. |
| `scripts/render_delivery.py` | Lists delivery artifacts or renders a draft with placeholders. |

## Runtime Permissions

| Capability | Boundary |
|---|---|
| Files read | Bundled templates, references, examples, `assets/logo.png`, and user-provided Markdown or variable inputs. |
| Files written | Only user-selected `--out`, `--png`, `--markdown-out`, or default `output/` artifact paths. |
| Local commands | `scripts/render_delivery.py` and `scripts/render_pdf.py`. |
| Not required | Network access, credential access, persistence, privilege escalation, destructive file operations, background services, or project-system API calls. |

## Renderer

| Task | Command |
|---|---|
| List all delivery artifacts | `python3 scripts/render_delivery.py --list` |
| List artifacts for a stage | `python3 scripts/render_delivery.py --stage status --list` |
| Render a kickoff agenda | `python3 scripts/render_delivery.py --template kickoff-agenda --var client_name=Acme --var workflow="support triage"` |

| Output Rule | Requirement |
|---|---|
| Draft status | Rendered artifacts remain drafts until verified by the delivery owner. |
| Placeholders | Replace every placeholder with verified project facts before sending, storing, or using as evidence. |
| Approval-sensitive outputs | Do not treat acceptance, launch, production, or handoff language as final without recorded approval. |

## Rendering to a Branded PDF

| Render Goal | Use |
|---|---|
| Primary artifact | Branded CompleteTech LLC delivery PDF. |
| Optional outputs | Markdown source and PNG preview from the same local command. |
| Delivery boundary | PDF output is still a delivery draft until approval evidence is recorded. |

One-command delivery artifact render:

```bash
pip install -r requirements.txt
python3 scripts/render_delivery.py --template launch-readiness-checklist \
  --out artifact.pdf --png artifact.png \
  --markdown-out artifact.md \
  --title "Launch Readiness Checklist" --doc-type "DELIVERY ARTIFACT" \
  --subtitle "Northwind Trading Co. - Support Email Triage Agent (Pilot)" \
  --meta "DOCUMENT NO.=DEL-2026-0233" --meta "DATE=2026-06-12" \
  --var client_name="Client Name" --var workflow="support triage"
```

| Output Option | Flag |
|---|---|
| Branded PDF | `--out artifact.pdf` |
| PNG preview | `--png artifact.png` |
| Markdown source | `--markdown-out artifact.md` |
| Markdown only | `--no-pdf` |
| No cover page | `--no-cover` |

| Existing Markdown Render | Command |
|---|---|
| Convert delivery Markdown to PDF | `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "Launch Readiness Checklist" --doc-type "DELIVERY ARTIFACT"` |

| Rendering Support | Details |
|---|---|
| Markdown subset | `#`, `##`, `###`, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. |
| Required package | `reportlab==4.5.1` for PDF rendering. |
| Optional preview packages | `pypdfium2==5.8.0` and `pillow==12.2.0` for `--png`. |
| Example output | See `assets/examples/` for rendered Markdown, PDF, and PNG artifacts. |

## Network Boundary

| Boundary | Requirement |
|---|---|
| Local-only runtime | No outbound network helpers, callbacks, telemetry, receipt helpers, or delivery-run metadata posting. |
| External actions | Does not deploy, launch, send, publish, or call project-management systems. |
| Approval-sensitive work | Launch, production, customer send, and acceptance actions require verified approval outside this renderer. |
