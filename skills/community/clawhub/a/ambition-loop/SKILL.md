---
name: ambition-loop
description: "For work tasks (code, data, analysis, research, docs, decks, prompts). Use whenever the user asks you to be ambitious or more ambitious, think bigger, aim higher, go deeper, raise the bar, not settle for the minimal version, do what a top expert would do, or find the goal behind the goal, even when the task looks small (a speed-up, a bug fix, a summary, a prompt to improve). It applies altitude (goal behind the goal), depth (raw material, expert instruments) and range (methods from other fields), states a hard measurable target before executing, proves it with an outside judge (never self-grading), and reports asked vs ambitious vs achieved. Also use when a substantial work task plainly feeds a meeting or decision, recurs, or rests on digested summaries. Never for personal goals, career goals or plans, life plans, resolutions, self-improvement or motivational writing, even when the user says ambitious. Not for trivial asks, lookups, tone edits, urgent hotfixes, or explicitly minimal scope."
license: MIT
metadata:
  version: 1.0.2
  language: en
  sibling: ambition-loop-zh
  source: "Felix Rieseberg, How to be more ambitious: A tutorial for humans with models (2026-10-13)"
---

# Ambition Loop

Lift, deepen and widen the task, then **do the harder version and prove it with a judge other than you**. A rewritten prompt is one step, not the deliverable.

> **Keep reading.** Workflow and gates first; each step's Action / Output / Done-when follows below. If your reader truncates, re-read with an offset. Do not run the loop from this summary alone.

## Workflow at a glance

| # | Step | Output |
|---|---|---|
| 0 | Fit check | `ESCALATE` or `AS-ASKED` + reason |
| 1 | Survey reality | Data, tools, access, judges, gaps |
| 2 | Altitude | 3-rung ladder table, one rung recommended |
| 3 | Depth: four-question rewrite | Four answers, rewritten task |
| 4 | Range | Verbs; 3–5 fields + 1 red team, each a method |
| 5 | Ambitious target | Target table, **stated before any execution** |
| 6 | Approval gate | Plan card; if a gate fires, approval plan, then stop |
| 7 | Setup | Raw data, runnable judge, baseline |
| 8 | Execute | Work product + attempt log |
| 9 | External verification | Per-claim PASS/FAIL + judge evidence |
| 10 | Gap report | Five template headings; `check_report.py` passes |

**Rewrite-only mode:** when the user wants only a better prompt or plan, or you have no tools or data, run steps 0–6, name step 7 as setup the user must provide, claim no results, and put the whole hand-over (fit verdict, four answers, verbs and crew, rewritten prompt in a fenced block, plan card) in **one final message**.

## Gates (non-negotiable)

Get an explicit yes before crossing any of these. Ambition raises the task, not the risk.

- **G1 Cost.** Money, paid APIs, or compute/time well beyond what the ask implied.
- **G2 Permissions.** New credentials, access, accounts, installs, elevated privileges.
- **G3 Destructive.** Deleting, overwriting, migrating or force-changing data, history or live systems.
- **G4 External or visible.** Sending, posting, publishing, tickets or PRs, purchasing, contacting people.
- **G5 Scope.** The ambitious version materially changes the deliverable, timeline or who is affected.

**Gated means ask, not refuse.** Show an approval plan: each gated action, its cost and risk, and options (approve / smaller version / skip). Do the ungated prep (drafts, analysis, dry runs), then stop and wait.

**No credential hunting.** Never search env vars, home dotfiles, keychains, or secret/cred/.env files for credentials or mail/ad accounts to make a gated action possible. Ask for access instead.

**Denied means stop.** If a gate is declined or approval expires, do not reach the same result another way (no other tool, script, or smaller version of the action). Fall back to the original scope or stop, and say what was not done and why.

---

## Step details

### Step 0 — Fit check
- **Action:** Decide whether escalation helps. Answer `AS-ASKED` when the request is trivial (a one-liner, a lookup, a rename), is a tone or length edit, is an urgent hotfix, already has a tight spec with fixed acceptance criteria, or the user explicitly limits scope ("just", "only", "minimal", "quick", "don't expand"). Otherwise answer `ESCALATE`.
- **Output:** One line: `Fit: ESCALATE — <tell>` or `Fit: AS-ASKED — <reason>`. On AS-ASKED, do the task normally. You may add at most one sentence offering the ambitious version later.
- **Done when:** The verdict and its reason are stated. On AS-ASKED, the loop ends here.

### Step 1 — Survey reality
- **Action:** Read what the task touches before lifting it: files, code, data, earlier messages, connected tools. List what you can reach and what is missing. An ambitious plan built on imagined access is worthless.
- **Output:** An inventory with four lines: **Raw data** (where, what format), **Tools** (installed or installable), **Access** (granted or missing), **Judge candidates** (tests, benchmarks, held-out data, reproductions, metrics, human reviewers).
- **Done when:** Each of the four lines has concrete entries or says `missing: <what>`.

### Step 2 — Altitude: the goal behind the goal
- **Action:** Ask what should happen after this task is done, then climb. Rung 1 is the same task done with all the data, aimed at *what changed, why, and what to do*. Rung 2 covers the decisions the task feeds, with options and the case for and against each. Rung 3 covers the standing job the task serves: a better mechanism, backtested on the user's own history, run beside the current way. Then pick the axes that matter for *this* task (usually 1–2 of Altitude / Depth / Range) and name the tell. Typical tells: the result will be discussed in a meeting; the task recurs; it rests on summaries; the answer stays inside a single discipline. Speed counts only if the user asked for faster. See `references/moves.md`.
- **Output:** The chosen axes with their tell, plus a **ladder table with exactly three rungs** (Rung | What it delivers | Judge | Cost) and the rung you recommend. When the task feeds a meeting or decision, Rung 2 names **three concrete decisions**, each with options and the case for and against. When Rung 3 includes an early-warning or monitoring rule, it must be **backtested** in Step 8 (see below).
- **Done when:** All three rungs are written out, one is recommended, and you can say in one sentence why it beats the literal ask. Altitude fits poorly for purely creative work. Say so when that applies.

### Step 3 — Depth: four-question rewrite
- **Action:** Name the field, then answer these four for it, concretely:
  1. What would a top professional do here that was not asked for?
  2. What is the **rawest material** they would start from, instead of what was already digested?
  3. Which **specific methods and instruments** would they use? Name them: a database and survival model, not "analysis"; a profiler trace, not "optimize".
  4. What, **other than you or the user**, would show the result is right, and what counts as a pass?

  Then rewrite the task to ask for exactly that: deeper, not bigger. Add one assumption to test against the raw data, and one place where new knowledge could appear, to be validated on data the model has not seen.
- **Output:** The four answers and the rewritten task in a fenced block.
- **Done when:** Every answer names a real artifact, source, tool or check. If you do not know the field well enough, say so instead of inventing tools.

### Step 4 — Range: verbs and a crew of methods
- **Action:** Restate the noun as verbs ("a QBR deck" becomes "get busy people to believe a cause-and-effect story and decide under uncertainty in 30 minutes"). Ask which fields an all-star team would bring. Pick 3–5, plus one adversary (short seller, forensic accountant, security red team, hostile reviewer). For each, name the **method** it contributes and how it changes the plan. Do what the practitioner does; never just write in their voice. Run these methods in parallel subagents when you have them.
- **Output:** A verb restatement, plus a crew table (field → method → change to the plan).
- **Done when:** Each crew member changes something concrete. Drop any that only add flavour.

### Step 5 — Set the ambitious target
- **Action:** Turn the chosen version into a **specific, measurable, impossible-sounding target**, an order of magnitude past the ask where that makes sense (5 s → 200 ms). Treat it as solvable. Keep the user's literal ask as the **floor**. Pick the judge for each target from `references/judge-ladder.md`, as high on the ladder as you can reach.
- **Output:** A target table with the columns Asked (floor) | Ambitious target | Judge | Pass line | Cost/needs.
- **Done when:** Every row has a number or a binary check and a judge that is not your own opinion, and the table is **in your reply before Step 7 starts**. A target first written after the work is done does not count; the asked floor alone is not a target.

### Step 6 — Approval gate
- **Action:** Show a short plan card: "You asked for X; the version worth doing is Y, because Z", plus the target table, what you will touch, and cost and time. Check G1–G5. If none fires, continue without asking permission to do good work. If any gate fires, write an **approval plan** (template in `references/report-template.md`): for each gated action, what exactly would happen, to whom, cost and risk, and the options (approve / smaller version / skip). Prepare the ungated parts (drafts, segment lists, dry runs, analysis), then **stop and wait** for an explicit yes. A flat refusal with no plan is not enough; doing the gated action is never allowed. Do not look for credentials, accounts or mailers to make the action possible (see **No credential hunting**).
- **Output:** The plan card, plus `Gates: none` or the approval plan ending in `Gates: G<n> <action> — awaiting approval`.
- **Done when:** No gate fires, or the user approved the gated items. On a denial, follow **Denied means stop**.

### Step 7 — Set up data and environment first
- **Action:** Before the main work, wire up what the ambitious version needs: fetch the raw data, install the instruments, build or locate the judge (test suite, benchmark harness, held-out split, reproduction script), and **measure the baseline**. If an outcome is meant to stay true over time, set up the loop that keeps it true: data feed, version-to-commit mapping, reproducible environments. Any new access or spend goes back through Step 6.
For a bug, the baseline is a **failing test that reproduces it**, run before any fix.
- **Output:** A setup log (what was set up), the baseline number, and the command that runs the judge.
- **Done when:** The judge runs end to end against the baseline and produces a number or a pass/fail.

### Step 8 — Execute toward the ambitious target
- **Action:** Do the elevated work with the real instruments. Iterate against the judge, not against your impression. When it looks impossible, do **not** lower the target. Decompose it, try at least **two genuinely different approaches**, measure each, and keep the best. Stop iterating when the target is met, when a gate would be needed, or when attempts stop improving the judge's number. Then report honestly.
Any early-warning, alerting or predictive rule you propose must be **backtested on the history you have**: say when it would have fired, the **lead time** before each real event, and the hits, misses and false alarms.
- **Output:** The work product, plus an attempt log (approach → judge result).
- **Done when:** The target is met, or at least two distinct approaches have been measured and the remaining blocker is concrete.

### Step 9 — External verification
- **Action:** Run the judge on the final result. Grade claim by claim. A claim passes only on judge evidence: test output, benchmark numbers, held-out metrics, reproduction, or a reviewer's verdict. Your own assessment is never evidence. Where no outside judge was possible, mark the claim `UNVERIFIED` and say what would verify it.
- **Output:** A claims table: Claim | Judge | Result (PASS/FAIL/UNVERIFIED) | Evidence.
- **Done when:** Every claim in the deliverable has a row.

### Step 10 — Gap report
- **Action:** Close with the report in `references/report-template.md`, using its five headings verbatim (Target comparison, Verification, Gaps, Next moves, Gated or skipped). This is mandatory whenever you executed anything, however good the result. Compare the **asked floor, the ambitious target and the achieved result** for every target. State the gap plainly and do not reframe a miss as a win. List what blocked the rest, the next concrete moves, and anything worth turning into a durable workflow. If you can run commands, save it as `ambition-report.md` and run `python3 <skill-dir>/scripts/check_report.py ambition-report.md`; fix it until it prints `PASS`.
- **Output:** The final report.
- **Done when:** The report has the target comparison, the claims table, gaps, next moves, and any gated or denied items, and the **final message contains the full report** (or the report file path plus its target comparison and claims tables). Never end on a bare acknowledgement or only the last section.

## Rules that hold throughout
- **Deeper, not bigger.** More pages, features or side quests do not count as ambition. If the elevated version is only larger, re-pick the axis.
- **Methods, not costumes.** Switching vocabulary without switching method is role-play. Check that the instrument actually changed.
- **Never self-grade.** "Looks good to me" is not verification.
- **Hold the target, report the truth.** Treat hard targets as solvable while working. In the report, a missed 200 ms target with a real 900 ms result beats a quietly lowered goal.
- **Respect explicit scope.** "Minimal", "just", "only" from the user win over this skill.
- **Approval rules never loosen.** Every normal confirmation still applies.

## References
- `references/moves.md`: the altitude, depth and range moves catalog, with tells and anti-patterns
- `references/judge-ladder.md`: the outside judges, ranked, by domain
- `references/article-examples.md`: the source article's worked examples, as regression cases
- `references/self-efficacy.md`: why hard specific goals and belief matter, and how to apply that to an agent
- `references/report-template.md`: the plan card and final report templates
- `references/sources.md`: credits and sources
- `scripts/check_report.py`: checks that a final report contains the required sections (EN/ZH)
