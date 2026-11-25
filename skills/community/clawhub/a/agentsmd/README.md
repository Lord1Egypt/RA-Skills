English | [简体中文](docs/zh-CN/README.md)

# agentsmd

**The pitfalls you hit — your AI never hits them twice.**

[![GitHub stars](https://img.shields.io/github/stars/kelegele/agentsmd-skill?style=flat-square)](https://github.com/kelegele/agentsmd-skill/stargazers)
[![skills.sh installs](https://skills.sh/b/kelegele/agentsmd-skill?style=flat-square)](https://www.skills.sh/kelegele/agentsmd-skill)
![Agent Skill](https://img.shields.io/badge/format-Agent_Skills-blue?style=flat-square)
![Claude Code](https://img.shields.io/badge/supports-Claude_Code-purple?style=flat-square)
![Codex](https://img.shields.io/badge/supports-Codex-black?style=flat-square)
![Cursor](https://img.shields.io/badge/supports-Cursor-gray?style=flat-square)

Hand this session's pitfalls and corrections to your AI, say "write the lessons into AGENTS.md", and it distills them into one-line executable rules in the project root's AGENTS.md. From then on, every new session — Claude Code, Codex, or Cursor alike — reads it before starting work and follows it.

> This skill came from my own endless "re-training" sessions. In every project there are things you want to cement: how this project builds, which boundaries must not be crossed, what coding conventions apply. If they don't live in AGENTS.md, you re-teach them to the agent in every new session — the same mistake three times, three corrections, all day gone.
>
> It became a habit: whenever there was a general rule to keep, I had the agent write it into AGENTS.md. Then a new problem crept in — the file grew into a pile of common sense, so bloated that the real rules drowned in it.
>
> So I thought: why not hand the cementing itself to a skill? Now I just say "solidify this session's lessons into AGENTS.md" and it handles collecting, distilling, merging, and verifying — I only approve. That's this skill.

## Start in 30 seconds

```bash
npx skills add kelegele/agentsmd-skill
```

Then tell your agent:

> Use agentsmd to solidify this session's lessons into AGENTS.md

Rather not install anything? Just paste the repo URL to your agent:

> Install this skill for me: https://github.com/kelegele/agentsmd-skill , then show me how to use it.

## What does it do for you?

| What you have | What it does with it |
|---|---|
| Pitfalls, corrections, repeated preferences from this session | Three-pass admission bar (will recur + real loss if violated + fits in one line), generalized into rules, compressed to one-line imperatives, written into AGENTS.md |
| An ever-fatter AGENTS.md | Five merge gates: discard equivalents / merge overlaps / generalize special cases / prefer the newer on conflict / delete outdated — unconditional appending is forbidden |
| Approaching the 120-line cap | Content still worth keeping moves to `docs/<topic>.md` with a one-line reference — pruning removes redundancy, not memory |
| A new project without AGENTS.md | Scans directory structure, README, and build/CI configs to generate one that fits; every command is run or cross-checked — nothing unverified gets written |
| A lesson that only applies to one subdirectory | Sinks into a local AGENTS.md for that subdirectory; the root file keeps globally applicable content only |
| A docs-only / data-only work directory (report library, collaboration space) | Auto-adapts: scans doc structure and naming conventions instead of build configs; rules lean toward data definitions, archiving, and delivery; collection relaxes the fixed buckets into a folder taxonomy that fits the work type |
| Documents and data files scattered at the root | Checks code references before proposing: docs go to `docs/<topic>/`, data to `data/<topic>/`; files move only after approval, and every broken link gets fixed |
| Memory, TODO / CHANGELOG of personal agents like Hermes / OpenClaw | Sediments project memory through the host's own mechanism — host format, dedupe first, approval before write; silently skips if there is none |

## Why not just "let the AI write one"?

Every new session starts from zero: the mistakes you corrected today repeat tomorrow, lessons scatter across dozens of session logs, and switching sessions or tools evaporates all of it. Let the AI write your guidelines and you'll get a 500-line "best practices" pile — half common sense, half commands that were never run. The fatter the file, the less anyone follows it.

agentsmd goes the other way: **one sentence per rule**, **a hard 120-line cap**, **every command verified**, **nothing written without your approval**. Guidelines are a constitution, not a landfill.

## How to ask for it, so it lands right the first time

**Solidify this session's lessons** (most common):

> Turn the pitfalls from this session into project rules

**Slim down an already-bloated guidelines file**:

> Update project guidelines: merge this session's lessons using the merge decision table; over 120 lines, delete before adding

**New project init**:

> No AGENTS.md yet — generate the first version with agentsmd; verify every command by actually running it

**Work directory (docs / data only)**:

> Sediment working rules for this collaboration directory, and collect the scattered reports, data, and reference material

**Archive while you're at it**:

> Write the lessons into AGENTS.md, and collect the docs and data scattered at the root

## From session to guidelines, it does seven things

1. **Collect lessons**: extracts errors you pointed out, pitfalls actually hit, preferences repeated (≥2 times), validated approaches; one-off details and common sense are excluded outright.
2. **Distill rules**: generalize → compress to one line → file into the closest section; three-pass admission, miss one and it's dropped.
3. **Read current state**: existing AGENTS.md gets a full rule inventory; none? Detect coding / work scenario first, then generate — coding verifies commands one by one, work verifies referenced paths.
4. **Organic merge**: a rule gets in only through the five gates; near 120 lines, delete before adding; valuable content migrates to `docs/`.
5. **Confirm and write**: presents the complete change plan (adds / merges / deletes / migrations / line count); files are touched only after your approval.
6. **Sync memory and progress**: rides the host, builds nothing new — if the agent has a memory mechanism, project memory settles in its format; TODO / CHANGELOG get updated too; no private memory formats, so it fits whichever agent it's installed in.
7. **Collect docs and data** (optional): checks references before proposing — docs to `docs/`, data to `data/` by default; work scenarios get a type-fitted taxonomy, recorded in AGENTS.md once approved; files move and links get fixed only after approval.

## What you end up with

- An `AGENTS.md` **≤120 lines**, sections fitted to the project, no placeholder fluff
- Migrated reference content in `docs/`, with one-line references in the root file
- Updated agent project memory and progress files
- A tidy, link-clean folder layout (`docs/`, `data/`, `references/` defaults; work scenarios a taxonomy fitted to the work type)

## Install

### Claude Code / Codex / Cursor (git clone)

```bash
git clone https://github.com/kelegele/agentsmd-skill.git ~/.claude/skills/agentsmd   # global
git clone https://github.com/kelegele/agentsmd-skill.git .claude/skills/agentsmd    # this project only
```

### Manual copy (any agent)

Copy the repo into the agent's skill directory, folder named `agentsmd`:

| Agent | Global skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |
| Cross-agent | `~/.agents/skills/` |
| WorkBuddy | `~/.workbuddy/skills/` |

### WorkBuddy URL import

Sidebar **Skills → Add Skill → Import via URL**, paste `https://github.com/kelegele/agentsmd-skill`, confirm to enable.

### Install from skill marketplaces

```bash
clawhub install agentsmd   # ClawHub (OpenClaw ecosystem: openclaw skills install agentsmd)
```

Also available on the [LobeHub Skills Marketplace](https://lobehub.com/skills/kelegele-agentsmd-skill).

> Note: some agents need a restart or a new conversation to load new skills.

## Update

Follow the way you installed it (per-version changes in the [CHANGELOG](CHANGELOG.md)):

**npx skills install**: use the CLI's own update command

```bash
npx skills update agentsmd   # updates agentsmd only; without a name, updates all
```

**git clone install**: pull in the cloned directory

```bash
git -C ~/.claude/skills/agentsmd pull   # global install path; adjust for project-local installs
```

**Manual copy**: overwrite the skill directory with the repo contents.

**WorkBuddy URL import**: redo "Skills → Add Skill → Import via URL".

> Note: after updating, some agents need a restart or a new conversation to load the new version.

## FAQ

**Will it make the AI pile up generic common sense?**
No. Every write passes the three-pass admission bar, and "no piling up generic common sense to look complete" is hard-wired into the workflow.

**What if a command in the guidelines doesn't run?**
Every first-version command must be actually run, or cross-checked against build / CI configs; anything that fails or can't be verified is never written.

**Will the file grow forever?**
No. Hard cap 120 lines, new rules must pass the merge gates, "append-only" is explicitly forbidden by the workflow.

**Does it work with other agents?**
Yes. AGENTS.md follows the open [agents.md](https://agents.md/) spec — Claude Code / Codex / Cursor / Gemini CLI / OpenCode / WorkBuddy all read the same file.

**Personal agents like Hermes / OpenClaw?**
Yes. The skill is pure Markdown — no build, no dependencies, not tied to any CLI; if the agent has a memory mechanism, memories settle in its own format (dedupe first, approval before write); if not, it skips silently.

**Non-code directories?**
Yes. Once detected as a work scenario it adapts automatically: scanning shifts to doc structure and naming conventions, rules lean toward data definitions, archiving, and delivery, and collection frees itself from the fixed `docs/ data/ references/` buckets — the agent proposes a folder taxonomy that fits the work type (approval still required, then recorded in AGENTS.md). The AGENTS.md format stays the same.

**Will it touch files without my consent?**
Never. Every write — AGENTS.md, memory, progress files, moving documents — is proposed first and executed only after approval.

## Repository structure

```
agentsmd/
├── SKILL.md                     # core workflow (7 steps)
├── references/
│   └── agents-md-spec.md        # agents.md spec summary
└── assets/
    ├── AGENTS-template.md       # section skeleton (standard + optional sections)
    └── AGENTS-example.md        # official agents.md sample as a finished-file benchmark
```

> The above is the skill package itself — that's all that gets installed. The repo also contains project collaboration files (HANDOVER.md, docs/, scripts/, .zcode/, etc., Chinese docs under [docs/zh-CN/](docs/zh-CN/)); they are not part of the skill.

## Related

- [project-handoff-skill](https://github.com/kelegele/project-handoff-skill) — hand work across agents without re-explaining. agentsmd remembers *how* to work; project-handoff remembers *where you left off*.
- Blog: [design philosophy](https://www.kelegele.com/blog/agents-md-lessons-without-bloat) · [two months of iteration](https://www.kelegele.com/blog/agentsmd-skill-iteration-retrospective) · [usage guide](https://www.kelegele.com/blog/agentsmd-scene-guide)

## Feedback

Issues and ideas are welcome at [GitHub Issues](https://github.com/kelegele/agentsmd-skill/issues). More projects on the author's site [kelegele.com](https://kelegele.com).
