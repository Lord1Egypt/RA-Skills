# Stage C: claim verification (adjudication layer)

> **Role**: it does not find bugs — it only adjudicates whether an existing suspected bug is real.
> Trigger phrases: "is this true", "verify this finding", "is it exploitable".
>
> This file is euthyna's core asset. Anyone can do the measurement layer; **adjudication discipline is the differentiator**.
> Methodology source and license: see `NOTICE.md`.

---

## C.0 Step zero: restate the claim (not skippable)

Restate it in your own words, item by item, in writing. **No jumping straight into analysis.**

| What to restate | What to cover |
|---|---|
| Exact vulnerability claim | One sentence, decidable as true or false |
| Claimed root cause | Where the defect is, and **why** |
| Claimed trigger path | What the attacker does |
| Claimed impact | Lands on RCE / privilege escalation / information disclosure |
| **Threat model** | What privileges does the code run with? Is it sandboxed? What can the attacker already do before triggering? |
| Defect class | One of the 9 classes (see `bug-classes.md`) |
| Execution context | Single-threaded? Synchronized? Lifecycle? |
| Caller analysis | Who calls it, and with what arguments |
| Architecture context | Where it sits in the system |
| Historical context | When and why this code was added |

> **Half of all false positives collapse at this step** — when the claim is restated precisely, it simply does not hold together.
> So this is not formalism: it is the highest-value filter.

**Output**: write the restatement as `subject.claim` in the fact contract (see `docs/fact-contract.md`).

---

## C.1 Routing: standard verification vs deep verification

### Standard verification (linear single-pass checklist) — **all** must hold

- The claim is clear and specific
- Single component (no cross-component interaction)
- The defect class is known
- No concurrency or async
- The data flow is straightforward

### Deep verification (task-based orchestration + subagents) — **any** one triggers it

- The claim is vague or has multiple readings
- Cross-component (data flows through 3+ modules)
- Involves race conditions or TOCTOU
- A logic defect with no clear spec to compare against
- Standard verification cannot reach a conclusion, or was escalated
- The user explicitly asks

**Start with standard by default.** Standard verification has two built-in escalation checkpoints:

1. After Step 1: if more than 3 trust boundaries, callback/async control flow, or an ambiguous validation chain appear → escalate
2. After Step 5: if any issue leaves unresolvable genuine uncertainty → escalate

**On escalation, hand over all evidence gathered so far** — deep verification continues from where it stopped and **does not redo completed work**.

---

## C.2 The 6 steps of standard verification

### Step 1: data flow

1. Map the trust boundaries crossed (internal trusted vs external untrusted)
2. Identify **all** validation and sanitization between source and sink
3. Check API contracts — some APIs carry their own boundary protection
4. Check environmental defenses, and **distinguish** "fully prevents" from "only raises the bar"
5. Apply the class-specific checks for the defect class (`bug-classes.md`)

> **Pitfall: analyzing code in isolation.** Upstream conditional logic can make the defect mathematically unreachable.
> You must follow the full validation chain — not just the few lines around the dangerous operation.

### Step 2: exploitability

- **Attacker-controlled**: internal storage written by trusted components is **not** attacker-controlled
- **Boundary proof**: write out an explicit algebraic proof verifying "IF the check passes THEN the boundary guarantee holds"
- **Race feasibility**: single-threaded initialization and synchronized contexts **cannot** race

### Step 3: impact

- Distinguish **real security impact** (RCE, privilege escalation, information disclosure) from **operational robustness** (crash recovery, cleanup failures)
- Distinguish **primary security controls** from **defense in depth**

### Step 4: demonstration sketch

```
Data flow: [Source] → [validation?] → [transformation?] → [fragile operation] → [impact]
```

Write down: what the attacker controls, how, and the triggering pseudocode.

### Step 5: devil's advocate spot-check (7 questions)

5 opposing questions (against **false positives**) + 2 supporting questions (against **false negatives**, marked always ask).

See C.5.

### Step 6: gate review

Run all 6 gates + all 13 items of the false-positive checklist.

---

## C.3 The six gates (all must pass before something is reported as a vulnerability)

| # | Gate | Criterion | Pass | Fail |
|---|---|---|---|---|
| 1 | **Process** | All stages completed with written evidence | Evidence at every stage | A stage lacks concrete evidence |
| 2 | **Reachability** | The attacker can reach and control the data in question | Clear evidence of an attacker-controlled path + PoC confirmation | Control or reachability cannot be shown |
| 3 | **Real Impact** | Exploitation leads to RCE, privilege escalation, or information disclosure | Direct impact in a concrete scenario | Only operational-robustness issues |
| 4 | **PoC Verification** | The PoC demonstrates the attack path | Shows control, triggering, and impact | The PoC fails to show the path or the impact |
| 5 | **Mathematical Boundary** | Mathematical analysis confirms the fragile condition can occur | Algebraic proof that the condition is possible | Mathematical proof that the check prevents it |
| 6 | **Environment** | No environmental defense can fully prevent exploitation | Defenses do not eliminate the vulnerability | An environmental defense fully blocks it |

### Adjudication rules (fixed)

| Condition | Verdict |
|---|---|
| **All** 6 gates `pass` | `TRUE POSITIVE` |
| Any gate `fail`s | `FALSE POSITIVE` |
| No `fail`, but some `not_evaluated` | **`INCONCLUSIVE`** |

**Key rule**: if any stage's verification fails, **record the failure evidence and continue through the remaining stages**;
only when **all stages are complete** do you issue the `FALSE POSITIVE` verdict.

> `INCONCLUSIVE` is an outcome **added** by euthyna beyond Trail of Bits' original definition.
> Reason: the original implementation used the Stop hook to force continuation indefinitely until complete, while DSH's Stop hook
> **must rate-limit itself** (otherwise it loops forever) and cannot force indefinitely. See `docs/dsh-stop-gate.md`.

### Adjudication format (evidence required)

```
BUG #3 FALSE POSITIVE — integer underflow in packet_handler.c:142
  Gate 5 (Mathematical Boundary) FAIL: line 98's check guarantees packet_size >= 16,
  so (packet_size - header_size) >= 8. Underflow is mathematically impossible.

BUG #4 TRUE POSITIVE — command injection
  All gates passed. Evidence: src/archive.js:42 (abc1234)
  Reproduce: node tools/poc.js
  Exploitability: EASY
  Impact: arbitrary command execution as the service account
```

**The format is machine-enforced**: after writing, validate with `euthyna gate <report file>` (see the "programmatic gate validation" section of SKILL.md). A TRUE POSITIVE that lacks evidence, lacks reproduction, or carries a FAIL gate is **downgraded to "observation"** by the validator and reported with exit code 10 — discipline does not depend on the adjudicator's self-awareness.

---

## C.4 The thirteen-item false-positive checklist (apply item by item to **every** suspected defect)

| # | Item | Question to ask |
|---|---|---|
| 1 | **Trace the full validation chain** | What are all the prior checks before the dangerous operation? Do not analyze isolated fragments |
| 1a | **Map the full conditional logic flow** | Is the seemingly unsafe `buffer[length-4]` only reachable when `length > 12`? |
| 2 | **Recognize defensive programming** | `ASSERT(size == expected)` is defense, not a vulnerability |
| 3 | **Confirm an exploitable data path** | Report only vulnerabilities with a **confirmed** exploitable data flow; do not assume network data reaches the dangerous function |
| 4 | **Understand the data source context** | API return values, compile-time constants, and network data carry different risk levels. Determine the true source |
| 5 | **Analyze the boundary-check logic** | If `size >= MIN` is checked and `MIN >= sizeof(header)`, the subtraction **cannot** underflow |
| 6 | **Verify the TOCTOU claim** | Can the checked value change between the check and the use? Checked then immediately used within the same function with no external modification = no TOCTOU |
| 7 | **Understand API contracts and trust boundaries** | Some APIs carry their own boundary protection and never write out of bounds regardless of input |
| 8 | **Distinguish internal storage from external input** | Config stores and registries are controlled by trusted components — they are **not** attacker-controlled |
| 9 | **Do not mistake pattern recognition for vulnerability analysis** | Code that "looks fragile" can be safe given the context and API contracts |
| 10 | **Verify concurrent access is actually possible** | Single-threaded initialization contexts cannot race; verify the threading model and synchronization mechanisms |
| 11 | **Assess real vs theoretical impact** | Failed storage of non-critical data is an operational issue. Ask: does it lead to code execution, privilege escalation, or information disclosure? |
| 12 | **Distinguish defense in depth from primary controls** | When the primary defense exists, a failing defense-in-depth layer is not necessarily a vulnerability |
| 13 | **Apply this checklist rigorously, not superficially** | Having a checklist does not stop false positives. **Every** suspected vulnerability must go through **all** items |

---

## C.5 Devil's advocate (two-way symmetric doubt)

This is the most elegant part of the whole design: **it prevents false positives and false negatives at the same time**.

### Opposing the defect (11 questions, against false positives)

1. Am I **hallucinating** this defect? (models are biased toward seeing bugs everywhere and rating them all critical)
2. Am I doing **pattern matching** rather than analysis?
3. Am I **confusing trust boundaries**?
4. Is my proof **rigorous**? (any "probably" / "should"?)
5. Am I treating **defense in depth** as a primary control?
6. Does the attacker really **control** this input?
7. Is this path really **reachable**?
8. Am I **ignoring upstream validation**?
9. Does the environmental defense **fully prevent** exploitation?
10. Is the impact **real** or operational?
11. Am I **overestimating severity**?

### Supporting the defect (2 questions, **asked in every case**, against false negatives)

12. **Am I dismissing a real defect because the exploitation path is complex or unlikely?**
13. **Am I inventing mitigations or validation logic that I did not verify in the source code?**
    → After reaching a conclusion, **re-read the code**.

> Questions 12 and 13 are the key to preventing false negatives. The model's default bias is "reporting too much",
> so most false-positive defenses suppress it; but over-suppression misses real defects.
> These two questions are the symmetric counterweight — they must not be skipped.

---

## C.6 Deep verification: task dependency structure

```
Phase 1: 1.1 map trust boundaries + trace data flow
           ├─ 1.2 research API contracts and security guarantees   ┐
           ├─ 1.3 environmental defense analysis                  ├─ all blocked by 1.1
           └─ 1.4 cross-reference analysis                        ┘
Phase 2 (blocked by P1): 2.1 confirm attacker-controlled input    ┐
                         2.2 mathematical boundary verification   ├─ parallel
                         2.3 race-condition feasibility proof     ┘
                         └→ 2.4 adversarial analysis (blocked by 2.1/2.2/2.3)
Phase 3 (blocked by P2): 3.1 prove real security impact         ┐ parallel
                         3.2 primary control vs defense in depth ┘
Phase 4 (blocked by P3): 4.1 pseudocode PoC + data-flow diagram (always required)
                         ├─ 4.2 executable PoC (if feasible)       ┐
                         ├─ 4.3 unit-test PoC (if feasible)        ├─ parallel
                         └─ 4.4 Negative PoC                       ┘
                         └→ 4.5 verify the PoC actually demonstrates the vulnerability
Phase 5 (blocked by P4): 5.1 devil's advocate review (13 questions)
Gate Review (blocked by P5): 6-gate assessment → verdict
```

### Execution rules

- Mark a task in-progress when it starts; mark it completed **only with concrete evidence**
- Launch parallel substages with concurrent subagents; **collect all results** before entering the next dependency gate
- **Never start a stage before all its dependencies are complete**
- **Phase 3 / Phase 5 / Gate Review must not be delegated** — they require cross-stage synthesis

### Subagent permissions are deliberately asymmetric

| Subagent | Permission |
|---|---|
| Data-flow analysis | **read-only** |
| Exploitability verification | **read-only** |
| PoC construction | the only one with write access |

**The ability to manufacture evidence is concentrated in a single stage**; the earlier stages can only observe — this reduces the risk of contaminating evidence.

---

## C.7 PoC rules

### Feasibility skip conditions (skipping requires a reason)

**Executable PoC**:

- Requires hardware or network unavailable locally
- The target language runtime is not installed
- Exploitation requires **modifying** production code (rather than calling it)
- The defect is in a closed-source component

**Unit-test PoC**:

- The project has no test infrastructure
- The fragile code cannot be invoked in isolation (deep dependency chain with no test fixtures)
- The build system is broken

### The 5 PoC-verification questions

1. Does the pseudocode accurately trace Step 1's data flow?
2. Did the executable PoC **actually run** and show the impact? (capture **real output**, not expected output)
3. Does the unit test pass and demonstrate the problem?
4. Does the Negative PoC correctly identify the preconditions?
5. **Is there any artificial bypass** (mocks, stubs, disabled checks)? — **if so, the PoC is invalid**

### The purpose of the Negative PoC (not optional)

Shows the same path working normally under **benign input** → shows the **specific preconditions** exploitation requires →
explains why it does not hold under normal use, but the attacker can force it to hold.

**This is not proving the defect false** — it records the delta between the safe and unsafe conditions, which is useful for fixes.

---

## C.8 Batch triage

When there are multiple suspected bugs:

1. Run step zero on **all** of them first (restatement often dismantles obvious false positives outright)
2. Route each one independently
3. **Process all standard-routed ones first, then deep-routed ones**
4. After all verifications, check for **exploit chains** — findings that individually fail the gates may combine into a viable attack

## C.9 Final summary format

1. Count: X TRUE POSITIVE, Y FALSE POSITIVE, Z INCONCLUSIVE
2. TRUE POSITIVE list: each with a brief vulnerability description
3. FALSE POSITIVE list: each with a brief rejection reason
4. INCONCLUSIVE list: **each with what is missing and why**

5. **Triggerability cannot carry a dismissal.** When a claim is excluded because "this path cannot be reached / never runs / is dead code":
   - Neither outlet of the coverage producer can carry that argument. **ESTABLISHED (never invoked — including the "file does not appear in the coverage data" outlet) records only "not exercised in this run"**: it may sit in the evidence column as corroboration, but it proves nothing about whether the path *can* fire; **the UNKNOWN "symbol not located" is the absence of a coverage fact**.
   - When no coverage fact was obtained, the gate that would carry the argument is recorded **NOT EVALUATED** with the reason `coverage=not-measured`. Not-evaluated is that gate's **completed state**, not a skipped step: every other gate is still evaluated in full. The verdict then follows the folding — any other gate FAILs and the FALSE POSITIVE is carried by that gate (whose own argument must not rest on triggerability); with no other FAIL, the verdict is INCONCLUSIVE.
   - **So a triggerability-based FALSE POSITIVE has exactly one legal form**: some refutation that does not rest on triggerability carries it — impossibility by data flow (hardcoded arguments, no attacker-controlled input), or a PoC that disproves it directly. Coverage adds nothing to and takes nothing from such an argument, and this rule does not apply to it. "This path did not fire" is never "this path cannot fire".
