---
name: agentic-case-study-skill
description: >-
  Create CompleteTech LLC case studies, testimonials, and proof assets for completed agentic development engagements, including intake questionnaires, outcome interview guides, anonymized and named-client case studies, before/after workflow summaries, implementation stories, technical notes, risk/control summaries, approval-gate summaries, evaluation results, testimonial requests/drafts, proof libraries, sales one-pagers, website stories, LinkedIn posts, nurture emails, referral blurbs, portfolio entries, pitches, award submissions, press releases, quote approvals, and anonymization checks. Use after delivery when Codex needs to package verified client-approved outcomes without exposing confidential details or inventing proof.
version: 1.0.3
metadata:
  openclaw:
    skillKey: agentic-case-study-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-case-study-skill
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

# Agentic Case Study Skill

## Purpose

Create case studies, testimonials, and proof assets after CompleteTech LLC agentic development delivery, using only verified and client-approved facts.

## System Boundary

This skill owns approved outcome packaging and reusable proof after delivery. Use `agentic-delivery-skill` for raw delivery evidence, `agentic-customer-success-skill` for relationship and approval routing, and `agentic-email-skill` only for messages that request approval or share the proof. Do not turn internal notes, unapproved metrics, private client details, or speculative outcomes into public proof.

## Core Workflow

1. Identify the proof need: intake, interview, internal brief, anonymized/public case study, sales asset, social post, quote, referral, award, press, or approval checklist.
2. Gather verified facts: client approval status, workflow, before state, implementation, controls, evaluation evidence, qualitative observations, measured outcomes, quotes, confidentiality constraints, and allowed attribution.
3. Use `references/use-case-decision-table.md` to choose the right proof artifact.
4. Use `references/proof-positioning.md` for CompleteTech LLC proof language, evidence rules, and anonymization guardrails.
5. Use `references/proof-catalog.md` for the near-exhaustive proof asset library.
6. Distinguish measured outcomes from qualitative observations. Do not fabricate ROI, savings, approvals, quotes, metrics, regulated-use assurances, legal claims, or client facts.

## Proof Asset Selection Guide

- Starting proof collection: use `case-study-intake-questionnaire`.
- Interviewing client stakeholders: use `client-outcome-interview-guide`.
- Internal sales enablement: use `internal-case-study-brief`.
- Confidential client or sensitive details: use `anonymized-case-study`.
- Client approved public attribution: use `public-named-client-case-study`.
- Show process change: use `before-after-workflow-summary`.
- Tell delivery narrative: use `implementation-story`.
- Technical buyer proof: use `technical-implementation-note`.
- Governance proof: use `risk-control-summary`.
- Approval workflow proof: use `human-approval-gate-summary`.
- Evaluation evidence: use `evaluation-results-summary`.
- Ask for testimonial: use `testimonial-request`.
- Draft testimonial for approval: use `testimonial-draft`.
- Build reusable proof snippets: use `proof-point-library`.
- Sales handout: use `sales-one-pager`.
- Website page: use `website-case-study`.
- Social post: use `linkedin-post`.
- Nurture campaign: use `email-nurture-story`.
- Referral ask: use `referral-enablement-blurb`.
- Portfolio listing: use `portfolio-entry`.
- Speaking or podcast outreach: use `speaker-podcast-pitch`.
- Award entry: use `award-submission-draft`.
- Press announcement: use `press-release-draft`.
- Quote approval: use `customer-quote-approval-checklist`.
- Confidentiality review: use `confidentiality-and-anonymization-checklist`.
- Short proof for proposal/email reuse: use `micro-proof-snippet`.
- Internal proof QA: use `proof-approval-status-tracker`.

When several artifacts fit, choose the safest asset that matches approval status. If client approval is unknown, use internal or anonymized artifacts and run the approval/anonymization checklist before public use.

## Quality Rules

- Use only verified, client-approved facts.
- Separate measured outcomes from qualitative observations.
- Preserve confidential details and anonymize when required.
- Keep the CompleteTech LLC frame: bounded workflow implementation, human approval gates, evaluation, monitoring, documentation, support, and handoff.
- Do not imply regulated-use approval, legal conclusions, or guaranteed outcomes.
- Use `TBD`, "not approved for public use", or "client approval required" where facts or permissions are missing.

## Resource Guide

- `references/proof-positioning.md`: load for evidence rules, brand language, and anonymization boundaries.
- `references/use-case-decision-table.md`: load when choosing a proof artifact.
- `references/proof-lifecycle.md`: load for flow from outcome collection through public proof approval.
- `references/proof-catalog.md`: load for the near-exhaustive proof asset templates.
- `references/template-index.json`: machine-readable template metadata used by the renderer.
- `scripts/render_proof.py`: list proof assets or render a draft with placeholders.

## Runtime Permissions

This skill needs local filesystem access only for its documented renderer workflow:

- Reads bundled templates, references, examples, `assets/logo.png`, and user-provided Markdown or variable inputs.
- Writes only to the user-selected `--out`, `--png`, `--markdown-out`, or default `output/` artifact paths.
- Runs local Python entry points `scripts/render_proof.py` and `scripts/render_pdf.py`.
- Does not require network access, credential access, persistence, privilege escalation, or destructive file operations.

## Renderer

```bash
python3 scripts/render_proof.py --list
python3 scripts/render_proof.py --stage case_study --list
python3 scripts/render_proof.py --template anonymized-case-study --var workflow="support triage"
```

Rendered artifacts are drafts. Replace placeholders with verified facts and confirm approval status before publishing or sending externally.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents, not raw Markdown. The renderer emits the PDF (and prints the Markdown) in **one command**, using the same reportlab branding engine as the contract skill:

```bash
pip install -r requirements.txt
python3 scripts/render_proof.py --template public-named-client-case-study \
  --out artifact.pdf --png artifact.png \
  --title "Customer Support Email Triage Agent" --doc-type "CLIENT CASE STUDY" \
  --subtitle "Northwind Trading Co. × CompleteTech LLC" --meta "CASE NO.=CASE-2026-007" --meta "DATE=2026-07-01" \
  --var client_name="Client Name" --var workflow="support triage"
```

- `--no-pdf` emits Markdown only (the original behavior); `--no-cover` drops the cover page.
- Already drafted the Markdown yourself? Render it directly: `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."`.
- The PDF supports a Markdown subset: `#`/`##`/`###` headings, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. PDF requires `reportlab`; the optional `--png` preview requires `pypdfium2` and `pillow`. See `assets/examples/` for a rendered example.

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, or any helper that posts case-study run metadata to an external service.
