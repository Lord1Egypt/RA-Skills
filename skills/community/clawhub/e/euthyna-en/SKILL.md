---
name: euthyna-en
description: 'The adjudication discipline and delivery gate for code security audits. Use when the user asks to audit the security of a piece of code, a pull request, a change, or to verify an existing vulnerability claim. It does three things: supply the deterministic facts a model cannot compute (callers, test coverage, git history origins), judge every claim against six gates, and downgrade any claim that cannot produce evidence to "observation" rather than a finding. The slash command may carry a mode word: pr = audit a change; graph = draw the provenance lineage of deleted code; repo = dependency surface only; claim = verify an existing vulnerability conclusion; gate = check an already-written report; help = print this table. With no mode word the full audit runs (the mapping table lives in the body). Not for: asking about the details of a single CVE, running an existing scanner once, pure documentation or formatting changes, or when the user explicitly wants a quick summary and accepts the risk.'
whenToUse: Use when the user asks to audit the security surface of code or a repository, verify whether a suspected vulnerability is real, decide whether a finding is exploitable, review whether a change introduces a security regression, or asks to "audit before delivery". For single-topic checks such as only searching for secrets or only checking dependency versions, use the dedicated specialist skill instead and do not trigger this one.
disable-model-invocation: true
user-invocable: true
---

# euthyna — the adjudication discipline for code security audits

> εὔθυνα: the audit every Athenian official had to submit on leaving office; you did not
> get to walk away without handing over your accounts. That is this skill's core
> mechanism: **saying "the audit is done" does not count. Evidence is handed over and the
> gates decide.**

**This skill does not find bugs; it polices conclusions.** Finding bugs is the model's and
the existing tools' job. This skill's job: every conclusion must pass the gates, and a
conclusion that cannot pass is downgraded to "observation".

---

## When to use / when not to use

**Use**:

- The user asks to audit the security surface of code, a repository, or a change (PR / commit / diff)
- The user brings a suspected vulnerability and asks "is this real" or "is it exploitable"
- The user asks to review whether a change weakened an existing security control
- The user asks to "verify before delivery"

**Do not use** (refuse directly or route to another skill):

- Only asking about a specific CVE or dependency detail → use a dependency audit tool
- Only asking to run an existing scanner and paste its output → that is a tool call, not an audit
- Pure documentation, formatting, or lint changes → no security surface
- The user explicitly wants a quick summary and accepts the risk → state that this is
  "non-audit mode" and do not apply this skill's adjudication format

---

## Three non-negotiable rules

These three rules are the entire difference between this skill and "tell the model to be
more careful". No stage, no path may skip them.

### Rule 1: measurable quantities come from commands, the model only interprets

Caller counts, test coverage, dependency versions, line numbers, commit hashes — **none of
these may be answered from impression**. The model may say "not measurable" when a command
is unavailable, but it must not estimate and then write the estimate into a conclusion as a
fact.

> This comes from a measured failure: a package showed "5+ maintainers" on the code hosting
> platform while the package manager's actual permission list had 1 person; another package
> with 160 million weekly downloads showed zero downloads in one data source. **Estimating
> numbers by feel is always wrong.**

### Rule 2: evidence is mandatory down to `file:line`; placeholders are banned

- Every claim cites a concrete location in the form `path:L123`, and `path:L123 (commit abc1234)` when a version exists
- `probably` / `likely` / "roughly" are banned — chase the real code, and if you cannot, say you cannot
- PoCs must not contain `TODO`, `...`, or `// attacker does something here`
- **Once a PoC is found to use an artificial bypass** (mock, stub, disabled check), that PoC is **invalid**

### Rule 3: missing data is not clean

Every criterion falls into exactly one of three states: **evaluated-clean / evaluated-flagged /
not evaluable for a stated reason**.

- A run that measured nothing produces "not evaluable", **not** "no problems found"
- Before citing any "clean" conclusion, read the coverage table first
- **Numbers must be quoted verbatim** — no re-deriving, rounding, or dressing up
- Finding nothing is not an endorsement

---

## Entry decision tree

```
What did the user give?
│
├─ An existing suspected-vulnerability claim ──► Stage C: claim verification
│   ("is this real", "is it exploitable")          read references/verification-gates.md
│                                                 ★ if the conclusion depends on "was it tested" → run coverage
│
├─ A change (PR / diff / commit) ───────────────► Stage B: change audit
│   ("is this PR safe")                            read references/change-audit.md
│                                                 ★ first command: euthyna audit --base <fork point>
│                                                   (history + deps in one run, see below)
│                                                 ★ if test coverage matters   → then run coverage
│
├─ A repository / dependency surface ───────────► Stage A: dependency audit
│   ("do the dependencies have problems")          read references/dependency-audit.md
│
└─ A full repository security audit ────────────► Stage B as the core, with A and C as sub-steps
```

★ = **run before reading code by hand**, not as a follow-up after reading. The deterministic
facts from the producers decide where the manual reading must be directed.

**Multiple stages may run, but stages must not substitute for each other.**
In particular: every suspected finding reported by Stage B must go through Stage C one by
one — never write it straight into the report as a conclusion.

### Modes (slash commands)

When a user arrives through a slash command, map the mode to the stage and the first
command using this table. **The table is maintained only here**; the host command files
(Cursor / OpenCode / Copilot / Hermes) point at this section instead of each keeping their
own copy.

| You type | Which branch | First command |
|---|---|---|
| `/euthyna pr` | Stage B, the change surface | `euthyna audit` (omit `--base` and the fork point is inferred and declared) |
| `/euthyna graph` | Stage B, the provenance view | `euthyna audit --graph` (`--base` may be omitted here too) |
| `/euthyna repo` | Stage A, the dependency surface | `euthyna deps --all` |
| `/euthyna claim <assertion>` | Stage C, the claim surface | `euthyna coverage --symbol <name>` |
| `/euthyna gate <report>` | Validating a written report | `euthyna gate <report>` |
| `/euthyna help` | Print this table only | run nothing, change no state |

`/euthyna graph` is not a new measurement: `--graph` only draws the attribution `history`
already emits, as Mermaid. **A missing second edge does not mean the content never moved** —
the boundaries are in references/fact-producers.md.

---

## The two deterministic measurements this skill ships

Callers, coverage, dependency vulnerabilities and secrets are **not re-built** (see the
division of labor at the end). But two things nobody else does — and a model cannot compute
reliably — are shipped by this skill as a zero-dependency CLI:

| Measurement | Question it answers | When it is **mandatory** |
|---|---|---|
| `audit` | **Both questions below in one run** (history traces original introducers by default + deps enumerates every lockfile dependency), one merged report | **the first command of every audit** (opening Stage B) |
| `history` | Which commit does the code this change **deleted** come from? Was that commit a security fix? | when re-running history alone (e.g. a different `--base`) |
| `coverage` | Was this symbol **ever actually invoked** by a test run? | when the report claims "tested / not tested" (Stage B / C) |

```powershell
# --base may be omitted: then the fork point is inferred as merge-base(HEAD, origin/main) and
# declared as range-inferred in the report. When given, it is used exactly as given:
node <euthyna repo>/bin/euthyna.js audit --base <pre-change revision> --repo <audited repo>

# history / coverage run alone when needed:
node <euthyna repo>/bin/euthyna.js history  --base <pre-change revision> --repo <audited repo>
node <euthyna repo>/bin/euthyna.js coverage --coverage <absolute path to coverage file> --symbol <symbol name>
```

⚠️ **A relative `node bin/euthyna.js` always fails.** During an audit the current directory
is the **audited project**, not the euthyna repo, and it will report `Cannot find module`.
Use the euthyna repo's path and pass the audited repo explicitly with `--repo` (`--base` /
`--head` resolve against it).

**Exit codes** — the difference between `2` and `0` is the reason this whole thing exists:

| Code | Meaning | What to do |
|---|---|---|
| `0` | measured, no security-related finding | continue, but **read the "criteria not evaluated" section** |
| `10` | measured, at least one fact classified `security` | **raise priority**, run each through Stage C; do not treat as a conclusion |
| `1` | usage error | fix the command. This is not a measurement result |
| **`2`** | **could not measure at all** | **must not be read as clean**. Change the measurement approach, or mark the criterion "not evaluable" |

When a command is unavailable (not installed, no checkout): **mark the criterion "not
evaluable" — never fill the gap with a hand estimate.**

Operations manual (commands, real output samples, failure modes): `references/fact-producers.md`.

### Execution discipline (reproduce commands and PoCs)

`--verify` and PoCs execute commands **on the user's machine**. Before running any
reproduce/verification command:

- **Get the user's explicit approval first**, listing the exact commands — never run
  an unannounced command
- Prefer a sandbox or throwaway container (e.g. Docker) whenever one can run the
  command; when sandboxing is impossible, state the risk before running
- A report's PoC is written for whoever receives the report; every command the agent
  itself runs during adjudication follows this same rule

---

## The fact contract (the interface between measurement and adjudication)

This skill defines the interface between the measurement layer and the adjudication layer:
`references/fact-contract.md`.

Key points:

- The contract carries only **facts** — no scores, no severity levels, no remediation advice
- Every fact must carry a **reproduce command** or **producing tool + version**
- **Scores must not be used as gates** (learned from `dsh-trust-check`: its contract explicitly says "do not use `score` or `band` as a gate")
- `approximate` facts **must not participate in gates**
- **`unknown` is not "clean"** — it is the most misused of the three states

How to read a fact (what it lets you infer, and **what it does not**): `references/fact-contract.md`.

---

## The adjudication format

Whatever path was taken, the output must land in this shape:

```
BUG #N TRUE POSITIVE — [one-line claim]
  All gates passed. Evidence: path:L123 (commit abc1234)
  Reproduce: <re-runnable command or PoC location>
  Exploitability: EASY / MEDIUM / HARD
  Impact: specific to funds / elevated privilege / exposed data

BUG #N FALSE POSITIVE — [reason for rejection]
  Gate N (gate name) FAIL: <specific evidence>
  e.g. line 98's check guarantees packet_size >= 16, so (packet_size - header_size) >= 8.
       Underflow is mathematically impossible.

BUG #N INCONCLUSIVE — [reason it cannot be decided]
  Gate N (gate name) NOT EVALUATED: <why>
```

**The third state `INCONCLUSIVE` must exist.** Trail of Bits' original fp-check has only two
states because it uses a Stop hook to force infinite continuation until completion;
**DSH cannot do that** (the Stop hook must rate-limit itself or it loops forever; the measured
record lives in the project repository's DSH stop-gate document). So this honest exit must exist — "not finished" must never be
written as `FALSE POSITIVE`.

---

## The programmatic gate check (euthyna gate)

The format above is not decoration: `euthyna gate <report file>` mechanically checks every
finding —

- **TRUE POSITIVE**: evidence must reach `path:L123`, a reproduce command is mandatory, impact
  must be stated, and all six gates must pass;
- **FALSE POSITIVE**: at least one gate FAIL with specific evidence;
- **INCONCLUSIVE**: at least one gate not evaluated, and no FAIL.

A finding that lacks evidence, lacks reproduction, or whose gates contradict its verdict
(such as a TRUE POSITIVE carrying a FAIL gate) is **downgraded to "observation"** and
reported with exit code `10` — the checker does the policing, no self-awareness required.

```powershell
node <euthyna repo>/bin/euthyna.js gate <report file>
# re-run each reproduce command to verify (allowlisted tools, argv execution, no shell):
node <euthyna repo>/bin/euthyna.js gate <report file> --verify --cwd <audited repo>
```

- Exit code `0` = everything passed; `10` = at least one finding downgraded; `2` = the report
  cannot be read / has no checkable finding.
- Under `--verify`, a reproduce command that fails to run is also a downgrade — "I can
  reproduce it" is not a claim until the run actually succeeds.

**Run `euthyna gate` on the report before handing it over.** It validates the report's own
self-declared claims; it does not audit the target repository — so it cannot replace
adjudication, it only guarantees that a conclusion without evidence cannot leave as
"established".

---

## The report must be written to disk

- Outputting only to chat is a **failure**. A report file is mandatory
- Filename: `<PROJECT>_EUTHYNA_AUDIT_<YYYY-MM-DD>.md`
- Fallback order when writing fails: current working directory → user desktop → temp
  directory → **last resort** only then output to chat and ask the user to save it manually

---

## Pre-delivery self-check (tick every item; without all of them you may not say "audit done")

- [ ] Every suspected finding went through **complete** Stage C, not "looked at it and it seems false"
- [ ] **Ran `audit` (or `history` when the diff has deleted lines)**; code deleted from a security-fix commit handled at highest risk
- [ ] Every "tested / not tested" sentence in the report is backed by `coverage` output, or marked "not evaluable"
- [ ] **No criterion with exit code `2` appears in a "clean" column**
- [ ] Every conclusion carries a `file:line`
- [ ] Every conclusion carries one of the three states (clean / flagged / not evaluable)
- [ ] The coverage table states **which criteria were not evaluated and why**
- [ ] All 13 devil's advocate questions answered (including the false-negative 12 and 13)
- [ ] The report file has been written to disk
- [ ] The report has passed `euthyna gate` (exit code `0`; if there are downgrades, read why)
- [ ] "Missing data" was not written as "clean"

---

## Reference files

Load on demand. **Do not read them all at once** — progressive disclosure is why this stays
effective in long sessions.

| File | Contents | When to read |
|---|---|---|
| `references/verification-gates.md` | **Stage C**: routing, the six gates, false-positive list, devil's advocate, PoC rules | when judging an existing claim (**most used**) |
| `references/change-audit.md` | **Stage B**: baseline, depth vs risk, origin attribution, blast radius, adversarial modeling | when auditing a change |
| `references/dependency-audit.md` | **Stage A**: manifests/lockfiles, the three states, report style, prohibitions | when auditing the dependency surface |
| `references/bug-classes.md` | Per-class checklists for 9 defect classes and their **default assumption direction** | once the defect class is chosen |
| `references/meta-mechanisms.md` | The six meta-mechanisms that keep the process from degrading into a formality | **read once at the start of an audit** |
| `references/fact-producers.md` | **Operations manual**: when to run the two measurements, how to write the commands, how to handle exit codes, real output samples, failure modes | **before running a producer** (Stage B / C) |
| `references/fact-contract.md` | Once you have a fact: what it lets you infer, **and what it does not** | after reading a producer's output |

> **The skill text is self-contained**: every file above lives inside `references/`, depends
> on nothing outside the skill directory, and the whole directory can be copied into any
> skill root.
>
> ⚠️ **But the producer is a separate program, not inside the skill directory.** Copying the
> skill does not carry the CLI along. A new environment must install it separately, or ship a
> checkout of this project; otherwise the related criteria can only be marked "not
> evaluable" — which is an honest result, better than a hand estimate. See
> `references/fact-producers.md` section 1.

---

## Division of labor with the existing ecosystem (no duplicated work)

| Already built by someone else | What euthyna does |
|---|---|
| Call graph / blast radius (`dsh-tool-lens`, `dsh-blast-radius`) | **does not rebuild**, consumes their output |
| Coverage (`dsh-code-coverage`) | does not rebuild, consumes its output |
| Dependency vulnerabilities (`dsh-dep-vuln-scan` etc.) | does not rebuild, consumes its output |
| Secret scanning (`dsh-code-security`) | does not rebuild, consumes its output |
| Delivery gate mechanisms (`dsh-doublecheck`, `formalswarm`) | mechanisms worth borrowing; euthyna's gate content is the **security-specific** six gates |
| Evidence lifecycle and PoC lab (`dsh-omv`) | can coexist: `dsh-omv` can be a **consumer** of the fact contract |

**euthyna only supplies the two deterministic measurements nobody else does** (the argument
lives in section 7.2 of the project repository's positioning document): the mechanical adjudication of git security regressions, and
the "symbol × real execution coverage" join.
