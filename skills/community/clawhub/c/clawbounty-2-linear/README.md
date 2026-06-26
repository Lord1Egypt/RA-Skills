# linear-skill

[![Skill Lint](https://github.com/effectorHQ/linear-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/effectorHQ/linear-skill/actions/workflows/ci.yml) [![ClawHub Ready](https://img.shields.io/badge/ClawHub-publish%20ready-E03E3E)](https://clawhub.com) [![Reference Implementation](https://img.shields.io/badge/effectorHQ-reference%20impl-1A1A1A)](https://github.com/effectorHQ)

An [OpenClaw](https://github.com/openclaw/openclaw) skill for managing Linear issues, projects, and cycles via the Linear GraphQL API.

This is the **reference implementation** for effectorHQ — a real, working skill that demonstrates the full Effector pattern: typed interface, security-auditable permissions, lint-clean structure, and ClawHub-ready packaging.

---

## Install

```bash
# Copy to your OpenClaw workspace
cp -r . ~/.openclaw/workspace/skills/linear/

# Or install from ClawHub (once published)
clawhub install linear
```

Then add your Linear API key to your OpenClaw config:

```
LINEAR_API_KEY=lin_api_xxxxxxxxxxxxxxxx
```

Get your key at Linear → Settings → API → Personal API keys.

## What it does

- List and search issues by team, assignee, priority, or status
- Create issues from conversation
- Update issue state, priority, or assignee
- Check sprint progress (active cycle)
- Add comments to issues

## Typed Interface

This skill declares a typed interface in `effector.toml`:

```
input:   String              → natural-language task
output:  JSON                → structured Linear API response
context: [GenericAPIKey]     → requires LINEAR_API_KEY
```

This means the effector type system knows — before any code runs — that this skill consumes text, produces structured data, and needs an API key. Downstream tools (type checker, composition engine, security audit) all use this interface.

## File structure

```
linear-skill/
├── SKILL.md          # Agent-executable instructions (the actual skill)
├── effector.toml     # Typed manifest (interface + permissions + runtime binding)
├── README.md         # You're reading this
├── LICENSE.md        # Apache-2.0
├── CHANGELOG.md      # Version history
└── .github/
    └── workflows/
        └── ci.yml    # Lint + validate on every push
```

## Why this is the reference

- `SKILL.md` passes [`skill-lint`](https://github.com/effectorHQ/skill-lint) with **zero errors, zero warnings**
- `effector.toml` declares a complete typed interface per [`effector-spec`](https://github.com/effectorHQ/effector-spec) v0.2.0
- Permissions match actual behavior — `effector-audit` finds no drift
- CI uses `skill-lint-action` via the org's reusable workflow
- Description is optimized for ClawHub vector search discovery
- All frontmatter fields are properly filled
- Body has Purpose, When to Use, When NOT to Use, Setup, Commands, Examples, and Notes sections

Use this repo as a template when building your own skill. The [plugin-template](https://github.com/effectorHQ/plugin-template) repo has the scaffolding; this repo shows what a finished skill looks like.

## Reference

See [SKILL.md](./SKILL.md) for the full command reference and examples.

## Contributing

Issues tagged **good first issue** or **help wanted** are a great place to start. See [effectorHQ contributing guide](https://github.com/effectorHQ/.github/blob/main/CONTRIBUTING.md).

## License

This project is currently licensed under the [Apache License, Version 2.0](LICENSE.md) 。
