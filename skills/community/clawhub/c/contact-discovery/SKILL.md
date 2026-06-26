---
name: contact-discovery
description: >
  Find public contact details for a person or company using Prismfy-powered web search.
  Use when a user wants a public email, contact path, press/support page, or company email-format clue before outreach.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PRISMFY_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: PRISMFY_API_KEY
    emoji: "📬"
    homepage: https://prismfy.io
---

# Contact Discovery

Use this skill when you need to find public contact details for a company or a specific person at that company.

Why it helps:
- finds public emails when they are actually exposed on the public web,
- finds contact paths when no direct email is visible,
- surfaces company email-format clues without guessing,
- keeps the agent from inventing private contact data.

Best for:
- pre-outreach contact discovery,
- finding public press/support/team contact pages,
- checking whether a person has a public email trail,
- finding company email-format clues for later human review.

Need a key?
- Get free search access and your API key at: https://prismfy.io

## Setup

1. Install the skill:
```bash
openclaw skills install contact-discovery
```

2. Add your Prismfy API key:
```bash
export PRISMFY_API_KEY="ss_live_your_key_here"
```

To keep it after restart:
```bash
echo 'export PRISMFY_API_KEY="ss_live_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

Preflight:
- `PRISMFY_API_KEY` is set
- `curl` and `jq` are installed

Advanced setup:
- if quota lives on a different endpoint than search, set `PRISMFY_API_ROOT` or `PRISMFY_ME_URL`

3. Verify API access:
```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --quota
```

4. Quick smoke test:
```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --company "Vercel" --query-family company
```

5. Export a JSON report:
```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --person "Guillermo Rauch" --company "Vercel" --query-family all --out contact_discovery_report.json
```

Optional automation:
```bash
# Run from this skill directory:
# ~/.openclaw/workspace/skills/contact-discovery

cp -r hooks/contact-discovery ~/.openclaw/hooks/
find ~/.openclaw/hooks/contact-discovery -maxdepth 1 -type f | sort
openclaw hooks enable contact-discovery
openclaw hooks list
```

## When to Use
Use this skill when:
- a user asks for a public email or public contact method,
- a user wants a contact path for a person or company,
- the next step is outreach and contact discovery is the blocker,
- a lead already exists and the missing piece is how to reach them.

## When NOT to Use
Avoid using this skill when:
- the task is lead qualification rather than contact discovery,
- the user wants private or guessed contact data,
- the task only needs company/person verification,
- there is no person, company, or domain anchor at all.

## Inputs
- `--company` (optional)
- `--domain` (optional)
- `--person` (optional)
- `--role` (optional)
- `--query-family` (optional: `identity|direct|company|pattern|all`)
- at least one of `--company`, `--domain`, or `--person` is required

Family notes:
- person-only mode is strongest with `direct`, `identity`, or `all`
- if `company` or `pattern` is used with person-only input, the helper falls back to weaker public-web clues and should be treated as lower confidence

## Outputs
Primary chat output:
- short verdict in plain language,
- `public_email_found | contact_path_found | company_contact_found | company_email_pattern_found | not_found | ambiguous`,
- best public contact clue,
- one concrete source URL.

Optional artifact output:
- JSON when the user asks for a file, export, or machine-readable report.
- Use `--out <file>` to write the report to disk.

If JSON artifact is produced, required fields are:
- `timestamp_utc`
- `skill_version`
- `entity_type`
- `identity_status`
- `contact_verdict`
- `summary`
- `public_emails[]`
- `contact_paths[]`
- `email_pattern_clues[]`
- `source_urls[]`
- `run_failure_code`

## Execution
1. Resolve identity first:
   - canonical company domain if possible,
   - person + company match if person-focused.
2. Run Prismfy query families in this order:
   - `identity`
   - `direct`
   - `company`
   - `pattern`
3. Return the strongest safe verdict:
   - `public_email_found`
   - `contact_path_found`
   - `company_contact_found`
   - `company_email_pattern_found`
   - `not_found`
   - `ambiguous`
4. Reply in chat first.
5. Emit JSON only when requested or when `--out` is used.

Command examples:
```bash
# Check quota / connectivity
bash contact-find.sh --quota

# Company contact discovery
bash contact-find.sh --company "Vercel" --query-family company

# Person + company contact discovery
bash contact-find.sh --person "Guillermo Rauch" --company "Vercel" --query-family all

# Export a report
bash contact-find.sh --person "Guillermo Rauch" --company "Vercel" --query-family all --out contact_discovery_report.json
```

Execution contract:
- preferred mode: balanced
- source cap: up to 5 URLs per query
- default chat mode: concise, human-readable, no raw JSON dump
- only treat an email as found if it appears explicitly in public evidence
- do not infer a private email from a pattern clue alone
- strongest verdicts come from `--query-family all`
- human review is still recommended before high-value outreach

## Query families

### `identity`
- official site
- contact/about/team pages
- person + company exact match

### `direct`
- person + company + email/contact
- person + company + author/press
- person + domain clue

### `company`
- company or domain contact pages
- press/support/help/team pages
- general company contact email traces
- in person-only mode, falls back to public contact/profile page discovery

### `pattern`
- company email format pages or mentions
- domain email format clues
- pattern-only evidence for later review
- in person-only mode, only yields weak clue discovery and should stay conservative

## Failure Handling
Use these failure codes:
- `PRISMFY_UNAVAILABLE`
- `PRISMFY_INVALID_RESPONSE`
- `IDENTITY_UNCLEAR`
- `NO_PUBLIC_EVIDENCE`
- `RATE_LIMIT_OR_TIMEOUT`

Handling guidance:
- If Prismfy is unavailable, say so explicitly.
- If identity is unclear, mark `ambiguous`.
- If only a pattern clue exists, say that clearly and do not present it as a real email.
- Never invent or guess a personal email.

## Response Style
- In normal chat, do not lead with JSON.
- Lead with the verdict.
- Then show the best public email or best contact path.
- Keep it compact.
- Mention a report filename only if `--out` created one.

## Safety
- Do not expose API keys.
- Do not guess personal emails from patterns.
- Do not claim a contact method exists unless backed by public evidence.
- Do not present likely deliverability as confirmed deliverability.

## Minimal Example
Input:
- `--person`: `Guillermo Rauch`
- `--company`: `Vercel`

Default chat output:
- `Contact path found.`
- `1. Identity: canonical domain = vercel.com`
- `2. Evidence: emails=0, direct_hits=2, company_hits=3, pattern_hits=1, official_hits=2`
- `3. Path: https://vercel.com/contact`
- `4. Source: https://vercel.com/contact`
