# References

Optional directory for extended documentation:

- **Setup guides** — step-by-step walkthroughs for complex auth (e.g. certificate auth, OAuth flows)
- **API documentation** — additional API reference material
- **Architecture diagrams** — system integration diagrams
- **Examples** — sample configs, thread files, workflow templates

## When to use this directory

Use `references/` when your skill needs documentation that is too long for SKILL.md or README.md but essential for setup.

Examples from production skills:
- SharePoint: `references/setup-guide.md` — full Entra app + certificate + Sites.Selected walkthrough

## Convention

- Link from SKILL.md: `See [references/setup-guide.md](references/setup-guide.md) for the full guide.`
- Keep SKILL.md concise — move deep setup docs here
- This directory is included in ClawHub publishes
