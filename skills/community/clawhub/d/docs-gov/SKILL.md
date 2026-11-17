---
name: docs-gov
description: >-
  Installs a documentation governance architecture in a project and diagnoses what it is missing.
  Three actions: audit diagnoses the current state against seven components (source-of-truth
  layering / decision records / cascade discipline / planning system / checkpoints bound to
  actions / gates / incident traceability); init installs what is missing (config, a script copy,
  a pre-commit gate, two Claude Code hooks, decision and plan templates); check keeps verifying
  that what the docs claim about reality still holds (TODOs left hanging too long, cascade memos
  never carried out, plan status that doesn't match reality, broken references, broken links,
  § section references pointing to the wrong place, missing index entries, broken tables,
  endpoints the docs declare but the code doesn't have).
  The framework was distilled from the documentation system of a large protocol project, and every
  check is tied to a real incident. ⚠️ init modifies the repository and installs hooks that keep
  running after the session ends (a git pre-commit gate and two Claude Code hooks that can block
  commits and new plan files); without --yes it only lists the planned changes. audit and check
  are read-only. Use only when the user explicitly asks about documentation governance in the
  current repository: "doc governance", "audit the docs against the code", "set up a documentation
  system for this project", "audit before I write a plan", "is the spec the single source of
  truth", or when a commit or file write was blocked by this skill's own gate output.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - git
      config:
        - .doc-governance.json
        - .claude/settings.json
    envVars:
      - name: DOC_GOVERNANCE_HOME
        required: false
        description: Where the skill is installed, if not in ~/.claude, ~/.cursor or ~/.codex skills. Used only by the installed pre-commit hook to find the source for its read-only drift comparison; never used to choose what init installs.
      - name: CLAUDE_PROJECT_DIR
        required: false
        description: Set by Claude Code; the two installed Claude Code hooks use it to find the project root.
---

# docs-gov

> What the system actually does and what the team believes it does have diverged, **and no measurement anywhere lets anyone see the divergence**; every fix starts by making it visible.
> — the core diagnosis from a real project postmortem, and the master principle of this whole thing

The framework is distilled from the documentation system of a large protocol project ([framework.md](framework.md) holds the criteria, including what was deliberately not ported).
**It is a program, not a style guide**: the reasoning lives in [incidents.md](incidents.md) and in the tests —
Of the 181 tests, **141** name the incident they guard against in their docstring, so every run restates it;
the other 37 are positive cases (verifying that what shouldn't be reported isn't), with no incident to name.

Dependencies: `python3` (3.10+, standard library only) and `git`. Running the self-tests needs `pytest`.

## What it touches

| | Scope |
|---|---|
| **Reads** | Only files inside the repository given by `--root`: `.doc-governance.json`, Markdown under the configured directories, files matched by `contract_checks`, and — for `audit` — root entry docs (`CLAUDE.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `BRIEFING.md`), `.github/workflows/`, `scripts/`, `.claude/settings.json`. Config paths must be repo-relative — absolute paths and `..` are refused, and anything that resolves outside the repo through a symlink is skipped, never read. |
| **Writes** | `audit` and `check` write nothing. Only `init --yes` writes, and only these: `.doc-governance.json`, `scripts/governance.py`, `.githooks/pre-commit` (+ a forwarding shim in `.git/hooks/pre-commit` if none exists), `.claude/hooks/` (two scripts), their registration in `.claude/settings.json`, and a `README.md` template in the decision/plan directory if that directory is missing. Existing files are left alone; a pre-existing `.claude/hooks/` script is registered only if it is byte-identical to the bundled one. |
| **Runs** | `git log` / `git rev-parse` (read-only, fixed argument lists, no shell). The installed hooks run `python3 scripts/governance.py check`, `git`, `jq`, and `find`. |
| **Persists** | The pre-commit gate blocks commits whose `.md` changes fail the checks; the Claude Code hooks block creating a new `PLAN-*.md` / `TASK-*.md` while checks are red, and report cascade problems after a decision record is edited. Remove them by deleting those files and the two entries in `.claude/settings.json`; skip once with `git commit --no-verify`. |
| **Environment** | Reads `HOME` (to find the skill in the common install directories), and in the installed hooks `CLAUDE_PROJECT_DIR` and, for pre-commit's drift comparison only, `DOC_GOVERNANCE_HOME`. Nothing else. What `init` copies is always the `governance.py` you ran and the `templates/` beside it (or, when running from a copy, the ones in a common install directory) — never something an environment variable points at; the plan printed before `--yes` shows the source file and its sha256. |
| **Network** | None. |

**Document language**: checks recognize both English and Chinese phrasing — deferred promises (“rewrite once X is confirmed”, “TODO: update after …”), `Status:` lines and `| Status |` table rows, `## Cascade memo` sections, implementation-status labels (“deprecated”, “not yet implemented”, “planned”), source-of-truth declarations, and “before/after X, run Y” checkpoints. Detection is pattern-based: unusual phrasing can slip through, so treat a clean run as “nothing detected”, not proof.

## Three actions

```bash
S=<skill dir>/governance.py          # e.g. ~/.claude/skills/docs-gov/governance.py

python3 $S audit --root .            # diagnose: each of the seven components present/partial/missing + what goes wrong without it
python3 $S init  --root .            # list what would be installed, change nothing
python3 $S init  --root . --yes      # install
python3 $S check --root .            # continuous checks (nine modes)
python3 $S check --root . pending    # run just that one
```

**Run `audit` the first time you enter a project.** It is read-only and changes no files; it outputs the project's governance maturity,
plus which past incident each missing piece sets you up to repeat.

## What audit checks (G1–G7, criteria in framework.md)

| | Component | In one sentence |
|---|---|---|
| G1 | Source-of-truth layering | Is it written down who is authoritative for what? |
| G2 | Decision record system | Sequential numbering, an index, consistent metadata conventions |
| G3 | Cascade discipline | Which documents each decision lands in, verifiable item by item |
| G4 | Planning system | What is being done now and how far along it is **+ whether there is a second, abandoned answer** (a scaffold ledger more than 30 days behind the repo) |
| G5 | Checkpoints bound to actions | Is it written down **+ is a device bound to it** (written only in a doc = a sticky note) |
| G6 | Gates | Can both CI **and** local commits block it? |
| G7 | Incident traceability | Every gate states the failure it guards against |

⚠️ **G3 and G7 can't be installed** — they only come from filling them in as you write docs. audit lists them separately and doesn't pretend a single command fixes them.

`init` installs four devices: `.doc-governance.json`, a copy at `scripts/governance.py`,
`.githooks/pre-commit`, and **two Claude Code hooks** —
one runs the full check when a new `PLAN-*.md` / `TASK-*.md` is created and hard-blocks on red (this is the moment CI can't catch),
the other checks the cascade right after a decision record is edited. All of them live in the project and go into git. In addition, if the decision directory or plan directory is **missing**, it adds a README template (existing ones are left alone).
`pre-commit` also carries a **copy comparison**: if `scripts/governance.py` differs from the skill source, the commit is blocked (skipped when the source can't be found, so CI is unaffected).
For that comparison the hook looks for the source in this order: env var `DOC_GOVERNANCE_HOME` → `~/.claude/skills/docs-gov` →
`~/.cursor/skills/docs-gov` → `~/.codex/skills/docs-gov`. If you installed it elsewhere, set the env var. (The variable only affects this read-only comparison; what `init` installs is always the script you ran.)
Cursor projects have to write an equivalent `.mdc` themselves.

## The nine check modes

`pending` TODOs left hanging too long · `cascade` cascade memos never carried out · `status` plan status doesn't match reality ·
`refs` decision references broken or circular · `links` broken links · `sections` § section references pointing to the wrong place ·
`index` decision directory and index out of sync · `tables` tables that will break when rendered ·
`contract` **endpoints/fields the docs declare that the code doesn't have**

`contract` needs `contract_checks` configured in `.doc-governance.json` (how to read the doc side, how to read the code side) —
every framework is different, so this can only be configured; if a bad config leaves the code-side extraction empty, it reports a self-check failure instead of pretending to pass.
If the doc line marks an implementation status (retired / planned / …), it is skipped: **honest labeling is the fix, not a violation**.

**Self-check**: missing config, nonexistent directory, zero files scanned — all red.
"The checking mechanism itself stops working and doesn't report it" is exactly the disease this whole thing exists to prevent.

**This skill is watched by contract too** (the self-audit group at the end of `test_governance.py`):
the mode list matches `ALL_MODES` · no advertising modes that don't exist · the mode count stated in prose must equal the real count ·
everything `init` installs must be documented · G1–G7 consistent across code / SKILL.md / framework.md ·
every mode has an incident in `incidents.md` · test counts match the docs.
**Add a feature without updating the docs, and the tests go red.**

## When to run check

| Moment | Why |
|---|---|
| **Before writing a new plan** | The most important one. CI can't catch "a compliant new plan written on top of an outdated spec" |
| After changing a decision | Did the cascade memo actually get carried out |
| After a bulk rename/move | Broken links and § references |
| Every commit (with .md changes) | The pre-commit installed by init runs it automatically |
| Every PR | Wire it into the project's existing CI |

## How to ask

**Trigger:** when the user asks how to use **doc-governance itself** — e.g. “how do I use docs-gov”, “what is docs-gov for”, “docs-gov tutorial” (a bare “help” in an unrelated conversation is not this),
**reproduce the block below verbatim, then stop** — don't follow up with "which situation are you in?".
Someone asking this is **reading**, not **doing**; a follow-up question turns a reading request into a commitment they never meant to make.

---

**The most important thing first: once installed, you don't need to call me day to day.**
`pre-commit`, CI, and the two Claude Code hooks will stop you on their own — you only need to step in when something goes red.

When you do want to ask, use the table below — these are typical situations, not fixed syntax; say it another way and it will still be recognized:

| | Typical situation | What I'll do | Command |
|---|---|---|---|
| A | The docs in this project are a mess and I need to know where things stand | Run a diagnosis and report which pieces are missing and what went wrong in the past without them | `audit --root .` |
| B | My last commit got blocked and I want to know why | Find which rule blocked it and explain what it guards against | `check --root .` |
| C | What the docs say doesn't match the code | Compare every endpoint/field the docs declare against the code, one by one | `check --root . contract` |
| D | I don't understand what this red error is guarding against | Dig up the real incident behind it and decide whether to fix the doc or the checker | (none — see incidents.md) |
| E | I want something to keep an eye on the docs automatically from now on | Install four automatic checks so you don't have to remember | `init --root . --yes` |
| F | I want to know the overall state right now | Run the checks and report where the docs and reality disagree | `check --root .` |

The command column omits the `python3 $S` prefix (`S=<skill dir>/governance.py`).
To start now, say any of the sentences in A–F, or just reply with the letter. If you only wanted to look, you can stop reading here.

---

(Everything above is the text for the user. Below are notes for myself:)
Typing `/docs-gov` works the same as plain language, just more deterministically.
`python3 $S check --root .` doesn't need AI — it's exactly what CI and pre-commit run.

> **This section was forced into existence by four pieces of real feedback**:
> ① "Do I need its commands, or does plain language work?" — at the time the docs didn't say how to ask.
> ② After that was added, someone pointed out the example sentences were all jargon ("documentation system", "spec", "cross-check") —
> **whoever writes the examples already knows how to use the tool, so their perspective is wrong by default**; real beginners describe symptoms, not tools.
> ③ The original plan was to list the options and then ask "which one sounds like you?" — rejected:
> **"tutorial" is a reading intent, not an execution intent**; a follow-up question forces a commitment. Changed to plain statements that leave an exit.
> ④ Added the letter column (A–F) and the command column, and renamed the heading from "You can say" to "Typical situation" —
> **the letter and command columns don't carry the risk from ②**: they mark "this is a different thing", not "this is the only way to say it".
> But there was also a proposal to rename the heading to "Commands", which would have stitched back the "you must recite this exactly" implication that ② had just removed;
> "Typical situation" was used instead — the sentences are still symptom-shaped, the tone just moved from purely colloquial to a balance of professional and plain.

## Installing in a new project

1. `audit` to see what's missing → 2. `init --yes` to install → 3. **Manually** wire `check` into the project's existing
verify/CI chain (don't build a new mechanism, hook into the existing one) → 4. Add this project's own incidents under the `incidents.md` section "Project-specific additions".

## How to read the output

**When it goes red, read the matching incident in `incidents.md` first, then the line number.** Most of the time what you need isn't "which line is wrong"
but "why this kind of error is dangerous" — that decides whether you fix the doc or fix the checker.

⚠️ **An inaccurate checker is worse than no checker**: people start distrusting its output, then ignore the real hits along with the false ones.
The first run on a real repo reported 26 findings, 7 of which were bugs in the checker itself — every one of them got a regression test.
(Those two numbers were counted on the spot and can't be recomputed after the fact; the regression tests themselves are in the repo and can be checked.)
