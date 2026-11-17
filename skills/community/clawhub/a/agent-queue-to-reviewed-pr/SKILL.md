---
name: agent-queue-to-reviewed-pr
description: Turn a ticket queue into reviewed draft PRs with an agent that never merges. Use when wiring an agent to a ticket board or issue tracker. Trigger on "auto PR agent", "agent queue".
metadata: {"clawdbot":{"emoji":"🔁","requires":{"bins":["git","gh","curl","python3"]},"homepage":"https://clawhub.ai/@AlexBloch-IA"}}
---

# Agent Queue → Reviewed PR

**The agent proposes, a human validates. Every link in the loop must have a consumer — an unconsumed state is a ticket stuck forever.**

## Access, data and network — read before wiring anything

**Default is inert: no variable set → no outbound call.** Every network destination is opt-in and listed here — there are no others.

| Thing | What it is | Default |
|---|---|---|
| `${AGENT_API_TOKEN}` | Bearer for all four endpoints below. Keep it in a file outside git, never in the workspace, never in a notification. | Unset → this skill is inert, no call leaves the machine |
| `${QUEUE_URL}` | **Outbound read** to your work source. Ticket ids, titles and briefs cross the network. | Unset → inert |
| `${ACK_URL}` | **Outbound write**: ticket id + PR URL. | Unset → inert |
| `${GROUNDING_ACK_URL}` | **Outbound write**: the full brief (10k–16k chars) leaves the machine. | Unset → the grounding link is inert |
| `${STALE_ACK_URL}` | **Outbound write**: ticket id + reason + commit sha. | Unset → the drift watcher is inert |
| Git forge token | Fine-grained PAT, **`contents:write` + `pull_requests:write` on one repo**, no Administration, no Workflows. | Must be provisioned by a human |
| `${NOTIFY_CHANNEL}` | Chat/webhook for run summaries. Summaries **leave the machine**. | Optional; omit for local-only logs |
| Browser profile (QA step only) | A browser profile logged into a **dedicated test account on a preview environment** — never a personal profile, never a production account. It carries real session cookies. If a CAPTCHA, bot check or rate limit appears, the run **stops and hands over to a human**; behavior is never adapted to get past a defense. | Opt-in. Skip the QA link entirely and the rest still works |
| Persisted on disk | Indexes `memory/pr-index.json`, `memory/qa-index.json`, `memory/remediation-index.json`. QA screenshots under `work/qa-runs/PR-<n>/`. Plus the journal `memory/YYYY-MM-DD.md`. | Local only. Retention is **executed by `scripts/retention.py`** (§Retention), not just declared: the three indexes are purged when the PR closes, screenshots deleted at close and capped at 7 days. The journal is **deliberately out of retention scope** — it is the audit trail, and holds only ids and PR URLs, never personal data (§Retention) |

**Data minimization is a default, not your problem to solve.** A brief cites code, never people: never copy a requester's name, email address, or any other personal identifier into a brief, a payload, a PR description, or a screenshot. Honor your forge's and hosting provider's ToS, and the law that applies to you (GDPR where applicable). Never point the QA link at a production tenant.

## When to Use

| User says | Action |
|---|---|
| "make an agent that opens PRs from our board / Linear / Jira" | Build the whole loop below, starting at §Contract — not at the PR. |
| "the agent opened the same PR twice" | §Anti-duplicate — usually the server ack is missing. |
| "the agent's PRs are garbage / off-scope" | §Grounding. The brief is the product. |
| "our QA bot labels PRs and nothing happens" | A state with no consumer. `references/browser-qa.md`. |
| "the agent coded against files that no longer exist" | §Brief staleness. |
| "should the agent merge if CI is green?" | No. Never. See the coda. |

## The closed loop

```
  human triage (prioritize)          ← the cheapest guardrail there is
        │
        ▼
  [GROUND] raw request ──read-only code──▶ anchored brief ──▶ grounding-ack
        │
        ▼
  [RUN] queue ──▶ head of queue only ──▶ worktree ──▶ implement ──▶ blocking QA ──▶ draft PR ──▶ ack
        │                                                                                        │
        ▼                                                                                        ▼
  [STEWARD] merge integration branch in, map inter-PR conflicts        [QA] browser-test the preview → verdict + label
        │                                                                                        │
        ▼                                                                                        ▼
  [DRIFT] audit briefs still in queue ──STALE──▶ back to GROUND        [REMEDIATE] consume needs-work → fix on PR branch → back to QA
```

Read the arrows as *consumers*: `stale-ack` → grounding, `needs-work` → remediation. Ship a link whose output nobody reads and you have built the graveyard.

## Contract — queue and ack

Design the HTTP surface first; the agent is the easy part. Full spec + typed errors: `references/queue-contract.md`.

```bash
curl -fsS --max-time 30 "${QUEUE_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}"
# Output: {"ok":true,"count":2,"arrangementUpdatedAt":"2026-07-16T09:00:00.000Z","tickets":[
#   {"id":"tkt-401","title":"…","prompt":"…","status":"ready","column":"P0","globalOrder":0}, … ]}
```

| Rule | Why it is non-negotiable |
|---|---|
| `globalOrder` is a **total order** computed server-side (P0→P3, then array position) | The board is the single source of order. The agent never re-sorts, never skips. |
| `GET` is read-only and safe to poll | Preflights can poll a cheap `count` every 10-15 min with no LLM involved |
| Ack is **conditional + idempotent**: `ready → pr-opened` only if still `ready` | Two overlapping runs cannot both consume the ticket. Repeat calls return `{ok:true,idempotent:true}`. |
| `401` on a **timing-safe** comparison (`crypto.timingSafeEqual`) | A naive `===` on a shared secret leaks its length/prefix under repeated probing |
| Unknown id → `404 unknown_card`, never a silent `200` | A lying ack is worse than a failing one |

**"Ready" = status AND prioritized column.** Both, or the ticket is invisible: a card sitting in `INBOX` is invisible to the agent **whatever its status**, and a human dragging it to `P0..P3` *is* the explicit authorization to spend agent time. That drag is the **human triage gate** — the cheapest guardrail in the system. Empty or missing arrangement → empty queue → the agent does nothing. Fail-safe, not fail-open.

## The executable grounding gate

Never implement a raw request. Ground it: read the real code read-only, verify **every** anchor (path, line, helper, convention) **before** writing it down, and emit a brief so self-contained that another agent can implement it without ever reading the original request. Method + payload template: `references/grounding-brief.md`. Checks run in one canonical order — the same in the script, in the server, and in the table below; any other order and the two sides are not mirrors.

| # | Gate | Threshold | Enforced |
|---|---|---|---|
| 1 | Mandated first line | exactly `Read CLAUDE.md AND AGENTS.md at the root of ${TARGET_REPO} first`, with your repo name substituted | client + server (`startsWith`) |
| 2 | Brief length | **≥ 3000 chars**, target **10k–16k** | client + server |
| 3 | `technical` non-empty | verified paths + line ranges + helpers to reuse | client + server |
| 4 | `definition` non-empty | acceptance criteria + explicit out-of-scope | client + server |
| — | Unverifiable anchor | **no ack** — the card stays in the grounding queue, alert a human | agent rule |

**Duplicate the gate on purpose.** Locally you fail *before* the network call; server-side because your endpoint must never depend on the politeness of its client — a retry script or a hand-written curl will send garbage eventually. **Configure the prefix first.** `${TARGET_REPO}` is a placeholder: export `BRIEF_GATE_PREFIX` with your repo name substituted, byte-identical to the string your server checks. The script refuses to run on a placeholder — **or on an empty value**, since `startswith("")` matches every prompt and would report a disabled gate as a passed one.

```bash
export BRIEF_GATE_PREFIX="Read CLAUDE.md AND AGENTS.md at the root of app-example first"
python3 scripts/brief-gate.py tkt-401 payload.json prompt.txt > body.json
# Output (rejected, exit 1): brief-gate: prompt too short (1180 < 3000 chars). Flesh out the brief: target 10000-16000 -- NOTHING was sent.
# Output (accepted, exit 0): stdout → body.json = {"card_id":…,"payload":{…},"prompt":"…"}
#   plus, on stderr, if the brief is under the 10k target: "brief-gate: note - prompt is 4061 chars,
#   outside the 10000-16000 target (gate still green)". Judge the exit code, never the silence.
curl -fsS -X POST "${GROUNDING_ACK_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}" \
  -H "Content-Type: application/json" -d @body.json
# Output: {"ok":true,"status":"ready"}
# Output (server mirror rejects): 400 {"ok":false,"error":"grounding_too_thin"}
#   Same predicate, both sides, or it is not a gate.
```

## The run, step by step

1. **Fetch.** `count == 0` → answer `QUEUE_EMPTY`, stop. HTTP/auth error → STOP + alert, touch nothing.
2. **Select `globalOrder == 0` only.** One ticket per run. No batch, no parallel, no skipping.
3. **Anti-duplicate before any work** (§below).
4. **Deterministic branch** = pure function of the ticket: `agent/<id>-<slug>`. Same ticket ⇒ same branch, forever. This is what makes step 3 possible.
5. **Clean worktree from the up-to-date integration branch** (`git fetch origin` then branch off `origin/<integration-branch>`) — never from a stale local state. Gotcha: if `node_modules` is a symlink in the worktree, bundlers fail with an unrelated error → `rm node_modules && <install command>` inside the worktree.
6. **Read the target repo's conventions BEFORE implementing**: `CLAUDE.md` + `AGENTS.md` at its root. They outrank your habits.
7. **Implement strictly per the brief.** No opportunistic refactor. Ambiguity or a red line in play → STOP + ask. Do not guess.
8. **Blocking QA before any commit**: `<lint>` → `<type-check>` → `<test>` → `<build>`. One red = **no PR, no ack**.
9. **One draft PR per run.**
10. **Ack, then bookkeeping**: `memory/pr-index.json`, journal line, remove the worktree.

```bash
git config user.email          # Output: agent@example.com  ← must match the authenticated forge account
gh pr create --repo acme-corp/app-example --base <integration-branch> \
  --head "agent/${id}-${slug}" --draft --fill --label agent
# Output: https://github.com/acme-corp/app-example/pull/42
curl -fsS -X POST "${ACK_URL}" -H "Authorization: Bearer ${AGENT_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys;print(json.dumps({"card_id":sys.argv[1],"pr_url":sys.argv[2]}))' "$id" "$pr_url")"
# Output: {"ok":true,"status":"pr-opened","pr_url":"https://github.com/acme-corp/app-example/pull/42"}
# Build the body with python3, never by string-concatenating a title into JSON.
```

**Git identity gotcha, root cause:** a commit authored with a local email (`*@Mac-*.local`) is not linked to any forge account, so preview hosts refuse to build the PR ("No account was found matching the commit author email address"). The build never fails — it simply never happens, and the browser-QA link starves with no error to read. Check `git config user.email` **before** the first commit of every run.

## Anti-duplicate — 4 locks, in order of strength

| # | Lock | Strength | Survives |
|---|---|---|---|
| 1 | **Server conditional ack** — `ready → pr-opened` only if still `ready`; next poll no longer lists it | **Strongest** — makes duplicates *impossible* | a crashed run, a cloned workspace, a wiped disk, two agents racing |
| 2 | One ticket/run (`globalOrder=0`) | Serializes work; the next run picks up the new head | a crash (state is server-side) |
| 3 | Local index `memory/pr-index.json`, keyed by ticket id — entry: `{"tkt-401":{"number":42,"pr_url":"…/pull/42","branch":"agent/tkt-401-invoice-filter","ts":"…"}}` | Fast, but the truth lives on a disk you might lose — never trust it alone | nothing: a fresh machine forgets everything |
| 4 | `gh pr list --head agent/<id>-<slug> --state all` before any create | Catches what the index forgot | a wiped disk (queries shared state) |

**Negative proof, at the permission layer:** provision the PAT with `contents:write` + `pull_requests:write` and nothing else. Then `gh pr merge` fails with a permission error and `git push origin <release-branch>` is refused by branch protection. The agent doesn't merge because it **cannot** merge — not because it was asked nicely. Verify this before going autonomous: run `gh pr merge` once and confirm it fails.

## The decision tree

| Situation | Action |
|---|---|
| Queue KO / bad Bearer | STOP + alert. No PR, no ack, no work. |
| `count = 0` | `QUEUE_EMPTY`, end. Silence is a valid outcome. |
| PR already exists for the ticket | Never recreate. Never reopen a closed one. Ack if it was missed, finish `action=skipped`. |
| Checks red | **No PR AND no ack.** Clean the worktree, alert with a short error excerpt, `tests_ok=false`. |
| Scope doubt / red line | STOP + alert. Do not touch the queue. We do not guess. |

> **GOLDEN RULE — red = no PR AND no ack, the ticket stays in the queue.**
> This one line is what makes the queue **self-healing**: a failed run leaves the world exactly as it found it, the ticket is still head-of-queue, and the next healthy run retries it. No retry logic, no dead-letter queue, no state machine. The design does not depend on the scheduler's retry — it depends on never acknowledging work that didn't happen.

## The queue you do not control

The golden rule is **purchased by the conditional ack** (§Anti-duplicate, lock 1). Take that away and it inverts. Sooner or later the work source is a spreadsheet, a shared board, or someone else's API: no compare-and-swap, no conditional write, no transaction. Everything above still applies except the one line you most rely on.

| You own the endpoint | The store you do not control |
|---|---|
| Claim = `ready → pr-opened` **only if still `ready`**. Two runs cannot both win. | Claim = a plain write. There is no predicate, so the lost race is **undetectable at write time**. |
| A crashed run acked nothing → the ticket is still head-of-queue → **retry is free**. | A crashed run already wrote `in_progress`. Nothing rolls it back. The item is now claimed by a **ghost owner**, forever. |
| Failure is safe by default: do nothing, and the world is unchanged. | Doing nothing **leaks the item**. Silence is not neutral. |

**So the rule flips: failure must be terminal, and explicitly written.** "No ack" stops being self-healing the instant claiming stops being conditional — the row is already marked. Three consequences, none optional:

1. **Confirm the claim by reading it back.** Write your claim (`status=in_progress` **plus a `runId` that is yours**), then re-read the row and compare both fields. A mismatch means another writer won — abandon, do not proceed. This read-back is the only race detection you get; there is no `409` coming.
2. **Write the failure.** Wrap the run so every exit path — crash included — writes a terminal status with a short reason. An unwritten failure is an item claimed by nobody, and it is invisible: the row looks *busy*, not *broken*.
3. **Reclaim orphans by TTL, never by trust.** The claim carries the instant it was taken. An `in_progress` older than your longest possible run is an orphan; reclaim it. Without this, one `kill -9` removes an item from the world permanently and raises no error, ever.

**A local lock does not fix this.** A `mkdir` lock on your own disk serializes *your* runs and says nothing about a second machine, a re-provisioned host, or a human editing the row by hand. The read-back is what protects you; the lock only makes the race **rarer** — which is worse, because rare enough to pass testing is not the same as absent.

> If you can put a conditional write behind the queue, do it. Everything in this section is the tax you pay for not having one.

## Integration steward

| Rule | Reason |
|---|---|
| Integrate by **merge** (`git merge origin/<integration-branch>`), **never rebase, never `--force`** | Rebasing a pushed PR branch rewrites history under an in-flight review and invalidates every QA verdict already keyed to a commit |
| **Inter-PR conflict map**: cross the `files` arrays of every open agent PR; any pair sharing ≥1 file is a potential conflict | Sequence them (oldest/highest priority first), comment "potential conflict with #N on `path` — integrate after", and do not heavily touch the downstream PR this run |
| Conflict too ambiguous → `git merge --abort`, comment, alert | A conservatively resolved conflict is still a human decision |
| Re-run the blocking QA after the merge; red → **do not push the merge** | |
| **`gh pr ready` is forbidden.** Signal readiness (comment + label), stay in draft | Leaving draft is the human's move. That's the whole doctrine in one command. |
| **Every comment the loop posts opens by disclosing it is agent-written** (`> Automated — proposed by an agent, not a human review.`) | The PR is labelled `agent`, but a comment read in isolation isn't. A reader must never mistake a proposal for a human review — and if anyone asks whether this is automated, the answer is yes. |

```bash
gh pr list --repo acme-corp/app-example --label agent --state open \
  --json number,headRefName,headRefOid,files,updatedAt
# Output: [{"number":42,"headRefName":"agent/tkt-401-invoice-filter","headRefOid":"9f2c1ab…","files":[…]}]
```

## Idempotence by headSha

**One verdict per commit. One remediation attempt per commit.** Key every index `<number>@<headSha>`:

| Index | Key | Meaning |
|---|---|---|
| `qa-index.json` | `42@9f2c1ab` | this exact commit already has a QA verdict → don't re-test |
| `remediation-index.json` | `42@9f2c1ab` | this exact commit already got one fix attempt → don't retry, a new commit reopens the right |

A new commit changes `headSha`, so the QA label goes **stale automatically** — no cleanup job, no TTL. **Labels are human signals, NOT the source of idempotence**: `qa-needs-work` present but the current `headSha` absent from `qa-index.json` = stale → QA re-tests, remediation skips. Without this key, QA and remediation fight over the same PR forever, each undoing the other's premise. **Whoever laid down the verdict removes it**: remediation pushes and stays silent on labels; QA re-verdicts the new commit and replaces the label. Every run that examines a PR writes an entry — `pushed` on success, or one of **five** named escalations, the agent's explicit right *not* to improvise (without it, an agent facing a hard bug ships a plausible-looking wide fix). Both: `references/browser-qa.md`.

## Brief staleness is a first-class state

A brief anchored in code that has since moved is a loaded gun pointed at the implementation link. Audit briefs still in the queue against the integration branch, read-only. Full method: `references/brief-staleness.md`.

| Technique | Why not the obvious thing |
|---|---|
| `test -e` on the path, **never grep the path as text** | Route paths contain dynamic segments (`[id]`, `[locale]`) — grep produces false negatives |
| Path mapping before verdict (`lib/x` → also test `src/lib/x`) | Briefs cite import-alias paths, not disk paths |
| Judge only anchors presented as **EXISTING** ("modify", "reuse", "already", "lines X-Y") | A file described as "to create" is not drift when absent |
| Symbol must have a **definition** (`function|const|class|interface|type|enum|export {…}`), not a mention | |
| `git log -S '<symbol>' --all` when absent from current code | Distinguishes "renamed/removed" from "never existed" |
| Verdicts: `FRESH` / `MINOR_DRIFT` / `STALE` | Line drift alone with file+symbol present = `MINOR_DRIFT`, not `STALE` |

**The technique worth stealing — the skeptical refutation pass.** Before any destructive verdict, hand the candidate `STALE` to a *second* agent whose only mission is to prove the first wrong (basename, mapped variants, rename, barrel re-export, `git log --diff-filter=D`, `--follow`, `-S`). Refuted → `MINOR_DRIFT`. **Doubt = never STALE.** A single agent asked to check itself confirms itself; it has already committed to the reasoning.

The drift watcher's only write is a conditional `stale-ack` (`ready → needs-grounding`). Never raw SQL. Never hand-patch a brief — flip the status, let grounding regenerate it. A `pr-opened` ticket is **never** re-grounded (`action: "check_pr"`).

## Retention — declared is not enforced

QA screenshots are authenticated-session data; indexes name PRs forever. A retention nobody runs is a claim, not a control — so run it weekly, from the repo root, on the loop's cron:

```bash
gh pr list --repo acme-corp/app-example --label agent --state all --json number,state > pr-states.json
python3 scripts/retention.py pr-states.json           # dry run: prints the plan, changes nothing
# Output: retention: DRY RUN (3 PRs known) / memory/qa-index.json: 3 -> 1 entries
#         work/qa-runs/PR-42: removing (PR MERGED) / work/qa-runs/PR-99: removing (older than 7 days)
# On stderr, if an entry cannot be expired: retention: WARN memory/pr-index.json: key tkt-401
#   carries no PR number, cannot expire -- add a "number" field to this entry.
python3 scripts/retention.py pr-states.json --apply    # same plan, executed
```

No network call — it consumes the states fetched above. It removes only `PR-<digits>` directories directly under `work/qa-runs/`. The two scopes do **not** have the same rule. **Indexes:** an entry whose PR is absent from the listing, or whose key resolves to no PR number, is **kept** (absence ≠ closure) and WARNed. **Screenshots:** a `PR-<n>` directory goes as soon as its PR is no longer OPEN, and in every case at 7 days — open, closed or unknown alike. Screenshots carry authenticated-session data: 7 days is a hard ceiling, not a fallback, so a PR still in review on day 8 loses its evidence by design. It **refuses to run** from a root holding neither `memory/` nor `work/qa-runs/` (`--root=<path>` for cron), because a purge that silently did nothing is the failure this section exists to prevent. The journal `memory/YYYY-MM-DD.md` is out of scope on purpose — it is the audit trail, holds ids and PR URLs and never personal data, and no code touches it: the enforcement claim is scoped to the three indexes and the screenshots.

**An entry is expirable only if a PR number resolves from it** — hence `number` on every `pr-index` entry (§Anti-duplicate lock 3): that index is keyed by ticket id, so `tkt-401` alone resolves to nothing and the entry would live forever. `qa-index`/`remediation-index` resolve from their `<number>@<sha>` key. **An unresolvable entry is kept and WARNed on stderr**, never kept silently — a retention that quietly skips an index it claims to purge is the "declared, not enforced" failure this section exists to prevent. Grep your cron log for `WARN`.

## Output format

Every run answers with the same block — short, factual, no dump, no secret, no PII:

```text
<link> - <Done | Nothing to process | Started | Blocked | Human action required | Error to fix>
Result: …
Item: …
Next action: …
Details: …

# Filled:
autopr - Done
Result: Draft PR opened and ticket acknowledged.
Item: tkt-401 - Filter invoices by status
Next action: Human review of the PR.
Details: branch=agent/tkt-401-invoice-filter, PR=…/pull/42, checks=green, action=created
```

## Troubleshooting

| Symptom | Root cause | Fix |
|---|---|---|
| Queue always empty, no error | Agent token ≠ server token → every `GET` is a `401` your script swallows | Assert `401` without Bearer **and** `200` with, as a deploy gate |
| Two PRs for one ticket | Ack is unconditional, or only the local index guards | Make the ack conditional server-side (lock 1) |
| `gh pr create` fails on `--label agent` | The label doesn't exist in the repo | `gh label create agent` — and the QA labels too (§First-run) |
| PRs are off-scope | The agent implemented a raw request instead of a grounded brief | The grounding gate + "nothing beyond the brief" (§Grounding) |
| PRs are broken on arrival | Checks run after the PR, or not at all | Blocking QA **before** the commit (§The run, step 8) |
| The agent merged something | Permissions allowed it | PAT without merge rights + the `NEVER` coda. Verify `gh pr merge` fails |
| No preview deploy, no error anywhere | Commit authored with a local git email → the forge can't link it → the host never builds | `git config user.email` before the first commit |
| PR stuck `needs-work` forever | No consumer for the label | Add remediation, or remove the label |
| QA and remediation loop on one PR | Idempotence keyed by label instead of `<number>@<headSha>` | Re-key both indexes |
| Briefs cite deleted files | No drift watcher; briefs age silently in the queue | Add the staleness audit + refutation pass |
| Every brief passes the gate, even a garbage one | `BRIEF_GATE_PREFIX` resolved to empty (`export X="$UNSET_VAR"`) → `startswith("")` is always true | Fixed: the script now exits 1 on an empty prefix. Assert it in §First-run |
| Screenshots of closed PRs still on disk | Retention declared but never executed | `scripts/retention.py … --apply`, weekly (§Retention) |
| `pr-index` never shrinks, other indexes do | Entries written without `number` → the ticket-id key resolves to no PR → kept forever | Write `number` on every entry (§Anti-duplicate lock 3). The `WARN` on stderr names each unresolvable key |

## First-run checklist

- [ ] Labels `agent`, `qa-passed`, `qa-needs-work` exist in the repo (`gh label create agent`) — `gh pr create --label` fails on a missing label.
- [ ] `BRIEF_GATE_PREFIX` exported with your repo name substituted, byte-identical to the server's string.
- [ ] `GET ${QUEUE_URL}` → `401` without Bearer, `200` with. Both asserted.
- [ ] Ack tested twice on one id → second returns `idempotent:true`.
- [ ] Local gate rejects a 1k-char brief **without any network call**; server returns `400 grounding_too_thin` for the same input.
- [ ] `BRIEF_GATE_PREFIX=""` → the gate **refuses to run** (exit 1). An empty gate must never look like a passed one.
- [ ] `python3 scripts/retention.py pr-states.json` (dry run) prints a plan and changes nothing; `--apply` on a cron, weekly. Zero `WARN` on stderr — a `WARN` means something it claims to purge was not purged.
- [ ] Run retention from `/tmp` → **exit 1**, not a green no-op. Your cron's `WorkingDirectory` (or `--root=`) is the difference between a retention and a claim.
- [ ] `gh pr merge` **fails** (negative proof). Release branch protected, force-push and deletion off.
- [ ] Dry run on an empty queue → `QUEUE_EMPTY`, nothing created.
- [ ] Dry run on one ticket, then **immediate re-run** → no duplicate.
- [ ] Every state your loop can emit has exactly one consumer. List them. Any orphan = future graveyard.

## Scope

**This skill ONLY:** reads a prioritized queue over an authenticated read-only endpoint; grounds briefs by reading code read-only; opens **draft** PRs on one repo from a deterministic branch; runs lint/type/test/build **before** proposing; browser-tests preview deploys non-destructively, on a dedicated test account, against test data; proposes verdicts and fixes, always disclosed as agent-written; acknowledges work that actually happened; talks to the four endpoints you configured, and to nothing else.

**This skill NEVER:** merges, marks a PR ready, pushes to an integration or release branch, force-pushes, rewrites history; acks a run whose checks were red; touches a ticket a human hasn't prioritized; invents an anchor it could not verify; clicks a destructive or irreversible action during QA (scan, delete, invite, payment) or points QA at a production tenant or a personal profile; works around a CAPTCHA, bot check or rate limit — if a challenge appears, it **stops and hands over to a human**; passes its output off as a human review, or denies being automated if asked; copies a requester's name, email or any personal identifier into a brief, a payload, a PR or a screenshot; keeps QA screenshots past the PR's close, or 7 days; hides a failure behind a fake success.
