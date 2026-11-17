# Acceptance

Walk every line. A checked template without an evidence-backed consumer adaptation is incomplete.

## Before deploy

- `RECORDER` in `scripts/collect/config.ts` names the recorder the team actually records on.
  `npm run typecheck` proves the slug is one the registry holds; nothing proves it is the right
  one, so it was confirmed out loud with whoever answered. A recorder that does not ship has a new
  adapter under `collect/recorders/`, registered under a key equal to its own `provider`.
- Neither choice is an environment variable on the agent, and the agent declares no `env` at all:
  a choice in a deployed spec is one no compiler checks, and changing it needs a redeploy where an
  edit to `config.ts` reaches the next run as soon as it merges.
- The collector was run by hand once (`CALL_RECORDER_API_KEY=… npx tsx
  scripts/call-capture/collect/calls.ts`) and wrote real raw files into
  `cadence/log/raw/calls/`, each carrying a `source:` line naming that recorder and a uuid.
- Running it a second time wrote nothing. If it re-captured the same calls, the dedup key and the
  `source:` line have drifted apart and every run will duplicate the window.
- The transcript response shape was checked against the live API, not assumed. A wrong field name
  here produces a clean, empty run every morning rather than an error. Eight of the nine adapters
  were written from vendor documentation and print a warning saying so on every run: on one of
  those, this check is the whole acceptance test, and passing it is what earns `written: "live"`.
- `--dry-run` listed calls whose dates, subjects and account slugs are recognisably real. An
  adapter reading the wrong timestamp field files everything under one day; one reading no
  attendees files everything as internal and captures nothing at all.
- `INTERNAL_DOMAIN` in `scripts/collect/config.ts` is the company's real domain, and an internal-only call in the
  window was **not** captured.
- `scripts/call-capture/package.json` exists in the project, and `cargo-ai project plan` did not
  hit the recorder's API while planning. If it did, that file is missing and the loader is importing
  the collector.
- Exactly one `defineContext` exists in the project, resolving to the `context/` directory at the
  repository root.
- `cargo-ai project check` prints `agent:call_scribe bound to <repo>#<branch>` with no trailing
  subdirectory. The repo is the one holding `context/` and `cadence/`, and the grant can push to it.
  A trailing `in infra/` means the harness was rooted at the resources folder rather than at the
  package.json that declares `@cargo-ai/cdk`: that directory has no node_modules, so `npx tsx`
  cannot run the collector at all.
- `CALL_RECORDER_API_KEY` is a workspace environment variable —
  `cargo-ai workspaceManagement envVar list` shows it, marked secret — and its value appears in no
  committed file and in no `secret()` call. A key that only ever lived in the deploying shell is not
  deployed: it is one machine away from a morning with no pull request, and a rotation would need a
  re-apply to land.
- The cadence paths in the system prompt match what `cadence/README.md` describes, or the new folders
  are introduced deliberately and that README is updated to name them.

## First scheduled run

- Exactly one pull request, unmerged, titled `[call-capture] scribe <date>`.
- Its body reports four numbers: captured, scribed fresh, scribed from backfill, pending remaining.
- Every scribed call has exactly one entry under `cadence/log/calls/`, each carrying the recorder's
  uuid in frontmatter.
- No raw capture was edited, moved or deleted.
- Re-running the agent the same day opens no duplicate entry for any call already scribed.
- No entry invents an attendee, a quote or a figure absent from the transcript. Spot-check two
  entries against their recordings; this is the check nothing automated can do for you.
- A call where the company was the buyer rather than the seller is filed as vendor intel and appears
  nowhere as pipeline or expansion.

## The context diff

- Every `context/` file in the diff cites two or more independent occurrences, by log path.
- No file in the diff cites only one occurrence.
- Changes prefer updating an existing file over creating a near-duplicate; a new file restating an
  existing one under a different name is a failure of the domain lookup, not of the bar.
- Every new or changed file carries the frontmatter `context/README.md` requires, and the
  repository's context lint passes.
- Nothing under `plan/` or `infra/` is touched.

## After merge

- `cargo-ai project deploy` syncs the changed `context/` files into the workspace context repository.
- An agent with the `context` capability quotes the changed file back when asked about its subject.

## Over the first two weeks

- The pending remainder in the pull request body falls run over run. A flat or rising remainder means
  the cap is too low, or a class of call is failing to parse and being silently reselected every
  morning — check the same uuids are not reappearing.
- The raw archive grows by roughly the number of external calls actually held. A day with calls and
  no captures means the readiness flags or the window are wrong.
- At least one claim was promoted into `context/` on its second occurrence, and at least one stayed
  in a log entry because it only ever occurred once. If everything is being promoted, the bar is not
  being applied.
