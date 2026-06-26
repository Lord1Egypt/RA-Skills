# Cyber Fantasy UI Skill

Formerly Aoleme UI. A discoverable OpenClaw skill for dark neon dashboards, glassmorphism-heavy interfaces, and gamified React or Tailwind UI generation.

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/English-README-2563EB" alt="English README"></a>
  <a href="README.zh-CN.md"><img src="https://img.shields.io/badge/简体中文-README.zh--CN-34A853" alt="Chinese README"></a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-111827" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/Style-Cyber--Fantasy-7C3AED" alt="Cyber Fantasy">
  <img src="https://img.shields.io/badge/Use%20Case-Dashboard%20%7C%20Gamified%20UI-0EA5E9" alt="Use Case">
  <img src="https://img.shields.io/badge/License-MIT-2563EB" alt="License">
</p>

## Demo

![Cyber Fantasy UI demo](./demo/preview.svg)

- Preview file: [`demo/index.html`](./demo/index.html)
- Demo stylesheet: [`demo/styles.css`](./demo/styles.css)

This demo shows the core visual language of the skill: dark layered surfaces, cultivation-purple accents, liquid progress treatments, glass panels, status chips, and game-like information hierarchy.

## What This Skill Does

Use this skill when you want OpenClaw to:

- design a dark, mystical, game-like dashboard
- restyle an existing React or Tailwind page into a cyber-fantasy direction
- apply glow, glass surfaces, liquid progress bars, and immersive UI patterns consistently

Best for:

- dashboards
- membership centers
- growth systems
- event pages
- profile screens
- status panels

Not for:

- backend logic or API workflows
- conservative enterprise products unless the user explicitly wants this aesthetic

## Example Prompts

- Design a cyber-fantasy dashboard for a habit tracker using React and Tailwind.
- Restyle this page into a dark neon glassmorphism UI with purple glow and liquid progress bars.
- Build a gamified profile screen with merit points, cultivation levels, and mystical status cards.
- Create an immersive mobile event page with dark glass panels and restrained sci-fi motion.
- Turn this plain admin interface into a game-like dashboard without changing its data model.

## Why This Skill

- It gives the agent a concrete visual target instead of vague prompts like "make it cooler".
- It includes reusable Tailwind tokens and CSS utilities rather than only a style description.
- It encourages selective adaptation instead of destructive redesign.
- It warns against risky global rules such as forcing `overflow: hidden` across an entire app.

## Included Files

- `SKILL.md` - skill entrypoint, trigger rules, and execution guidance
- `resources/tailwind.config.js` - colors, fonts, animations, and keyframes
- `resources/global.css` - glass, liquid, glow, and performance helper styles
- `demo/index.html` - static local demo
- `demo/styles.css` - demo stylesheet
- `demo/preview.svg` - README preview image
- `PUBLISHING.md` - local verification and release steps

## Install

### Shared install

```bash
mkdir -p ~/.openclaw/skills/cyber_fantasy_ui
rsync -av ./ ~/.openclaw/skills/cyber_fantasy_ui/
```

### Workspace install

```bash
mkdir -p <your-project>/skills/cyber_fantasy_ui
rsync -av ./ <your-project>/skills/cyber_fantasy_ui/
```

Start a new OpenClaw session after installing.

If your OpenClaw setup restricts skill discovery to the workspace root, copy or sync the folder instead of symlinking it.

## Verify

```bash
openclaw skills info cyber_fantasy_ui --json
openclaw skills list --json
```

Expected:

- `name` is `cyber_fantasy_ui`
- `eligible` is `true`
- the description mentions cyber-fantasy, dark neon, or gamified UI

## Manual Use Without OpenClaw

1. Merge the needed parts of `resources/tailwind.config.js` into your Tailwind config.
2. Copy or import the utilities from `resources/global.css`.
3. Use `demo/` as a style reference and reuse the guidance from `SKILL.md`.

## Naming

Public-facing name:

- `Cyber Fantasy UI Skill`

Internal skill key:

- `cyber_fantasy_ui`

Legacy aliases kept in docs:

- `Aoleme UI`
- `Cyber Xianxia UI Skill`

## Publish

```bash
git add .
git commit -m "Rename skill to cyber_fantasy_ui"
npx clawhub login
npx clawhub publish . --slug cyber-fantasy-ui --name "Cyber Fantasy UI Skill" --version 1.1.1
```

If `clawhub` fails under your current Node version, switch to an LTS runtime such as Node 20 and retry.

## License

[MIT](./LICENSE) © 2026 isdou
