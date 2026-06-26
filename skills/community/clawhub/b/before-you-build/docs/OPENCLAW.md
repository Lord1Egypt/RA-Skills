# OpenClaw Publishing Notes

Last updated: 2026-05-26 22:40:43 CST

This document prepares Before You Build Skill for OpenClaw and ClawHub distribution.

## Goal

Publish `before-you-build` as an OpenClaw-compatible skill without creating a separate long-term fork.

The canonical package remains this repository:

```text
https://github.com/bin1874/before-you-build-skill
```

OpenClaw users should be able to install the same source package or find it through ClawHub once it is accepted there.

## Why No Separate Fork

The skill is mostly portable already because it is a text-first Agent Skill package:

- `SKILL.md` contains YAML frontmatter and task instructions.
- No executable payload is required.
- No API key is required for normal use.
- Optional Case Memory lookup is documented separately and should only be used after user permission.

A separate OpenClaw-only fork would create duplicate maintenance work and increase the chance that the public instructions drift apart.

## Recommended OpenClaw Install

If OpenClaw supports GitHub skill installation in the user's setup:

```bash
openclaw skills install github:bin1874/before-you-build-skill
```

If that form is not available, install manually:

```bash
git clone https://github.com/bin1874/before-you-build-skill.git ~/.openclaw/skills/before-you-build
```

Expected layout:

```text
~/.openclaw/skills/before-you-build/
  SKILL.md
  README.md
  references/
  examples/
  docs/
```

Then invoke it with:

```text
Use before-you-build to review this idea before implementation:
...
```

## Suggested ClawHub Listing

Name:

```text
before-you-build
```

Display name:

```text
Before You Build Skill
```

Tagline:

```text
Ask why your product or feature might fail before your AI agent builds it.
```

Short description:

```text
A pre-build reality check for SaaS, AI app, side project, startup, and feature ideas. It reviews demand, distribution, pricing, retention, trust, and failure patterns before the agent writes code.
```

Category candidates:

```text
Productivity
Development
Business
```

Tags:

```text
product, startup, saas, ai-builder, validation, risk-review, feature-review, indie-hacker
```

Repository:

```text
https://github.com/bin1874/before-you-build-skill
```

Website:

```text
https://beforeyoubuild.fyi/en/skill
```

License:

```text
Repository: MIT
ClawHub published release: MIT-0 under ClawHub policy
```

Confirm that the ClawHub MIT-0 release policy is acceptable before publishing. The source repository can remain MIT, but ClawHub states that published skills on its registry are released under MIT-0.

## CLI Publish Flow

The ClawHub CLI package is `clawhub`.

```bash
npm i -g clawhub
clawhub login
clawhub whoami
```

If you do not want to install it globally, use `npx --yes clawhub ...` for the same commands.

Publish from the repository root after login:

```bash
clawhub skill publish . \
  --slug before-you-build \
  --name "Before You Build Skill" \
  --version 0.1.1 \
  --owner YOUR_OWNER_HANDLE \
  --changelog "Add OpenClaw metadata, install notes, and ClawHub publishing guidance." \
  --clawscan-note "Text-only pre-build review skill. No executable payload, no required secrets, and no required network access. Optional Case Memory lookup is documented separately and only used after user permission."
```

Replace `YOUR_OWNER_HANDLE` with the ClawHub publisher handle that should own the skill. ClawHub owner handles are account or organization scoped, and publishing requires permission for that owner.

Optional preflight checks:

```bash
clawhub search before-you-build --limit 10
clawhub skill publish --help
```

After publishing, ClawHub may hide the new release from normal install/download surfaces until automated review and verification finish.

## Security Statement

Suggested submission note:

```text
Before You Build Skill is a text-only Agent Skill package. It does not require an API key, does not include executable install scripts, and does not need file, shell, or network access for normal use. The optional Case Memory API is documented separately and should only be queried after the user explicitly allows external lookup.
```

## Submission Checklist

- [ ] Confirm `SKILL.md` frontmatter uses the public slug `before-you-build`.
- [ ] Confirm `SKILL.md` frontmatter includes the current semver version.
- [ ] Confirm README mentions OpenClaw compatibility and install notes.
- [ ] Confirm `docs/INSTALL.md` includes OpenClaw-specific local install paths.
- [ ] Confirm `.clawhubignore` excludes repository metadata, generated archives, and local artifacts.
- [ ] Confirm no secrets, tokens, generated archives, or local machine paths are committed.
- [ ] Publish or submit the skill through ClawHub / OpenClaw's current official workflow.
- [ ] Wait for automated review and verification if the release is temporarily hidden.
- [ ] Record the submission URL and status in `docs/SUBMISSIONS.md`.
- [ ] After it appears in OpenClaw's public skill source, consider submitting to third-party directories such as `awesome-openclaw-skills`.

## Third-Party Directory Timing

Do not submit to OpenClaw awesome lists before the skill exists in the official OpenClaw / ClawHub source. Some directories only accept skills that already have a ClawHub link and a `github.com/openclaw/skills` source link.
