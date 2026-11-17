# 🧠 Context Compactor

[![SkillQA CI](https://github.com/vnbochkarev-netizen/context-compactor/actions/workflows/skillqa-ci.yml/badge.svg)](https://github.com/vnbochkarev-netizen/context-compactor/actions/workflows/skillqa-ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![npm](https://img.shields.io/npm/v/@vibo-dev/context-compactor)](https://www.npmjs.com/package/@vibo-dev/context-compactor)

<p align="center"><img src="assets/banner.svg" alt="Context Compactor" width="100%"></p>

**Condense a long agent session into a handoff memo — decisions, open tasks, risks, facts — without losing what matters.**

Every agent developer knows the pain: your session grows to 200k tokens, context gets
compacted, and **the important stuff vanishes** — the decision you made, the task you
promised, the URL you need tomorrow.

Context Compactor reads a raw transcript (txt/md, any language mix of **Russian/English**)
and produces a compact **handoff memo** grouped into:

- ✅ **Decisions** — what was actually decided
- 📌 **Open tasks** — what still needs to be done
- ⚠️ **Risks** — blockers, broken things, dependencies
- 🔗 **Facts & links** — URLs, handles, versions

## Safety first: credential values are redacted

Handoff memos travel to other agents and files. Context Compactor therefore
**redacts credential values** before scoring: `password`, `token`,
`api key`, `secret`, `private key`, `sk-…`/`ghp_…` tokens, JWTs,
URL-embedded credentials and PEM key blocks become `<REDACTED: …>`.
The decision/context around them is kept — the secret value is not.

> ⚠️ Redaction is **best-effort pattern matching**, not a guarantee.
> Review generated memos before sharing them, especially when transcripts
> may contain credentials, tokens, private URLs or other sensitive details.
> For conservative output use `--strict` (whole suspect lines are dropped).
> `--self-test` asserts the covered cases (incl. URL creds, JWT, Cyrillic,
> PEM blocks larger than 600 chars).

## Why you need it

- Survive context compaction: paste the memo back into the next session.
- Hand work to another agent (or a human) without dumping 500KB of transcript.
- Daily session digest in one command.

## Install

```bash
# direct (recommended — runs the reviewed source)
python3 compactor.py --input session.md

# npm — pinned release, version-synced with this repo (any OS with Python 3.8+).
# The package ships the exact reviewed source: compactor.py, the bin/ wrapper and
# SKILL.md (see package.json "files"). npx asks for confirmation before downloading.
npx @vibo-dev/context-compactor@1.1.7 --input session.md

# ClawHub / OpenClaw registry: install "context-compactor-cli"
# GitHub: clone this repo
```

## Quick start

```bash
git clone https://github.com/vnbochkarev-netizen/context-compactor
cd context-compactor

# Condense a session transcript
python3 compactor.py --input session.md

# Save to a handoff file for the next session
python3 compactor.py --input session.md --output handoff.md

# Verify the tool itself
python3 compactor.py --self-test
```

No dependencies. Python 3.8+. Works on Linux/macOS.

## How it works

Heuristic line scoring (no LLM, no API costs, runs offline):

- Decision verbs: "decided / agreed / we will" (Russian equivalents are covered)
- Task markers: "todo / next step / don't forget" (Russian equivalents covered)
- Risk words: "broken / blocker / depends on" (Russian equivalents covered)
- Links, handles and version-like facts get boosted
- Code dumps, tool output and noise are filtered out
- Bucketing is context-aware: "agreed, link: <url>" is a **fact**, not a decision;
  strong verbs ("decided" and Russian equivalents) always win
- Long transcripts: the head AND the tail are analyzed (final decisions usually sit at
  the end); skipped middle is counted and reported in the memo header, which also carries
  the tool version, date and source file

## Example memo

```markdown
# Handoff memo (auto-compacted)

## ✅ Decisions
- decided to build skill-injection-scanner in Python, MIT-licensed
- agreed: we publish tomorrow

## 📌 Open tasks
- need to run the tests before publishing

## ⚠️ Risks
- risk: without tests there will be many false positives

## 🔗 Facts & links
- project repo: https://github.com/vnbochkarev-netizen/skill-injection-scanner
```

## Use cases

- **Handoff files** after context compaction (Hermes, Claude, OpenClaw, Codex…)
- **Agent-to-agent handoff** — pass the memo through an agent bridge
- **Daily digests** — what did we actually do today?

## License

MIT © 2026 Viacheslav Bochkarev
