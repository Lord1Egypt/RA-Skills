---
name: founder-signal
version: "0.2.14"
description: >
  Founder Signal turns verified Reddit and V2EX evidence into a small, reviewable signal package
  for founders evaluating product demand and positioning across one or more configured
  product profiles.
  Use this skill when the user wants founder research from Reddit or V2EX evidence, a scored
  review artifact, or a Draft page generated from any run outcome.
  This skill depends on the canonical draft-cli skill. Draft is the default founder
  review surface, so Founder Signal emits a Draft-ready public publish intent for every
  run, regardless of success or failure. Every run should be published through the downstream
  draft-cli skill with `draft page create -> draft page append -> draft page publish`
  so the run returns a human-reviewable Draft public page URL without asking for
  another approval; later public web publication outside that Draft page requires
  explicit confirmation.
metadata:
  clawdis:
    author: innosage-llc
    emoji: "📡"
    dependencies:
      - name: "toliuweijing/draft-cli"
        type: "other"
        url: "https://clawhub.ai/toliuweijing/draft-cli"
    requires:
      bins:
        - "bash"
        - "python3"
        - "draft"
    install:
      - id: "npm"
        kind: "node"
        package: "@innosage/draft-cli"
        bins:
          - "draft"
        label: "Install draft-cli (npm)"
---

# Founder Signal OpenClaw Skill

Use this skill to turn verified Reddit and V2EX evidence into a small, reviewable signal package
for founders evaluating product demand and positioning across one or more configured
product profiles.

## Founder Signal Invariant

No saved verified snapshot means no scoring, but it does not skip the public run review.

Every run must persist a run folder before later steps execute so failures still leave
traceable artifacts. The skill should only score verified evidence and should only
generate an Action Card after verified candidate evidence exists. Every profile run,
regardless of success, no-candidate result, partial completion, or runtime failure, must
write `public-run-review.md`, write `draft-publish-intent.json`, and automatically
attempt Draft page create -> append -> publish for that public-safe review. A failed
business run may still yield a successful Draft review page. If Draft publication
fails, preserve the local review artifact and explicit publish-failure metadata so the
publication is retryable. Public web publication outside that Draft page requires
explicit founder confirmation.

## Setup Contract

After installation, ask the founder for one canonical Founder Signal JSON config,
validate it, then import it into an internal runtime profile. Do not ask the founder
to hand-edit package-local `profiles/*.json` unless they explicitly want to debug the
skill source. The installed ClawHub skill directory is source code; mutable runtime
data belongs under `${FOUNDER_SIGNAL_HOME:-~/.founder-signal}` unless `--root-dir` is
passed explicitly.

Recommended flow:

1. Share or fill `founder-signal.config.example.json`.
2. Initialize the runtime home:

```bash
python3 -m founder_signal init
```

3. Validate it:

```bash
python3 -m founder_signal doctor --config founder-signal.config.json
```

4. Import it:

```bash
python3 -m founder_signal config import founder-signal.config.json
```

5. Run it:

```bash
python3 -m founder_signal run --config founder-signal.config.json
```

The shell shortcut is also valid:

```bash
bash scripts/run_founder_signal_once.sh --config founder-signal.config.json
```

Canonical config requirements:

- `profile_id`
- `product_name`
- `product_one_liner`
- `target_audience`
- `keywords`
- `scoring_terms`
- `platforms`
- `discovery_mode`
- `max_candidates`
- `draft.require_confirmation_before_public_publish: true`

Reject legacy user-facing fields such as `subreddits`, `seed_reddit_urls`,
`excluded_reddit_urls`, or any `draft_publish_command` escape hatch in canonical setup
JSON. The import step writes an internal runtime profile under
`<runtime-home>/profiles/` plus a normalized canonical copy under
`<runtime-home>/config-imports/`.

## Inputs

- one canonical Founder Signal config JSON during setup
- one or more active imported product profiles from `<runtime-home>/profiles/*.json`
- optional `--profile <profile_id>` selection for single-profile runs
- platform configuration from the canonical `platforms` object or existing internal legacy profiles
- deterministic Reddit/Eddrit research discovery from profile communities,
  `keywords`, and scoring terms; discovery always runs before configured Reddit hints
- optional Reddit `discovery_mode: live` using subreddit new feeds with age/comment
  filtering and product-term matching
- V2EX discovery through SOV2EX, search, node latest pages, or configured seed topics; third-party discovery is candidate-finding only
- optional platform `excluded_urls` or legacy `excluded_reddit_urls` to suppress known old candidates
- `history_ttl_days` to expire old private repeat-candidate exclusions
- optional `verified_evidence_snapshots` when a Claw/browser agent has verified a source post but automated fetch is blocked

## Draft Publish Handoff

Founder Signal depends on the canonical `draft-cli` skill for Draft public-page
publication. Draft handoff preparation is on by default for every run: Founder Signal
writes `public-run-review.md`, writes `draft-publish-intent.json` next to it, and does
not hardcode custom or local shell publish commands. The intent contains the artifact
path, title, profile, Draft visibility request, and
`requires_confirmation: false` and `draft_public_publish_requires_confirmation: false`
for the `draft page create -> draft page append -> draft page publish` sequence. It
also contains `external_public_publish_requires_confirmation: true` for any later
public web publication outside the Draft page.

When any test run or scheduled run writes this intent, the agent must
immediately use the `draft` CLI supplied by the required `draft-cli` skill installed in
the agent workspace to run `draft page create`, `draft page append`, and
`draft page publish` for `public-run-review.md`, then report the resulting
human-reviewable Draft public page URL. Do not ask the founder for another approval
before this Draft page step. Ask for explicit confirmation only before running a
separate public web publish action outside that Draft page.

The `draft-cli` skill is the source of truth for daemon readiness, page creation,
append/patch behavior, public publishing, invite codes, and Draft URL extraction.

## E2E Verification Playbook

When the founder asks for an end-to-end verification run, the agent must deliver a
Draft public page URL or clearly report E2E incomplete.

1. Enable the target profiles.
2. Use the built-in discovery phase. Do not start from placeholder URLs.
3. Try the normal Eddrit search/listing and post mirror paths first.
4. If the mirror is blocked, use browser/manual verification and add
   `verified_evidence_snapshots` to the profile:

```json
{
  "platform": "reddit",
  "source_url": "https://www.reddit.com/r/ChatGPT/comments/abc123/real_slug/",
  "verification_method": "agent_browser",
  "verified_by": "openclaw-agent",
  "text_snapshot": "Copy the relevant source post text observed by the agent here."
}
```

The snapshot must be real source text from the source post, not invented content.
Placeholder URLs such as `POST_ID`, `REAL_ID`, `SUB`, `/slug/`, or V2EX placeholder topic IDs are invalid and must
not be used. Founder Signal treats `verified_read_via_agent_browser` and
`verified_read_via_manual_snapshot` as verified reads only after the snapshot is
persisted.

Run E2E checks with:

```bash
python3 -m founder_signal run --config founder-signal.config.json --require-action-card --require-publish-intent
```

When the run creates `draft-publish-intent.json`, inspect its `requires_confirmation`
field. If it is `false`, immediately invoke the `draft` CLI from the installed
`draft-cli` skill in the agent workspace to run `draft page create`, `draft page
append`, and `draft page publish` for `public-run-review.md`, then return the resulting
human-reviewable Draft public page URL to the founder. Reporting only that
`draft-publish-intent.json` exists is incomplete. If a later action would make the
page publicly reachable outside that Draft page, inspect
`external_public_publish_requires_confirmation` and ask for explicit approval before that
separate public web publish action.

## Outputs

- `runs/<RUN_ID>/run.json`
- `runs/<RUN_ID>/REPORT.md`
- `runs/<RUN_ID>/profiles/<profile_id>/run.json`
- `runs/<RUN_ID>/profiles/<profile_id>/REPORT.md`
- `runs/<RUN_ID>/profiles/<profile_id>/public-run-review.md` for every profile run,
  regardless of success or failure
- `runs/<RUN_ID>/profiles/<profile_id>/evidence/`
- `runs/<RUN_ID>/profiles/<profile_id>/outputs/candidates.json`
- `runs/<RUN_ID>/profiles/<profile_id>/selected-candidate.json` when a verified
  candidate is selected
- `runs/<RUN_ID>/profiles/<profile_id>/daily-review.md` when an Action Card is generated
- `runs/<RUN_ID>/profiles/<profile_id>/draft-publish-intent.json` for every profile
  run when Draft public-page publishing is prepared for automatic downstream
  `draft-cli` handling
- `state/past-candidates.json` as private local candidate history used to avoid repeat
  candidates in future runs

These output paths are relative to the runtime home, not the installed skill package.
The runtime home defaults to `${FOUNDER_SIGNAL_HOME:-~/.founder-signal}`.

Action Cards use `Source platform` and `Source URL` labels and must not expose private local evidence paths in Draft-bound Markdown.
High-quality structured evidence should improve Action Card quality, not decide whether
the card exists. If a selected candidate is verified, eligible, not agent-rejected, and
has a readable saved text snapshot, generate `daily-review.md` even when structured
evidence is missing or low quality. In that fallback mode, render from the raw snapshot
and record `action_card_generation_mode: snapshot_fallback`; structured cards record
`action_card_generation_mode: structured`.
## Manual Execution

```bash
python3 -m founder_signal doctor --config founder-signal.config.json
python3 -m founder_signal config import founder-signal.config.json
python3 -m founder_signal run --config founder-signal.config.json
bash scripts/run_founder_signal_once.sh
bash scripts/run_founder_signal_once.sh --profile draft
bash scripts/run_founder_signal_once.sh --config founder-signal.config.json --require-action-card --require-publish-intent
```

Without `--profile`, the runner processes all enabled profiles.

## Bundled Runtime Payload

This published skill package includes the minimum local runtime payload needed to run
from the installed skill directory:

- `scripts/run_founder_signal_once.sh`
- `src/founder_signal/`
- `founder-signal.config.example.json`
- `profiles/README.md`
- `profiles/draft.example.json`

Before a real run, create one canonical config JSON, validate it, and import it. No
Draft publish settings file is required; Draft public-page publication is part of the
default flow and every run should be published to Draft automatically until a
human-reviewable Draft public page URL exists or an explicit publish failure is
recorded. Public web publication outside that Draft page remains confirmation-gated.

## Runtime Order

1. Persist the run folder early, then load either all enabled profiles or one selected profile.
2. For each profile, run enabled platform adapters, skipping profile exclusions and previous local candidate history before capping, then consider configured hints and verified snapshot fallbacks.
3. Catch and record business-run failures with public-safe failure fields instead of returning before finalization.
4. Save evidence from mirror or verified snapshot fallback when available, enforce the verified-read
   gate, score only verified candidates, and optionally generate an Action Card.
5. Always write `public-run-review.md` and `draft-publish-intent.json`.
6. Always attempt automatic `draft page create -> draft page append -> draft page publish` for the public run review.
7. Persist final artifacts with business failure and Draft publish failure represented separately, with explicit confirmation before any later public web publish outside that Draft page.

Eddrit search/listing and post mirror pages are the Reddit read layer. V2EX discovery providers are never the verified evidence source; verified V2EX reads use the original `https://www.v2ex.com/t/<topic_id>` topic URL or future official API reads. Browser/manual fallback remains a verified snapshot path when automated reads are blocked.
