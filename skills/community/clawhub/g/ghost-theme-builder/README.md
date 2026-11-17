# Ghost Theme Builder

An AI skill for building, customizing, reviewing, and optimizing production-ready [Ghost CMS](https://ghost.org) themes using the official Ghost Theme API and modern frontend best practices.

## Overview

This repository turns an AI assistant into a Ghost CMS theme development expert. It provides structured documentation, reusable Handlebars partials, reference examples, and predefined workflows so the AI can consistently produce high-quality, accessible, and performant Ghost themes.

## Directory Structure

```bash
├── SKILL.md              # Skill entry point — identity, workflow, standards
├── docs/                 # Official Ghost theme docs (synced from TryGhost/Docs)
├── snippets/             # Reusable Handlebars partials
│   ├── base-layout.hbs
│   ├── post-card.hbs
│   └── membership-cta.hbs
├── examples/             # Reference implementations
│   ├── minimal-theme.md  # Bare minimum theme structure
│   └── starter-kit.md    # Starter kit with pre-configured tooling
├── prompts/              # Predefined workflows
│   ├── build.md          # Theme build checklist
│   └── review.md         # Theme review checklist
├── agents/               # Agent configuration (OpenAI, etc.)
│   └── openai.yaml
├── scripts/              # Utility scripts
│   └── sync-ghost-docs.mjs
├── .github/workflows/    # CI/CD — nightly doc sync
│   └── sync-ghost-docs.yml
├── package.json
└── README.md
```

## Install

Install the skill from the [ClawHub registry](https://clawhub.ai/frontendweb/skills/ghost-theme-builder):

```bash
# via OpenClaw
openclaw skills install @frontendweb/ghost-theme-builder

# or via npx
npx skills add https://clawhub.ai/frontendweb/skills/ghost-theme-builder
```

## Usage

### As an AI skill

Once installed, the skill loads automatically when you ask the AI to build, review, or debug a Ghost theme. It follows the workflow in `SKILL.md`.

Supported platforms:

| Platform | Skill directory |
|---|---|
| **opencode** | `~/.config/opencode/skills/ghost-theme-builder/SKILL.md` |
| **Claude** | `~/.claude/skills/ghost-theme-builder/SKILL.md` |

### Manual reference

All files are useful standalone:

- **[snippets/](snippets/)** — Ready-to-use Handlebars partials for layouts, post cards, and membership CTAs
- **[docs/](docs/)** — Concise Ghost theme development reference (structure, contexts, helpers, routing, members, SEO, assets, content, search, share, GScan, custom settings)
- **[examples/](examples/)** — Starting points: minimal theme or full starter kit
- **[prompts/](prompts/)** — Checklists for building or reviewing themes

### Key features covered

- Ghost Theme API and Handlebars helpers
- `routes.yaml` dynamic routing (routes, collections, channels, taxonomies)
- `package.json` configuration (image sizes, custom settings, card assets)
- Membership, Portal, signup forms, content visibility
- Comments, search, and native share
- Responsive images with `{{img_url}}` and format conversion (WebP, AVIF)
- Editor cards (gallery, bookmark, audio, video, toggle, signup, etc.)
- SEO with `{{meta_title}}`, `{{meta_description}}`, and `{{ghost_head}}`
- Accessibility (landmarks, headings, focus, reduced-motion)
- GScan validation

## Doc sync

Documentation in `docs/` is synced from [TryGhost/Docs](https://github.com/TryGhost/Docs/tree/main/themes) via GitHub Actions (nightly or on push to main).

## Requirements

- Node.js 22+ (for sync script)
- Ghost 5.x (latest recommended)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide — how to add snippets, update docs, publish a new version, and submit changes.

## License

MIT
