---
name: build-tam-list
description: "Build a total addressable market list of companies filtered by industry, headcount, and geography, powered by Cargo. Triggers: \"build a TAM list\", \"how many companies match our ICP\", \"list every SaaS company in Europe under 200 employees\", \"size our addressable market\", \"find target accounts\", \"list building\", \"build a list of companies\". Providers: salesNavigator. Skip when: you want the people at those companies — use find-b2b-leads or find-stakeholders; or you want companies by tech stack — use find-companies-using-tech."
version: "1.2.4"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - revops
    - sales-leadership
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

# Build TAM List

Build a total addressable market list of companies filtered by industry, headcount, and geography.

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
run this skill end to end without a purchase gate. Say the free balance out loud before the first
paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Do the job

```bash
cargo-ai orchestration action execute \
  --action '{"kind":"connector","integrationSlug":"salesNavigator","actionSlug":"searchAccounts"}' \
  --data '{
    "companyHeadcounts": ["D", "E"],
    "industryCodes": ["43"],
    "headquarterLocationIds": ["103644278"],
    "limit": 100
  }' \
  --wait-until-finished
```

A list of companies with name, domain, headcount band, industry, and LinkedIn URL.

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Example

> Size the market of US fintech companies with 50–500 employees and give me the first 100.

Illustrative output, fictional records:

| name | domain | headcount | industry | linkedinUrl |
|---|---|---|---|---|
| Northwind | northwind.example | 51-200 | Financial Services | linkedin.com/company/northwind-example |
| Tailspin | tailspin.example | 201-500 | Financial Services | linkedin.com/company/tailspin-example |
| Initech | initech.example | 51-200 | Financial Services | linkedin.com/company/initech-example |

The first 100 companies for 20 credits (100 × 0.2); nothing is enriched yet, so the market is sized before any per-company spend.

## What it costs

| Action | Credits |
|---|---|
| `salesNavigator.searchAccounts` | 0.2 |

**Never run this across a full list on the first attempt.** Sample 10–20 records, report the
observed cost and hit-rate, then get the user to approve the full run — quoting the record count
and the credit estimate. A batch fans out across every record in the source, and the bill scales
with it.

## Worth knowing

- Not the cheapest company search in the catalog. `FullEnrich.searchCompanies` is **free** (0 credits) and takes plain-string filters — `industry`, `headcount` `{min,max}`, `headquarters`, `technologies`, `keywords` — up to 2,000 per run; `FullEnrich.fetchCompanies`, also free, pulls up to 10,000 straight into a Cargo model. `aiArk.searchCompanies` (0.01) is the cheapest paid option and takes lookalike seeds. Sales Navigator is the default when the list is defined by LinkedIn-native filters.
- `FullEnrich.lookupCompany` (free) returns one company's name, industry, headcount and LinkedIn URL from its domain.
- Filters take LinkedIn's internal codes, **as strings**: `industryCodes: ["43"]` (Financial Services), `headquarterLocationIds: ["103644278"]` (United States), `companyHeadcounts: ["D","E"]` (51-200, 201-500; `B` is 1-10 and `C` 11-50). Names like `"fintech"` or `"50-200"` silently match nothing, and bare numbers fail validation. Resolve a name to its code with `cargo-ai connection connector autocomplete --connector-uuid <uuid> --slug listIndustries --params '{}' --value fintech` (`listGeoCodes` for locations).
- Billed per returned record, and the response carries the records only, not a total match count. Pull a small `limit` first, check the rows fit, then pull the approved scope.
- Size the market before you enrich it — a count is nearly free, a 5,000-company pull is ~1,000 credits.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/recipes/build-tam.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/recipes/build-tam.md) —
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
