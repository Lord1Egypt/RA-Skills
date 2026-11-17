# Browser QA of the preview, and remediation

Two links, one key. QA proposes a verdict on a commit; remediation consumes it and hands back. Neither merges, neither leaves draft.

**This link is opt-in.** It drives a real browser, logged into a **dedicated test account on a preview environment**, against a preview deploy. Skip it and the rest of the loop still works. If you run it, point it at disposable test data — never at a production tenant, never with a personal profile.

## QA — invariants

| Rule | Reason |
|---|---|
| **One PR per run**: the most recently updated open agent PR with no verdict for its current `headSha` | |
| Read-only on code: `gh pr diff`, `gh pr view`. No commit, no push, no merge, no `gh pr ready` | QA that fixes code is no longer QA |
| Real browser, **non-headless so a human can watch the run** — not to look human to a bot defense. Accessibility refs over coordinates | Visibility is the point: a QA run you cannot watch is a QA run you cannot trust. Coordinates are a last resort; they break on every reflow |
| **If a CAPTCHA, bot check or rate limit appears: stop and hand over to a human.** Never adapt behavior to get past a defense | A defense firing means a human should be driving. Working around it would defeat the control the site's owner chose to place there |
| **Strict scope**: test only what the PR changes | The diff is the control surface. A QA agent left free explores, times out, and reports noise |
| Non-destructive by default | No scan, delete, invite, payment, or irreversible action |
| Verdict is a recommendation | The human triages and merges |

## Tool preflight — before touching any PR

`<browser-cli>` is **your** browser-automation CLI or MCP driver — any tool exposing a doctor/start/snapshot surface (a Playwright-based MCP server, for instance). It is **not** part of this skill's declared `requires.bins`: the QA link is opt-in and needs it plus a logged-in test profile that you provision. Substitute the real command below.

Verify the tools exist **before** acting, not mid-run:

```bash
<browser-cli> doctor          # Output: ok
<browser-cli> start           # only if not running
<browser-cli> snapshot --format aria   # Output: accessibility tree
```

Missing tool → **STOP immediately**: comment nothing, label nothing, alert `Blocked: tool <name> unavailable, no QA performed`. A half-run QA that labels a PR it never tested is worse than no QA — it launders an untested commit as verified.

## Selection — `<number>@<headSha>`, not labels

```bash
gh pr list --repo acme-corp/app-example --label agent --state open \
  --json number,headRefName,headRefOid,title,url,labels,updatedAt
# Output: [{"number":42,"headRefOid":"9f2c1ab…","labels":[{"name":"qa-needs-work"}], …}]
```

1. Read `memory/qa-index.json`. Skip a PR **only if** `<number>@<headRefOid>` is already a key.
2. **Labels are human signals, NOT the source of idempotence.** A `qa-passed`/`qa-needs-work` label whose `headRefOid` is absent from `qa-index.json` is **stale**: a commit landed since the report. Re-test, and replace the label at the end with the new commit's verdict.
3. No candidate → `QA_EMPTY`.

## The preview

1. Find the preview URL in the PR checks or comments.
2. Wait for HTTP 200 before launching the browser. Cold starts are normal — wait and retry.
3. No usable preview → `NEEDS-WORK` **only with clear evidence** the preview is missing; otherwise STOP + alert with no label. Never guess a verdict.
4. Host says *"No account was found matching the commit author email address"* → the cause is upstream: the commit was authored with a non-forge git email. Verdict `NEEDS-WORK`, clear comment, and **do not try to work around the host**.

## Test plan — derived from the diff, and bounded

```bash
gh pr diff 42 --repo acme-corp/app-example
```

1. Read the diff and the PR description (and the card's Definition of Done if referenced).
2. Derive **3 to 8 checks** tied to the DoD and the changed files.
3. Write down explicitly **what must not be touched**. That list steers the browser.

Do not test the whole app. Context is the control.

## The loop

**snapshot → reason → act → re-verify.** Never act on a stale snapshot.

- Wait 2-4s after any action that triggers a reflow or a fetch.
- Checkpoint screenshots under `work/qa-runs/PR-<number>/`: `01-login`, `02-context`, `03-feature`, then `before`/`after` for each important action.
- If a session is already open, **explicitly verify** which account/tenant you're in before testing.
- **Forbidden: clicking a destructive action** (delete, scan, invite, payment, anything irreversible). If the expected button is destructive → STOP, document the risk, do not click.
- If a CAPTCHA, bot check or rate limit appears: **stop and hand over to a human**. Never adapt behavior to get past a defense.

### Screenshots are authenticated-session data — treat them as such

A screenshot taken after login carries, by construction, an account identity, a tenant, and whatever the page displays. So:

| Rule | |
|---|---|
| **Retention: delete `work/qa-runs/PR-<number>/` when the PR closes or merges — and in all cases within 7 days.** | The index entry can outlive the images; the images have no reason to |
| **Never commit a screenshot, never attach one to the PR.** Reference local paths in the report | A PR attachment is public and permanent; a local path is neither |
| `01-login` must never show a filled credential field. Capture the post-login state, not the form | |
| Test data only. A screenshot of a production tenant is a data leak, not a QA artifact | |

## Verdict report — verbatim template

The first line is **mandatory and never dropped**: a reader scanning the thread must not mistake an automated verdict for a human review. Same rule for every other comment the loop posts (steward conflict notes, remediation summaries) — one line, up front, saying an agent wrote it.

```markdown
> Automated QA run — proposed by an agent, not a human review.

## Browser QA

Verdict: PASS | NEEDS-WORK
Preview: <url>
Account: <login/tenant/persona — never a password>
Commit tested: <headSha>

### Targeted checklist
- [x] …
- [ ] …

### Bugs / risks
- <repro steps, expected, observed, screenshot>

### Screenshots
- <local paths>

### Out of scope / not tested
- …
```

Then: `gh pr comment <number> --body-file report.md`, and replace previous QA labels with exactly one — `qa-passed` or `qa-needs-work`. Labels absent from the repo → comment the verdict and report the gap.

Index it:

```json
{ "42@9f2c1ab": { "number": 42, "headSha": "9f2c1ab", "verdict": "NEEDS-WORK",
  "preview": "https://…", "report": "work/qa-runs/PR-42/report.md", "ts": "2026-07-16T11:04:00+02:00" } }
```

## Remediation — the consumer of `qa-needs-work`

Without this link, the label is a tombstone. With it, the loop closes: QA verdicts → remediation fixes → QA re-verdicts the new commit.

| Rule | |
|---|---|
| Only a PR labelled `agent` + `qa-needs-work`, open, **draft** | |
| **Stale label → SKIP.** If the current `headRefOid` is not in `qa-index.json` with `NEEDS-WORK`, a commit landed since the report: it's QA's job to re-test. **Do not double QA's work.** | This is the hand-off rule that prevents the two agents from fighting |
| **One attempt per commit**: `<number>@<headSha>` in `remediation-index.json` → SKIP | A new commit changes the sha and reopens the right to one attempt |
| Take the **oldest** unresolved QA finding (smallest `qa-index` `ts`), tie-break on smallest number | |
| **Never remove the `qa-needs-work` label yourself** | Your push creates a new `headSha`, which makes the verdict stale automatically. **Whoever laid down the verdict removes it.** |
| Fix **on the PR branch only**. Never integration/release. Never `--force`. **Stays draft.** | |
| Blocking local QA before any push; one red → no push, `outcome=qa_local_failed`, alert | |

### Diagnosis before code

Richest to poorest: the QA report's `Bugs / risks` section (repro, expected, observed, browser evidence) → the latest QA comment on the PR → the card's Definition of Done → `gh pr diff` → the screenshots.

**Reproduce the bug mentally**: tie the observed symptom to a cause **inside the diff**. If you cannot, escalate. Do not improvise.

### Every run that examines a PR writes an entry — success OR escalation

```json
{ "42@9f2c1ab": { "number": 42, "headSha": "9f2c1ab",
  "outcome": "pushed | qa_local_failed | not_reproducible | out_of_scope | non_trivial | blocked",
  "qaReport": "work/qa-runs/PR-42/report.md", "fixCommit": "<new sha or null>",
  "summary": "<what was fixed, or why escalated>", "ts": "2026-07-16T14:20:00+02:00" } }
```

This is what makes "one attempt per commit" enforceable. An escalation that leaves no trace gets retried forever.

### Escalation taxonomy — the single source of truth

The six `outcome` values, and nothing else. This table is the one the `SKILL.md` points to; the JSON above enumerates exactly these.

| `outcome` | Trigger | Then |
|---|---|---|
| `pushed` | fix done, local QA green | comment the fixed points (disclosed as agent-written), let QA re-verdict |
| `not_reproducible` | can't tie symptom to a cause in this diff, or the report is ambiguous | escalate, no code |
| `out_of_scope` | the fix would touch code unrelated to the diff/DoD | escalate, no code |
| `non_trivial` | >~3 files outside the diff's scope, or DB migration / schema / auth / payment / cross-cutting risk | escalate. **Do not tinker.** |
| `qa_local_failed` | fix written, checks red | no push, PR left as-is, alert |
| `blocked` | a precondition failed and no fix was attempted: browser tool unavailable, no usable preview, a CAPTCHA or rate limit handed the run over to a human | alert with the reason, PR untouched, no label |

Named outcomes are permission. Without them, an agent facing a hard bug does the worst possible thing: a plausible-looking wide fix that passes lint and breaks something a reviewer won't catch.
