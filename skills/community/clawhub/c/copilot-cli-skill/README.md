# Copilot CLI Operator — OpenClaw Skill

🤖 An [OpenClaw](https://clawhub.ai) skill that enables your agent to run **GitHub Copilot CLI** (`copilot`) for coding tasks — implementation, debugging, refactoring, review, and GitHub operations.

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill instructions for OpenClaw agent |
| `references/copilot-doc-summary.md` | Summary of Copilot CLI documentation |
| `references/copilot-usage-recipes.md` | Usage recipes and execution patterns |
| `scripts/run-copilot-example.sh` | Example runner script |

## Prerequisites

- [Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli): `npm install -g @github/copilot`
- Active GitHub Copilot subscription
- Authentication: run `copilot` and use `/login`, or set `COPILOT_GITHUB_TOKEN`

## Install

```bash
clawhub install copilot-cli-operator
```

## Publish

```bash
clawhub publish . --version 1.0.0 --changelog "Initial release"
```

## License

MIT-0 (as per ClawHub policy)
