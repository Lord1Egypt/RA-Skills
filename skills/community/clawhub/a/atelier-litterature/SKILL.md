# Atelier Litteraire - Ideation & redaction de romans courts

**Atelier** is a complete literary writing workflow for OpenClaw, combining two specialized agents:

- **Hermine** — narrative ideation agent (H0→H4 pipeline)
- **Herbert** — literary writing agent (Pacte Narratif → Seeds → Jury → Final text)

## What it does

Starting from a pitch (one word, one sentence, a news article, a historical fact), Atelier:

1. **Hermine** analyzes the raw material and generates 5 narrative axes (3 natural + 2 radical counter-axes), scores them, and recommends the strongest
2. **Herbert** builds the Pacte Narratif, constructs character and world bibles, writes all seeds through 3 iterations with a 3-reader jury, compiles the final DOCX + PDF locally

## Agents

### Hermine — Ideation Agent
- Pipeline H0 (raw fact) → H1 (narrative substrate) → H2 (3 axes) → H3 (jury scoring) → H4 (2 radical counter-axes with Opus-level reasoning)
- Axes 1-3: natural ideation (Sonnet)
- Axes 4-5: forced rupture thinking — no reuse of any element from axes 1-3 (Opus)
- Scoring: f(x) = (x/100)^1.5 × 100, composite /10

### Herbert — Writing Agent
- Builds character bibles, world bibles, narrative pact
- Writes seeds (narrative units ~750 chars) through 3 iterations
- 3-reader jury: ordinary reader / demanding reader / world expert
- 10 weighted dimensions, composite score /10
- Thresholds: ≥8.0 validated / 6.0-7.9 iterate / <6.0 alert
- Compiles DOCX + PDF (continuous text, no chapter titles, no page breaks between units)
- Produces iteration report with jury scores


## ⚠️ Scope & Permissions

This skill operates **locally by default**. It generates DOCX and PDF files saved to your workspace.

- No external accounts are accessed without explicit user confirmation
- No files are uploaded or published automatically
- Any export to external services requires the user to configure and trigger it manually
- Final human review is required before any publication or sharing

## Usage

Trigger Hermine with a pitch:
> "Activate Hermine on this pitch: [your pitch]"

Or go directly to Herbert with a fully defined project:
> "Activate Herbert, here is the Pacte Narratif: [...]"

## Format rules (validated by author)

All final documents:
- No unit/seed titles in the final text
- No page breaks between units
- Continuous text flow, blank lines between sections
- Liberation Serif 12pt, 1.5 line spacing, 2.5cm margins
- DOCX + PDF both produced
- Final DOCX + PDF saved locally

## Requirements

- OpenClaw with subagent support
- Anthropic Claude API (Sonnet for standard tasks, Opus for H4 counter-axes)

## Install

```bash
clawhub install atelier
```
