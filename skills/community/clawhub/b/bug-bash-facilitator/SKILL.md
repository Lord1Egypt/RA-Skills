---
name: cm-bug-bash-facilitator
description: Plan, run, and debrief a structured pre-release bug bash session. Defines scope (areas, devices, user roles), invites the right participant mix (eng/PM/design/CS/sales), generates exploratory test charters, runs in-session severity triage, post-session de-duplication, fix prioritization, and the retro. Use when asked to organize a bug bash, run a pre-launch test sprint, set up a hackathon-style QA day, write test charters, triage bugs across teams, or build a bug intake form. Triggers on "bug bash", "bug hunt", "test sprint", "exploratory testing", "test charter", "session-based testing", "pre-release QA", "release readiness", "triage session", "go/no-go review".
metadata:
  tags: ["bug-bash", "qa", "exploratory-testing", "release-management", "test-charter", "triage", "facilitation", "engineering-process", "saas", "shipping"]
---

# Bug Bash Facilitator

Plan, run, and debrief a high-signal bug bash before a release. Acts as an experienced release manager / staff QA who has run dozens of these for SaaS products. Outputs the artifacts you need to actually ship: scope doc, charter board, intake form, triage rubric, prioritized fix list, retro notes.

## Usage

Invoke this skill when a release is 1-2 weeks out and you want a coordinated, time-boxed exploratory test pass — not a substitute for unit/integration/E2E automation, but the layer that catches the things automation cannot.

**Basic invocation:**
> Plan a bug bash for our v3.2 release shipping next Friday
> We launch onboarding redesign in 10 days, run a bug bash for it
> Generate test charters for the billing area
> Build the bug intake template for tomorrow's bash

**With context:**
> 12 engineers, 3 PMs, 2 designers, 2 CS, 1 sales — design the invite list
> Here are 47 bugs filed during yesterday's bash, de-dupe and triage
> We have 6 hours total on Tuesday — give me the run-of-show
> Last bash had 80% noise, redesign the intake form

The agent produces the eight runbook artifacts plus templates ready to paste into Slack, Notion, Linear, or Jira.

## How It Works

### Step 1: Scope Definition

A bash without a scope doc devolves into "click around for an hour." The agent forces the scope to declare four axes before invites go out.

| Axis | What to declare | Example |
|------|----------------|---------|
| **Surfaces** | Named features and screens. Exclude legacy. | New onboarding flow, billing dashboard, settings v2 — exclude admin console |
| **Devices** | OS + browser + form factor matrix | macOS Chrome, Windows Edge, iOS Safari, Android Chrome, iPad Safari |
| **User roles** | Personas to test as | Free trial, paid solo, paid team admin, paid team member, suspended |
| **Out of scope** | Explicit non-goals, pinned to stop scope creep | Performance, accessibility audit, copy review, integrations beyond Slack |

**Anti-pattern**: "Test the whole product." A 6-hour bash with 15 people on the whole product yields shallow coverage everywhere and depth nowhere. Pick 3-5 surfaces, exhaust them.

**Scope doc template** — declare goal, time box, in-scope surfaces, device matrix, roles with seeded test accounts, explicit out-of-scope items, severity rubric link, intake form link, and war room (Slack channel + always-on Zoom). Lock all six sections before invites — late additions destroy charter assignments.

### Step 2: Participant Mix

The participant ratio decides what kinds of bugs get found. Engineers find race conditions and edge cases; CS and sales find "users will complain about this." A bash that's 100% engineers misses the entire UX layer.

**Recommended mix for a 11-person bash:**

| Role | Count | What they catch |
|------|-------|-----------------|
| **Engineering** | 5 | Edge cases, error states, concurrency, console errors, API misuse |
| **Product Management** | 2 | Spec drift, missing flows, requirements ambiguity |
| **Design** | 1 | Visual regressions, micro-interactions, copy tone |
| **Customer Success / Support** | 2 | "This will generate tickets" pattern recognition |
| **Sales / Solutions** | 1 | Demo-killer bugs, enterprise-customer landmines |

Rules:
- No more than 50% engineering or you lose the user-empathy lens.
- At least one CS rep who handles the most tickets — they have the production failure modes loaded in memory.
- Avoid VPs and execs unless they will actually file bugs (most won't, and their presence dampens junior contributors).
- One designated **scribe** (rotates) outside the head count — captures triage decisions in real time.
- One designated **facilitator** (you) who does not file bugs.

**For smaller orgs**, the agent scales the mix proportionally:

```
6-person bash:  3 eng / 1 PM / 1 design / 1 CS
11-person bash: 5 eng / 2 PM / 1 design / 2 CS / 1 sales
20-person bash: 9 eng / 3 PM / 2 design / 3 CS / 2 sales / 1 marketing
```

### Step 3: Test Charter Generation

A **charter** is a 1-2 sentence mission for a 60-90 minute exploratory session. It frames what to explore without scripting steps. Charters outperform scripted test cases for finding novel bugs because they preserve human creativity inside a bounded mission.

**Charter formula** (Cem Kaner / James Bach session-based testing):

```
Explore [target]
  with [resources]
  to discover [information]
```

**Sample charters by SaaS surface:**

```
AUTH: Explore signup, login, password reset with multiple browsers,
  +alias emails, and an account that already exists, to discover
  state confusion, lockouts, concurrent-session races, and email
  deliverability failures.

BILLING: Explore plan upgrade/downgrade/seat changes with trial-to-paid,
  annual-to-monthly, prorated mid-cycle upgrade, and card decline
  mid-checkout, to discover charge correctness, invoice line-item drift,
  webhook idempotency failures, and access-rights timing bugs.

DASHBOARD: Explore with empty, partial, and large datasets (0, 5, 5000
  rows) under slow network, stale tokens, and tab-switching, to discover
  loading-state regressions, infinite spinners, data freshness, and
  pagination edge cases.

ONBOARDING: Explore as first-time user on desktop and mobile, plus a
  returning user who abandoned at step 3 yesterday, to discover step
  skipping, back-button breakage, missing validation, and persistence
  bugs.

MOBILE: Explore fresh-install iOS with Wi-Fi off mid-session, push
  disabled, Face ID disabled, and 30+ min backgrounded, to discover
  offline handling, notification opt-in, session expiry, cold-start.

INTEGRATIONS: Connect/disconnect Slack, Google, Stripe webhooks with
  revoked tokens, expired tokens, and rate-limited upstreams, to discover
  error clarity, retry behavior, and orphaned data after disconnect.

PERMISSIONS: Explore as admin/member/viewer/suspended with role changes
  during active session and cross-tab role drift, to discover privilege
  escalation, stale UI, and 403 handling.

DATA EXPORT/IMPORT: CSV with empty, large, malformed files; non-ASCII;
  CRLF vs LF; Excel-saved-as-CSV, to discover encoding bugs, parser
  brittleness, and partial-failure reporting.
```

**Charter assignment**: pair each charter with 1-2 testers and a target device. Two testers per charter is the sweet spot — one explores while the other watches and asks "what about…", which catches what a solo tester habituates past.

### Step 4: Bug Intake Template

A bad intake form produces 50 bugs that all say "Submit button broken on Safari" with no repro. The agent enforces a strict template — required fields gate submission.

**Intake form fields** (all required unless noted):

- **Title** (80 char max): `[Surface] [Action] [Result]` — e.g. "Billing — Annual toggle — Price doesn't update"
- **Severity dropdown**: P0/P1/P2/P3 (rubric in Step 5)
- **Surface dropdown**: matched to scope doc surfaces
- **Repro steps**: numbered, must be reproducible from a clean session
- **Expected** vs **Actual**
- **Environment**: browser + version, OS + version, device, account email, feature flags on
- **Attachments**: screenshot/recording required for UI bugs; console log + HAR required for JS errors or 5xx
- **Charter dropdown**: which charter the tester was running
- **Dupe-check checkbox**: "I searched the existing intake list before filing"

### Step 5: Severity Triage During the Session

Triage in real time, not after. Stale bugs become stale priorities. The agent runs a 15-minute triage huddle every 60-90 minutes during the bash.

**P0/P1/P2/P3 rubric** with hard tests:

| Severity | Hard test | Examples |
|----------|----------|----------|
| **P0** | Affects all users OR involves money/data/security/legal. **Blocks release, no exceptions.** | Payment double-charge, data loss on save, auth bypass, GDPR/PII leak, total outage |
| **P1** | Core happy path is broken for a non-trivial segment (>5% users or any paid tier). **Blocks release unless explicit waiver.** | Login fails on Safari, signup form rejects valid emails, dashboard blank for paid users |
| **P2** | Workaround exists, affects narrow segment, or is recoverable. **Ship-with allowed.** | Tooltip cuts off, sort order wrong, edge case on iPad landscape |
| **P3** | Cosmetic, polish, or enhancement. **Backlog.** | 1px off alignment, copy nit, missing animation |

**The "would I tweet about this?" test**: if a normal user would tweet a screenshot of this bug to complain, it's at least P1.

**The "would Stripe/Slack ship this?" test**: cosmetic regressions in core flows (typography in checkout, alignment in the inbox) are P1 for category-leading products even if functionally fine.

**Triage huddle script (15 min):**

```
0:00  Facilitator screen-shares the new bug list (filter: filed since last triage)
0:02  Round-robin — filer reads the title only, says "P0/P1/P2/P3"
0:08  Group challenges any P0/P1; facilitator assigns owner if confirmed
0:12  P2/P3 marked "post-bash review" — no debate now
0:14  Facilitator notes blockers and unblocks testers (test data, env, perms)
0:15  Back to charters
```

### Step 6: Post-Session De-duplication and Ranking

After the bash ends, the raw list is 30-80% noise: dupes, P3s, and "not bugs" (intentional behavior). The agent runs a structured de-dupe pass.

**De-dupe rubric:**

1. **Group by surface**, then by symptom. "Submit button broken" + "Form won't submit" + "Save does nothing" → likely the same root.
2. **Read the repros side-by-side**. Same steps, same actual? Merge. Different steps, same actual? Note as "manifests in 2+ flows" but keep as one.
3. **Pin the canonical bug** with the cleanest repro and the best attachment. Close the others as duplicates linking to the canonical.
4. **Promote any duplicate-cluster of 5+** by one severity level — high reproduction count is a signal.

**Ranking pass:**

Sort by:
1. Severity (P0 > P1 > P2 > P3)
2. Within severity, by **reach** (% users affected — flag-gated, paid-only, mobile-only, etc.)
3. Within reach, by **fix cost** (1-line copy fix < CSS fix < client logic < migration)
4. Within fix cost, by **release-blocking dependency** (blocks marketing launch, contractual SLA, customer demo)

The agent outputs a ranked CSV ready to import to Linear/Jira with severity, owner, reach, est-effort, and ship-decision columns.

### Step 7: Fix Prioritization Rules

Not every P1 gets fixed before ship. The agent applies explicit rules so the trade-offs are visible.

**Decision matrix:**

```
P0  →  ALWAYS FIX before ship. No exceptions, no waivers.
P1  →  Fix unless 3 conditions ALL met:
        a. Workaround documented and shippable in release notes
        b. Reach < 5% of impacted user segment
        c. Fix is not low-effort (>4h estimated)
        Otherwise: fix.
P2  →  Fix if low-effort (≤2h) OR if it touches a marketed feature.
        Otherwise: ship-with, file as fast-follow patch within 2 weeks.
P3  →  Backlog. Review at next quarterly polish sprint.
```

**Fast-follow patch SLA:**

A bash typically generates 3-8 P2 bugs that ship-with. Commit to a patch release within 2 weeks of the main release with all of them fixed. Without this commitment, P2s rot to P3 and accumulate as platform debt.

**Waiver template** (when shipping with a known P1):

```
WAIVER — [Bug ID] — [Title]

Severity: P1
Reach: [%] of [segment]
Workaround: [user-facing instruction in release notes]
Fix ETA: [date] in patch release [version]
Approver: [name]  Date: [date]
Communicated to: [#support, #cs, status page]
```

### Step 8: Retro Template

The bash ends with a 30-minute retro — separate from the triage. Format: "Start / Stop / Continue" plus three numeric metrics.

**Retro template:**

```
# Bug Bash Retro — [Release] — [Date]

Headline metrics:
  Bugs filed:           [N]
  After de-dupe:        [N]   (signal ratio: [%])
  P0 found:             [N]   (released-with: [N])
  P1 found:             [N]   (released-with: [N], waivers: [link])
  Coverage:             [surfaces tested fully / surfaces in scope]

Start (do this next time):
  -

Stop (don't repeat):
  -

Continue (worked well):
  -

Charters that produced the most signal: [top 3]
Charters that produced the least signal: [bottom 3] — replace?

Tooling debt:
  -  (e.g. seed-data script broken, test accounts not enough,
       intake form too slow)

People debt:
  -  (e.g. need a CS rep next time, designer was overbooked)

Action items (owner + date):
  -
```

### Step 9: 8-Step Facilitator Runbook

Calendar-anchored. Adapt spacing for shorter release windows but never drop a step.

```
T-7d  1. KICKOFF — lock scope doc with EM + PM, save-the-date,
         identify scribe and backup facilitator
T-5d  2. INVITES — send invite (mix per Step 2), share scope doc +
         severity rubric + intake link, request 15-min pre-read
T-3d  3. TEST DATA + ENV — seed accounts for every role, verify
         staging mirrors prod, file a fake bug yourself end-to-end
T-1d  4. CHARTERS — generate 8-15 charters across surfaces × devices,
         assign 2 testers per charter, post board, confirm war room
T-0   5. RUN OF SHOW (6h):
         0:00 Kickoff 15m (scope, rules, severity, intake demo)
         0:15 Round 1 charters (75m)
         1:30 Triage huddle (15m)
         1:45 Round 2 charters (75m, partner rotation)
         3:00 Lunch (30m, keep filing)
         3:30 Triage huddle (15m)
         3:45 Round 3 charters (75m, focus on triage gaps)
         5:00 Final triage (30m)
         5:30 Retro (30m)
T+0pm 6. DE-DUPE + RANK — within 4h of end, output ranked CSV to EM
T+1d  7. FIX SPRINT — standup with owners, P0/P1 due dates assigned,
         P2 fast-follow milestone created, waivers drafted for ship-with P1
T+1d  8. RETRO PUBLISH — send retro doc, file tooling/people debt as tickets
```

### Step 10: Slack and Notion Templates

**Slack invite**: announce date/timezone/duration, role on the matrix, link to scope doc and intake form, war room channel and always-on Zoom, what to bring (laptop + secondary device).

**Notion charter board**: columns are Charter ID, Surface, Charter sentence, Tester 1, Tester 2, Device, Status. One row per charter, kanban-style with Active/Done states.

**Slack triage huddle ping**: `@channel triage huddle in 2 min — [N] new bugs since last. Filers ready to read title + propose severity.`

## Worked Examples

### Example 1: 6-Hour Bash for SaaS Onboarding Redesign

**Context**: a 25-person seed-stage SaaS shipping a redesigned signup-to-first-value onboarding flow. Release in 7 days. Available: 9 people for one afternoon.

**Scope**: signup, email verification, plan selection, workspace creation, invite teammates, first-task creation. Out of scope: existing user upgrade flow, mobile app (separate bash next month).

**Mix**: 4 eng + 1 PM + 1 design + 2 CS + 1 sales = 9 people.

**Charters generated** (10 charters, 2 hours each across 3 rounds with rotation):

```
C-01 Signup flow: Chrome desktop, valid emails, +aliases
C-02 Signup flow: mobile Safari, deferred email verification
C-03 Workspace creation: name collisions, special chars, very long names
C-04 Invite teammates: email typos, already-member, expired invites
C-05 Plan selection: trial-to-paid mid-onboarding, card decline
C-06 First-task creation: empty state, large paste, abandoned mid-create
C-07 Browser back button across every step
C-08 Tab duplication mid-onboarding
C-09 Returning user who abandoned at step 3 yesterday
C-10 Slow network (DevTools throttle, "Slow 3G") through entire flow
```

**Outcome**: 31 bugs filed, 19 after de-dupe. 1 P0 (workspace creation race condition double-creates on slow network), 4 P1 (back-button data loss in 3 steps, Safari email validation), 8 P2, 6 P3. Released on schedule with the P0 fixed and 2 P1 waivers (Safari ones, fixed in patch 9 days later).

### Example 2: De-dupe of 47 Raw Bugs into 22 Canonical

**Context**: bash just ended, raw intake CSV has 47 rows.

Agent groups by surface then symptom: Billing has a 5-dupe cluster on "annual toggle doesn't update price" — pick canonical with the cleanest repro, escalate P2 → P1 because 5+ reports is signal. A 3-dupe cluster on card-decline error stays P2 (workaround = retry). Onboarding has a 4-dupe cluster on back-button losing workspace name → P1 (data loss, however small). Singletons kept as-is unless tagged "not a bug" (close as invalid).

Outcome: 47 raw → 22 canonical → 1 P0, 5 P1, 9 P2, 6 P3, 1 invalid. Output is CSV with one row per canonical bug, dupes referenced in a child column.

## Output

The agent produces:

- **Scope document** — surfaces, devices, roles, out-of-scope, war room links
- **Participant invite list** — role mix calculated for the team size
- **Charter board** — 8-15 charters tailored to in-scope surfaces with assignments
- **Bug intake template** — Linear/Jira/Notion-ready with required fields
- **Severity rubric** — P0/P1/P2/P3 with hard tests and examples
- **Run-of-show** — minute-by-minute facilitator script for the day
- **De-dupe + ranked output** — canonical bug list sorted by severity × reach × cost
- **Fix prioritization decisions** — fix-now / fix-fast-follow / waiver / backlog
- **Waiver document** — for any P1 shipping with the release
- **Retro template** — populated with metrics from the session

## Common Scenarios

### "Our last bash was 80% noise"
Tighten the intake form: required severity, required repro steps, required attachment for UI bugs, required charter ID. Add a dupe-check checkbox. Most noise comes from missing fields, not bad testers.

### "We only have 2 hours, not 6"
Cut to 2 charter rounds (45 min each) on the highest-risk surface only. Skip the formal retro; do a 10-min Slack-thread retro async. Coverage will be narrower but the signal-per-hour is the same.

### "Engineering doesn't show up"
Tie the bash to the release readiness review — exec sign-off requires bash participation by the on-call eng for the release. Make it a calendar block, not a "if you have time."

### "We find the same bugs every release"
Your automation pyramid is upside-down. Bashes should find novel exploration bugs, not regressions. File the recurring bugs as missing test coverage and require an automated test before the next release. The bash should not catch what unit + E2E tests should.

### "Triage devolves into debate"
Use the rubric strictly — read the hard tests aloud. If two engineers disagree on P1 vs P2, default to P1 (the higher severity) and let the EM downgrade in writing afterwards. Debate in async, not in the room.

### "Should we run a remote-only bash?"
Yes — remote bashes match in-person on bug count if the war room is loud (Zoom always-on, Slack channel pinged on each filing, triage huddles on camera). They lose the side-conversation discoveries but gain device variety (everyone's home setup is different).

## Tips for Best Results

- Tell the agent your release date so it can produce a calendar-anchored runbook.
- Share the participant roster (count per role) so the mix matches reality, not the ideal.
- Name the surfaces in scope using the actual feature names — generic charters produce generic bugs.
- Provide last bash's signal-to-noise ratio so the agent can tune the intake form's strictness.
- If you ship weekly, ask for a 2-hour "mini-bash" template; the 6-hour version is for monthly+ releases.
- Mention your bug tracker (Linear, Jira, GitHub Issues, Shortcut, Notion) so the templates are paste-ready.

## When NOT to use

- **Daily / hourly continuous deployment** — bashes are too heavy. Run mini-bashes (45 min) tied to feature flags before the flag rollout, not before each deploy.
- **Pre-PMF early-stage products** with 1-3 engineers — formal facilitation overhead exceeds the bug yield. Pair-test for 30 min and ship.
- **Pure automation gaps** — if you're finding regressions, fix the test coverage; bashes are not for catching what should be in CI.
- **Performance, accessibility, or security reviews** — these need specialist methodology (load testing, axe / WCAG audit, threat modeling). A general bash will miss most of what specialists catch.
- **Hardware / firmware testing** — different methodology (bring-up, environmental, regulatory). Software bash playbooks don't transfer.
- **Internal tools used by 5 employees** — the cost-benefit doesn't justify a structured bash. File bugs as you find them.
