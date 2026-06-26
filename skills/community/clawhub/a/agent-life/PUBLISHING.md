# Publishing the agent-life Skill to ClawHub

Internal documentation for team members. This file is not published to ClawHub.

## Prerequisites

1. Node.js installed (for the `clawhub` CLI)
2. ClawHub CLI: `npm i -g clawhub`
3. ClawHub account: `clawhub login` (browser-based auth flow)
4. Verify: `clawhub whoami`

## First-Time Publish

Run from the repository root:

```bash
clawhub publish ./skills/agent-life \
  --slug agent-life \
  --name "Agent Life" \
  --version 1.0.0 \
  --changelog "Initial release: backup, sync, restore for OpenClaw agents" \
  --tags "backup,sync,memory,migration,alf"
```

## Version Updates

On each `alf` release that changes CLI behavior, JSON output schemas, or SKILL.md instructions:

```bash
clawhub publish ./skills/agent-life \
  --slug agent-life \
  --version <new-version> \
  --changelog "<what changed>"
```

Use semver. The version tracks SKILL.md content changes, not the `alf` binary version (they may differ).

## When to Update

Publish a new skill version when:

- A new `alf` command is added or an existing command's flags change
- JSON output schemas change (new fields, renamed fields, removed fields)
- Error codes or issue codes change
- The install URL or authentication flow changes
- Workflow instructions in SKILL.md are updated

No update needed for:

- Internal bug fixes that don't change CLI behavior
- Performance improvements
- Changes to files outside `skills/agent-life/`

## Verification

After publishing, verify the skill is discoverable and installable:

```bash
clawhub search agent-life
clawhub install agent-life
clawhub list  # should show agent-life in installed skills
```

Test with an OpenClaw agent: ask it to "check if alf is set up" and verify it runs `alf check -r openclaw` and parses the JSON output.
