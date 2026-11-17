# Contributing to Ghost Theme Builder

Contributions of all kinds are welcome — new snippets, improved docs, better examples, refined prompts, or fixes to the sync tooling.

## Project overview

This is an **AI skill** — the core is `SKILL.md` which tells the AI how to behave. Supporting directories provide reference material the AI reads on demand.

| Directory | Purpose | When to contribute |
|---|---|---|
| `snippets/` | Reusable Handlebars partials | Add a new component pattern (e.g. header, footer, pagination) |
| `examples/` | Reference theme implementations | Document a new theme architecture or migration pattern |
| `prompts/` | Workflow checklists for the AI | Improve the build/review process or add a new workflow |
| `docs/` | Synced from TryGhost/Docs — do not edit directly | Fix upstream docs at [TryGhost/Docs](https://github.com/TryGhost/Docs) |
| `scripts/` | Utility scripts (doc sync, snippet generation) | Fix or improve tooling |
| `SKILL.md` | Skill entry point — identity, rules, routing | Add new capabilities, update instructions, fix metadata |

## Making changes

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/ghost-theme-builder.git
cd ghost-theme-builder
```

### 2. Install dependencies

```bash
pnpm install
```

### 3. Make your changes

Follow these conventions:

| File type | Convention |
|---|---|
| **Snippets** (`.hbs`) | Self-contained Handlebars partial. Use `{{asset}}`, `{{img_url}}`, responsive images, and semantic HTML — match the style of existing snippets. |
| **Examples** (`.md`) | Write in Markdown. Use fenced code blocks with `handlebars` or `yaml` language tags. Show both the code and the expected outcome. |
| **Prompts** (`.md`) | Write in Markdown. Use checklists (`- [ ]`) for actionable steps the AI must follow. |
| **SKILL.md** | Follows the [opencode SKILL.md spec](https://opencode.ai/docs/skills/). Frontmatter must include `name`, `description`, and `license`. Keep instructions concise and actionable. |
| **Code** (`.mjs`) | ES modules (`import`/`export`). Run `npx ultracite check` before committing. |

### 4. Test locally

```bash
# Lint and format check
npx ultracite check

```

### 5. Commit and open a PR

```bash
git checkout -b my-change
git add .
git commit -m "describe your change"
git push origin my-change
```

Then open a pull request against `main`. Include a clear description of what your change does and why.

## Updating documentation (`docs/`)

The `docs/` directory is auto-synced from [TryGhost/Docs](https://github.com/TryGhost/Docs/tree/main/themes). **Do not edit `docs/` directly** — changes are overwritten by the nightly sync workflow.

To update documentation:

1. Fork [TryGhost/Docs](https://github.com/TryGhost/Docs)
2. Make your changes under the `themes/` path
3. Open a PR upstream
4. Once merged, the nightly sync will pull the changes here automatically

To force an immediate sync:

```bash
npm run sync:ghost-docs
```

## Publishing a new version

The skill is published on [ClawHub](https://clawhub.ai/frontendweb/skills/ghost-theme-builder). To publish an update:

1. Bump the `metadata.version` field in `SKILL.md`
2. Update the version in the `publish` script in `package.json`
3. Run the dry-run to verify:

```bash
npm test
```

4. Publish:

```bash
npm run publish
```

The `--source-repo` and `--source-commit` flags link the published version to the exact Git commit for traceability.

## Need help?

Open an issue on GitHub or reach out on the [Ghost forums](https://forum.ghost.org) for theme development questions.
