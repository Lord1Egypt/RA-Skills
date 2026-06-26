# Install Before You Build Skill

Before You Build Skill works without an API key. The core package is local text instructions plus references and examples.

## Option 1: Clone the Repository

```bash
git clone https://github.com/bin1874/before-you-build-skill.git
```

Add the full folder to your AI coding tool if it supports local skills or instruction folders.

## Option 2: Download ZIP

Open the GitHub repository and use GitHub's **Code -> Download ZIP** option.

Unzip the folder, then add it to your tool's skill, agent, or custom instruction location.

## Codex

If your Codex setup supports local skills, place the repository folder in your local Codex skills directory.

Typical local layout:

```text
~/.codex/skills/before-you-build-skill/
  SKILL.md
  agents/
  references/
  examples/
```

Then ask:

```text
Use before-you-build to review this idea before implementation:
...
```

## Claude Code

If your Claude Code workflow uses project instructions, copy the relevant parts of `SKILL.md` into your project instructions or `CLAUDE.md`.

Recommended use:

```text
Before implementing this feature, apply the before-you-build review from the project instructions.
```

## Cursor

If your Cursor project uses rules, copy `SKILL.md` into a project rule file, for example:

```text
.cursor/rules/before-you-build.md
```

Then invoke it explicitly before implementation:

```text
Use the before-you-build rule to review this feature before writing code.
```

## OpenCode, OpenClaw, and Similar Tools

If the tool supports custom agents, skills, memories, rules, or instruction files, add `SKILL.md` as a named instruction called `before-you-build`.

If it only supports one global instruction field, paste the "Core Behavior", "When To Use", and "Output Modes" sections from `SKILL.md`.

## OpenClaw

Before You Build Skill is designed to work as a text-first OpenClaw skill. Normal use does not require shell access, file writes, network access, or an API key.

If your OpenClaw setup supports GitHub skill installation, try:

```bash
openclaw skills install github:bin1874/before-you-build-skill
```

After the skill is published on ClawHub, OpenClaw users can also install it from the registry:

```bash
clawhub install before-you-build
```

If you prefer manual installation, clone the repository into OpenClaw's managed skills directory:

```bash
git clone https://github.com/bin1874/before-you-build-skill.git ~/.openclaw/skills/before-you-build
```

Expected local layout:

```text
~/.openclaw/skills/before-you-build/
  SKILL.md
  README.md
  references/
  examples/
  docs/
```

Then invoke it explicitly before implementation:

```text
Use before-you-build to review this product or feature idea before writing code:
...
```

For ClawHub publishing notes, see `docs/OPENCLAW.md`.

## Minimal Prompt-Only Setup

If you do not want to install anything, paste this before a build request:

```text
Before building, review this idea using a before-you-build risk check.

Do not recommend code, architecture, or implementation yet. First identify:
- the target user and concrete scenario;
- the biggest product risk;
- the most likely failure pattern;
- what evidence is weak or missing;
- the smallest validation step before building;
- a verdict: Build small, Validate first, Pivot first, or Don't build yet.
```

## Case Memory

Normal use does not require an API key.

If a compatible agent can call external APIs, it may optionally query Before You Build Case Memory after asking for permission. See `references/case-memory-api.md`.
