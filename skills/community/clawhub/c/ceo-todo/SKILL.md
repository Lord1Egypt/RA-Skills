---
name: ceo-todo
description: Maintains one canonical markdown file as a CEO's single source of truth for everything they're on the hook for, and runs the Getting Things Done loop over it — capture, clarify, organize, reflect, engage. Turns pasted emails, meeting notes, and asks into clarified next-actions with an owner and a priority, tracks status with a fixed vocabulary ([OPEN]/[DONE]/[STALE]/[WAITING]), ages open items to [STALE] after 7 days, flags [WAITING] items past their reply-by date, archives done work without ever deleting it, and never auto-closes an item the CEO added by hand. Every mutating run is snapshot-backed and gated by a bundled deterministic validator so a commitment is never lost, corrupted, or silently changed. Use this skill whenever the user says "run my to-do", "update my todo doc", "what am I on the hook for", "GTD", "getting things done", "capture this", "triage my inbox into my todos", "weekly review", "single source of truth", "CEO to-do", "/ceo-todo", or points at a markdown to-do file and asks to keep it current. Based on the single-doc system Brian Halligan shared publicly. For the automated Gmail + Slack daily version, see the ceo-todo-daily agent.
---

# CEO To-Do — Single Source of Truth

## Role

You maintain **one canonical markdown file** that holds everything the CEO is on the hook for, and you run the Getting Things Done loop over it. The goal is that the CEO trusts the doc enough to get every commitment out of their head. You capture new commitments (from pasted email, meeting notes, or a direct ask), clarify each into a real next-action with an owner and a priority, keep the doc's state current, and surface what matters today — without ever losing, corrupting, or silently changing a commitment.

## When to Activate

Activate when the user asks to run, update, or review their to-do doc; when they paste an email / note / ask and want it captured; when they ask "what am I on the hook for"; when they ask for a weekly review; or on any of the trigger phrases in the description. If no canonical file exists yet, offer to create one from the format below (a good starting point is `references/sample-todo.md`).

## Credit

The single-doc format this skill encodes — one living file as the CEO's source of truth, with a compact status vocabulary and priority tags — is based on the system **Brian Halligan** (co-founder of HubSpot) shared publicly:

- https://x.com/bhalligan/status/2054689082857730097
- https://x.com/bhalligan/status/2054691150175584330 (thread)

This skill generalizes that pattern for any CEO. It does not reproduce Halligan's text.

## The canonical doc format

One markdown file. Every item is a single line with **fixed slots** so a validator can check it deterministically (free prose on an item line is not allowed):

```
- [STATUS] [#id] (Pn|parked) [reply-by: YYYY-MM-DD]? [user-added]? · <text> · updated: YYYY-MM-DD
```

- **Status vocabulary:**
  - `[OPEN]` — active, being worked.
  - `[DONE]` — complete. Moves to the `## Archive` section (append-only, never deleted).
  - `[STALE]` — an OPEN, prioritized item with no update for **more than 7 days**. A flag, not a close.
  - `[WAITING]` — delegated / blocked on someone else. Carries a **required** `[reply-by: YYYY-MM-DD]`; flagged if that date passes with no reply.
- **Stable ID:** `[#id]` is an immutable 4-hex id assigned at capture (e.g. `[#a7f3]`). All disappearance and dedup checks are exact ID-set comparisons, never fuzzy text matching.
- **Priority:** `P0` / `P1` / `P2`, or the literal `parked` (= GTD someday/maybe; exempt from staleness).
- **`[user-added]`:** an item the CEO entered by hand. The archive-as-DONE automation **never** fires on these — only a human may close a `[user-added]` item, and closing it removes the flag.
- **Doc stamp:** the file carries a `last updated: YYYY-MM-DD` line that advances on every mutating run.
- **`## Archive`:** done/dropped items move here with a reason + date. Append-only.
- **`## NEEDS-REVIEW`:** anything you can't confidently classify goes here **verbatim** — never dropped, never forced into a wrong bucket. Lines here are exempt from the strict grammar.

See `references/sample-todo.md` for a complete, validator-clean example.

## GTD, mapped onto operations on the one file

- **Capture** → add the raw input to the doc (a new line, or into `## NEEDS-REVIEW` if unclear). Nothing stays in the CEO's head.
- **Clarify** → is it actionable? If yes, write it as a next-action with an owner and a priority. If it's blocked on someone, it's `[WAITING]` with a reply-by. If it's someday/maybe, it's `parked`. If you can't tell, it goes to `## NEEDS-REVIEW`.
- **Organize** → assign status, priority, and (for waiting items) a reply-by. Give it a stable ID.
- **Reflect** → the weekly review below.
- **Engage** → surface today's P0/P1 shortlist so the CEO knows what to do next.

## Scan rules (state transitions)

On each run, apply these deterministically:

- **OPEN → STALE:** a prioritized (P0/P1/P2) OPEN item whose `updated` date is more than 7 days ago becomes `[STALE]`. Parked items are exempt.
- **WAITING past reply-by → flag:** a `[WAITING]` item whose `reply-by` date has passed is surfaced for follow-up. You do **not** invent a reply or change the item's substance — you flag it.
- **DONE → archive:** an item marked `[DONE]` moves to `## Archive` with a reason + date. It is never deleted.
- **NEVER auto-DONE a `[user-added]` item.** You may surface a `[user-added]` item that looks complete for the human to close, but you must never move it to `[DONE]` yourself.

## Triage rules (turning input into a next-action)

Given a pasted email, meeting note, or ask:

1. Decide if the CEO is now on the hook for something. If not, don't create an item.
2. Write the next-action in the CEO's terms (what *they* must do), not a restatement of the email.
3. Assign an owner (usually the CEO; if delegated, `[WAITING]` + reply-by), a priority, and a stable ID.
4. **Dedup by ID and by commitment, not by text.** If the same commitment already exists (e.g. it arrived once by email and once by Slack), update the existing item — do not create a second one.
5. If you can't confidently classify it, park it in `## NEEDS-REVIEW`. Fail loud, never guess.

## The reliability procedure (STOP-gated, non-negotiable order)

This skill is for people who need to trust the doc. The guarantee is **never lose, never corrupt, never silently change a commitment, and always be recoverable** — enforced by deterministic code, not by model judgment. Every mutating run follows this exact order. If any gate fails, **STOP and do not write.**

**Step 0 — Confirm the validator can execute (fail closed).**
The very first action is to confirm `references/validate.mjs` can run in this environment. Run it once against the current doc:

```
node references/validate.mjs <path-to-doc>
```

The script runs in **Claude's code-execution sandbox** — the same mechanism the built-in `docx`/`pptx`/`xlsx` skills use to run their bundled Python. It does **not** run on the CEO's machine; the CEO installs the skill, never a runtime. **If code execution is not available in this surface (a thin chat with no sandbox), STOP immediately and do not touch the doc.** Tell the user to run this in Claude Code, Cowork, or Claude Desktop. Never do an unvalidated write — the worst acceptable case is "did not update," never "updated and lost something."

**Step 1 — Snapshot.** Copy the canonical doc to a timestamped backup before any change:

```
mkdir -p <doc>.bak && cp <doc> <doc>.bak/<UTC-timestamp>.md
```

No write proceeds without a snapshot.

**Step 2 — Propose.** Build the proposed new version of the doc in full (append/archive only — never delete or overwrite an item in place). Keep the old file untouched on disk for now.

**Step 3 — Validate the proposal (gate).** Write the proposal to a temp path and validate it against the prior doc as the snapshot:

```
node references/validate.mjs <proposed-doc> --prev <original-doc>
```

**Non-zero exit ⇒ STOP. Do not write.** Report the exact violation the validator named. Do not attempt to "fix it up" silently.

**Step 4 — Write.** Only on a clean validation, move the proposed doc into place.

**Step 5 — Validate the written doc (gate).** Re-run the validator on the file that is now on disk:

```
node references/validate.mjs <doc> --prev <doc>.bak/<UTC-timestamp>.md
```

**Non-zero exit ⇒ STOP, restore from the Step 1 snapshot, report.** A corrupt write is never left in place.

**Step 6 — Postcondition report.** End every run by printing, in one glance:

- items in / items out (net),
- archived count,
- IDs added,
- IDs moved (e.g. OPEN→STALE, →Archive),
- validator result (PASS/FAIL),
- today's **P0/P1 shortlist**.

This is the CEO's proof that nothing vanished.

### What the validator enforces

`references/validate.mjs` asserts: every prior OPEN/WAITING/STALE ID is still present (no-loss), no duplicate IDs, staleness math is correct (>7 days ⇒ STALE for prioritized items, and nothing flagged STALE early), no `[user-added]` item was auto-closed, the `last updated` stamp advanced (with `--prev`), and every item line matches the fixed grammar. The invariants live in code so the guarantee does not depend on the model following prose.

## Weekly review procedure

Once a week, walk the whole doc with the CEO:

1. Run the full reliability procedure above (snapshot → validate → write → validate → report).
2. Confirm every `[OPEN]` item is still real and still theirs; re-prioritize or park what isn't.
3. Clear `## NEEDS-REVIEW` with the CEO — disambiguate each parked capture into a real item or drop it explicitly (to Archive with a reason, never silently).
4. Review `[WAITING]` items: which are past reply-by and need a nudge?
5. Review `[STALE]` items: revive, re-scope, or archive each with a reason.
6. Surface the P0/P1 shortlist for the week ahead.

## The automated version

For a hands-off daily run that sweeps the CEO's Gmail and Slack for new commitments and applies these same rules, see the **`ceo-todo-daily`** agent (Gmail via the Google Workspace connector + Slack connector, read-only). It reproduces this loop against real inboxes on a daily schedule.

---

**More from Skills and Agents Co:** see this skill in the [Skills & Agents catalog](https://skillsandagents.co/skills/ceo-todo/).
