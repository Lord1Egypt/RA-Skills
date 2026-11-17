<div align="center">
  <a href="https://www.eonik.ai">
    <img src="https://www.eonik.ai/logo.svg" alt="eonik" width="160" />
  </a>
  <h1>eonik companion skill</h1>
  <p><strong>Finished, on-brand ads — without the busywork.</strong></p>
  <p>How Claude should work once it can see your eonik account: read first, draft from receipts, never spend. You approve every cut.</p>
  <p>
    <a href="https://www.eonik.ai">Website</a> ·
    <a href="https://www.eonik.ai/download">Download for Mac</a> ·
    <a href="https://github.com/eonik-ai/eonik-mcp">eonik-mcp</a> ·
    <a href="https://www.eonik.ai/mcp">Setup</a>
  </p>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT--0-18181B?style=flat-square" alt="MIT-0 license" /></a>
    <a href="https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview"><img src="https://img.shields.io/badge/Claude-Agent%20Skill-d97706?style=flat-square" alt="Claude Agent Skill" /></a>
  </p>
  <p>
    <strong>English</strong> ·
    <a href="docs/readme/README.es.md">Español</a> ·
    <a href="docs/readme/README.pt-BR.md">Português</a> ·
    <a href="docs/readme/README.fr.md">Français</a> ·
    <a href="docs/readme/README.hi.md">हिन्दी</a> ·
    <a href="docs/readme/README.zh-CN.md">简体中文</a> ·
    <a href="docs/readme/README.ja.md">日本語</a> ·
    <a href="docs/readme/README.ko.md">한국어</a>
  </p>
</div>

---

eonik is a **Mac app for making ads**. This repo is **not** the Mac app and **not** the connector.

- **[eonik-mcp](https://github.com/eonik-ai/eonik-mcp)** connects Claude, Cursor, or Codex to your account.
- **This skill** is the playbook those hosts load: ground in the brand, use the research archive, remember what you said, write briefs from facts. **Never launch ads or move budget.**

## What it covers

| Goal | How |
|------|-----|
| Orient | Brand + notes you already saved |
| Research | Competitor archive, ad breakdowns, how surviving ads are built |
| Remember | Save your words verbatim |
| Produce | Receipts in, **you** (or the assistant) author the brief |

There is no “deploy to Meta.” Upload stays a human click.

## Install

Clone into the host’s skills folder, or zip with **`SKILL.md` at the archive root**.

Connection is separate: install [eonik-mcp](https://github.com/eonik-ai/eonik-mcp) (or the hosted connector). This skill does not hold API keys.

Tool names for agents: [reference.md](reference.md).

## The eonik family

| | |
|---|---|
| Mac app | [Download](https://www.eonik.ai/download) · editor free · macOS 15+ · Apple silicon |
| Connector | [eonik-mcp](https://github.com/eonik-ai/eonik-mcp) |
| This playbook | [eonik-mcp-skill](https://github.com/eonik-ai/eonik-mcp-skill) |
| Homebrew | [homebrew-tap](https://github.com/eonik-ai/homebrew-tap) |
| Save ads you see | [Chrome extension](https://chromewebstore.google.com/detail/eonik/ikjbopcpohlogfbccbpcoglefjlbdcie) |

## License

MIT-0 — see [LICENSE](LICENSE).
