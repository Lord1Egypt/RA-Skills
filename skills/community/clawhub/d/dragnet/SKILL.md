---
name: dragnet
description: Generate a verified Dragnet marketplace profile. Scans your OpenClaw workspace — SOUL.md, AGENTS.md, USER.md, MEMORY.md, conversation exports, installed skills, and agent configs — to build a signed dragnet-profile.json proving your Claude-building expertise. Use when you want to get listed on dragnet.unrelated.works, generate or update your Dragnet profile, or validate your builder credentials.
---

# Dragnet — Builder Profile Generator

Generate a cryptographically signed profile for the [Dragnet marketplace](https://dragnet.unrelated.works) — where verified Claude builders get found and hired.

## What It Does

1. Scans the workspace for evidence of Claude-building expertise
2. Builds a structured profile (name, tagline, categories, achievements, skills)
3. Signs it with HMAC-SHA-256 so Dragnet can verify authenticity
4. Outputs `dragnet-profile.json` ready to upload

## Workflow

### 1. Gather Evidence

Scan these sources (read what exists, skip what doesn't):

| Source | What to extract |
|--------|----------------|
| `SOUL.md` | Builder personality, working style, specialisation signals |
| `AGENTS.md` | Agent architecture sophistication, multi-agent patterns |
| `USER.md` | Name, location, professional context |
| `MEMORY.md` | Notable projects, decisions, recurring themes |
| `TOOLS.md` | Tool integrations, infrastructure knowledge |
| `skills/*/SKILL.md` | Installed/authored skills (count and categories) |
| `memory/*.md` | Recent activity, project history, achievements |
| Conversation exports (if any `*.json` exports exist in workspace) | Real usage patterns, problem-solving depth |

**Privacy:** Never include raw personal data, API keys, secrets, or private conversation content in the profile. Only extract professional capability signals.

### 2. Build the Profile Object

Construct a JSON object with these fields:

```json
{
  "dn_v": "1.2",
  "issued": "<ISO-8601 timestamp>",
  "builder": {
    "name": "<builder name>",
    "location": "<city, country — or 'Remote'>",
    "tagline": "<one-line expertise summary, max 80 chars>"
  },
  "categories": ["<1-3 categories from: Legal, E-commerce, HR, Marketing, Healthcare, Finance, Education, DevOps, Automation, Creative, Data, Security, Research>"],
  "achievements": [
    "<achievement 1 — specific, quantified where possible>",
    "<achievement 2>",
    "<achievement 3>"
  ],
  "skills": ["<skill 1>", "<skill 2>", "...up to 8"],
  "systemSummary": "<2-3 sentence summary of builder's agent architecture and approach>",
  "_nonce": "<random 8-char alphanumeric string>"
}
```

**Achievement guidelines:**
- Lead with impact ("Reduced X by Y%" / "Built Z handling N items")
- Be specific — vague claims like "good at prompting" are worthless
- Derive from actual workspace evidence, not imagination
- 3 achievements exactly

**Category selection:**
- Pick 1-3 categories that best match the builder's demonstrated work
- If work doesn't fit listed categories, use the closest match

### 3. Interactive Review

Present the draft profile to the builder before signing:

```
Here's your Dragnet profile draft:

Name: <name>
Tagline: <tagline>
Categories: <categories>
Achievements:
  1. <achievement 1>
  2. <achievement 2>
  3. <achievement 3>
Skills: <skills list>
Summary: <systemSummary>

Want to adjust anything before I sign and generate the file?
```

Let the builder edit any field. Re-present after changes until they confirm.

### 4. Sign and Output

Once confirmed, write the profile JSON to a temp file, then sign it:

```bash
# Write unsigned profile
cat > /tmp/dragnet-unsigned.json << 'PROFILE'
<the JSON object without _sig>
PROFILE

# Sign it
node <skill-dir>/scripts/sign-profile.mjs /tmp/dragnet-unsigned.json ./dragnet-profile.json
```

The signing script:
- Computes HMAC-SHA-256 over the canonical JSON (sorted keys, `_sig` excluded)
- Appends `_sig` field
- Verifies round-trip integrity
- Writes final `dragnet-profile.json`

### 5. Next Steps

After generating, tell the builder:

> Your signed profile is at `./dragnet-profile.json`.
>
> To go live on Dragnet:
> 1. Go to [dragnet.unrelated.works](https://dragnet.unrelated.works)
> 2. Click **Get Listed**
> 3. Upload your `dragnet-profile.json`
> 4. Dragnet verifies the signature and publishes your profile
>
> To update your profile later, just run this skill again.

## Profile Schema Reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `dn_v` | string | yes | Always `"1.2"` |
| `issued` | string | yes | ISO-8601 timestamp |
| `builder.name` | string | yes | Full name or pseudonym |
| `builder.location` | string | yes | City, Country or "Remote" |
| `builder.tagline` | string | yes | Max 80 characters |
| `categories` | string[] | yes | 1-3 from allowed list |
| `achievements` | string[] | yes | Exactly 3 |
| `skills` | string[] | yes | 2-8 skill labels |
| `systemSummary` | string | yes | 2-3 sentences |
| `_nonce` | string | yes | Random 8-char alphanumeric |
| `_sig` | string | auto | Added by signing script |
