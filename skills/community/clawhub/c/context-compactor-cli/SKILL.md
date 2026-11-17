---
name: context-compactor-cli
description: "Condense a long agent session transcript into a compact handoff memo: decisions, tasks, risks, facts & links. Credential values are auto-redacted before output (best-effort - review memos before sharing; --strict drops whole suspect lines). EN/RU heuristics, zero dependencies. The CLI prints what it reads and where it writes. Use ONLY with the user's explicit consent: tell the user which transcript file will be read."
version: 1.1.7
tools: [python]
license: MIT
---

# Context Compactor

**Local-first. No telemetry, no cloud sync — the transcript you feed it never leaves your machine.**

## When to use
- Your session is about to be compacted and you want a handoff memo to paste into the next one.
- You hand work to another agent (or a human) without dumping 500 KB of transcript.
- You want a daily digest of what was actually decided and what is still open.
Don't use for: summarizing code repositories, translating documents, chat-style Q&A.

## Quick start
```bash
# from this package (or the git repo: github.com/vnbochkarev-netizen/context-compactor)
python3 compactor.py --input session.md
python3 compactor.py --input session.md --output handoff.md
python3 compactor.py --self-test
```

## Safety first: credential values are redacted (best-effort)
Handoff memos travel to other agents and files. Context Compactor **redacts credential values**
before scoring: `password`, `token`, `api key`, `secret`, `sk-…`/`ghp_…` tokens,
JWTs, URL-embedded credentials and PEM private-key blocks become `<REDACTED: …>`.
The surrounding decision/context is kept — the secret value is not.

⚠️ Redaction is **best-effort pattern matching** — review memos before sharing them.
`--strict` drops whole lines that still carry a credential marker.
`--self-test` asserts the covered cases (incl. URL creds, JWT, Cyrillic, PEM > 600 chars).

## How it works
- Bucketing: strong decision verbs (EN and RU, e.g. "decided") → Decisions; weak markers
  with a link ("agreed, link: <url>") → Facts; tasks, risks and links get their own section.
- Long transcripts: the head AND the tail are analyzed (final decisions usually sit at the end);
  the skipped middle is counted and reported in the memo header together with the tool version,
  date and source file.
- Code dumps and tool noise are filtered out; duplicates are removed.

## Privacy, consent, retention & deletion
| What | Where | How to delete |
|---|---|---|
| Transcript file you point at | in memory only | nothing is written |
| Output memo | stdout or `--output <file>` you choose | delete the file |

Get explicit consent before processing a transcript: tell the user which file will be read.
The tool writes nothing by itself, phones nothing and keeps no logs.

## Permissions
- **Files**: read-only access to the transcript file the user explicitly points at; writes only
  to an `--output` path the user provides.
- **Process**: none — no subprocesses, no installs.
- **Network**: NONE.
- **Secrets**: values are redacted before any output; the tool never stores or transmits them.

## License
MIT © 2026 Viacheslav Bochkarev. Free to use, modify and redistribute.
