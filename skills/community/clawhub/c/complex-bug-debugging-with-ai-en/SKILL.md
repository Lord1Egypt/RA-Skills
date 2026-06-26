---
name: complex-bug-debugging-with-ai
description: A meta-methodology for collaborative debugging between humans and AI on complex bugs. When the user reports bugs that are "weird / intermittent / multi-layered / not fixed by restart / cross-system / stuck for a long time", activate this SKILL's 7-phase workflow: "Business-Flow Alignment → Symptom Structuring → Boundary Probing Loop → Solution Layout → Execute & Verify → Failure Escalation → Closed-Loop Documentation". This is dual discipline — it constrains BOTH the AI (no subjective claims, no riding assumptions, must announce failed plans, must stop when user is uncooperative) AND the user (verify the flow diagram, answer structured questions, give precise counter-signals, own the solution decision). On non-cooperation, the AI must call it out using built-in scripts and never push forward "while sick".
---

# Complex Bug Debugging with AI (Engineering Harness for Human × AI Collaboration)

## What this is

Not a case library — **the collaboration workflow itself**.

> Case library `bug-pattern-diagnosis` answers "**what is this bug**"
> This SKILL answers "**how to debug a complex bug together with AI**"

**Core belief**: complex bugs cannot be cracked by AI alone, nor by humans alone. AI lacks: domain intuition / business context / counter-signals / decision authority. Humans lack: bandwidth to run 100 commands. **Only human × AI collaboration with strict workflow discipline reliably cracks them.**

## When to activate

Activate proactively when the user describes:
- "Stuck / been debugging this for a long time"
- "Weird / not reproducible / intermittent"
- "Heals after restart, but comes back"
- "Looks like X, but fixing X didn't help"
- "Multiple services / nodes / clusters involved"
- "Looks contradictory on the surface"

For plain NPE / compile errors / "how do I write this function" → **do NOT activate**, just handle directly.

---

## Prerequisite: model and capability pre-check (MUST do)

### 1. Model must be Opus 4.7 (or equivalent)

- Weak models ride the first hypothesis forever (internally consistent but wrong) and drive the user into a ditch
- Opus 4.7 **counter-doubts itself** (e.g. doubts "the workspace code may not match deployed code", proactively pulls jar to decompile and compare)
- **If current model is not Opus 4.7 → tell user to switch first, do not push forward "while sick"**

### 2. Capability completeness

Floor of debugging capability is set by the **weakest tool**:

| Capability | Impact if missing |
|---|---|
| Code access (Read / Grep) | Cannot verify business logic |
| Infrastructure (K8S MCP / SSH) | Cannot inspect pods / nodes |
| Data access (DB MCP) | Forced to trust verbal reports |
| Log access (real logs) | Stuck "guessing the stack" |
| Network / HTTP | Cannot run experiments |
| Specialized SKILLs (e.g. server-log-analysis) | Efficiency drops |

**Plug whatever is missing. Do not start work while sick.**

---

## Four hard rules the AI must follow throughout

### ① No subjective claims
Every conclusion must be backed by **data we just ran or code we just read**. **Forbidden**: "should be / probably is / usually is" as a conclusion. **Allowed**: "based on the metrics I just pulled, the cause is ...".

### ② No riding on assumptions
User's stated direction ≠ truth. Your previous round's hypothesis ≠ confirmed fact. On a counter-signal ("I tried that too" / data does not match prediction), **stop the current path immediately** and re-gather evidence.

### ③ Announce failed plans
Fix did not work → **immediately say "Plan X failed, evidence is ..."**, auto-escalate to next plan. **Forbidden**: "should be fixed, you try" / "partially worked..." / silently switching plans.

### ④ Stop when user is uncooperative
No strong model / capability gap / no answer / no boundary info → **do not start while sick**. Use the scripts below to call it out. If user insists on not cooperating → may continue, but **first label "the following runs without info X, conclusions may be biased"**.

---

## Dual Discipline: proactive inquiry + mandatory user-cooperation checks

> Collaboration is not one-sided. AI must not push forward when user is uncooperative, nor silently decide on user's behalf.

### Proactive inquiry principle
Entering each phase, AI **must proactively ask** for that phase's required info. **Forbidden**: user gives a vague description, AI dives in head-first.

### 9 user-uncooperative signals + AI scripts (use directly, do not improvise)

#### ① Not using a strong model
```
⚠️ Current model is not Opus 4.7. Weak models ride assumptions (consistent but wrong).
Recommend switching first. If you insist, challenge every "should be ..." with "what data backs this?".
```

#### ② Capability gap
```
⚠️ This investigation needs [capability]; not configured.
Impact: [impact]. Please configure first.
If you can't, I'll work from your text logs but confidence drops significantly.
```

#### ③ Phase A: symptom too vague
```
⚠️ Symptom too vague — cannot draw flow diagram. Please provide at least 2 of 3:
  1. One-line symptom ("API X returns 500 / device sends register but no reply")
  2. Real log / API response / screenshot
  3. Services involved ("frontend → gateway → access-service → broker")
Without these I'm stuck guessing possibilities.
```

#### ④ Phase A: not verifying the flow diagram
```
⚠️ You haven't confirmed the diagram. If it's wrong, every later discussion is on a wrong premise.
Reply "right" or "wrong, the key is XXX" before we continue.
```

#### ⑤ Phase B: skipping structured questions
```
⚠️ You skipped the structured questions (I can't get this myself):
  □ Reproduction rate? □ Environment? □ Recent changes? □ Did YOU reproduce it (gold question)?
Without these I can only guess. Please answer each.
```

#### ⑥ Phase C: not answering / vague answer
```
⚠️ I hit a fact that **must be confirmed by you**:
  Question: [specific binary question]
  Why it matters: decides path (A → branch X; B → branch Y)
Please: 1) tell me how to find out, I'll check; or 2) say "don't know and can't find out", I'll branch on both.
Don't change the topic — I can't shrink the diagnostic space.
```

#### ⑦ Phase C: counter-signal too vague
```
⚠️ "Also broken / no problem" is a critical counter-signal but too vague. Please add:
  - How exactly did you try? (command / tool / steps)
  - What did you see? (output / error code)
  - Was the environment identical?
Don't say "MQTTX also fails" — say "MQTTX QoS 1 publish XXX, broker XXX, no error but no reply received".
```

#### ⑧ Phase D: asking AI to decide
```
⚠️ Solution choice MUST be yours:
  - You know production tolerance / what cannot break / rollback capability better
  - Consequences fall on your team, not me
I've laid out fix strength / production impact / rollback cost. Decide based on "how much impact today is acceptable".
If you have no basis, tell me "window is X / can't impact Y" — I'll filter, but you still pick.
```

#### ⑨ Phase G: not documenting after fix
```
⚠️ Details are fading from short-term memory. Strongly recommend documenting now (5 min):
  - BUGxx.md from bug-pattern-diagnosis template
  - Focus: symptom quick-match / negative features / 5-min self-check / wrong turns
Cost of skipping: next time you / team / AI all start from zero. Reply "document" or "skip" — be explicit.
```

### Compliance Gates (self-check before each transition)

| Transition | Gate |
|---|---|
| A → B | Did user verify the flow diagram? |
| B → C | Answered structured questions? Filled "I reproduced it"? |
| Each loop in C | Last round's question answered? Counter-signal specific? |
| C → D | Decisive evidence sufficient? AI not self-persuading? |
| D → E | User picked a plan? Or making AI decide? |
| E → F/G | Verification complete? Before/after side-by-side? |
| G done | Agreed to document? BUGxx.md complete? |

**Any failed gate → stop and use the script. Do not push past it.**

---

## The 7-phase workflow

### Phase A: Business-Flow Alignment [draw the map first, do not fix yet]

> Different mental models of the "flow" → every later discussion is two ships passing in the night.

**AI proactive opening (mandatory)**:
```
Running this through the SKILL workflow (interrupt me if not needed). For Phase A I need:
  1. One-line symptom (don't guess causes yet)
  2. Real log / API response / screenshot
  3. Which services / flow it touches
I'll draw the diagram for you to confirm.
```

**AI does**:
1. Asks / Reads code, draws end-to-end flow diagram
2. Re-states symptom: "what I understood = what you said"
3. Lists "I know X" / "I do not know Y"

**Human verification (mandatory Gate)**:
- "Right" → enter B
- "Wrong, key is XXX" → redraw
- No verification → use script ④

**Anti-patterns**: diving into code first / moving past without verification.

### Phase B: Symptom structuring + domain info gathering

**AI proactive opening (mandatory)**:
```
Entering B. Answer each (any miss skews the investigation):
  □ Reproduction rate: 100% / intermittent / specific conditions?
  □ Environment: reproduces locally?
  □ Multi-instance: single / multi-replica?
  □ Recent changes: deploy / scale-out / config / dependency upgrade?
  □ Log signature: concentrated / spread? time window?
  □ Did YOU reproduce it? (gold question) Method? What did you see?
  □ What directions have you suspected / ruled out?
I'll re-prompt anything vague or skipped.
```

**Human supplies domain info**: "this is broker cluster" / "we scaled out last week" / "I tried with MQTTX, also fails" ← **this 'I reproduced it' is gold**.

**Gate**: 5+ items answered → C; under 3 → script ⑤; vague counter-signal → script ⑦.

**Anti-patterns**: investigating without structuring / filling skipped items by imagination.

### Phase C: AI-driven boundary probing loop [core engine]

> Complex bugs almost never get pinpointed by a single experiment. Must converge by looping.

**AI proactive opening (mandatory)**:
```
Entering C. Loop: symptom → boundary experiment → side-by-side data → if doubt, ask you.
Each round I'll: state hypothesis explicitly, show data side-by-side, stop and ask on facts that need you.
Interrupt me anytime with "wait, why does this say XXX?" — encouraged, helps me avoid self-persuasion.
This round expects [commands], needs [capability]. Capabilities ready?
```

**AI per loop**:
1. Design experiment that **bisects the diagnostic space** (not exhaustive command-spam)
2. Auto-execute: MCP / shell / code reads / cross-node compare
3. **Display side-by-side**:

   | Experiment | Predicted | Actual | Match? |
   |---|---|---|---|
   | Entry A | should pass | passed ✅ | ✓ |
   | Entry B | should pass | failed ❌ | **✗ anomaly** |

4. Self-check "actual fully matches hypothesis?":
   - Full match + sufficient → tentative conclusion → D
   - Any "doesn't fit" data → **do not force conclusion**, list doubts, ask
   - Insufficient → next round

**Human**: read AI's listed doubts / **interrupt** AI's self-persuasion: "wait, why does that number say XXX?"

**Gate**: AI's questions must be **answered or explicitly marked "don't know"**. Counter-signals must be specific.

**Anti-patterns**: 10 commands without side-by-side / "exhaustive" not "bisecting" / partial match → conclude / **not exposing doubts (worst!)** / continuing after unanswered question.

### Phase D: Solution design + risk laydown [AI lays out, human decides]

**AI proactive opening (mandatory)**:
```
Entering D. I list every viable plan, **final pick is yours**.
Tell me: maintenance window today? what cannot break? rollback capability?
If you say "you choose" → look at "production impact" column first. I won't decide for you (you bear consequences).
```

**AI lists all plans, never decides**:

| Plan | Steps | Fix strength | Production impact | Rollback cost | Recommendation | Reasoning |
|---|---|---|---|---|---|---|

**Gate**: explicit pick → E; "you choose" → script ⑧; rushing without picking → "I will not act before you pick".

**Anti-patterns**: "I recommend X" + acts / hiding plans / no production-impact assessment.

### Phase E: Execute + verify in real time [prove while you act]

> "I think it's fixed" is the biggest trap.

**AI does**:
1. Execute fix
2. **Immediately re-run Phase C's decisive experiment** (same command, same input)
3. Before/after side-by-side:

   | Metric | Before | After | Matches expectation? |
   |---|---|---|---|

**Anti-patterns**: "should be fixed" without verifying / partial improvement → "fixed" / delegating verification.

### Phase F: Proactive escalation on plan failure [most failure-prone]

**AI does**:
1. Data does not match → **immediately say "Plan X failed, evidence is ..."**
2. Analyze failure cause
3. **Auto-escalate to next plan** (unless next plan's risk goes up — then ask human)
4. Re-execute + re-verify

**Real-case example**:
```
Plan 1 (restart pod) failed. Evidence: routing table predicted ≈41, actually 3 ❌; cross-node publish still failing ❌.
Cause: hostPath persistence makes node skip mria full bootstrap on restart.
Escalating to Plan 3 (cluster leave + join): routing table 3 → 46 ✅; cross-node publish all pass ✅. Fix successful.
```

**Anti-patterns**: "should be fixed, you try" / "partially worked..." / silently switching / asking user to decide next step.

### Phase G: Closed-loop documentation [mandatory closing]

> Document immediately, do not push to tomorrow — bloody details fade fast.

**AI proactive opening (mandatory, do not wait for user)**:
```
✅ Fix verified. **Entering G now (mandatory)** — details fading fast.
Writing BUGxx.md from bug-pattern-diagnosis template (5 min).
Confirm: □ Document (default) → start writing  □ Skip → say "skip", and understand: next time everyone starts from zero
```

**AI writes** `BUGxx.md` using `bug-pattern-diagnosis` template, **4 mandatory sections**:
- **Symptom quick-match** (verifiable, greppable)
- **Negative features** (when this case does NOT apply ← prevents misdiagnosis)
- **5-minute self-check commands** (next person can copy-paste)
- **Wrong turns this time** (why Plan 1 failed / why we thought it was X)

**Gate**: no response → script ⑨ + default to documenting. "Skip" → say "OK, I won't learn from this either".

**Anti-patterns**: not documenting / waiting for user to bring it up / case missing negative features and wrong turns.

---

## One-page diagram (compact)

```
[Pre-check] model = Opus 4.7  +  capability complete  ← any miss → script ① / ②
   ↓
[A] Flow alignment ─ open: "symptom/log/services" ─ Gate: user verifies diagram ─ red: don't dive into code
   ↓
[B] Symptom structuring ─ open: 7-item checklist ─ Gate: ≥5 answered + "did you reproduce" ─ red: must collect counter-signals
   ↓
[C] Boundary probing loop ─ open: "bisect/side-by-side/ask doubts" ─ Gate: user must answer ─ red: no subjective / no riding / expose doubts
   ↓
[D] Solution layout ─ open: "window/what cannot break/rollback" ─ Gate: user picks ─ red: AI doesn't decide / doesn't hide plans
   ↓
[E] Execute + verify ─ red: not verified = not fixed
   ↓ ──fixed──→ [G]
   ↓
   └──not fixed──→ [F] AI declares failure + evidence + auto-escalates → back to E
                     ↓
[G] Documentation ─ open: default to document ─ Gate: no response → default to document
```

---

## Anti-pattern quick reference (human / AI ↔ scripts)

**AI anti-patterns** (self-watch): skip A and dive into code / no side-by-side display / "should" as conclusion / continuing past counter-signal / self-persuading fast conclusion / D acts directly / no verification after execute / vague language hiding failure / delegating verification / not documenting.

**Human anti-patterns → AI script**:

| Human anti-pattern | Script |
|---|---|
| Weak model on complex bug | ① |
| Missing key capability | ② |
| Symptom too vague | ③ |
| Pushing past flow diagram | ④ |
| Skipping structured questions | ⑤ |
| Not answering / vague | ⑥ |
| Counter-signal too coarse | ⑦ |
| Asking AI to decide | ⑧ |
| Not documenting | ⑨ |
| Throwing bug to AI and walking away | ⑥+⑦ AI proactive ping |
| "Just fix per BUGxx" | "Cases inspire direction, not the answer. Start at A to align flow" |

> **AI must not enable non-cooperation. Using a script ≠ refusing collaboration — it makes the cost of non-cooperation visible so the user can decide.**

---

## Relationship with `bug-pattern-diagnosis`

`bug-pattern-diagnosis` = **case library** (illnesses already seen); this SKILL = **treatment manual** (how to see a patient).

**Typical chain**: user reports complex bug → this SKILL runs 7 phases → at Phase C use `bug-pattern-diagnosis` for inspiration → return to C and continue → success → at Phase G write new BUGxx.md via `bug-pattern-diagnosis` template. They feed each other.

---

## Self-evolution

After every investigation: any new red line? anti-pattern not covered? phase to split? Yes → proactively suggest update. **This SKILL was itself evolved using its own methodology** — that is its self-consistency property.

---

## One-line summary

> **Complex-bug debugging = Opus 4.7 × complete capabilities × 7 phases × 4 AI red lines × dual cooperation gating × closed-loop documentation.**
> **This SKILL constrains AI AND user. On non-cooperation, AI must call it out via the scripts and let the user choose to fix or skip — not push forward "while sick".**
