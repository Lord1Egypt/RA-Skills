# Contributing

Thanks for improving Before You Build Skill.

This project is small on purpose. Contributions should make the skill more useful before an AI coding agent starts building, not turn it into a general startup advisor or a large prompt pack.

## Good Contributions

- Better failure patterns with concrete examples.
- Clearer install notes for Codex, Claude Code, Cursor, OpenCode, OpenClaw, or similar tools.
- Realistic examples of product ideas, feature requests, and launched-project diagnosis.
- Fixes for confusing instructions in `SKILL.md`.
- Privacy or safety improvements around optional Case Memory usage.

## What To Avoid

- Adding implementation, architecture, or tech-stack advice to the skill.
- Turning the skill into a long business plan generator.
- Adding many loosely related skills into this repository.
- Sending private customer data, secrets, or unreleased company details in examples.

## Before Opening A Pull Request

1. Keep the change focused.
2. Check that `SKILL.md` still tells the agent not to write code before the risk review.
3. If you add an example, make it public, fictional, or anonymized.
4. Run:

```bash
git diff --check
```

## Useful Templates

- Use the idea review issue template to test the skill against a real product or feature idea.
- Use the compatibility issue template to report how it works in a specific AI coding tool.
- Use the failure pattern issue template to suggest a repeated product failure mode.
