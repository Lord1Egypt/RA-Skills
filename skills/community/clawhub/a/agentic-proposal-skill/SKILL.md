---
name: agentic-proposal-skill
description: >-
  Create CompleteTech LLC agentic development proposals, statements of work, discovery recaps, pilot recommendations, evaluation plans, risk/control plans, implementation roadmaps, acceptance criteria, change orders, retainer proposals, and procurement-ready scope summaries. Use when Codex needs to bridge outreach emails and signed contracts/invoices by drafting buyer-facing proposal or SOW-style documents for bounded agentic workflow services.
version: 1.0.2
metadata:
  openclaw:
    skillKey: agentic-proposal-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-proposal-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab>=4.0
      - kind: uv
        package: pyyaml>=6.0
---

# Agentic Proposal Skill

## Purpose

Create proposal and SOW-style sales documents for CompleteTech LLC agentic development engagements, from discovery recap through buyer approval.

## System Boundary

This skill owns buyer-facing commercial scope before signature: proposals, SOW attachments, approval summaries, change-order proposals, and pilot recommendations. Use `agentic-discovery-skill` for upstream fact collection, `agentic-contract-skill` for agreement PDFs and legal-template artifacts, `agentic-invoice-skill` for payment requests, `agentic-delivery-skill` after approval, and `agentic-email-skill` only for the covering message that sends or follows up on the proposal.

## Core Workflow

1. Identify the commercial stage: post-discovery recap, pilot proposal, full proposal, SOW, procurement summary, change order, expansion, retainer, or evaluation/risk plan.
2. Gather only verified facts: client, workflow, pain, systems, timeline, budget model, stakeholders, decision criteria, constraints, approval rules, and desired next step.
3. Use `references/use-case-decision-table.md` to choose the right proposal type.
4. Use `references/proposal-positioning.md` for brand language, scope boundaries, proof rules, and guardrails.
5. Use `references/proposal-catalog.md` for near-exhaustive templates.
6. Draft in a practical, bounded, low-hype voice. Do not fabricate case studies, savings metrics, regulated-use assurances, legal claims, or client facts.

## Proposal Selection Guide

- Post-discovery summary: use `discovery-recap`.
- Short buyer-friendly pilot pitch: use `one-page-pilot-proposal`.
- Full services proposal: use `full-agentic-development-proposal`.
- Contract-ready scope attachment: use `statement-of-work`.
- Fixed-price first engagement: use `fixed-fee-pilot-proposal`.
- Hourly or flexible scope: use `time-and-materials-proposal`.
- Ongoing support/monitoring: use `monthly-retainer-proposal`.
- Advice without build: use `advisory-only-proposal`.
- Workflow assessment before implementation: use `workflow-assessment-proposal`.
- Multi-phase delivery plan: use `implementation-roadmap`.
- Testing and acceptance focus: use `evaluation-plan`.
- Governance or safety concern: use `risk-control-plan`.
- Approval architecture: use `human-in-the-loop-approval-model`.
- Added scope after agreement: use `change-order-proposal`.
- Second workflow after pilot: use `expansion-second-workflow-proposal`.
- Procurement or internal approval: use `procurement-ready-scope-summary`.
- Executive decision maker: use `executive-summary`.
- Buyer needs clear done criteria: use `acceptance-criteria`.
- Scope boundaries unclear: use `assumptions-and-exclusions`.
- Closeout and operations planning: use `support-and-handoff-plan`.
- After discovery when a recommendation is needed: use `post-discovery-recommended-pilot-memo`.
- Technical audience: use `technical-architecture-proposal`.
- Data/tool access concerns: use `data-and-tooling-readiness-proposal`.
- Training and enablement: use `training-enablement-proposal`.
- Proof of concept only: use `proof-of-concept-proposal`.
- Production rollout after pilot: use `production-rollout-proposal`.

When several templates fit, choose by buyer decision need first, then stage, then document length. If the buyer has not agreed on a workflow and success criteria, do not jump to a full SOW; use discovery recap, assessment, or pilot recommendation first.

## Quality Rules

- Frame agentic development as practical workflow implementation: discovery, tool routing, retrieval, approval gates, evaluation examples, logs, monitoring, documentation, support, and handoff.
- Keep humans in the loop for external communications, production changes, purchases, data export, and material business decisions.
- Include assumptions, exclusions, acceptance criteria, risks, and dependencies when the document is used for buying approval.
- Make scope concrete enough to become a contract or invoice input.
- Use `TBD` or ask for facts rather than inventing client details, legal terms, metrics, or proof.

## Resource Guide

- `references/proposal-positioning.md`: load for CompleteTech LLC offer framing, language, proof rules, and boundaries.
- `references/use-case-decision-table.md`: load when deciding which document type to use.
- `references/proposal-lifecycle.md`: load for end-to-end flow from discovery through contract/invoice handoff.
- `references/proposal-catalog.md`: load for the near-exhaustive proposal/SOW template library.
- `references/template-index.json`: machine-readable template metadata used by the renderer.
- `scripts/render_proposal.py`: list proposal templates or render a draft with placeholders.

## Renderer

```bash
python3 scripts/render_proposal.py --list
python3 scripts/render_proposal.py --stage pilot --list
python3 scripts/render_proposal.py --template one-page-pilot-proposal --var client_name=Acme --var workflow="support triage"
```

Rendered templates are drafts. Replace placeholders with verified facts and refine the narrative for the buyer.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. The renderer emits the PDF (and prints the Markdown) in **one command**, using the same reportlab branding engine as the contract skill:

```bash
pip install -r requirements.txt
python3 scripts/render_proposal.py --template one-page-pilot-proposal \
  --out artifact.pdf --png artifact.png \
  --title "Support Email Triage Agent — Pilot Proposal" --doc-type "PROPOSAL / STATEMENT OF WORK" \
  --subtitle "Prepared for <b>Northwind Trading Co.</b>" --meta "PROPOSAL NO.=PRO-2026-0188" --meta "DATE=2026-05-20" \
  --var client_name="Client Name" --var workflow="support triage"
```

- `--no-pdf` emits Markdown only (the original behavior); `--no-cover` drops the cover page.
- Already drafted the Markdown yourself? Render it directly: `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."`.
- The PDF supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. PDF requires `reportlab`; the optional `--png` preview requires `pypdfium2` and `pillow`. See `assets/examples/` for a rendered example.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts proposal run metadata to an external service.
