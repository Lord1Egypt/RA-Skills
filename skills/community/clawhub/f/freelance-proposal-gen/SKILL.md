---
name: freelance-proposal-gen
description: "Generates client-ready, single-page HTML proposals for freelancers, solo consultants, and small studios. This skill should be used when a user wants to create a polished sales proposal, quote, or pitch document to send to a client. Triggered by requests like 帮我写个接单提案, 给客户做个报价单, 生成服务方案书, or 做个能发给甲方的方案页. Produces a self-contained, print-friendly HTML file with cover, pain points, solution, deliverables, pricing table, case studies, and a call-to-action. Works offline with no external API required."
agent_created: true
---

# Freelance Proposal Gen

## Overview

Turn a one-paragraph brief into a professional, single-file HTML proposal that a
freelancer can send straight to a client. The skill collects a small set of
fields, renders them into a styled HTML template via a deterministic script, and
returns a file the user can preview, print to PDF, or email.

The advantage over a plain chat draft: the output is a real, branded, responsive
HTML page (not markdown), consistent every time, and ready to be white-labeled.

## When to Use

- User is a freelancer / solo consultant / small studio pitching a client
- Request mentions 提案 / 报价单 / 方案书 / 接单 / pitch / quote / proposal
- User wants something more presentable than a text doc to close a deal

## Workflow

### Step 1 — Collect the brief

Ask for (or infer sensible defaults for) these fields. Do not block on missing
optional fields; use the structure guide's defaults in `references/proposal-structure.md`.

Required:
- `PROPOSAL_TITLE` — what the proposal is for (e.g. "品牌官网重构提案")
- `PREPARED_FOR` — client / company name
- `SERVICE_SUMMARY` — one-line description of what is being sold

Strongly recommended (infer if absent):
- `PAIN_POINTS` — 3 bullet client problems
- `SOLUTION_BLOCKS` — 2–3 solution sections (title + paragraph)
- `DELIVERABLES` — bullet list of what the client receives
- `PRICING_TABLE` — package rows (name / scope / price)
- `CASES` — 1–2 proof points (result + metric)
- `YOUR_NAME`, `YOUR_TITLE`, `CONTACT_LINE`
- `WECHAT`, `WEBSITE` — contact channels shown in the optional corner watermark
  (lead-gen hook); set `SHOW_CONTACT_WATERMARK: "false"` to hide it (default on)

### Step 2 — Build the fields JSON

Assemble a JSON object whose keys match the template tokens (uppercase). Lists
and tables must be passed as ready HTML (`<li>…</li>`, `<tr>…</tr>`). See
`references/proposal-structure.md` for the full token list, copywriting rules,
and default copy to reuse when a field is missing.

### Step 3 — Render

Run the bundled renderer (deterministic, offline):

```
python <skill>/scripts/generate_proposal.py --data fields.json --out proposal.html
```

Replace `<skill>` with this skill's directory. The script reads
`assets/proposal-template.html`, substitutes tokens, blanks any leftover
placeholders, and writes the output file.

### Step 4 — Present

Open / preview the generated `proposal.html` for the user. Offer to (a) print to
PDF, (b) swap the accent color via the `{{ACCENT}}` token, or (c) regenerate with
revised fields.

## Design Rules (non-negotiable)

- Keep it ONE page when printed (A4). No infinite scroll for the client version.
- Accent color lives in one CSS variable; change it in one place.
- All copy Chinese unless the client is explicitly foreign-language.
- Pricing table must show at least one concrete number — vague "面议" loses deals.
- Every proposal needs a clear next-step CTA with a contact line.

## Resources

### references/
- `proposal-structure.md` — token dictionary, section anatomy, copywriting
  principles, and default copy for missing fields.

### assets/
- `proposal-template.html` — self-contained, print-friendly HTML template with
  `{{TOKEN}}` placeholders. Edit the CSS variables to rebrand.

### scripts/
- `generate_proposal.py` — deterministic token renderer (JSON in, HTML out).
