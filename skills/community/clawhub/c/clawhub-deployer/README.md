# clawhub-publish — Skill Publishing Assistant

A skill that helps AI coding assistants publish other skills to the [ClawHub](https://clawhub.ai) registry.

Works with Claude Code, OpenClaw, Codex, and any tool that supports skills.

## What it does

When you ask your AI assistant to publish a skill to ClawHub, this skill provides the step-by-step workflow:

1. Validate `SKILL.md` frontmatter
2. Filter out non-text files (ClawHub only accepts text)
3. Prepare a clean publish folder
4. Login and publish via `npx clawhub@latest`
5. Verify the published skill

## Install

<details>
<summary><b>Claude Code</b></summary>

```
Install the clawhub-publish skill from https://github.com/FuturizeRush/clawhub-publish-skill
```
</details>

<details>
<summary><b>OpenClaw / ClawHub</b></summary>

```bash
openclaw skills install clawhub-publish
# or
npx clawhub@latest install clawhub-publish
```
</details>

<details>
<summary><b>Manual</b></summary>

```bash
git clone https://github.com/FuturizeRush/clawhub-publish-skill.git
```

Copy `SKILL.md` into your skills directory.
</details>

## Usage

Just ask your AI assistant:

```
Publish my skill to ClawHub
```

The skill will guide the process automatically.

## License

MIT-0
