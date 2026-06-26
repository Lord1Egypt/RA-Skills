---
name: agentic-contract-skill
description: >-
  Generate branded CompleteTech Agentic Development Services Agreement packages from approved provider, client, project, commercial, and governance terms. Use when the user wants configurable contract PDFs, filled Markdown source, and optional envelope output for agentic workflow engagements.
version: 1.0.9
metadata:
  openclaw:
    skillKey: agentic-contract-skill
    homepage: https://github.com/CompleteTech-LLC/agentic-contract-skill
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: pyyaml==6.0.3
      - kind: uv
        package: reportlab==4.5.1
      - kind: uv
        package: jinja2==3.1.6
---

# Agentic Contract Skill

## At a Glance

| What it creates | Best for | Output |
|---|---|---|
| Agentic development agreement package | Approved service terms, pilot agreements, governance clauses, and signature-review packets | Branded PDF, filled Markdown, optional envelope |

Turns verified provider, client, scope, fee, timeline, human-review, evaluation, monitoring, and excluded-use facts into a polished CompleteTech-style agreement package.

## Included Contract Artifacts

| Artifact | Purpose |
|---|---|
| Agreement PDF | Branded Agentic Development Services Agreement for review and signature workflows. |
| Filled Markdown | Source text for review, redlines, and archival records. |
| Branded presentation | Optional cover, letterhead, header, footer, and watermark. |
| Addressed envelope | Optional #10 envelope PDF for physical delivery packages. |

## Use When

Use this skill when approved business terms need to become a structured agreement package. It is designed for bounded agentic workflow engagements, scoped pilots, review packets, and reusable contract templates.

## Boundaries

| This skill does | This skill does not |
|---|---|
| Generate agreement artifacts from verified terms. | Replace legal review or create legal advice. |
| Render branded PDFs and filled Markdown. | Invent client facts, pricing, authority, or approvals. |
| Optionally render an addressed envelope. | Issue invoices, approve delivery, or send documents. |
| Keep unknown facts as `TBD`. | Convert unapproved proposal terms into commitments. |

## Resource Guide

| Resource | Role |
|---|---|
| `generate_contract.py` | Contract, Markdown, and envelope generator. |
| `references/agentic_development_agreement.md` | Packaged agreement template with Jinja2 placeholders. |
| `config.ini` | Default provider, client, agreement, agentic-development, branding, and envelope settings. |
| `client_config.example.ini` | Client-specific override example. |
| `examples/minimum_client_override.ini` | Minimal runnable override for demos and smoke tests. |
| `assets/logo.png` | Primary CompleteTech logo used by rendered artifacts. |

## Required Inputs

| Input Area | Required Facts |
|---|---|
| Provider | Legal name, trade name, entity type, formation state, mailing address, email, phone, website, signatory name, signatory title. |
| Client | Legal name, entity type, address, signatory name, signatory title. |
| Project | Contract ID, effective date, project name, services summary, timeline, fee amount, payment terms. |
| Agentic development | System description, autonomy level, human-review requirements, model or stack, deployment environment, evaluation plan, monitoring plan, excluded uses. |
| Branding | Watermark text, monogram, accent color, letterhead, header, footer, and envelope settings. |

| Rule | Requirement |
|---|---|
| Unknown values | Use `TBD` unless the user explicitly asks for demo placeholders. |
| Real commitments | Do not invent legal terms, company facts, pricing, authority, or signature approval. |

## Quality Rules

| Rule | Requirement |
|---|---|
| Verified facts only | Do not invent legal terms, company facts, client facts, authority, acceptance, pricing, or signature approval. |
| Legal text | Preserve demonstration disclaimers unless the user supplies replacement counsel-reviewed terms. |
| Unknown values | Keep unknown provider, client, agreement, delivery, and agentic-development values as `TBD`. |
| Artifact status | Treat generated PDFs and Markdown as draft artifacts until the user confirms the terms and facts. |
| Skill boundary | Keep contract generation separate from proposals, invoices, delivery records, security signoff, customer success notes, email copy, and delivery packaging decisions. |
| Existing files | Do not overwrite user-specific config or generated output without checking whether it contains client-specific facts that should be preserved. |

## Configuration Toggles

In `[branding]`:

```ini
watermark_enabled = yes
watermark_text = DEMO DRAFT
letterhead_enabled = yes
header_enabled = yes
footer_enabled = yes
envelope_enabled = yes
```

Set any toggle to `no` to disable that feature. The envelope is generated as a separate #10 envelope PDF when `envelope_enabled = yes`.

## Generator

```bash
pip install -r requirements.txt

python generate_contract.py --config config.ini \
  --out output/agentic_development_contract.pdf

python generate_contract.py \
  --config config.ini examples/minimum_client_override.ini \
  --out output/acme_agentic_development_contract.pdf \
  --envelope-out output/acme_envelope.pdf

python generate_contract.py --config config.ini --out output/no_envelope_contract.pdf --no-envelope
```

## Agent Operating Guidance

| Step | Action |
|---|---|
| 1 | Read the user's business profile or provided inputs. |
| 2 | Update `config.ini` or create an override INI; keep unknown details as `TBD`. |
| 3 | Preserve demonstration disclaimers unless the user supplies replacement legal text. |
| 4 | Run `generate_contract.py`. |
| 5 | Return links to the PDF, Markdown source, and ZIP or folder as appropriate. |
| 6 | Note that the document is a demonstration template, not legal advice, unless the user supplied reviewed legal terms. |
| 7 | Preserve existing client-specific outputs unless the user asks to regenerate or replace them. |

## Customizing the Contract

Edit `references/agentic_development_agreement.md` to change clauses, add jurisdiction-specific language, or include business-specific statement-of-work text.

| Markdown Feature | Supported Form |
|---|---|
| Headings | `#`, `##`, and `###` |
| Paragraphs | Plain text separated by blank lines |
| Lists | `-` bullet lists |
| Tables | Simple Markdown tables |
| Emphasis | `**bold**` inline emphasis |
| Callouts | Block quotes beginning with `>` |
| Page breaks | `[PAGE_BREAK]` |

## Dependencies

Install dependencies with:

```bash
pip install -r requirements.txt
```

The generator uses `reportlab` for PDF creation and `jinja2` for contract template rendering.

## Network Boundary

| Boundary | Status |
|---|---|
| Runtime model | Local-only document generation. |
| Outbound network helpers | Not included. |
| Callbacks or telemetry | Not included. |
| External metadata posting | Not included. |
| Contract data handling | Remains in local inputs and user-selected output files. |
