# Aoleme UI Skill

Aoleme UI is an OpenClaw-ready skill for generating dark neon dashboards, gamified interfaces, and glassmorphism-heavy React or Tailwind UIs in a distinct cyber-xianxia aesthetic.

This repository packages that style as a reusable skill plus supporting resource files, so an agent can apply the look consistently across React and Tailwind projects.

## What This Skill Is For

Use this skill when you want an agent to:

- design a dark, mystical, game-like UI
- restyle an existing React or Tailwind page into a cyber-xianxia direction
- apply consistent visual tokens, glass surfaces, glow, and liquid status treatments
- reuse a documented UI language instead of inventing the style from scratch each time

This is primarily a design-system skill. It does not provide business logic, APIs, or a packaged component library.

## Example Prompts

These example prompts are useful both for testing locally and for making the listing more discoverable in ClawHub search:

- Design a cyber-xianxia dashboard for a habit tracker using React and Tailwind.
- Restyle this page into a dark neon glassmorphism UI with purple glow and liquid progress bars.
- Build a gamified profile screen with merit points, cultivation levels, and mystical status cards.
- Create an immersive mobile event page with dark glass panels and restrained sci-fi motion.
- Turn this plain admin interface into a game-like dashboard without changing its data model.

## Repository Contents

- `SKILL.md`: the OpenClaw skill entrypoint with trigger rules, workflow, and adaptation guidance
- `resources/tailwind.config.js`: Tailwind theme extensions for colors, fonts, animation names, and keyframes
- `resources/global.css`: shared CSS variables and utility classes for glass, liquid, glow, and performance helpers

## OpenClaw Installation

### Local shared install

Copy this repository to:

```bash
~/.openclaw/skills/aoleme_ui
```

### Workspace install

Copy this repository to:

```bash
<your-project>/skills/aoleme_ui
```

Then start a new OpenClaw session, or restart the gateway, so the skill is reloaded.

For local testing, prefer copying or syncing the directory instead of symlinking it. OpenClaw skips skill paths that resolve outside the configured workspace root.

## How The Skill Works

The skill tells the agent to:

1. inspect the host project before making stylistic changes
2. read the Tailwind and CSS resources from the skill directory
3. merge only the needed tokens and helper classes
4. apply the visual system without breaking the existing product structure
5. preserve accessibility, responsiveness, and runtime performance

The skill intentionally warns against blindly importing global rules such as `body { overflow: hidden; }` into regular application pages.

## ClawHub Readiness

This repository is structured to be publishable as a ClawHub skill:

- `SKILL.md` uses a snake_case skill name
- frontmatter includes a concise description and publishable metadata
- resource references are written using `{baseDir}` inside the skill instructions
- the body is written for agent execution, not just human design documentation

Before publishing, test the skill locally with a few real prompts in OpenClaw and confirm the generated changes match your quality bar.

See [`PUBLISHING.md`](./PUBLISHING.md) for a tested local install flow, verification commands, commit steps, and publish commands.

## Manual Use Without OpenClaw

You can also use the resources directly:

1. merge the needed parts of `resources/tailwind.config.js` into your Tailwind config
2. copy or import the necessary utilities from `resources/global.css`
3. follow the component and styling guidance in `SKILL.md`

## License

[MIT](./LICENSE) © 2026 isdou
