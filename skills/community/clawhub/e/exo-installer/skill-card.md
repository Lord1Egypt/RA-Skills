## Description:

Install, update, and monitor E.x.O. tools, manage OpenClaw plugins, and run health checks with a single command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emberdesire](https://clawhub.ai/user/emberdesire)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to install and update E.x.O. ecosystem packages, check tool health, and prepare OpenClaw plugin or cron integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can run mutable remote npm, npx, and GitHub code.

Mitigation: Install only if the publisher and referenced packages are trusted; prefer pinned versions or an isolated environment, and review packages before using --all or update.

Risk: The skill can persistently change OpenClaw-related tooling and propose cron integration.

Mitigation: Avoid elevated privileges and inspect OpenClaw extension or cron changes before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emberdesire/skills/exo-installer)
- [exo-installer GitHub repository](https://github.com/E-x-O-Entertainment-Studios-Inc/exo-installer)
- [exo-installer npm package](https://www.npmjs.com/package/exo-installer)
- [E.x.O. products documentation](https://exohaven.com/products)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health-check summaries, install or update commands, package status, and OpenClaw cron setup guidance.]

## Skill Version(s):

0.4.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
