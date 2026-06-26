# Client Installation

Use this reference when onboarding a new agent client to this skill.

## Remote Skill URLs

For live deployments:

- unified gateway skill: `/skill.md`
- published reusable skill: `/skills/clashofcoins-universal/SKILL.md`
- compatibility aliases: `/skills/SKILL.md`, `/skills/clashofcoins-universal/skill.md`, `/skills/clashofcoins-universal`, `/skills/clashofcoins/SKILL.md`, `/skills/clashofcoins/skill.md`, `/skills/clashofcoins`
- published skills index: `/skills/index.json`
- well-known skills index alias: `/.well-known/skills/index.json`

## Project-Local Skill Path

For clients that scan the repository:

- preferred path: `.agents/skills/clashofcoins-universal/SKILL.md`

Quick setup from repo root:

```bash
mkdir -p .agents/skills
ln -sfn ../../public/skills/clashofcoins-universal .agents/skills/clashofcoins-universal
```

## Cross-Client Guidance

- Agent Skills is an open format; use the same `SKILL.md` and references across compatible clients.
- If a client supports only explicit skill paths, pass the absolute local path to `public/skills/clashofcoins-universal/SKILL.md`.
- If a client supports URL-based skills, prefer `/skill.md` for instance-specific guidance and `/skills/clashofcoins-universal/SKILL.md` for stable reusable guidance.

## Recommended Starter Prompt

```text
Use the Clash of Coins skill at /skills/clashofcoins-universal/SKILL.md, discover the live instance first, then route me to the correct sale or shop checkout flow.
```
