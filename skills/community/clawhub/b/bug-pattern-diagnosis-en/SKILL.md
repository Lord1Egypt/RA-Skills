---
name: bug-pattern-diagnosis-en
description: Diagnoses bugs by matching user-reported symptoms against a curated library of past bug cases under experience/, using prior cases as memory references (never as copy-paste answers). Accumulates new cases after each successful investigation. Use when the user reports "weird error / intermittent failure / only reproduces in specific environments / strange logs".
---

# Bug Pattern Diagnosis (Symptom-Based Triage & Experience Accumulation)

## Skill Purpose

This skill works **like a doctor diagnosing a patient**:

1. **Collect symptoms** — Ask the user to describe the bug (error messages, reproduction rate, environment, log patterns, etc.)
2. **Recall past cases** — Look up similar bugs in the `experience/` folder as **reference memory**
3. **Diagnose independently** — Investigate using the current project's context. Past cases are only **sources of inspiration and hypotheses**, never reused as-is
4. **Accumulate new experience** — After successfully identifying a new bug, save it as a new `BUGxx.md` for future **reference**

**Core value**: Let past troubleshooting experience **inspire** the direction of new investigations — but never replace independent thinking. Similar symptoms do not guarantee the same root cause. Logs that look identical may hide completely different failures.

## Iron Rule: Experience Is Reference, Not the Answer

> **This is the single most important principle of this skill.**

The `BUGxx.md` files under `experience/` are **an old doctor's case notebook**, not **a prescription template**. When examining a new patient:

- ✅ **What you MAY do**: Use the notebook to learn "what conditions are worth suspecting given these symptoms", "what methods have worked before", "what traps are easy to fall into"
- ❌ **What you MUST NOT do**: Copy the root cause, copy the fix, or copy code changes just because the symptoms look similar

### Why Direct Reuse Is Forbidden

1. **Symptoms can match, root causes may not**: "NPE + intermittent + multi-replica" may be a missing header in one case, a Redis connection pool flake in another, or a GC stop-the-world race in yet another — or **multiple overlapping problems**.
2. **Projects differ wildly**: The same code pattern behaves differently across versions, configs, and dependencies.
3. **AI misdiagnosis is expensive**: Copy-pasting a case misleads the user into changing code based on a wrong premise, masking the real bug.
4. **The value of experience is in *prompting thought*, not *giving answers***: Good doctors read case files to broaden their thinking, not to copy-paste treatment plans.

### Correct Usage Posture

| Situation | Wrong approach | Right approach |
|---|---|---|
| Symptoms match closely | "This is BUG01, modify `invokeRemoteDeviceOpt` and add `x-token-payload`" | "Your description reminds me of BUG01 — one of its signatures was asymmetric logs across replicas. **Before proceeding**, can you verify: do the failing requests actually produce 'stack trace on one replica, one-liner on another'?" |
| Partial feature match | "Not exactly, but the BUG01 fix should still work" | "There's a **diagnostic trick from BUG01** that might apply here — send 100 requests in a row and see if the success rate is ≈ `1/N`. Let's validate that first." |
| Case contains specific code | Paste BUG01's fix and ask user to apply | "BUG01's fix idea was propagating headers, but for your project you need to first confirm: (1) What headers does your receiver actually depend on? (2) Is the serialization identical to the gateway's? We'll need these answers before writing any code." |

## Case Library Structure

```
bug-pattern-diagnosis-en/
├── SKILL.md                    ← This file (purpose, flow, matching rules)
└── experience/                 ← Case library
    ├── BUG01.md                ← One document per case
    ├── BUG02.md
    └── ...
```

Each `BUGxx.md` follows a fixed structure for fast lookup:
1. **Case summary** (one paragraph)
2. **Symptom / signature checklist** (like "positive findings" in a medical case — used for matching)
3. **Detailed explanation** (pathology / root-cause chain)
4. **Diagnostic methodology** (investigation flow / key techniques)
5. **Remediation plan** (fix + safety net + hardening)
6. **Prevention checklist** (to avoid recurrence)
7. **Playbook for similar intermittent bugs** (step-by-step for analogous cases)

## When to Activate This Skill

Prefer this skill when the user describes issues like:

- "This endpoint **sometimes** errors and sometimes works"
- "Reproduces in production but not locally/in testing"
- "The error in the logs looks weird / doesn't match the code / the stack points nowhere useful"
- "Multiple pods / instances / replicas / machines behave inconsistently"
- "I clearly sent xxx, but the server says xxx is missing"
- "Occasional timeouts / occasional 500s / occasional permission denied"
- Anything framed as "**intersection / intermittent / non-deterministic**"

## Core Flow

### Step 1: Read the Case Library Index

Read the **symptom / signature checklist** section from **all** `BUG*.md` files under `experience/` (the first 30-50 lines of each file typically suffice). Do not read full files upfront.

### Step 2: Structure the Symptoms

Extract **key features** from the user's description, covering at least these dimensions:

| Dimension | Examples |
|---|---|
| Error signal | NPE / 500 / 403 / timeout / data corruption / deadlock |
| Reproduction rate | 100% / 50% / sporadic / specific conditions |
| Environment delta | Doesn't repro locally? repros in test? in prod? |
| Multi-instance traits | Single replica / multiple? how many? |
| Log distribution | Concentrated on one instance / scattered / one has stack one doesn't |
| Triggering conditions | Specific user / specific params / specific time window |
| Recent changes | New release? config change? scale up/down? dependency upgrade? |

### Step 3: Recall Cases (Not Match Conclusions)

Compare the structured features against each case library entry for **similarity**, but **never** treat the result as a conclusion. No matter how high the similarity, a case is only a **"prior experience worth consulting"**, not a **"confirmed answer"**.

Similarity handling:

- **High overlap** (3+ key features match) → Treat the case as a **"priority suspicion direction"**, but guide the user to **independently verify** whether those key features actually hold
- **Partial overlap** (1-2 features match) → Treat the case as a **"possible source of ideas"**; mention that one or two of its diagnostic tricks may apply
- **No match** (0 features) → Go to the general methodology and investigate from scratch

### Step 4: Offer Investigation Suggestions (Not Diagnostic Conclusions)

**Do not** assert "this is BUGxx". Use the tone of "past cases had similar traits, here are **possible directions and ways to verify**".

Recommended response structure:

- 🧭 **Restate the structured symptoms** (confirm you understood correctly)
- 💭 **Experience reference**: Mention 1-2 relevant cases briefly ("this reminds me of BUGxx which had a similar trait X") — but **do not paste root cause or fix code**
- 🔬 **Independent verification steps**: List 2-3 quick checks the user can run to validate hypotheses (success rate over 100 requests / cross-replica log comparison / header packet capture, etc.)
- 🎯 **Project-specific investigation path**: Based on the user's project structure and code style, give **customized** next steps — not the generic steps from the case
- ⚠️ **State uncertainty clearly**: Say plainly "this is just a hypothesis based on similar symptoms; the real root cause needs your verification"

### Step 4 — Negative Example (DO NOT OUTPUT)

```
❌ "Based on your symptoms, this is BUG01 (multi-replica intermittent NPE).
    The root cause is that invokeRemoteDeviceOpt drops x-token-payload.
    Apply this fix: [pastes BUG01's code directly]"
```

### Step 4 — Positive Example

```
✅ "A few things in your description stand out:
   1) Intermittent failure with success rate near 50%
   2) The error looks token-related, but the client clearly sent a token

   This reminds me of a past case (BUG01) where similar symptoms were
   caused by 'multi-replica internal calls dropping an identity header'.
   Your project isn't necessarily the same thing, so **let's validate
   a couple of hypotheses first**:

   Q1: How many replicas does your service have? Does the success rate
       approximate 1/N?
   Q2: Can you tail logs from all replicas simultaneously and see if
       the failing request leaves traces on multiple replicas with
       asymmetric detail levels?

   Run those two checks, share the results, and we'll pick a path."
```

### Step 5: Accumulate a New Case (Optional)

Proactively **ask the user** whether to capture this investigation as a new case when:

- No case in the library matched, but the bug was successfully identified
- An existing case partially matched, but there's a significantly new variant
- A new diagnostic technique emerged during investigation

With user consent, create `BUGxx.md` (numbering = current max + 1) following the **case document template** below.

## General Methodology (When No Case Matches)

Investigate unknown bugs in this order:

### 1. Quantify the Symptom

- Success rate? Fire 100 consecutive requests and tally
- Reproduction conditions? Can a minimal case reproduce reliably?
- Time-of-failure distribution? Specific time window / user / machine?

### 2. Inspect Deployment Topology

- How many replicas? Does success rate ≈ `1/N` or `(N-1)/N`?
- Can a single replica reproduce? If not → strong signal of inter-replica inconsistency
- Any canaries / gray releases? Is there a mix of old and new versions?

### 3. Cross-Instance Log Comparison

- By traceId / time window, pull logs from **all relevant instances** and view side-by-side
- Look for cases where "the same request leaves dislocated evidence across instances"
- Watch for **asymmetric verbosity** (one instance has full stack, another has a one-liner)

### 4. Source vs Deployed Binary Parity

- `javap -c -p` the deployed jar's key classes and diff against local source
- Verify image tag, git commit hash match expectations
- Check ConfigMaps / env vars are identical across all replicas

### 5. Protocol Boundary Audit

If you suspect context propagation issues:

- Draw the full lifecycle of "identity / traceId / MDC / ThreadLocal"
- Mark every "cross-thread / cross-process / cross-instance" boundary
- For each boundary, does an explicit pack → unpack mechanism exist?
- Use tcpdump / print `getHeaderNames()` at the receiver to verify what headers actually arrive

### 6. Compare Against Sibling Code

- Does the project contain **similar code** that does **not** have this bug?
- Diff the buggy code vs the healthy code — the delta is often the culprit

## Case Document Template (for new BUG*.md files)

```markdown
# BUGxx: <One-line title emphasizing the most distinctive symptom>

## Case Summary

<One paragraph, under 200 words: phenomenon, reproduction conditions, root-cause type, blast radius>

## Symptom / Signature Checklist (for matching)

> If N+ of these hold simultaneously, high probability of this case

- [ ] Feature 1 (concrete, verifiable)
- [ ] Feature 2
- [ ] Feature 3
- [ ] ...

### Key Log Fingerprints

<Paste typical error log snippets so future investigations can grep-match them>

### Exclusion Criteria (Negative Signals)

- If <xxx> appears, this is NOT this case

## Detailed Explanation / Root Cause Chain

<The pathology. Use diagrams / tables / code references to show data flow, control flow, state transitions>

## Diagnostic Methodology

### Techniques Used

- <Technique 1, e.g. "cross-replica log comparison">
- <Technique 2, e.g. "javap bytecode diff">
- ...

### Diagnostic Steps (in order)

1. ...
2. ...
3. ...

## Remediation Plan

### Root-Cause Fix

<The core fix, with code reference, impact assessment>

### Safety Net / Defense in Depth

<Secondary defenses so a missed fix still doesn't crash>

### Hardening / Cleanup

<Long-term improvements, coding standards, sibling-code sweeps>

## Prevention Checklist

During development:
- [ ] ...

During deployment:
- [ ] ...

During review:
- [ ] ...

## Playbook for Similar Intermittent Bugs

When symptoms look similar, walk through:

1. Quantify reproduction (10 min)
2. Check topology (5 min)
3. Cross-replica log diff (30 min)
4. ...

## References

- Relevant file paths
- Relevant PRs / commits
- Relevant wiki
```

## Output Style Constraints

- **Lead with direction, not with the conclusion**: Tell the user what's worth suspecting and why, instead of asserting "this is bug X"
- **Never speak in 100% certain terms**: Similar symptoms ≠ same root cause. Use phrases like "looks like / worth suspecting / could be / past cases suggest"
- **Recommendations must be executable**: Provide concrete commands or quick checks, not abstract theory
- **Make the user verify before coding**: Better to ask 2 "please confirm..." questions than to let them edit code based on a guess

## Hard Rules (Forbidden Actions)

- ❌ **Never paste the fix code from a case directly**: The code in `BUGxx.md` is "how that project fixed it", not necessarily right for the current project
- ❌ **Never assert "this is BUGxx"**: At most say "this reminds me of BUGxx" / "has similar traits to BUGxx"
- ❌ **Never skip independent verification**: Even if 5 of 5 features match, run at least 1-2 quick checks before discussing fixes
- ❌ **Never copy-paste the case's prevention checklist or playbook wholesale**: These are **thinking material**; tailor and rewrite each time based on the current context

## Case Accumulation Rules

- Don't create a case just to create one — only capture truly novel value (new symptom combinations, new diagnostic techniques)
- Don't use generic bug taxonomy terms (OOM, deadlock) — use **symptom descriptions** to organize cases ("same request leaves dislocated evidence across replicas" matches better than "state consistency bug")
- Index the library by **phenomenon**, not by "tech stack" or "vulnerability class"
- End every case with **applicability boundaries** and **counter-examples** (what situations are NOT this case), to sharpen future identification
