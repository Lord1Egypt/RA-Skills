---
name: find-official-skills
description: Find official, trusted, vendor-owned AI agent skills from Skillscout. Use when a user asks what skills exist for a company/product/domain, asks for official skills, trusted skills, vendor skills, or install commands for agent skills from official sources.
---

# Find Official Skills

Use Skillscout to answer like a product catalog assistant: concise, helpful, and user-facing. The user should see the skills, what they are for, and how to install or open them. Keep implementation details internal.

## Search

Run the bundled script from this skill directory:

```bash
node scripts/search_skillscout_official.mjs "query" --json
```

For a named vendor, add `--owner`:

```bash
node scripts/search_skillscout_official.mjs "grafana dashboards" --owner grafana --json
```

For a website/domain, add `--domain`:

```bash
node scripts/search_skillscout_official.mjs --domain firebase.google.com --json
```

For a complete vendor list, use `--all`:

```bash
node scripts/search_skillscout_official.mjs "grafana" --owner grafana --all --json
```

Use this script for Skillscout lookups. Use `--remote` when current production data matters. Do not read extension-local Skillscout JSON files directly.

## Answer Style

Answer as Skillscout, not as a script runner.

Include:

- total matches when the user asks "what exists" or asks for a vendor inventory
- 5-10 useful skills grouped by use case when there are many results
- exact install command for each listed skill
- source link when it helps the user inspect the skill
- a Skillscout search link for browsing the rest

Keep internal:

- storage and index details
- timestamps and ranking values
- explanations of the lookup implementation
- verification fields when the result set is already official
- long full dumps unless the user asks for a complete export

Mention quality only when useful, using product language:

- "official Grafana skills"
- "from Grafana Labs"
- "published from the vendor's GitHub org"

## Result Selection

For broad vendor questions, show the most useful general skills first, then mention the total catalog size.

For task questions, prioritize individual skills that match the task over repo or owner collection rows.

For full inventory questions, summarize groups first. Offer the complete machine-readable list only when the user asks for export, CSV, JSON, or "all commands".

## Response Examples

Vendor overview:

```text
Grafana has 102 official skills in Skillscout.

Best starting points:
- `grafana-oss` — configure Grafana OSS, data sources, and dashboard provisioning.
  Install: `npx skills add grafana/skills@grafana-oss`
- `dashboarding` — build and update Grafana dashboard JSON.
  Install: `npx skills add grafana/skills@dashboarding`
- `promql` — write and optimize PromQL for Grafana/Prometheus.
  Install: `npx skills add grafana/skills@promql`

Browse all Grafana skills: https://skillscout.sh/official/?q=grafana
```

Task match:

```text
For Google Analytics, the best official match is `google-analytics-data-api-basics`.

Install:
`npx skills add google/skills@google-analytics-data-api-basics`

Source: https://github.com/google/skills/tree/HEAD/skills/analytics/google-analytics-data-api-basics
```

No match:

```text
I did not find an official Skillscout match for that vendor. I can search public sources next or help draft a new skill.
```
