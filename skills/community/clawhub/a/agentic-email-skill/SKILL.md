---
name: agentic-email-skill
description: >-
  Create polished, review-ready sales and lifecycle email sequences for agentic development services, then export them as branded PDF artifacts. Use for outreach, follow-up, proposal, close, kickoff, delivery, retention, referral, and win-back communication when the user wants structured copy without sending email.
version: 1.0.9
metadata:
  openclaw:
    skillKey: agentic-email-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-email-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: pyyaml==6.0.3
      - kind: uv
        package: pypdfium2==5.8.0
      - kind: uv
        package: pillow==12.2.0
---

# Agentic Email Skill

## At a Glance

| What it creates | Best for | Output |
|---|---|---|
| Sales and lifecycle email sequences | Agentic workflow outreach, follow-up, proposal support, and post-sale communication | Branded PDF, Markdown, optional PNG preview |

This skill turns verified buyer, workflow, offer, proof, and CTA details into concise CompleteTech-style email copy. It is local-only: it drafts and renders documents, but it does not send email or call mail-provider APIs.

## Included Email Sets

| Set | Covers |
|---|---|
| Outbound | Cold outreach, warm introductions, first follow-ups, examples, risk-control follow-ups, and breakups. |
| Discovery | Inbound response, qualification, booking, agenda confirmation, and post-discovery recap. |
| Sales motion | Proposal preview, proposal send, objections, close summaries, contract messages, invoice/deposit notes, and kickoff. |
| Post-sale | Delivery updates, review requests, handoff, expansion, referral, testimonial, retention, win-back, and nurture. |

## Use When

Use this skill when verified buyer, workflow, offer, proof, and CTA details need to become polished email copy or a branded PDF email-sequence artifact.

## Boundaries

| This skill does | This skill does not |
|---|---|
| Draft email copy and email sequences. | Send email or call mail-provider APIs. |
| Render branded PDF/Markdown artifacts. | Replace proposal, contract, invoice, delivery, customer-success, or proof artifacts. |
| Use verified facts from other skills as context. | Invent client proof, recipient authority, metrics, legal claims, or regulated-use assurances. |
| Keep messages review-ready and scoped. | Approve external sending or bypass recipient/routing verification. |

## Core Workflow

| Step | Action |
|---|---|
| 1 | Identify the stage: cold outreach, warm intro, follow-up, booked meeting, discovery recap, proposal, close, post-sale, retention, referral, or reactivation. |
| 2 | Gather only the facts needed for that stage. |
| 3 | Use `references/positioning.md` for service promise, risk controls, and language to avoid. |
| 4 | Use `references/email-catalog.md` for template selection, multi-step sequences, or near-exhaustive libraries. |
| 5 | Use `references/sequence-blueprints.md` for outreach and sales cadence design. |
| 6 | Draft in the requested voice, or default to concise, plain, consultative, and specific. |
| 7 | Include subject lines when useful and avoid unsupported claims. |

| Needed Fact | Examples |
|---|---|
| Buyer context | Name, company, role, industry. |
| Trigger | Observed change, operational pain, buying signal, or business problem. |
| Workflow | Agentic workflow being pitched or supported. |
| Message inputs | Proof, constraints, offer, CTA, timing, and tone. |

## Email Selection Guide

Choose by current decision point first, then by buyer persona, then by trigger.

| Decision Point | Templates |
|---|---|
| Cold outbound | `cold-problem-pilot`, `cold-operations-bottleneck`, `cold-technical-evaluation`, `cold-executive-risk`, `cold-revenue-team`, `cold-support-team`, `cold-ops-knowledge`, `cold-founders` |
| Cold follow-up | `followup-workflow-map`, `followup-risk-controls`, `followup-example`, `followup-proofless-value`, `followup-breakthrough-question`, `breakup-close-loop` |
| Warm or inbound | `warm-intro-context`, `warm-intro-workflow`, `inbound-fast-response`, `inbound-qualification`, `inbound-booking` |
| Discovery and proposal | `discovery-confirm-agenda`, `post-discovery-recap`, `proposal-preview`, `proposal-sent`, `proposal-followup-questions` |
| Closing and objections | `close-objection-budget`, `close-objection-risk`, `close-objection-timing`, `close-objection-internal-team`, `close-decision-summary`, `close-final-nudge` |
| Contract and payment | `contract-sent`, `contract-clarifications`, `deposit-invoice`, `signature-reminder` |
| Kickoff and delivery | `kickoff-after-signature`, `kickoff-agenda`, `access-request`, `weekly-update`, `review-ready`, `acceptance-request`, `handoff-complete` |
| Expansion and proof | `expansion-next-workflow`, `referral-request`, `testimonial-request`, `quarterly-checkin`, `winback-new-trigger` |
| Trigger and nurture | `trigger-hiring`, `trigger-new-tool`, `trigger-growth`, `nurture-educational`, `nurture-one-page-offer`, `reengage-old-opportunity` |

| Selection Rule | Guidance |
|---|---|
| Buyer has not agreed to a problem | Stay in cold, follow-up, warm intro, inbound, or discovery. |
| Buyer has agreed to scoped work | Move to proposal, closing, contract, or payment. |
| Project is signed | Use kickoff, delivery, acceptance, handoff, support, or expansion. |
| Several templates fit | Pick the one closest to the buyer's current decision point. |

## Quality Rules

| Rule | Requirement |
|---|---|
| Length | Keep cold emails under 120 words unless the user asks for long-form. |
| Opening | Lead with a concrete operational problem, not generic AI excitement. |
| Positioning | Present agentic development as workflow design, implementation, evaluation, monitoring, and human approval gates. |
| CTA | Use one clear CTA per email. |
| Follow-ups | Add a new angle, artifact, risk reducer, example workflow, or decision prompt. |
| Cold outbound | Include a polite opt-out line when appropriate. |
| High-risk sectors | Emphasize review, approvals, logs, and scoped pilots; do not imply autonomous production decisions. |

## Resource Guide

| Resource | Role |
|---|---|
| `references/positioning.md` | Offer framing, buyer pains, differentiators, proof rules, and compliance guardrails. |
| `references/use-case-decision-table.md` | Template selection for a specific use case. |
| `references/sequence-blueprints.md` | Recommended cadences across cold outbound, warm outbound, inbound, proposal, closing, and post-sale. |
| `references/email-catalog.md` | Near-exhaustive template library by stage. |
| `references/template-index.json` | Machine-readable template metadata used by the renderer. |
| `scripts/render_email.py` | Lists templates or renders a draft with placeholders. |

## Runtime Permissions

| Area | Runtime behavior |
|---|---|
| Execution | Runs local Python entry points: `scripts/render_email.py` and `scripts/render_pdf.py`. |
| Reads | Bundled templates, references, examples, `assets/logo.png`, and user-provided Markdown or email variables. |
| Writes | Only user-selected `--out`, `--png`, `--markdown-out`, or default `output/` artifact paths. |
| Network | Not required and not used for email drafting or document rendering. |

| Not Included | Boundary |
|---|---|
| Email delivery | Does not send email, contact prospects, call mail-provider APIs, add tracking pixels, or approve outreach. |
| Credentials | Does not read mail credentials, API keys, browser sessions, or CRM tokens. |
| System changes | Does not create persistence, escalate privileges, run background services, or perform destructive file operations. |

## Renderer

Use the renderer for repeatable output or quick template discovery:

```bash
python3 scripts/render_email.py --list
python3 scripts/render_email.py --template cold-problem-pilot --var prospect_name=Alex --var company=Acme --var workflow="support triage"
```

If a user needs polished, context-aware copy, use the references and rewrite the rendered draft rather than returning raw placeholders.

## Rendering to a Branded PDF

Artifacts from this skill are delivered as branded CompleteTech LLC **PDF** documents. The email renderer can emit PDF, Markdown, and optional PNG preview in one local command:

```bash
pip install -r requirements.txt
python3 scripts/render_email.py --template cold-operations-bottleneck \
  --out artifact.pdf --png artifact.png \
  --title "Outbound Email Sequence" --doc-type "EMAIL DRAFTS — VERIFY BEFORE SENDING" \
  --subtitle "Prospect: <b>Northwind Trading Co.</b>" --meta "SEQUENCE=PRO-OUT-014" --meta "STAGE=Cold outreach" \
  --var client_name="Client Name" --var workflow="support triage"
```

| Output Need | Use |
|---|---|
| Branded PDF | `--out artifact.pdf` |
| PNG preview | `--png artifact.png` |
| Markdown source | `--markdown-out artifact.md` |
| Markdown only | `--no-pdf` |
| No cover page | `--no-cover` |
| Existing Markdown to PDF | `python3 scripts/render_pdf.py --markdown artifact.md --out artifact.pdf --logo assets/logo.png --title "..."` |

| Rendering Support | Details |
|---|---|
| Markdown subset | `#`, `##`, `###`, paragraphs, `-` bullets, tables, `>` callouts, `**bold**`, and `[PAGE_BREAK]`. |
| Required package | `reportlab==4.5.1` for PDF rendering. |
| Optional preview packages | `pypdfium2==5.8.0` and `pillow==12.2.0` for `--png`. |
| Example output | See `assets/examples/` for rendered Markdown, PDF, and PNG artifacts. |

## Network Boundary

This skill is local-only. It does not include outbound network helpers, callbacks, mail-provider integrations, tracking pixels, or any helper that posts email run metadata to an external service.
