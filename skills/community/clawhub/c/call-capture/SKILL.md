---
name: call-capture
description: 'Turn your recorded calls into a go-to-market knowledge base: each recorded call is collected every morning, scribed into a log entry, and, once a claim repeats, promoted into context, as one pull request against your go-to-market repo. Nine recorders ship; a tenth is one adapter file. Triggers: "our call recordings never make it into the knowledge base", "turn our call transcripts into context", "we relearn the same objection every quarter", "scribe yesterday''s calls into the repo every morning", "replace the GitHub Action that summarizes our meetings", "we record on Granola, not Avoma". Cargo project, defineAgent, harnessSlug claudeCode, workspace env var, GitHub, Avoma, Granola, Fathom, Gong, Fireflies, Grain, tl;dv, Modjo, Clari Copilot, cadence, context. Skip when: you want one call summarized right now, which is a read against the recorder''s own API and needs nothing deployed.'
version: "0.2.0"
compatibility: "Requires @cargo-ai/cli 1.0.154 or later with @cargo-ai/cdk 1.0.150 or later (harness agents bound to the project's connected state), a Cargo workspace, an authenticated LLM connector, a GTM repository with `context/` and `cadence/` at its root (the shape `cargo-ai project init` scaffolds), and an API key for whatever records your calls, stored as a workspace environment variable."
homepage: https://github.com/getcargohq/gtm-skills/tree/main/call-capture
metadata:
  author: getcargo
  source: cookbook
  personas:
    - sales-leadership
    - account-executive
    - revops
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

# Call capture

**State: to-be-approved.** Deploy-verified against a live workspace: not yet. Treat `Done when`
below as the acceptance test and review `cargo-ai project plan` before deploying. Make no outcome claim
for this skill until it is approved.

## The outcome

What your team learns on calls stops living in a recording nobody reopens. Every morning one agent
runs, and three things land in your repository:

1. **The raw capture.** A committed script pulls every call the recorder has finished processing and
   writes one file per call into `cadence/log/raw/calls/`. That is the permanent archive, and it is
   never edited or deleted.
2. **The log entry.** The agent reads each raw capture and writes
   `cadence/log/calls/<date>-<account>.md`: what was said, the intel under fixed headings, the
   actions as checkboxes.
3. **The context update.** Where a claim has been heard twice — an objection, a competitor, a
   signal — the agent promotes it into `context/` at the repository root, citing both calls.

Then it opens one pull request and stops. A human merges, and the next `cargo-ai project deploy` syncs
`context/` into the workspace context repository, which is where every other Cargo agent reads
before it acts. A correction made once on a call propagates to everything that reasons about your
market, through code review rather than through someone remembering to update a doc.

This is a scheduled CI workflow plus a hosted agent, collapsed into one declared resource. The
schedule, the credentials and the repository binding live in
`infra/call-capture/agents/call-scribe.ts`, and the instructions beside it in
`call-scribe.prompt.ts`, in the same project as everything else the workspace runs. `harnessSlug: "claudeCode"` is what buys the working tree: the output of a call is a diff
across a dozen markdown files, and only an agent with a checkout can produce one.

Three properties make it safe enough to run unattended:

- **The collection is deterministic.** The agent does not fetch calls. `scripts/collect/calls.ts`
  does, the same way every morning, and the agent is told not to improvise that step.
- **The pull request is the gate.** The agent has repository write access and no other write path.
  It cannot email anyone, cannot touch the CRM, and cannot merge itself.
- **The repetition bar.** A claim reaches `context/` only on its second independent occurrence. One
  prospect's offhand remark stays in that call's log entry, where it is evidence; it does not become
  something the whole company believes.

## Example

> Every morning, pull yesterday's Gong calls into this repo as log entries and open one pull request with anything worth adding to our context.

Illustrative output, fictional records:

```diff
[call-capture] scribe 2026-10-06
Captured 5 · scribed fresh 5 · scribed from backfill 0 · pending 0

+ cadence/log/raw/calls/2026-10-05-northwind.md
+ cadence/log/calls/2026-10-05-northwind.md
+   ## Objections
+   - "We already pay for Globex, I can't justify a second tool" (Priya Raman, VP RevOps)
+   ## Actions
+   - [ ] Send the Globex migration one-pager to Priya
+ context/objection/already-have-globex.md
+   Heard on 2 calls: cadence/log/calls/2026-09-22-fabrikam.md,
+   cadence/log/calls/2026-10-05-northwind.md
```

Five calls became five log entries, and the Globex objection reached `context/` only because a second
account raised it; a single mention would have stayed in its log entry.

## Put it in your project

This folder is a **worked example**: real project resources written for some other company. The job is
to end up with the code your company would have written, in your project, and an agent does the
adapting. If the `cargo-project` skill is in your session it carries the long form of this; if not, this
is enough.

1. **Install it — the CLI does the copy.** From inside the project (the folder holding `cargo.json`),
   `cargo-ai project add cookbook/call-capture` writes this example to `infra/call-capture/` (resources
   **and** `scripts/`) and this procedure to `.agents/skills/call-capture/`. No project yet?
   `cargo-ai project init <dir> --cookbook call-capture && cd <dir> && npm install` does both; this
   folder never ships a shell. **If you are reading this from the project's `.claude/skills/`, the
   install already happened — start at step 2.** On a CLI too old to have `add`, copy this folder in
   as a sibling of what is there by hand; everything below is unchanged.
2. **Reconcile it with what is already declared.** If the project already has a GitHub connector or
   an agents folder, rewire the imports to the existing one and drop the copy; two resources with
   one slug is a collision at deploy. The knowledge layer needs no work: the scaffold already
   declares the repo's root `context/` in `infra/context.ts`, and `defineContext` is a per-workspace
   singleton, which is why this folder ships none. **Append nothing to `.env.example`:** this
   folder's one credential is a workspace environment variable, not a deploy-time one, and step 3
   creates it.
3. **Pick the recorder, or write one.** **Ask which recorder records the team's calls**, unless the
   repo's own context or the workspace connectors already say — it is the one input here with no
   reliable lookup, and every later step depends on it. Nine ship:
   `npx tsx scripts/call-capture/collect/calls.ts --list` prints them with what each wants for a
   credential. Set it as `RECORDER` in `scripts/call-capture/collect/config.ts` — a typed constant,
   so a slug that is not a recorder fails `npm run typecheck` and names the nine that are. It is
   **not** an environment variable on the agent: a choice the compiler can check and a reviewer can
   see beats a string in a deployed spec, and because the harness clones this repository every
   morning, editing it takes effect on the next run rather than on the next deploy. What no compiler
   catches is a wrong-but-valid slug — it reads the wrong vendor's API successfully and reports a
   clean, empty run every morning — which is the other reason the choice belongs in a diff.
   **Then put its key in the workspace, not in a file.** A harness agent inherits every workspace
   environment variable, so the credential is one CLI call and nothing in this project names its
   value:

   ```sh
   export CALL_RECORDER_API_KEY=…            # this shell only; nothing persists it
   cargo-ai workspaceManagement envVar create --key CALL_RECORDER_API_KEY --secret \
     --description "Call recorder API key read by scripts/call-capture"
   ```

   Omitting `--value` reads the exported variable, which keeps the key out of argv and out of shell
   history; `--secret` encrypts it at rest and the API never returns it again. Rotation is
   `envVar update <uuid> --value …` and reaches the next morning's run with no deploy at all. A
   `secret("CALL_RECORDER_API_KEY")` in the agent's env is the trade to refuse here: it sends the
   deploying machine's value, so the key has to be in a shell or a `.env` for every deploy, by
   whoever deploys, and a rotation only lands on a re-apply. Gong and Clari Copilot issue two values
   rather than one; that single variable holds `<first>:<second>` and the adapter splits it.
   **On a recorder that does not ship, this step is a new file, not an edit.** Write
   `scripts/collect/recorders/<slug>.ts` exporting one object that satisfies the `Recorder` type in
   `scripts/collect/recorder.ts` — a `provider` slug plus `listReady(from, to)`, `transcript(id)`
   and `notes(id)` — then register it in `recorders/index.ts`. Follow the shipped adapter closest
   in shape: `avoma.ts` for Bearer REST, `gong.ts` for POST-with-a-body and a speaker id that needs
   joining, `fireflies.ts` for GraphQL, `granola.ts` for a list too thin to carry attendees.
   Nothing else moves: deduplication, account slugging, the internal-domain filter, the file format
   and the rolling window are the same whoever records your calls, and they live in `recorder.ts`.
   `references/providers.md` carries the contract and the procedure;
   `references/recorder-apis.md` carries the endpoints and exact field names for all nine plus five
   more that do not ship, each with the reason. Whichever recorder you land on, **verify its
   response shapes against the live API before you deploy** — eight of the nine were written from
   vendor documentation and say so on every run, the field names around stable endpoints move, and
   a wrong one captures nothing while reporting a clean run. Then set `INTERNAL_DOMAIN` in the same
   `config.ts` to your own email domain, or every internal call is captured as a customer one.
   Those two constants are the whole configuration surface: everything else the collector needs is
   either derived or the one credential in the workspace.
4. **Adapt.** Work the sections below in order: _What should not change_ is what you argue back
   about (say what breaks, then do it if they still want it); _What you can change_ is what you
   offer unprompted (nobody asks for a variant they do not know exists); _What you will be asked_ is
   the floor, and you derive before you ask. If you are asking more than about four questions you
   have skipped lookups. Record what you changed and why under a `## Decisions` section in your copy
   of this file.
5. **Run the collector by hand once, then plan.** `CALL_RECORDER_API_KEY=… npx
   tsx scripts/call-capture/collect/calls.ts --dry-run` first: it exercises the list call and the
   readiness filter and prints what it would take, writing nothing. Read what it printed — real
   subjects, real dates, real account slugs — because that is the only thing separating a working
   adapter from one that will report a clean empty run every morning. Then drop `--dry-run`. If it does
   not produce raw files locally it will not produce them on a schedule, and that is far cheaper to
   find out now. Then
   `npm run check && cargo-ai project plan`, show the diff, and deploy only on an explicit yes:
   `cargo-ai project deploy`. Never `cargo-ai project init --force` into a non-empty directory.
6. **Verify.** Walk _Done when_ line by line and report each with evidence. Deployed cleanly and
   produced nothing is the normal failure — and the second normal failure is a pull request nobody
   can review, so read the first line before you call this done.

## What you will be asked

**Derive before you ask.** An input with a lookup is looked up, not asked. Only the ones marked
_asked_ genuinely live in the operator's head.

| Input                                                        | Kind   | How it is answered                                                                                                                                                                                                                                     | Why it matters                                                                                                                                                                                                       |
| ------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project binding (`infra/agents/call-scribe.ts`) | value | **derived**: leave `state` unset and deploy binds the project's connected state (`cargo.state.json`): its repository, directory and production branch. `cargo-ai project check` prints the binding; a project whose state is not connected deploys the agent unbound, with an empty sandbox.                | This is the working tree the harness clones and the only place its output can land. An `owner/name` written by hand is the one value nobody notices is wrong until a pull request opens against a stranger's repository.                                                |
| recorder (`RECORDER` in `scripts/collect/config.ts`)         | value  | **asked**, once derivation fails: check the repo's own context and `cargo-ai connection connector list` first, then ask which of the nine slugs (`--list` prints them) records the team's calls. A recorder that is not there is one new adapter file plus an entry, per `references/providers.md`. | It is the one input with no lookup anywhere in the project, and everything downstream is shaped by it. A typed constant rather than an env var so a slug that is not a recorder fails to compile, and so the one thing no compiler catches — a plausible-but-wrong slug, which reads the wrong vendor's API successfully and reports a clean empty morning indefinitely — is at least in a diff someone reads. |
| `CALL_RECORDER_API_KEY`                                              | env    | **asked**: the recorder's API key, put in the workspace with `cargo-ai workspaceManagement envVar create --key CALL_RECORDER_API_KEY --secret` (step 3) and named in no file here. A harness agent inherits the workspace catalog, so nothing declares it. Gong and Clari Copilot issue two values; that one variable holds `<first>:<second>` and the adapter splits it.                                  | It is the collector's only credential, and the workspace is the only copy of it that outlives the session that set it. In the catalog it is read server-side on every run, so a rotation needs no deploy; as a `secret()` in the agent's env it is the deploying shell's value, so every deploy needs the key again and a rotation lands only on a re-apply. |
| `INTERNAL_DOMAIN` (`scripts/collect/config.ts`)              | value  | **derived**: your own email domain, which the workspace members' addresses already name                                                                                                                                                                | It is how an internal call is told from a customer one. Avoma's `is_internal` is false on every meeting in some workspaces, so it cannot be used; leave the placeholder and every standup is captured as an account.  |
| adapter state (`scripts/collect/recorders/index.ts`)   | value  | **derived**: `--list` prints which adapters were verified against a live workspace (Avoma) and which were written from vendor docs (the other eight). Nothing to decide — it decides how hard you check step 5 before deploying.                          | The contract is compiler-enforced, so a half-written adapter fails to build rather than half-working. Pointed at the wrong API it fails on the first request, which is loud; pointed at the right API with a stale field name it captures nothing and reports a clean empty run every morning. |
| GitHub connector (`infra/connectors/git.ts`)                 | value  | **derived**: `cargo-ai connection connector list` shows whether one is authorized; if not, `cargo-ai project add connector/github` opens the OAuth consent. The declaration is `default: true` because a deploy cannot mint an OAuth grant.                    | It is the agent's entire write path. Without it the run does the work and has nowhere to put it.                                                                                                                      |
| LLM connector and model (`infra/connectors/anthropic.ts`)    | value  | **derived**: `cargo-ai connection connector list` shows whether an Anthropic connector is authorized; if not, `cargo-ai project add connector/anthropic` takes the key. `default: true` because a deploy cannot mint one. Any Anthropic model pairs with `claudeCode`; the agent's `languageModel` is a placeholder to set.        | A harness does not bring its own model — it runs against Cargo's LLM proxy, so this is what the daily run is billed and metered against. Omit either and `defineAgent` throws at `plan`; pair `claudeCode` with an `openAi` connector and it typechecks green and fails at deploy. |
| cadence and context paths                                    | value  | **derived**: read `cadence/README.md` and `context/README.md`, and `ls cadence/log/` for what already exists                                                                                                                                            | The agent writes into layers humans already curate. A second parallel folder splits the record in half and the repetition bar stops seeing the earlier occurrence.                                                    |

Checked before moving on, not after the deploy:

- `RECORDER` in `config.ts` is the recorder the team actually records on — `npm run typecheck`
  settles whether the slug exists, nothing settles whether it is the right one but a reviewer
- `cargo-ai workspaceManagement envVar list` shows a `CALL_RECORDER_API_KEY` entry, marked secret —
  that listing is the deployed credential, and a value only ever exported in a shell is not one
- the collector was run by hand once and wrote real raw files
- `cargo-ai project check` prints `agent:call_scribe bound to <your repo>#<branch>` with no trailing
  subdirectory — the repo is the one holding `context/` and `cadence/`, and the GitHub grant can
  push to it. A trailing `in infra/` is the failure to catch here: it roots the harness where there
  is no node_modules, so the collector cannot run
- exactly one `defineContext` in the project, resolving to the repo's root `context/`
- `scripts/call-capture/package.json` is present in the project after the install

## What you can change

The code is a worked example. These reshapes are expected, and the agent offers them rather than
waiting to be asked. Every one costs something; that is what makes it a variation and not the
default.

| Variation           | When it is right                                                                                          | How                                                                                                                                                                                    | What it costs                                                                                                                                                                                                                     |
| ------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `notes-not-transcripts` | The repo is growing faster than you want, or your recorder's AI notes are genuinely good                | Reorder the fallback in `collect/calls.ts` so notes are fetched first and the transcript is the fallback                                                                                | You lose the verbatim record, so the scribe can no longer quote and nobody can check a summary against what was actually said. Notes are already an interpretation; scribing them is interpreting an interpretation                 |
| `raise-the-bar`     | Your context is filling with claims that turn out to be one customer's opinion                            | Raise the repetition bar in `infra/agents/call-scribe.prompt.ts` from two independent occurrences to three, and require them to come from different accounts                                               | The knowledge layer lags the field by weeks. A real, fast-moving objection sits unwritten while it is costing you deals                                                                                                            |
| `widen-the-cap`     | The backfill queue is not draining — the pull request reports a remainder that never falls                | Raise the per-run cap in `infra/agents/call-scribe.prompt.ts`, or leave it and let the daily runs grind through the queue                                                                                  | The pull request stops being reviewable, which is the whole control. A diff nobody reads is an auto-merge with extra steps                                                                                                         |
| `internal-calls-too` | You want deal reviews, onboardings and retros in the record as well as customer calls                    | Drop the external-attendee filter in `collect/calls.ts` and file internal captures under their own folder                                                                               | Volume roughly doubles and the signal thins: internal calls restate what customers said, so the repetition bar counts the same occurrence twice and promotes it as if two customers had said it                                     |
| `two-recorders`     | You are mid-migration between recorders, or sales records on one and CS on another                        | Run the collector once per recorder in step 1 of `infra/agents/call-scribe.prompt.ts`: `--recorder=<a>` then `--recorder=<b>`. Both write into the same archive under their own `source:` prefix | Deduplication is per-recorder, because the ids are. A call both tools recorded is captured twice and scribed as two entries, and the repetition bar then counts one conversation as two occurrences and promotes it as if two customers had said it |

## What should not change

However far you adapt, these hold. Ask for one anyway and the agent tells you what breaks, then does
it if you still want it, and records why under `## Decisions` in your copy of this file.

- **The agent does not fetch calls; the script does.** (`scripts/collect/calls.ts`) A fetch
  loop an agent re-derives every morning is a fetch loop that silently changes shape — a window that
  drifts, a filter that quietly widens, a field read differently on a day the model was less careful.
  The raw archive is the one thing here that has to be byte-identical in its rules every day, because
  everything downstream is diffed against it.
- **`Recorder.provider` stays one field, and the registry key equals it.**
  (`scripts/collect/recorder.ts`, `scripts/collect/recorders/index.ts`) It is written into every
  `source:` line and compiled into the regex that reads those lines back. Split it into two
  literals, or file an adapter under a key that disagrees with its own `provider`, and the day they
  drift the collector stops recognising what it has already captured and re-captures the whole
  window every morning — producing files, never erroring, until someone notices the repository
  doubling in size. `resolve()` refuses the mismatch and `evals/contract.mjs` fails on it; leave
  both in place.
- **A recorder swap is a selection, and a new recorder is a new adapter — never an edit to the
  pipeline.** (`scripts/collect/recorder.ts`) Deduplication, slugging, the internal-domain filter,
  the file format and the window are the same whoever records your calls. Move one of them into an
  adapter to make a vendor fit and the next adapter has to reimplement it, which is how two
  recorders start writing subtly different frontmatter and the dedup stops seeing half the archive.
  That includes the internal/external flags four of the recorders offer: they disagree with each
  other, and one of them is wrong in some workspaces, so every adapter passes attendees through and
  one domain rule decides.
- **`written: "live"` is a claim someone made with evidence.**
  (`scripts/collect/recorders/index.ts`) It means an adapter was run against a real workspace, and
  the collector prints a warning on every run of one that was not. Flip it to silence the warning
  and the registry starts implying that nine recorders are tested when one is — which is exactly
  how a convenience becomes a promise nobody checked, on a pipeline whose failure mode is a clean
  empty run.
- **Choices stay in code, the secret stays in the workspace, and the agent declares no `env`.**
  (`scripts/collect/config.ts`, `infra/agents/call-scribe.ts`) The recorder and the internal domain
  are typed constants, so the compiler checks the slug, a reviewer reads both in the diff, and an
  edit lands on the next clone rather than the next deploy. The credential is the mirror image: a
  workspace environment variable read server-side on every run, so it outlives the shell that set
  it and rotates without a deploy. Move a choice into the spec and nothing checks it; move the key
  there as a `secret()` and the next deploy is blocked on whoever runs it having the value
  exported, which on an unattended 07:00 pipeline is discovered as a morning with no pull request.
- **`scripts/call-capture/package.json` stays.** (`scripts/package.json`) It is not
  decoration. The loader imports only the resources folder `cargo.json` names, but in a project whose
  `cargo.json` names its root it imports every `.ts` there except directories carrying a
  `package.json`; delete it and `cargo-ai project plan` imports the collector and runs it against the live
  API on every plan.
- **The harness root stays the directory holding the `package.json` that declares `@cargo-ai/cdk`.**
  (`infra/agents/call-scribe.ts`) That is where `node_modules` is, so it is the only place
  `npx tsx …/collect/calls.ts` resolves — and in the scaffolded layout it is the repository root,
  which is also where `cadence/` and `context/` live. The harness clones the project's connected
  state at that state's directory, so nothing declares it here; what must not change is the
  outcome: the state is connected at the directory holding that `package.json`. **Check it, do
  not assume it:** `cargo-ai project check` prints the binding. A state connected at a
  subdirectory with no package.json leaves the collector unable to run, and the morning reports
  clean and empty; an unconnected state deploys the agent unbound, with nothing cloned.
- **The agent opens a pull request and never merges it.** (`infra/agents/call-scribe.prompt.ts`) Everything
  downstream reads `context/` as fact. Remove the review gate and a hallucinated objection, a misheard
  number, or a vendor call misread as pipeline becomes what your scorer, your researcher and your SDR
  all believe — and nothing will ever contradict it, because they read the same file.
- **One entry per call, keyed on the provider uuid, and raw captures are never touched.**
  (`infra/agents/call-scribe.prompt.ts`) The uuid in each file's `source:` line is the only idempotency key
  in this system. Let the agent rewrite entries "to improve them" and the run stops being idempotent:
  a re-run re-litigates history, the diff is unreviewable, and the earlier occurrence the repetition
  bar counted changes underneath it.
- **A claim reaches `context/` only on its second independent occurrence.**
  (`infra/agents/call-scribe.prompt.ts`) Drop the bar and the knowledge layer fills with singletons at the
  same confidence as durable truths. The failure is not noise, it is that nobody can tell which is
  which any more, and the layer stops being trusted at exactly the moment it is big enough to matter.
- **The collector's window overlaps the previous run.** (`scripts/collect/calls.ts`)
  Transcripts are not ready when a call ends. A one-day window silently drops every call the recorder
  was still processing at the cron minute, and because the window only moves forward, those calls are
  never seen again. The overlap is free: uuids already on disk are skipped before any transcript is
  fetched.

## Done when

- `--dry-run` listed the calls it would take, and the run without it wrote those files into
  `cadence/log/raw/calls/` with a `source:` id in each; running it twice wrote nothing the second time
- `RECORDER` in `config.ts` is the recorder the team records on, and the captured `source:` lines
  carry that slug
- `cargo-ai workspaceManagement envVar list` shows `CALL_RECORDER_API_KEY` as a secret entry, and
  `grep -r CALL_RECORDER_API_KEY` finds its name in the collector and the docs and its value
  nowhere — the deployed run reads the catalog, so no local shell has to hold the key again
- on an adapter marked `docs` rather than `live`: `--dry-run` listed real calls with the right dates
  and account slugs through it, and one captured file was opened and read — that is what moves it to
  `live`, and until someone does it a clean run proves nothing
- on a recorder that does not ship: the new adapter compiles (a half-written one does not typecheck,
  and the error names the missing field), it is registered under a key equal to its own `provider`,
  `--dry-run` lists real calls through it, and nothing in `scripts/collect/recorder.ts` had to
  change to make it fit
- `cargo-ai project plan` reports three resources and does **not** hit the recorder's API while planning
- the first scheduled run opened one pull request whose body reports four numbers: captured, scribed
  fresh, scribed from backfill, and pending remaining
- every scribed call has exactly one entry under `cadence/log/calls/`, and no raw file was edited,
  moved or deleted
- at least one `context/` file in the diff cites two different calls as its occurrences, and no file
  in the diff cites only one
- a call where your company was the buyer, not the seller, is filed as vendor intel and appears
  nowhere as pipeline
- after merging and `cargo-ai project deploy`, the changed `context/` file is readable from the workspace
  context repository, and an agent with the `context` capability quotes it back

## What it costs

There are no connector actions in this skill, so it consumes no per-record credits: the collector
talks to your recorder directly from the harness environment, under whatever API limits your
recording plan already gives you. Those limits differ enough between recorders to be worth checking
once — a daily three-day window is nothing against Grain's per-minute allowance and is real against
Fireflies' Free tier of a few dozen requests a **day**, and `references/recorder-apis.md` records
each. The collector paces itself and backs off on a 429 regardless, so the failure is a slow run
rather than a half-captured one.

The recurring cost is the harness run itself, once a day, and it scales with how much the agent
reads — which is the raw captures it scribes. **The per-run cap is the cost control as well as the
review control.** A lower cap spreads the same backlog over more days at the same daily cost rather
than paying for it all at once, and the pending remainder in the pull request body is how you watch
whether it is keeping up.

## Composes into

`account-scoring` and any agent with the `context` capability (they read the ICP and objection files
this keeps current), `standup` (yesterday's scribed calls are evidence the recap reads),
`website-building` (the pages speak in the customer language and the objections the calls surface),
`web-capture` (it adds the website, competitors and news to the context the calls started),
`monitor-buying-signals` (the signals this promotes are what a feed then watches for).
