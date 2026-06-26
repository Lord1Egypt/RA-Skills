# Publishing

This document captures a tested local install flow for `cyber_fantasy_ui`, plus the git and ClawHub commands needed to publish it.

## 1. Local Install Test

OpenClaw on this machine uses the workspace:

```bash
/Users/suxiaohan/.openclaw/chat-workspace
```

Create the workspace skills directory if needed:

```bash
mkdir -p /Users/suxiaohan/.openclaw/chat-workspace/skills
```

Copy the skill into the workspace. Do not symlink it from outside the workspace root:

```bash
rsync -av --delete --exclude .git ./ /Users/suxiaohan/.openclaw/chat-workspace/skills/cyber_fantasy_ui/
```

Verify that OpenClaw can discover the skill:

```bash
openclaw skills info cyber_fantasy_ui --json
openclaw skills list --json
```

Expected result:

- `name` should be `cyber_fantasy_ui`
- `source` should be `openclaw-workspace`
- `eligible` should be `true`
- `emoji` should be `🪷`
- `homepage` should be `https://github.com/isdou/aoleme-ui-skill`

## 2. Optional Prompt Smoke Tests

Use prompts like these in a fresh OpenClaw session:

- Design a cyber-fantasy dashboard for a habit tracker using React and Tailwind.
- Restyle this page into a dark neon glassmorphism UI with purple glow and liquid progress bars.
- Build a gamified profile screen with merit points, cultivation levels, and mystical status cards.

## 3. Commit

Review the diff:

```bash
git diff -- README.md SKILL.md PUBLISHING.md demo/
```

Stage the release docs:

```bash
git add README.md SKILL.md PUBLISHING.md demo/
```

Commit:

```bash
git commit -m "Rename skill to cyber_fantasy_ui"
```

## 4. Publish Prerequisites

ClawHub CLI is the recommended publishing path. On this machine, `npx clawhub` failed under Node `v22.22.0` with a module compatibility error from `mime`.

Before publishing, switch to an LTS Node version such as Node 20:

```bash
node -v
nvm use 20
```

If you do not use `nvm`, use your preferred Node version manager and make sure `node -v` reports an LTS release before continuing.

## 5. Publish To ClawHub

Log in:

```bash
npx clawhub login
```

Publish from the repository root:

```bash
npx clawhub publish . --slug cyber-fantasy-ui --name "Cyber Fantasy UI Skill" --version 1.1.1
```

If the CLI supports additional options in your installed version, inspect them with:

```bash
npx clawhub publish --help
```

## 6. Post-Publish Checks

After publish succeeds:

```bash
openclaw docs clawhub
git status --short
```

Then verify the published listing from another environment or a clean OpenClaw setup.
