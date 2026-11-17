---
name: apollo-to-cargo
description: "Rebuild an Apollo list on Cargo and price the two side by side before you move anything, powered by Cargo. Triggers: \"Apollo alternative\", \"migrate off Apollo\", \"move my Apollo list to Cargo\", \"replace Apollo.io\", \"I have an Apollo export\", \"Apollo credits ran out\", \"is Cargo cheaper than Apollo\", \"Apollo coverage is bad in my niche\". Providers: apolloio, waterfall. Skip when: you are porting a Clay table rather than an Apollo list — use clay-to-cargo; or you simply want contacts sourced and have nothing to migrate — use find-b2b-leads."
version: "1.0.5"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/gtm-skills
metadata:
  author: getcargo
  source: one-off
  personas:
    - revops
    - gtm-engineering
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

# Apollo to Cargo

Take a list somebody built in Apollo and rebuild it on Cargo, with the cost of both measured on
the same rows rather than argued from price pages.

**Cargo keeps Apollo as one provider among many.** This is not a rip-out: `apolloio` is in the
stack, and the honest answer is sometimes "Apollo already covers this niche better, keep paying
for it". What changes is that Apollo stops being the only source, so the records it misses are
caught instead of lost.

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
migrate a sample of the list end to end without a purchase gate. Say the free balance out loud
before the first paid call on a new account.

Already signed in? `cargo-ai whoami` confirms it.

## Do the job

### 1. Take a sample, not the list

Export the Apollo list to CSV and pull **10 to 20 rows**. The whole point of this skill is that
the comparison is measured, and a measurement costs credits, so it is taken on a sample and
extrapolated.

### 2. Enrich the sample through Apollo, from inside Cargo

Same vendor, same data, so this is the control rather than the pitch:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"apolloio","actionSlug":"enrichPerson"}' \
  --records '[{"parameters":{"first_name":"Jane","last_name":"Doe","domain":"acme.com"}}]' \
  --wait-until-finished
```

Company side, where Apollo's firmographics are often the reason people stay:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"apolloio","actionSlug":"enrichOrganization"}' \
  --records '[{"domain":"acme.com"}]' \
  --wait-until-finished
```

### 3. Run the same rows through the waterfall

This is the comparison. Same input, several providers behind one call:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"enrichContact"}' \
  --records '[{"full_name":"Jane Doe","domain":"acme.com"}]' \
  --wait-until-finished
```

Then verify both sets, because a match rate counted on unverified addresses flatters whichever
source guessed more:

```bash
cargo-ai orchestration action execute-batch \
  --action '{"kind":"connector","integrationSlug":"waterfall","actionSlug":"verifyEmail"}' \
  --records '[{"email":"jane@acme.com"}]' \
  --wait-until-finished
```

### 4. Report both numbers before anyone decides

Two figures per source on the same rows: **verified hit rate** and **credits spent**. Say both.
A cheaper source with a worse hit rate is not cheaper, it is smaller, and the per-verified-record
cost is the only number that compares them honestly.

Operations are asynchronous. `--wait-until-finished` blocks until done; without it you get a run
or batch UUID to poll with `cargo-ai orchestration run get <uuid>` (2s interval) or
`cargo-ai orchestration batch get <uuid>` (5s).

## Example

> Before our Apollo renewal, compare it with Cargo on 20 rows from `apollo-q3-export.csv`.

Illustrative output, fictional records:

| Source | Emails found | Verified | Credits | Credits per verified |
|---|---|---|---|---|
| Apollo, via Cargo | 15 / 20 | 11 | 21.5 | 1.95 |
| Cargo waterfall | 18 / 20 | 17 | 41.8 | 2.46 |

63.3 credits for the whole comparison (20 × 1 + 15 × 0.1 on Apollo, 20 × 2 + 18 × 0.1 on the waterfall): the waterfall verified 6 more addresses at a higher cost per address, and the call is the user's.

## What it costs

| Action | Credits |
|---|---|
| `waterfall.verifyEmail` | 0.1 |
| `apolloio.enrichPerson` | 1 |
| `apolloio.enrichOrganization` | 1 |
| `waterfall.enrichContact` | 2 |

A 20-row comparison running both sides is roughly 20 × (1 + 2 + 0.1 × 2), around 64 credits,
which fits inside the free balance a new account starts with.

**Never run this across a full list on the first attempt.** Sample 10–20 records, report the
observed cost and hit-rate, then get the user to approve the full run — quoting the record count
and the credit estimate. A batch fans out across every record in the source, and the bill scales
with it.

## Worth knowing

- **Do not quote a saving you have not measured.** The comparison above exists because the answer
  varies by niche: Apollo's coverage is genuinely strong in some segments and thin in others, and
  the sample is what tells you which one you are in.
- **`apolloio.enrichPerson` costs 9 rather than 1 with `revealPhoneNumber: true`.** Leave it off
  unless phones are the reason for the migration, and say so when you turn it on.
- **An Apollo export is a snapshot.** Rows exported months ago carry stale titles and stale
  companies, so a low hit rate on an old export is a fact about the export, not about either
  vendor. Check the export date before reading anything into the numbers.

## Going further

This skill does one job. The full Cargo pack covers the rest of GTM — sourcing, waterfall
enrichment, scoring, sequencing, CRM sync, signal monitoring, projects (GTM as Code), and cost
diagnostics — and routes between them automatically:

```bash
npx skills add getcargohq/cargo-skills
```

The complete, validated flow behind this skill lives in
[`cargo-gtm/provider-playbooks/apolloio.md`](https://github.com/getcargohq/cargo-skills/blob/main/cargo-gtm/provider-playbooks/apolloio.md) —
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
