---
name: agentic-security-review-skill
description: >-
  Create CompleteTech LLC security, safety, permissions, and production-readiness review artifacts for agentic development workflows, including risk intake, tool permissions, secrets handling, data exposure, prompt-injection testing, retrieval trust, approval gates, external actions, audit logging, model/provider configuration, retention, dependency risk, least privilege, launch blockers, rollback, incident response, escalation, red-team results, and security signoff. Use before production launch or whenever tools, data, credentials, integrations, retrieval sources, or external actions change.
version: 1.0.2
metadata:
  openclaw:
    skillKey: agentic-security-review-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-security-review-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab>=4.0
      - kind: uv
        package: pyyaml>=6.0
---

# Agentic Security Review Skill

## Purpose

Create practical security review artifacts for CompleteTech LLC agentic development workflows. Use this skill before launch, before granting new access, after material configuration changes, and after incidents or near misses.

## System Boundary

This skill owns security, safety, permissions, data, credential, tool, and launch-risk review. Use it alongside discovery, proposal, or delivery when risk needs a dedicated artifact. It does not replace `agentic-delivery-skill` launch checklists, `agentic-contract-skill` legal terms, external compliance certification, formal penetration testing, or counsel-reviewed privacy/security advice.

## Core Workflow

1. Identify the review event: launch, new tool, sensitive data, external action, retrieval/RAG, credential change, dependency change, incident, or signoff.
2. Gather verified facts: workflow purpose, users, data classes, tools, permissions, credentials, integrations, retrieval sources, human approvals, logs, deployment path, rollback owner, incident contacts, and known constraints.
3. Use `references/use-case-decision-table.md` to choose the right review artifact.
4. Use `references/security-positioning.md` for CompleteTech LLC security language and guardrails.
5. Use `references/security-catalog.md` for the artifact library.
6. Keep the review bounded and evidence-based. Do not claim compliance, certification, legal approval, penetration-test completion, production readiness, or guaranteed security unless the user provides verified evidence.

## Artifact Selection Guide

- Starting a new agentic workflow: use `agentic-risk-intake`.
- Adding a tool or integration: use `tool-permission-inventory`.
- Handling API keys, tokens, service accounts, or secrets: use `credential-secret-handling-checklist`.
- Accessing sensitive, client, personal, regulated, or proprietary data: use `data-exposure-review`.
- Testing prompt injection or tool misuse: use `prompt-injection-test-plan`.
- Adding retrieval/RAG, indexed docs, websites, or knowledge stores: use `retrieval-source-trust-review`.
- Reviewing human-in-the-loop controls: use `approval-gate-audit`.
- Sending emails, creating calendar events, modifying files, posting messages, purchasing, billing, or changing production systems: use `external-action-review`.
- Needing traceability, audit trails, or operational evidence: use `logging-auditability-review`.
- Changing model, provider, system prompt, tool runtime, or safety settings: use `model-provider-configuration-review`.
- Defining storage, deletion, or retention behavior: use `data-retention-review`.
- Adding packages, services, scripts, or vendor dependencies: use `dependency-supply-chain-review`.
- Reducing access scope or sandboxing execution: use `sandbox-least-privilege-checklist`.
- Preparing for launch: use `production-readiness-security-checklist`.
- Deciding what blocks launch: use `launch-blocker-checklist`.
- Preparing a backout path: use `rollback-plan`.
- Responding to a security event or near miss: use `incident-response-plan`.
- Defining who to contact and when to escalate: use `human-escalation-procedure`.
- Summarizing adversarial testing: use `red-team-test-report`.
- Recording final approval status: use `security-signoff-memo`.

When several artifacts fit, start with the artifact closest to the change or decision being reviewed, then add supporting artifacts only when they materially reduce risk.

## Quality Rules

- Use verified contact routing. Do not invent client, security, legal, billing, support, or approval email addresses; ask for the right address or use `TBD`.
- Preserve least privilege: name each tool, permission, credential, data class, and external action that is actually needed.
- Protect human approval gates for irreversible actions, client-facing communication, payments, data export/deletion, production changes, and material business decisions.
- Separate facts from recommendations. Label unknowns, assumptions, residual risks, blockers, and owner decisions.
- Recommend technical escalation when secrets may be exposed, logs are missing, sandboxing is weak, prompt injection can trigger tools, approval gates are bypassed, production rollback is unclear, or sensitive data flows are not understood.
- Recommend client or human approval before launch, before expanding permissions, before connecting client systems, before sending external communications, and before closing incident follow-up.

## Resource Guide

- `references/security-positioning.md`: load for CompleteTech LLC review language and boundaries.
- `references/use-case-decision-table.md`: load when choosing a security review artifact.
- `references/security-lifecycle.md`: load for review flow from intake through launch and post-incident follow-up.
- `references/security-catalog.md`: load for the reusable artifact templates.
- `references/template-index.json`: machine-readable artifact metadata used by the renderer.
- `scripts/render_security_review.py`: list security artifacts or render a draft with placeholders.

## Renderer

```bash
python3 scripts/render_security_review.py --list
python3 scripts/render_security_review.py --stage launch --list
python3 scripts/render_security_review.py --template agentic-risk-intake --var client_name=Acme --var workflow="support triage agent"
```

Rendered artifacts are drafts. Replace placeholders with verified project facts before sending, storing, or relying on them.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. The renderer emits the PDF (and prints the Markdown) in **one command**, using the same reportlab branding engine as the contract skill:

```bash
pip install -r requirements.txt
python3 scripts/render_security_review.py --template security-signoff-memo \
  --out artifact.pdf --png artifact.png \
  --title "Security Signoff Memo" --doc-type "SECURITY REVIEW" \
  --subtitle "Workflow: <b>Support Email Triage Agent (Pilot)</b>" --meta "MEMO NO.=SEC-2026-0090" --meta "DATE=2026-06-17" \
  --var client_name="Client Name" --var workflow="support triage"
```

- `--no-pdf` emits Markdown only (the original behavior); `--no-cover` drops the cover page.
- Already drafted the Markdown yourself? Render it directly: `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."`.
- The PDF supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. PDF requires `reportlab`; the optional `--png` preview requires `pypdfium2` and `pillow`. See `assets/examples/` for a rendered example.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts security-review run metadata to an external service.
