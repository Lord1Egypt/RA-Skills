# METHOD — how breakage gets in, and what covers it

For whoever changes this skill: a maintainer, an auditor, or an agent asked to
"fix the findings." RESIDUAL_RISK.md says what the tool does not protect
against. This file says how the *tool itself* gets worse while every check
stays green — and what the method does about it, in code where code can, and
in stated rules where only judgment can.

Everything here comes from a defect this skill actually shipped (v1.2.1), not
from a list of things that might go wrong.

## 1. Three pressures, and how each one gets a defect through

| Pressure | How it slips (a real instance) | What covers it | What it leaves unseen |
|---|---|---|---|
| **Efficiency** — the quick call, the cheaper check | `--stow-to` copied with `shutil.copy2`: one line, and it sat beside a hardening pass that fixed every *other* write. The result followed a planted symlink and then reported a verified copy. The "restore drill" re-reads members in memory (cheaper than extracting to disk), while its name, message and docs described a restore rehearsal, and a leftover `rmtree` still ran on a directory it never wrote to. | **Code:** the sink inventory (`tests/check_sinks.py`, T40) lists every write/spawn/archive call and *refuses* pathname-reopening writers outright; the import allow-list makes "no network *code* in this script" a checked claim (commands the operator supplies — `--stow-cmd`, a ledger adapter — can reach a network by design; that is consent-gated, not scanned). **Rule:** R3, R7. | The inventory is syntax over one file. A registry row can be filled in carelessly; a sink reached through a construct the scan does not model is invisible to it (RESIDUAL_RISK 14). |
| **Control** — a gate that looks finished from one side | The "single-line" validators rejected `\n`, `\r`, NUL. The reader split lines with `str.splitlines()`, which also breaks on ten more characters, so a note validated as one line was read back as two, the second a forged ledger entry. Every check passed; the two halves disagreed about what a line is. | **Code:** one `has_line_break` definition, tested exhaustively against `str.splitlines()` over all of Unicode; enforced at the single `ledger_append` chokepoint; readers split on `\n` only; `LEDGER-ANOMALY` alarms on a poisoned line. **Rule:** R3, R6. | A third consumer that tokenizes differently (the far end of a command adapter, a human with `grep`). The exhaustive test pins Python's definition, not every tool's. |
| **Profit / incentive** — anything that rewards the *appearance* of soundness: a registry's audit badge, a ship date, a feature's appeal | A green scan is a target, and fixes drift toward what a scanner can see: the three High defects fixed in 1.2.2 were all invisible to it. A gate that prints `PASS` is read as stronger than the check behind it. New features (`stow`, `evict`, `ack-policy`) arrive because they make the skill more useful, and each one widens what the tool can do. | **Rule:** R1, R4 — a finding is closed by a reproduction, never by a rewording; a feature pays the standing rule *and* a registry row in the same change. **Code:** T40 turns "what can this tool now do?" into a diff somebody must read. | The incentives of the *reviewer* (a person or a model asked for "looks fine"). Nothing here detects bad faith; the method assumes maintainers who want the true answer, and is only a speed bump for those who do not. |

## 2. What each frame leaves unseen

A frame is how a question is asked. Each one below was in use, was reasonable,
and hid something that then shipped.

| Frame | It sees | It leaves unseen | Instance |
|---|---|---|---|
| **Scanner** (pattern categories over text) | `shell=True`, `subprocess`, persistence words | Semantic defects: writer/reader disagreement, false success claims, tests that cannot fail, tests that fail for the wrong reason. It also reads test fixtures and changelog prose as if they were behavior. | Of the 25 findings the 1.2.1 audit page lists in detail (its header says 32), 18 were test fixtures or changelog prose; none of the real defects was a finding. |
| **Threat model** ("config is adversarial; the operator is trusted") | Planted configs, planted paths, consent | *Data the operator legitimately handles turning into control in a trusted format* — a filename or a pasted note reaching the ledger. The operator's own clean keystrokes were assumed; agents paste untrusted text. | Newline-bearing member names and U+2028 notes forged ledger entries. |
| **"Witness, not gate"** | That a failure must not block the work | That a witness whose *reader* can be fooled is not a witness; and that a warn-only failure which **reports success** does more damage than a gate that blocks, because the failure is false evidence, not missing enforcement. | `stow: MATCH (hash roundtrip)` printed after the bytes landed through a symlink. |
| **"All green"** (the suite) | What was asked | Assertions that cannot fail (a substring token that contains its own failure token); assertions that fail only in another environment; behavior with no assertion. | A `NOT_REFUSED` / `REFUSED` substring match; `chmod 555` failing to stop root. |
| **Names** ("restore drill", "verified", "recoverable") | The strong reading | The weaker thing actually implemented. People trust the name, not the code. | G8 re-reads and hashes; it does not restore. |
| **"Every X" / "no X" sentences** | An intent | A counterexample nobody enumerated. | "Every temporary write is staged"; "no network" (true of the code, not of what an operator's own command may do). |

## 3. Admission rules

These are followed by people and agents when they change the skill. They are
judgment, not code; section 4 says which parts are also code.

- **R1 — Reproduce before fixing, and before dismissing.** A finding is closed
  by a reproduction (fixed) or a written reason in the changelog (disagree).
  "Known noise" is argued per finding, with the excerpt, not per category.
- **R2 — Mutation-check every regression test.** Run it against the code from
  before the fix; it must fail there. Use non-overlapping tokens in substring
  assertions. A test that has never been seen failing has not been shown to test.
- **R3 — Check each claim from the other side.** For every validator, run the
  consumer. For every "every X" or "no X" sentence, name the inventory that
  makes it checkable, or scope the sentence. For every status line, ask what
  the code actually did.
- **R4 — No edit whose purpose is the score.** Do not reword, rename, move or
  delete evidence (changelog prose, test fixtures, tests) to change a scanner
  result. Change text only when it is wrong or unclear to a human, and say so.
  If a finding is a coverage limit (a file too large to inspect), record it; do
  not remove the reference.
- **R5 — Vary the environment.** Run the suite as root and unprivileged, and
  run the new tests against the previous release.
- **R6 — A control names its blind spot in the same change** (the standing rule
  in RESIDUAL_RISK.md), and fails loud, not silent.
- **R7 — When the fix is smaller than the claim, change the claim.** The drill
  was not made to extract to disk (double the I/O, a decision for the
  operator); its name's promise was brought down to what it does, in the code,
  the message, and the docs.

## 4. What is code and what is judgment

| Enforced by the suite | Left to judgment |
|---|---|
| T40: sink inventory vs `tests/sink_registry.txt` — new/changed/stale rows, banned kinds (`shutil.copy*`/`move`, `open(…,'w'/'x')`, `os.open`), import allow-list, dynamic features (`eval`, `exec`, `__import__`, `importlib`, `getattr(os, …)`), the file set of `scripts/`. The tripwire is itself tested by planting each kind of drift. | What a registry **reason** says, and whether it is true. R1–R7. Which frames apply to the next change. |
| T37: every `str.splitlines()` separator refused by writers, inert to readers, alarmed. | Whether a new consumer of the ledger tokenizes the same way. |
| T38/T39/T41: stow staging, hostile names, drill honesty. | Whether the drill should become a true restore rehearsal. |

## 5. When the tripwire fails

1. Run `python3 tests/check_sinks.py`. Read each line; it names the function.
2. For a **NEW** sink ask: who chooses the path (operator CLI, config, archive
   content)? Does it reopen a pathname (then it is banned — stage it)? What is
   the boundary it crosses, and which check runs first?
3. Add the row with a class and a reason a skeptic could disagree with.
   `--print` emits `TODO` on purpose: regenerating the file and pasting it in
   is the failure this exists to make visible.
4. Add the blind spot to RESIDUAL_RISK.md in the same change.
