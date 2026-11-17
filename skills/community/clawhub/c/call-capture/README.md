# Call capture: turn recorded calls into your go-to-market knowledge base

To make what is said on calls reusable, collect every recorded call each morning, scribe it into a
log entry, and promote a claim into your context only once it has been heard twice. This cookbook
does that with a committed collector script and a Claude Code harness agent, delivered as one
reviewable pull request against your go-to-market repository. Nine call recorders ship; a tenth is
one adapter file.

```sh
cargo-ai project add cookbook/call-capture
```

## What it does

- **Collects.** `scripts/collect/calls.ts` pulls every call in a three-day rolling window whose
  transcript the recorder has finished processing, and writes one raw file per call into
  `cadence/log/raw/calls/`. Deterministic, idempotent, no LLM anywhere near it.
- **Scribes.** The agent reads each pending raw capture and writes
  `cadence/log/calls/<date>-<account>.md`: what was said, the GTM intel under fixed headings, the
  actions as checkboxes. Capped at 12 per run, fresh-first then oldest-backfill.
- **Promotes.** A claim reaches `context/` — the knowledge layer at the repository root — only on
  its **second independent occurrence**, citing both calls.
- **Stops.** One pull request, never merged. The agent has repository write access and no other
  write path: no email, no CRM, no merge.

## How it works

1. **The cron trigger fires** at 07:00 UTC, after the recorder has finished processing yesterday.
2. **The agent clones the repository** — the project's own, resolved from the checkout's git origin
   at deploy rather than written down. The harness's working tree is the GTM repo itself, which is
   what lets its output be a diff rather than a column value.
3. **It runs the collector** — `npx tsx scripts/call-capture/collect/calls.ts` — which takes its
   recorder and internal domain from `collect/config.ts` in the tree it just cloned, and
   `CALL_RECORDER_API_KEY` from the workspace environment variables a harness agent inherits in
   full. The agent is told not to fetch calls itself and not to edit the script's collection rules.
4. **It scribes** the pending captures, then promotes what repeats.
5. **It opens one pull request** whose body reports four numbers: captured, scribed fresh, scribed
   from backfill, pending remaining. The remainder is the drain gauge; a number that never falls
   means the cap is too low or a class of call is failing to parse.
6. **A human merges**, and the next `cargo-ai project deploy` syncs `context/` into the workspace
   context repository, where the scorer, the researcher and every other agent read it.

Adds 4 resources plus a script bundle.

| File                            | Resource                     | Role                                                       |
| ------------------------------- | ---------------------------- | ---------------------------------------------------------- |
| `infra/agents/call-scribe.ts`   | `defineAgent` (claudeCode)   | schedule, model, folder — and no env of its own            |
| `infra/agents/call-scribe.prompt.ts` | (not a resource)        | the scribe's contract: window, cap, repetition bar, limits |
| `infra/connectors/git.ts`       | `defineConnector` (`github`) | the clone, branch, push and PR path, resolved by binding   |
| `infra/connectors/anthropic.ts` | `defineConnector` (`anthropic`) | the model the harness runs on, billed and metered          |
| `infra/folders/index.ts`  | `defineFolder`               | the workspace folder this cookbook's resources are filed in |
| `scripts/collect/recorder.ts`   | (not a resource)             | the `Recorder` contract and the provider-agnostic pipeline |
| `scripts/collect/recorders/`    | (not a resource)             | nine recorder adapters and the registry that names them    |
| `scripts/collect/config.ts`     | (not a resource)             | the two project choices: which recorder, which domain      |
| `scripts/collect/calls.ts`      | (not a resource)             | the entrypoint: resolve a slug, then `capture`             |

## The two halves, and where they land

This cookbook has one directory per layer it touches, and the install mirrors each into its namesake
in the project:

```
call-capture/infra/     ->  infra/call-capture/      what is declared and deployed
call-capture/scripts/   ->  scripts/call-capture/    what the agent runs
```

Those are the layers `cargo-ai project init` already scaffolds — `infra/` holds the resources
`cargo.json` names, `scripts/` is imperative glue for runtime surfaces a project cannot declare yet —
so a cookbook that needs both contributes to both under its own name rather than inventing a third
place.

The `collect/` subdirectory is a namespace, not decoration: call recordings are the first sensor,
and the next one (Slack threads, reply metadata, product usage) lands beside it as its own
entrypoint rather than growing this one. The agent's step 1 names the collectors it runs, so adding
a sensor is a new file plus a line in the system prompt.

`scripts/package.json` is belt and braces. The loader imports only the resources folder `cargo.json`
names (`infra/` in a scaffolded project), so nothing under `scripts/` is ever imported as a resource.
In a project whose `cargo.json` names the repo root instead, the loader imports every `.ts` it finds
**except** directories carrying a `package.json` — without that file, `cargo-ai project plan` would
import the collector and run it against the live API on every plan.

## Why the split

The collection and the judgement are different jobs, and the failure modes for mixing them are not
symmetric.

A fetch loop an agent re-derives every morning is a fetch loop that silently changes shape: a window
that drifts, a filter that quietly widens, a field read differently on a day the model was less
careful. Nothing downstream can tell, because the archive is what everything downstream is diffed
against. So the fetch is a committed script and the agent is told not to improvise it.

The scribing is the opposite. It is judgement — what was actually agreed, whether this is the same
objection as last week, whether a vendor call is being misread as pipeline — and it produces a diff
across a dozen markdown files. That is what `harnessSlug: "claudeCode"` buys: a working tree, the
git history to read before writing, and a pull request. It does not buy its own model: the harness
runs against Cargo's LLM proxy, so `connector` and `languageModel` are required here exactly as
they are on a `streamText` agent, and they are what the run is billed and metered against.

## Whoever records your calls

The collector is a contract, nine implementations of it, and a slug that picks one.
`recorder.ts` defines `Recorder` — a `provider` slug and three methods (`listReady`, `transcript`,
`notes`) — and holds everything that is true whoever records your calls: deduplication, account
slugging, the internal-domain filter, file layout, the rolling window, `--dry-run`. `recorders/`
holds one adapter per vendor — Avoma, Granola, Fathom, Gong, Fireflies, Grain, tl;dv, Modjo and
Clari Copilot — plus the registry. `config.ts` names the one that runs, typed against the
registry's keys, and `calls.ts` resolves it and calls `capture`.

```sh
npx tsx scripts/call-capture/collect/calls.ts --list
npx tsx scripts/call-capture/collect/calls.ts --recorder=granola --dry-run
```

A recorder that is not there is one new file beside the others and one entry in `recorders/index.ts`.
The compiler is what keeps that honest: a half-written adapter does not typecheck, and the error
names the field that is missing. Auth deliberately stays in the adapter — Bearer, Basic, two custom
headers and a signed GraphQL POST are four different things — while the 429 backoff is shared
through `fetchJson(url, init)`, which takes the whole request.

Two rules keep a registry from becoming a graveyard of code nobody runs. Every entry declares
whether it was verified against a live workspace (Avoma) or written from the vendor's own
specification (the other eight), and one written from docs says so on every run. And the five
recorders in `references/recorder-apis.md` that do **not** ship each carry the reason — a list
endpoint with no date filter, a transcript that is not JSON, an OAuth token that expires in ten
minutes — rather than a stub.

## Why the context is not in this folder

`defineContext` is a per-workspace singleton, and the knowledge layer belongs at the repository root
where humans edit it — which is exactly where `cargo-ai project init` already declares it. So this folder
ships none.

## Placeholders (edit before deploy)

Two of them, both in `scripts/collect/config.ts`, because they are choices rather than secrets: in
code the compiler checks one of them, a reviewer sees both, and an edit reaches the next run as soon
as it merges — the harness re-clones this repository every morning, while a value in the agent's
spec would need a redeploy. The agent declares no environment of its own at all.

1. **`RECORDER`** — which of the nine slugs records your calls, typed against the registry, so a
   slug that is not a recorder fails `npm run typecheck`. A recorder that does not ship is one new
   file satisfying `Recorder` plus an entry in `recorders/index.ts`, and
   `references/recorder-apis.md` carries the endpoints for five more.
2. **`INTERNAL_DOMAIN`** — your own email domain, or every internal standup is captured as a
   customer call. Matched against the domain of each attendee's address, or a subdomain of it.

And one credential, which is **not** in any file: create it once in the workspace with
`cargo-ai workspaceManagement envVar create --key CALL_RECORDER_API_KEY --secret` and the harness
inherits it. Deliberately not a `secret()` in the agent's env, which would need the key in the
deploying shell on every deploy and a re-apply to pick up a rotation.

## What it does not do

It does not contact anyone, write to a CRM, merge its own pull request, edit or delete a raw capture
or an existing log entry, or touch `plan/` and `infra/`. It reports what the field said; it does not
change the strategy or the deployed engine.
