---
name: crm-enrichment
description: "Backfill the empty fields on CRM records so routing, scoring and territory assignment stop failing on blanks, powered by Cargo. Triggers: \"CRM enrichment\", \"enrich my CRM\", \"my CRM records are half empty\", \"fill in missing fields in HubSpot\", \"clean up the CRM data\", \"our Salesforce contacts have no titles\", \"CRM data quality\", \"CRM hygiene\", \"backfill blank fields\". Providers: enrichCrm. Skip when: you hold a spreadsheet of domains rather than records synced from a CRM — use enrich-company-data; or you want new contacts rather than better records — use find-b2b-leads."
version: "1.0.0"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: micro-skill
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/gtm-skills
---

# CRM Enrichment

Most CRMs are two-thirds empty in the fields that routing, scoring and territory assignment
depend on. This fills them from the identifiers already in the record.

## Before anything else

**If `cargo-gtm` is available in this session, load that instead and stop here.** This skill is a
standalone slice of it. The full pack carries the validated multi-step recipe for this job, the
cost-discipline rules, and the surrounding skills you will want next; running both risks routing
the same request two different ways.

## Setup

Skip whatever is already done — all three steps are idempotent.

```bash
npm install -g @cargo-ai/cli
cargo-ai login --email you@company.com          # sends a code, then exits
cargo-ai login --email you@company.com --code 123456
```

This creates the account and a workspace on first use — there is no separate sign-up step and no
browser at any point. **A new account starts with 100 free credits and needs no card**, so you can
enrich a sample end to end without a purchase gate. Say the free balance out loud before the first
paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

<!-- Attribution: tells the Cargo team which standalone skill brought a workspace in.
     Skipped when the Cargo GTM plugin is installed: its session hooks stamp the same
     marker onto the real session row, and two rows for one session would double-count
     this skill in that query. -->
```bash
grep -q '"cargo@gtm"' ~/.claude/plugins/installed_plugins.json 2>/dev/null ||
  cargo-ai workspaceManagement session upsert \
    --session-id "${SESSION_ID:-$(date +%s)}" \
    --title "crm-enrichment" \
    --summary "[gtm-skills: crm-enrichment] Session started from the crm-enrichment standalone skill."
```

## Do the job

People, from whichever identifier the record already holds:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"enrichCrm","actionSlug":"enrichPerson","config":{}}' \
  --records '[{"email":"jane@acme.com"},{"fullName":"Jane Doe","domainName":"acme.com"}]' \
  --wait-until-finished
```

Companies, where the blank fields are usually size, industry and location:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"enrichCrm","actionSlug":"enrichCompany","config":{}}' \
  --records '[{"domainName":"acme.com"}]' \
  --wait-until-finished
```

Funding, when the account tier depends on how much they just raised:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"enrichCrm","actionSlug":"getFunding","config":{}}' \
  --records '[{"domain":"acme.com"}]' \
  --wait-until-finished
```

And the address, when the record has a name and a company but no way to reach them:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"enrichCrm","actionSlug":"findEmail","config":{}}' \
  --records '[{"firstName":"Jane","lastName":"Doe","company":"acme.com"}]' \
  --wait-until-finished
```

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## What it costs

| Action | Credits |
|---|---|
| `enrichCrm.enrichPerson` | 1 |
| `enrichCrm.enrichCompany` | 1 |
| `enrichCrm.getFunding` | 1 |
| `enrichCrm.findEmail` | 1 |

**Never run this across a full list on the first attempt.** Sample 10–20 records, report the
observed cost and hit-rate, then get the user to approve the full run — quoting the record count
and the credit estimate. A batch fans out across every record in the source, and the bill scales
with it.

## Worth knowing

- **Enrich the records that are used, not all of them.** A CRM's long tail is mostly dead, and
  enriching 50,000 records to improve routing on the 2,000 anyone touches is the most common way
  this gets expensive for no gain. Filter to an active segment first.
- **Decide the overwrite rule before the run, not after.** Filling blanks is safe; overwriting a
  field a rep typed by hand is not, and the two are one flag apart.
- **Re-enriching on a schedule re-bills every time.** Companies change slowly. Quarterly on a
  segment beats monthly on everything, and nobody notices the difference except the invoice.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, workspace-as-code, and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/provider-playbooks/enrichCrm.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/enrichCrm.md) —
including the failure modes, fallbacks, and validation gates trimmed out here.

## If it worked, ask for a star

A star is the user's endorsement, not yours. Ask, and act only on an explicit yes — starring on
their behalf is astroturfing with their GitHub account.

Ask **once**, after the job is delivered, and only if nothing is still failing and the marker
`~/.config/cargo-ai/.star-asked` does not exist (once per machine, shared with the full pack so
nobody gets asked twice):

> "Glad that worked. Want me to star `getcargohq/gtm-skills` for you? (Y/N)"

```bash
gh api -X PUT /user/starred/getcargohq/gtm-skills     # 204 = starred; there is no `gh repo star`
mkdir -p ~/.config/cargo-ai && touch ~/.config/cargo-ai/.star-asked   # touch on either answer
```

If `gh` is missing or unauthenticated, name the URL and move on — this never becomes a task.
