# @bankofbots/skill

Trust layer for agentic commerce. Build a BOB Score from on-chain payment proofs, use non-custodial `2-of-3` treasury flows (agent + operator recovery key + BOB) for agent Safe accounts, and borrow USDC credit lines based on your score. Provides `SKILL.md` plus reference docs for wallets, treasury, payments, credit scoring, and lending via the BOB API.

## Install

```bash
npm install @bankofbots/skill
```

This package is content-only. It does not install the `bob` CLI binary.

Install the CLI separately from GitHub Releases:

```text
https://github.com/bankofbots/bob-cli/releases/latest
```

## Activate

Copy `SKILL.md` to your agent's skill directory:

**Claude Code**
```bash
mkdir -p .claude/skills/bankofbots
cp -r node_modules/@bankofbots/skill/SKILL.md node_modules/@bankofbots/skill/references .claude/skills/bankofbots/
```

**OpenClaw**
```bash
openclaw skills install bankofbots
```

## Programmatic use

```js
const { skillPath, referencesDir, content } = require('@bankofbots/skill');
// skillPath — absolute path to SKILL.md
// referencesDir — absolute path to bundled reference docs
// content   — SKILL.md contents as a string
```

## Links

- [BOB](https://bankofbots.ai)
- [Dashboard](https://bankofbots.ai)
- [API Docs](https://api.bankofbots.ai/docs)
- [Agent Setup Guide](https://bankofbots.ai/docs/agent-setup)
- [npm package](https://www.npmjs.com/package/@bankofbots/skill)
- [CLI Releases](https://github.com/bankofbots/bob-cli/releases/latest)
- [Agent Kit Source](https://github.com/bankofbots/bob-agent-kit)
