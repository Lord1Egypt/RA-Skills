# Stage B: change audit

> Audit one change (PR / commit / diff) and answer one question: **did this change make the system weaker?**
>
> Prerequisite: the three non-skippable rules in `../SKILL.md`.

---

## B.0 Establish the baseline first

**This is the first action, not prep work.** Without a baseline, every judgment that follows is guesswork.

Record these on the **pre-change** revision:

| What to record | Why |
|---|---|
| system-level invariants | "what must always be true" — without them you cannot tell whether this change broke one |
| trust boundaries and privilege levels | which data is trusted, which is not; what identity the code runs as |
| existing validation patterns | what validation this codebase habitually does, and where |
| call relationships of key functions | the change's blast radius is judged through them |
| state flow | where data comes from, what it passes through, where it goes |
| **what the code is supposed to do** | not what it currently does — its design intent |

Miss the last item and you misjudge "the implementation diverges from the design" as "the implementation has a bug" — or the reverse.

---

## B.1 Keep two things apart: analysis depth vs risk level

These two are routinely conflated, and conflating them guarantees mistakes.

**Analysis depth** is set by **change size** — it only decides how much effort you spend:

| Change size | Strategy | Approach |
|---|---|---|
| < 20 files | deep read | read all related code, full blame |
| 20–200 | focused | follow only one-hop dependencies, prioritize high-risk files |
| 200+ | surgical | only the critical paths |

**Risk level** is set by **what changed** — it is **unrelated** to size:

| Level | Trigger |
|---|---|
| high | authentication, crypto, external calls, money movement, **any validation deleted** |
| medium | business logic, state changes, new public interfaces |
| low | comments, tests, UI, logs |

> **A one-line change can be the highest risk; two thousand lines can be zero risk.** Judging risk by size is the most common shortcut.

---

## B.2 Read both versions, file by file

For every changed file, do not look at the diff alone. **Read the pre-change and post-change versions side by side**, then answer four questions per section:

| Question | What it answers |
|---|---|
| What was it before | the original logic |
| What is it after | the new logic |
| **What the change does** | the intent in one sentence |
| **What it means for security** | does the attack surface grow or shrink? does validation get stronger or weaker? |

A diff only shows "which lines changed", not "how the behavior changed". Deleting one line may delete nothing (the line may already have been dead code); adding one line may change the entire execution order.

### Deleted code must be traced to its origin separately

**This is the step most easily skipped in this stage, and the most valuable one.**

For every block of deleted code, trace its origin with this project's producer:

```powershell
node <euthyna repo>/bin/euthyna.js history --base <pre-change revision> --repo <audited repo>
```

⚠️ **Do not write `node bin/euthyna.js`** — during an audit the current directory is **the audited project**, not the euthyna repo, and a relative path fails with `Cannot find module`. `--repo` refers to **the audited repo**, and `--base` resolves against it.

It tells you which commit introduced the deleted code and whether that commit's message carries security keywords. **Code deleted from a `fix` / `CVE` / `security` commit defaults to the highest risk**, unless it can be shown to be superfluous.

Do not run `git blame` yourself and read commit messages by eye — that is exactly why this producer exists: a machine adjudicating the same diff twice gives the same result; a human reading twice may not.

When reading the output, watch the "⚠ criteria not evaluated" section: when it is non-empty, this run **cannot** be read as "checked, no problem". Exit code `2` means it could not measure at all — **must not be read as clean**. Commands and exit codes: see `fact-producers.md`.

### Three red lines

| Symptom | Default handling |
|---|---|
| deleted code came from a security-fix commit | treat as **highest** risk, unless shown to be no longer necessary |
| validation deleted with no equivalent replacement | treat as **highest** risk |
| code was added → removed for security reasons → **added back now** | treat as a **regression** |

The third one is mechanically detectable with the producer:

```powershell
node <euthyna repo>/bin/euthyna.js history --base <pre-change revision> --pickaxe --repo <audited repo>
```

---

## B.3 Test coverage: a gap escalates risk, it is not a footnote

**Missing tests are not "worth a mention" — they are grounds for escalating risk.**

| Situation | Handling |
|---|---|
| new function with no tests | medium risk escalates to **high** |
| validation modified but tests did not change | **high risk** |
| complex logic (> 20 lines) with no tests | **high risk** |

To claim "covered", you need real execution evidence, not an inference from "this file has a test file":

```powershell
node <euthyna repo>/bin/euthyna.js coverage --coverage <absolute path to coverage file> --symbol <changed function>
```

With no coverage file: **either produce one by running the project's own tests, or mark the criterion "not evaluable"** — `coverage` tells you explicitly with exit code `2` that it "could not measure"; that is not "not covered".

> ⚠️ This producer can **only refute, never confirm**. When it says "never invoked", that is trustworthy;
> when it says "invoked N times", it **cannot** imply "the related call sites were executed".
> See `fact-contract.md`.

---

## B.4 Blast radius

Count how many callers each modified function has:

| Number of callers | Tier |
|---|---|
| 1–5 | low |
| 6–20 | medium |
| 21–50 | high |
| 50+ | extreme |

**Priority is set by "risk × radius" together**:

| | radius extreme | radius high/medium | radius low |
|---|---|---|---|
| **risk high** | P0 — deep analysis + all dependencies | P1 | P2 |
| risk medium/low | P1 | P2 | P3 |

Numbers must come from tooling, not from eyeballing. Optional upstream producers: see the ecosystem division-of-labor section in `../SKILL.md`.

---

## B.5 High-risk changes require adversarial modeling

For every high-risk change, answer:

**1. Who is the attacker**

| Dimension | Values |
|---|---|
| WHO | unauthenticated external user / authenticated ordinary user / malicious admin / compromised dependency / race winner |
| WHAT | can only use public interfaces / needs an authenticated role / needs specific privileges |
| WHERE | the specific endpoint or function |

**2. Attack path**: entry point → concrete calls and arguments → how the vulnerable code is reached → what happens inside the code → what is achieved.
**A reachability proof is mandatory**: the function really is publicly reachable, the attacker really has that privilege, and the path really goes through a real interface.

**3. Exploitability tiers**

| Tier | Condition |
|---|---|
| easy | public interface, no special privilege, single call |
| medium | needs a specific condition or elevated privilege, multi-step |
| hard | needs privileges or rare conditions, needs significant resources |

**4. Full exploitation scenario**: starting point → step by step (commands and arguments / why it works / how the system state changes) → **a concrete, testable impact**.

> Impact must **never** be written as "may cause problems". It must land on exact data, specific privileges, concrete quantities.
> If you cannot write it, you usually have not chased the impact far enough.

**5. Cross-check against the baseline**

- Does it violate a system-level invariant recorded in B.0?
- Does it cross or break a trust boundary?
- Does it bypass this codebase's habitual validation patterns?
- Is it a regression of a previously fixed issue?

---

## B.6 Report

**Output to chat only counts as failure.** It must be written to disk, or the findings are lost.

The report must cover at least:

| Section | Content |
|---|---|
| conclusion summary | severity distribution + overall judgment + key metrics |
| change overview | what changed, how big, which surfaces it touches |
| findings | each with location, origin commit, blast radius, test coverage, historical context, attack scenario |
| test coverage analysis | where the gaps are, why they count as gaps |
| blast radius analysis | the numbers and tiers |
| historical context | where deleted code came from, whether it was a security fix, whether there is a regression |
| recommendations | three tiers: block immediately / before production / technical debt |
| analysis method | which strategy was used, **what the limitations are**, confidence |
| appendix | evidence |

> **The "limitations" section is not a formality.** What was not tested and why must be written clearly —
> that is what lets the reader judge how far this report's conclusions reach.

**Scenarios where this stage does not apply** (say so explicitly, do not force it): brand-new code (no baseline to compare against), pure documentation changes, formatting/lint, and when the requester explicitly wants only a quick summary and accepts the risk.

---

## B.7 Handoff to Stage C

**Every suspected finding this stage reports must go through Stage C verification one by one — none may be written into the report as a conclusion directly.**

Stage B produces "suspicions"; only Stage C produces "verdicts".
Treating a suspicion as a conclusion is exactly the problem this project exists to solve.
