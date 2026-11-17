<div align="center">

# 🔍 FirstWhy

### Ask why until you hit the wall. Then break the wall.

**5Why × First Principles**, fused at the exact point where drilling stops working —
and closed with a verification gate that refuses to let coherence pass for truth.

An Agent Skill for Qoder, Claude Code, and any agent that reads `SKILL.md`.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)
[![Format](https://img.shields.io/badge/format-SKILL.md-blue.svg)](SKILL.md)
[![Dependencies](https://img.shields.io/badge/dependencies-none-success.svg)](#-design-notes)
[![Works with](https://img.shields.io/badge/works%20with-Qoder%20%7C%20Claude%20Code-orange.svg)](#-quick-start)

**English** | [简体中文](./README.zh-CN.md)

[**Quick Start**](#-quick-start) · [**How It Works**](#-how-it-works) · [**Examples**](#-worked-examples) · [**Anti-patterns**](#-anti-patterns) · [**SKILL.md**](SKILL.md)

</div>

---

## 💡 TL;DR

Most root-cause analysis stops one layer too early — at the layer where the answer becomes *"that's just how it's done."*

FirstWhy treats that sentence not as an answer but as **the target**. It splits it into real constraints and inherited habits, rebuilds from the constraints alone, walks back up the chain to prove every layer is accounted for, and then **verifies the one assumption the whole solution stands on**.

Invoke it with `/firstwhy <your problem>`.

---

## 🔥 Why the two classics fail alone

### 5Why hits a wall it cannot argue with

The drill goes down until the answer becomes a convention: *"everyone does it this way"*, *"it's the standard"*, *"legacy reasons"*.

**A drill cannot argue with a convention.** So you fix a habit, label it a root cause, and the problem returns a month later wearing a different face.

### First principles can break any wall but doesn't know where to start

It decomposes anything down to bedrock — but a complex problem decomposes in ten directions. Doing all ten is unbounded work, and you end up reinventing the wheel without ever touching the original pain.

### Each one's weakness is exactly what the other fixes

| | 5Why alone | First principles alone | **FirstWhy** |
|---|---|---|---|
| Can it break through "everyone does it this way"? | ❌ No | ✅ Yes | ✅ Yes |
| Does it know where to start decomposing? | ✅ Yes | ❌ No | ✅ Yes |
| Does it prove the fix covers every layer? | ❌ No | ❌ No | ✅ Yes |
| Does it verify its own ground assumption? | ❌ No | ❌ No | ✅ Yes |

---

## 🧠 The key insight: the stall point is the handoff point

Ask why until the answer hardens into an unexamined assumption. **That sentence is the target.**

Then split it:

<table>
<tr>
<th width="50%">✅ Real constraints — these count</th>
<th width="50%">🗑️ Inherited habits — void, re-choosable</th>
</tr>
<tr>
<td>

- Physically or mathematically unavoidable
- Genuine ceilings on cost, time, headcount
- Hard legal, safety, or compatibility requirements

</td>
<td>

- Someone's temporary choice at the time
- Carried forward, never questioned
- "Industry convention" nobody can justify

</td>
</tr>
</table>

> **The test**: every real constraint must state *what concretely goes wrong if it is violated*.
> Anything that cannot state a consequence goes in the habits pile.

Drilling locates **one** target, so decomposition stays bounded. Decomposition breaks the shell, so drilling doesn't stall. Neither works without the other.

---

## ⚙️ How it works

```
1 Pin down the symptom
2 Ask why ──reached something actionable──→ 5 Walk back up → 6 List assumptions → 7 Verify ground → Close
   │                                                ↑                          │
   └─hit "everyone does it this way"→ 3 Split → 4 Rebuild ┘                    │
                                                                  assumption falsified
                                                                        ↓
                                                              back to step 3, re-split
```

| Step | What happens | Skip when |
|---|---|---|
| **1** Pin down the symptom | One sentence. No causes allowed. Ask if vague — never guess. | never |
| **2** Ask why | Each layer needs evidence. Unevidenced guesses get marked `[assumption]`. **No preset round count** — stop at a stall or at something actionable. | never |
| **3** Split the target | Constraints vs. habits. Anything with no stateable consequence is a habit. | you reached an actionable cause |
| **4** Rebuild | **Reuse by default.** From-scratch design only when a constraint the existing solution depends on was falsified — and you must name which. | you reached an actionable cause |
| **5** Walk back up | Account for every layer. Any layer unexplained → you patched a symptom → back to Step 4. | never |
| **6** List assumptions | Every `[assumption]`, plus constraints lacking measured evidence. Each gets the cheapest possible test. | never |
| **7** Verify the ground | Sort into load-bearing vs. peripheral. Verify load-bearing **now**. Fail → solution void → back to Step 3. | never |

### The two steps that actually close the loop

Most frameworks stop at Step 4. FirstWhy doesn't, because Steps 5 and 7 catch two distinct failure modes:

**Step 5 — Walk back up** catches *half-fixes*. Logical coherence across every layer. In all four full-tier examples here, making only half the changes leaves a layer unexplained:

| Example | Half a fix leaves this unsolved |
|---|---|
| Skill library nobody uses | Verification gate but no routing → *"the agent can't find the skill"* |
| Stock investing | Prior expectations but no reconciliation → *"is the whole winning or losing"* |
| Recurring bug class | Reproduction tests but no static check → *"the same pattern elsewhere"* |
| ML experiment design | Unified config but no naive baseline → *"where does it beat the dumb approach"* |

**Step 7 — Verify the ground** catches *false ground*. Coherence is not truth. Skip this and the method is just issuing itself a certificate.

| | Load-bearing | Peripheral |
|---|---|---|
| Test | "If this is false, does the solution still work?" **No** | Yes, just less well |
| Action | **Verify now**, cheapest available test | Note it, watch while doing |
| If it fails | Solution void → back to Step 3, re-split | Adjust details, keep the skeleton |
| Count | Usually one or two | Everything else |

> **Ground verification should always be cheap.** If it's expensive, you probably picked the wrong assumption.

Until a load-bearing assumption has evidence, output is marked **`pending`** and must not be treated as an established conclusion for anything consequential.

**Closing condition**: every load-bearing assumption verified, *or* the target re-split and the new ground verified. Peripheral assumptions may stay open — demanding all of them makes the analysis unclosable.

---

## 🚀 Quick start

Flat layout, so one clone is the whole install:

```bash
# Qoder
git clone https://github.com/h4444433333/firstwhy ~/.qoder-cn/skills/firstwhy

# Claude Code
git clone https://github.com/h4444433333/firstwhy ~/.claude/skills/firstwhy

# Any agent that reads SKILL.md
git clone https://github.com/h4444433333/firstwhy <your-skills-dir>/firstwhy
```

Restart the agent so it reloads skills. That's it — no dependencies, no build step, no config file.

---

## 📖 Usage

```
/firstwhy our skill library has hundreds of entries but almost none get used
```

```
/firstwhy should we build a custom evaluation harness or adopt an existing one
```

```
/firstwhy this same null-handling bug keeps coming back after every fix
```

**Command first.** Without the command, the skill activates in only three situations:

- A requirement too vague to act on
- A design tradeoff needing defensible justification
- The same problem returning after it was supposedly fixed

It stays out of everything else — routine Q&A, lookups, clearly-scoped small changes.

Natural-language triggers also work: *5why*, *five whys*, *first principles*, *root cause analysis*, *why does this keep happening*.

### Not for

A single reproducible crash, error, or test failure. That belongs in a debugging workflow with evidence and reproduction steps (e.g. `systematic-debugging`). FirstWhy handles **structural recurrence**, not one-off failures.

---

## 📤 Output

Two tiers, chosen automatically by whether drilling hit a wall:

<details>
<summary><b>Light tier</b> — reached an actionable cause, no wall (a dozen lines)</summary>

```
Symptom: …
Chain: … → … → root cause
Solution: …
Walk-back: …
Load-bearing assumption: … (may be empty; if present, verify now)
Verification result: …
Status: closed / pending
```

</details>

<details>
<summary><b>Full tier</b> — hit a wall, ran decomposition and rebuild (about a page)</summary>

```
Symptom: …
Chain: … (marks which layer stalled, and the exact stalling sentence)
Target split:
  Real constraints: … (each with its violation consequence)
  Inherited habits (void): …
Rebuilt solution: … (states why existing solutions can't be reused)
Walk-back: accounts for every layer
Load-bearing (verify now): … → result: …
Peripheral (may stay open): … + tests
Status: closed / pending
```

</details>

**Both tiers always include the walk-back and ground verification.** Those are the only two non-negotiable steps.

---

## 📚 Worked examples

[`examples.md`](examples.md) contains five complete runs — not sketches, full chains with evidence, splits, walk-backs, and ground tests:

| # | Domain | Tier | The wall it hits |
|---|---|---|---|
| 1 | Project conventions re-explained every session | Light | — *(never stalls)* |
| 2 | A skill library nobody actually uses | Full | *"a skill is a written guide; once the model reads it, it'll naturally use it"* |
| 3 | Stock investing: every trade made sense, the year lost money | Full | *"following the information everyone watches can't be wrong"* |
| 4 | The same class of bug keeps coming back | Full | *"the tests are enough; fix it when it breaks"* |
| 5 | Experiment scores swing, unclear whether the method works | Full | *"get results first, add the protocol later"* |

Example 5 is worth reading even if you don't do ML — its two load-bearing assumptions have a **mandatory order**, and until the first one produces a number, "my method works" cannot be called true *or* false.

---

## 🚫 Anti-patterns

Eight are defined in [SKILL.md](SKILL.md#anti-patterns-any-one-of-these-is-a-failure). The three that bite hardest:

1. **Padding to five whys** — layers four and five are usually filler. If three rounds close it, use three. The "5" is a shape, not a quota.
2. **Treating a habit as a constraint** — *"everyone uses X"* is not a constraint. No stateable consequence → habits pile.
3. **Listing assumptions then treating the output as a conclusion** — the judge is written on paper but never seated on the bench.

And two that guard against the skill itself becoming a time sink:

7. **Verifying nothing** — see #3.
8. **Demanding every assumption be verified** — the analysis will never close. Verify the ground, leave the periphery open.

---

## 🏗️ Design notes

**Zero dependencies.** Four files, all Markdown plus one license. No runtime, no build, no package manager. A thinking method shouldn't need `npm install`.

**Flat layout.** `SKILL.md` sits at the repo root, so `git clone <repo> <skills-dir>/firstwhy` *is* the install. Nesting the skill in a subdirectory would force every user to move files by hand.

**Two content files, deliberately.** `SKILL.md` carries the method (~190 lines, under the 500-line budget for skill instructions). `examples.md` carries the worked runs. No badges directory, no docs site, no versioned changelog — for a method this size, packaging cost would exceed maintenance value.

**Boundaries are written into the skill, not left implicit.** Both `SKILL.md` and Example 4 state explicitly when to hand off to a debugging workflow. Two skills that quietly overlap produce contradictory output.

---

## ❓ FAQ

<details>
<summary><b>Why not just prompt "use first principles thinking"?</b></summary>

Because that's a vibe, not a procedure. Without a defined stall signal, a constraint/habit split test, a walk-back, and a ground-verification gate, the model produces confident-sounding analysis with no way to tell whether it reached the root or merely narrated it.

</details>

<details>
<summary><b>Why is "reuse by default" written into Step 4?</b></summary>

First-principles thinking has a well-known failure mode: it justifies rebuilding everything. Step 4 permits from-scratch design only when a constraint the existing solution depends on has been *falsified* — and requires naming which one. Without that brake the skill becomes an over-engineering machine.

</details>

<details>
<summary><b>Does it work for non-technical problems?</b></summary>

Yes. Example 3 is stock investing. The mechanism targets any domain where convention has replaced justification — process design, org decisions, product tradeoffs, personal systems.

</details>

<details>
<summary><b>What if the load-bearing assumption can't be verified cheaply?</b></summary>

Then you probably picked the wrong assumption. Across all four pending examples here, the ground tests cost: read a trade log, count 20 fix records, run ten tasks, run one dumb baseline. None required building a system. A genuinely expensive ground test usually means the real load-bearing claim is something else.

</details>

<details>
<summary><b>Can I use it in Chinese?</b></summary>

The skill files are English, but it responds in whatever language you write in. Natural-language triggers work in both.

</details>

---

## 🤝 Contributing

Issues and PRs welcome. Two things this repo is *not* looking for:

- Additional packaging (badges, docs site, CI, versioning) — see [Design notes](#-design-notes)
- New examples that don't complete the full chain including Step 7

What *is* wanted: examples from domains not yet covered, sharper anti-patterns observed in real use, and corrections where the method misfires.

---

## 📄 License

MIT © 2026 [h4444433333](https://github.com/h4444433333). See [LICENSE](LICENSE).

---

<div align="center">

**English** | [简体中文](./README.zh-CN.md)

**First, why?**

</div>
