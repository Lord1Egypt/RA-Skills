---
name: agentic-customer-success-skill
description: >-
  Create CompleteTech LLC customer success and account management artifacts for agentic development clients, including account profiles, contact maps, approved email/contact routing, meeting notes, follow-up trackers, health scorecards, relationship risk logs, renewal readiness, expansion briefs, QBRs, support escalations, satisfaction surveys, testimonial/referral plans, executive check-ins, at-risk recovery, offboarding, stakeholder changes, communication cadence, success criteria reviews, and post-launch adoption check-ins. Use after first contact, during delivery, after launch, and through renewal or expansion when Codex needs to manage customer relationships without inventing facts.
version: 1.0.2
metadata:
  openclaw:
    skillKey: agentic-customer-success-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-customer-success-skill
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

# Agentic Customer Success Skill

## Purpose

Create customer success and account management artifacts for CompleteTech LLC agentic development clients. Use this skill to keep communication organized, route messages to verified contacts, track health, prevent missed follow-ups, and identify retention or expansion opportunities.

## System Boundary

This skill owns post-contact and post-sale relationship state: contacts, routing, follow-ups, health, renewal, expansion, advocacy planning, and at-risk recovery. Use `agentic-delivery-skill` for implementation execution records, `agentic-email-skill` for polished outbound copy, `agentic-invoice-skill` for billing documents, and `agentic-case-study-skill` for public or reusable proof after client approval.

## Core Workflow

1. Identify the customer situation: onboarding, contact routing, meeting follow-up, missed response, concern, support escalation, post-launch check-in, renewal, expansion, referral/testimonial, stakeholder change, executive update, at-risk account, or offboarding.
2. Gather verified facts: client name, workflow, current stage, contacts, approved email/channel routing, owner roles, open commitments, support items, renewal dates, success criteria, risks, approvals, and next actions.
3. Use `references/use-case-decision-table.md` to choose the right customer success artifact.
4. Use `references/customer-success-positioning.md` for CompleteTech LLC language, contact routing, and guardrails.
5. Use `references/customer-success-catalog.md` for the artifact library.
6. Do not invent client facts, customer sentiment, approvals, renewal intent, testimonials, referrals, email addresses, or business outcomes. Use `TBD` or open questions when evidence is missing.

## Artifact Selection Guide

- New client onboarding: use `client-account-profile`.
- Unclear contact ownership: use `customer-contact-map`.
- Choosing which email, role, or channel to use: use `approved-contact-routing-guide`.
- Capturing a customer conversation: use `meeting-notes`.
- Preventing missed commitments or responses: use `follow-up-tracker`.
- Checking account status: use `client-health-scorecard`.
- Client concern or relationship risk: use `relationship-risk-log`.
- Renewal planning: use `renewal-readiness-review`.
- Expansion opportunity: use `expansion-opportunity-brief`.
- Executive update or scheduled account review: use `quarterly-business-review` or `executive-check-in-brief`.
- Support escalation: use `support-escalation-summary`.
- Asking for customer feedback: use `client-satisfaction-survey`.
- Referral or testimonial request: use `testimonial-referral-request-plan`.
- At-risk account: use `at-risk-customer-recovery-plan`.
- Offboarding or transition: use `offboarding-transition-checklist`.
- Stakeholder change: use `stakeholder-change-note`.
- Communication schedule: use `communication-cadence-plan`.
- Reviewing promised outcomes: use `success-criteria-review`.
- Post-launch usage/adoption check: use `post-launch-adoption-check-in`.

When several artifacts fit, choose the one closest to the customer event. Use supporting artifacts only when they clarify ownership, timing, risk, or approval.

## Quality Rules

- Use verified contact routing. Billing, support, executive sponsor, technical escalation, delivery owner, security contact, legal/contract contact, and referral/testimonial approver are `TBD` unless verified.
- Do not send or draft sensitive, billing, legal, executive, support, renewal, testimonial, referral, or at-risk-account communications as final without human review.
- Recommend client approval before publishing testimonials, named case references, referrals, public outcomes, or executive summaries.
- Recommend escalation when a client concern affects trust, scope, timeline, access, billing, security, production reliability, renewal risk, or contractual expectations.
- Separate facts, assumptions, risks, recommendations, and next actions.
- Keep every artifact practical, direct, professional, and implementation-focused.

## Resource Guide

- `references/customer-success-positioning.md`: load for CompleteTech LLC relationship language, routing, and guardrails.
- `references/use-case-decision-table.md`: load when choosing a customer success artifact.
- `references/customer-success-lifecycle.md`: load for flow from first contact through renewal, expansion, or offboarding.
- `references/customer-success-catalog.md`: load for reusable artifact templates.
- `references/template-index.json`: machine-readable artifact metadata used by the renderer.
- `scripts/render_customer_success.py`: list customer success artifacts or render a draft with placeholders.

## Runtime Permissions

This skill needs local filesystem access only for its documented renderer workflow:

- Reads bundled templates, references, examples, `assets/logo.png`, and user-provided Markdown or variable inputs.
- Writes only to the user-selected `--out`, `--png`, `--markdown-out`, or default `output/` artifact paths.
- Runs local Python entry points `scripts/render_customer_success.py` and `scripts/render_pdf.py`.
- Does not require network access, credential access, persistence, privilege escalation, or destructive file operations.

## Renderer

```bash
python3 scripts/render_customer_success.py --list
python3 scripts/render_customer_success.py --stage relationship --list
python3 scripts/render_customer_success.py --template client-account-profile --var client_name=Acme --var workflow="support triage agent"
```

Rendered artifacts are drafts. Replace placeholders with verified account, contact, communication, delivery, support, renewal, and approval facts before use.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. The renderer emits the PDF (and prints the Markdown) in **one command**, using the same reportlab branding engine as the contract skill:

```bash
pip install -r requirements.txt
python3 scripts/render_customer_success.py --template client-health-scorecard \
  --out artifact.pdf --png artifact.png \
  --title "Client Health Scorecard & QBR Summary" --doc-type "CUSTOMER SUCCESS — INTERNAL" \
  --subtitle "Account: <b>Northwind Trading Co.</b>" --meta "DOCUMENT NO.=CS-2026-0051" --meta "DATE=2026-06-10" \
  --var client_name="Client Name" --var workflow="support triage"
```

- `--no-pdf` emits Markdown only (the original behavior); `--no-cover` drops the cover page.
- Already drafted the Markdown yourself? Render it directly: `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."`.
- The PDF supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. PDF requires `reportlab`; the optional `--png` preview requires `pypdfium2` and `pillow`. See `assets/examples/` for a rendered example.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts customer-success run metadata to an external service.
