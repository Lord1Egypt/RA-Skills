# Find Public Contact Details Before Outreach

`contact-discovery` helps an agent find public contact details for a person or company using Prismfy web search.

It is built for the last-mile outreach problem: you already know who the lead is, but you still need a public email, contact page, press path, support path, or company email-format clue.

You give:
- `company`, `domain`, or `person + company`

You get:
- public emails when they are actually exposed
- contact page or team/press/support path
- company email-format clues
- source-backed contact evidence
- optional JSON export

Powered by Prismfy web search. Get your API key at [prismfy.io](https://prismfy.io).

## Example

Input:

```text
Find public contact details for Guillermo Rauch at Vercel.
```

Expected result:

```text
Contact path found.

1. Identity: canonical domain = vercel.com
2. Evidence: direct and company contact signals found from public pages.
3. Path: https://vercel.com/contact
```

## What it does

Given a company, domain, or person, this skill:
1. resolves identity,
2. checks for public emails,
3. finds contact/support/press/team paths,
4. surfaces company email-format clues,
5. returns a conservative contact verdict,
6. optionally writes a JSON artifact.

The default behavior is chat-first. It should not invent an email from a weak clue.

Person-only note:
- person-only lookups work best in `direct` or `all` mode
- `company` and `pattern` families can still run, but they are weaker clue-finding paths without a company/domain anchor

## Setup

### 1. Install the skill

```bash
openclaw skills install contact-discovery
```

### 2. Add your Prismfy API key

```bash
export PRISMFY_API_KEY="ss_live_your_key_here"
```

To keep it after restart:

```bash
echo 'export PRISMFY_API_KEY="ss_live_your_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Preflight

- `PRISMFY_API_KEY` is set
- `curl` and `jq` are installed

### 4. Verify API access

```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --quota
```

Advanced setup:
- if quota lives on a different endpoint than search, set `PRISMFY_API_ROOT` or `PRISMFY_ME_URL`

### 5. Quick smoke test

```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --company "Vercel" --query-family company
```

### 6. Export a JSON report

```bash
cd ~/.openclaw/workspace/skills/contact-discovery
bash contact-find.sh --person "Guillermo Rauch" --company "Vercel" --query-family all --out contact_discovery_report.json
```

## Optional automation

Recommended if you want OpenClaw to remember this workflow more consistently.

```bash
# Run from this skill directory:
# ~/.openclaw/workspace/skills/contact-discovery

cp -r hooks/contact-discovery ~/.openclaw/hooks/
find ~/.openclaw/hooks/contact-discovery -maxdepth 1 -type f | sort
openclaw hooks enable contact-discovery
openclaw hooks list
```

## Included files

- `SKILL.md` — OpenClaw skill instructions
- `contact-find.sh` — bundled Prismfy query helper
- `hooks/contact-discovery/` — optional bootstrap reminder hook

## Important note

This skill is for public contact discovery, not private-data inference.

It can find:
- explicit public emails,
- public contact pages,
- company email-format clues.

It should not:
- guess a personal email from a pattern alone,
- claim deliverability,
- present weak clues as confirmed contact data.
