# Meta-mechanisms: six things that make the process actually work

> Stages A / B / C are the **process**. This file is the **mechanisms** that keep the process from degrading into going through the motions.
>
> What they share: **none of them relies on self-discipline**. Any constraint that depends on "remember to be careful" fails in long sessions.

---

## 1. Against "wrong numbers": separate measurement from judgment

**Rule**: every measurable quantity is produced by a command or script. The model only interprets.

Number of callers, test coverage, dependency versions, line numbers, commit hashes, how many times a function is invoked —
**none of these may be answered from memory**. When a tool is unavailable, say "not measurable" —
**never estimate and then write the estimate into a conclusion as fact**.

### Why this rule must be hardened

Model estimates of such numbers are not "slightly off" — they are **systematically wrong**, and wrong in a way nobody notices:

- a package shows 5+ maintainers on the code-hosting platform, while its actual permission list in the package manager has **1 person**
- a package downloaded 160 million times a week shows **zero downloads** in some data source

Both are real cases that failed in measurement. What they show is not "be more careful" — it is
**estimating numbers by feel is unreliable no matter how hard you try**.

### How it is implemented

For this, the project provides producers and defines the contract (`fact-contract.md`):

```powershell
# <euthyna repo> = where this project is checked out, not the audited project's path
node <euthyna repo>/bin/euthyna.js history  --base <rev> --repo <audited repo>
node <euthyna repo>/bin/euthyna.js coverage --coverage <file> --symbol <name>
```

⚠️ Writing the relative `node bin/euthyna.js` fails: during an audit the current directory is the audited project.
Commands, exit codes, and failure modes: see `fact-producers.md`.

---

## 2. Against "fabricated findings": evidence enforcement + the barrier dichotomy

### 2.1 Enforce evidence down to `file:line`

- every claim cites a concrete location: `path:L123`, or `path:L123 (commit abc1234)` when a version exists
- `probably` / `likely` / "roughly" are banned — chase the real code; when you cannot, **say you cannot**
- no `TODO`, `...`, or `// the attacker does something here` in demonstration code
- **the moment a demonstration uses an artificial bypass** (mock, stub, disabled check), that demonstration is judged **invalid**

### 2.2 "Raising the bar" is not "eliminating the defect"

This is the easiest point to confuse, and the easiest place to overestimate severity. Protections fall into two classes:

| Class | Example | Meaning |
|---|---|---|
| **fully prevents** | Rust's safe type system against memory corruption; parameterized queries against SQL injection | that class of defect cannot occur |
| **only raises the bar** | ASLR, stack canaries, CFI | harder, but **not eliminated** |

Likewise, keep apart:

- **primary security control** vs **defense in depth** — when the primary protection is intact, a failing defense-in-depth layer is **not a defect**
- **mathematically impossible** / **practically infeasible** / **feasible** — the three states must be stated clearly, not conflated

---

## 3. Against "missing the real thing": two-way skepticism + three-state honesty

A system that only guards against false positives degenerates into "nothing is ever a defect" — as useless as "everything is a defect".

### 3.1 The devil's advocate must work both ways

Besides the questions arguing against a defect (guarding against false positives), these two **must** also be asked:

> **12. Did I dismiss a real defect because the exploitation is complex or unlikely?**
> **13. Did I invent mitigations or validation logic that I did not verify in the source?** (**re-read the code** after concluding)

Questions 12 and 13 must be asked **in every case**. The model's default bias is "report too much", so most mechanisms suppress it;
**over-suppressing misses real vulnerabilities** — these two questions are the symmetric counterweight.

### 3.2 Three states, not two

Every criterion lands in exactly one of: **evaluated · clean / evaluated · flagged / not evaluable for a stated reason**.

- a run that measured nothing produces "not evaluable", **not** "no issues found"
- before citing any "clean" conclusion, look at the coverage table first
- **numbers must be quoted verbatim** — no re-deriving, no rounding, no dressing up
- **finding nothing is not an endorsement**

### 3.3 Verdicts need a third state

With only "true / false" states, "not finished checking" is forced to be written as "false" — that manufactures false negatives.

So verdicts must have `INCONCLUSIVE`, and **must state what is missing and why it is missing**.

---

## 4. Against "laziness": enumerate the excuses in advance

**"Be careful" is useless. What works is listing in advance the lazy impulses a model will produce in a real audit, and shutting each one down.**

| Excuse | Why it is wrong | What you must do |
|---|---|---|
| the change is small, take a quick look | the most severe historical vulnerabilities can be two lines | classify by **risk**, not by size |
| I know this codebase | familiarity creates blind spots | establish a baseline explicitly |
| digging through git history takes too long | history reveals regressions | origin attribution is **not skippable** |
| the impact is obvious at a glance | transitive callers get missed | compute quantitatively |
| missing tests are not my problem | missing tests = escalated risk | write it in the report and **raise** the severity |
| it is just a refactor, no security impact | refactors break invariants | analyze as high risk until **proven** low risk |
| I can explain it verbally | no artifact = lost findings | a report file is mandatory |
| this pattern looks dangerous | pattern recognition is not analysis | no conclusion without completing the data-flow trace |
| similar code elsewhere is a vulnerability | context, callers, and protections differ per site | verify this instance independently |
| this is obviously a severe vulnerability | the model is biased toward seeing bugs and overestimating severity | complete the devil's advocate review and prove it with evidence |
| skip full verification to save time | partial analysis is not allowed | execute **all** steps of the chosen path |

**This table must be explicitly loaded at the start of every audit**, and it **grows with real incidents** —
every new lazy pattern found adds a row. It is a living list.

---

## 5. Against "loss": output must be written to disk

- **output to chat only counts as failure**. a report file must be written
- fallback order when writing fails: current working directory → desktop → temp directory → **last resort** only: output to chat and prompt for manual saving
- filenames carry the project name and date

Design intent: chat transcripts scroll away and get compressed; **files do not**. A deliverable's survival should not depend on session length.

---

## 6. Against "contamination": isolate capabilities by stage

### 6.1 Gates must not be delegated

Some stages need **cross-stage integrated judgment**; handing them to a subagent shreds the responsibility:

- impact assessment
- devil's advocate review
- gate adjudication

**These three must not be delegated.**

### 6.2 Subagent permissions are deliberately asymmetric

| Role | Permission |
|---|---|
| data-flow analysis | **read-only** |
| exploitability verification | **read-only** |
| PoC building | the only one that may write |

Rationale: **the ability to manufacture evidence is concentrated in a single stage**. Earlier stages may only observe —
if the analysis stage could write files, it could "conveniently" reshape the evidence to support its own conclusions.

### 6.3 Never start the next stage before dependencies are done

Mark tasks in-progress when they start; **only concrete evidence marks them completed**.
Parallel substages start concurrently; before entering the next dependent gate, **collect all results**.

---

## How the six relate

```
1. separate measurement from judgment ─┐
                                       ├─→ makes "facts" trustworthy
2. evidence enforcement ────────────────┘
                                       ├─→ makes "conclusions" trustworthy
3. two-way skepticism ──────────────────┘
4. excuse table ───────────────────────────→ keeps the process from being bypassed
5. written to disk ────────────────────────→ keeps output alive
6. capability isolation ───────────────────→ keeps the process from being contaminated
```

The first three decide **conclusion quality**; the last three decide **process quality**. Missing any one, and the whole thing degrades at some point.
