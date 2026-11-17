## Description:

Long-term memory, anti-hallucination, self-evolution, and workflow orchestration for OpenClaw, delivered as a plugin plus skill hybrid with lifecycle hooks, maintenance scripts, and optional embedding configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crusheart-7](https://clawhub.ai/user/crusheart-7)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this release to add persistent memory, message-pipeline validation, workflow orchestration, self-evaluation, maintenance automation, and skill/memory scanning to an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-privilege workspace changes can affect agent behavior and local state.

Mitigation: Review the workspace changes before installation and install first in an isolated or backed-up OpenClaw workspace.

Risk: The release can create persistent memory and index files and deploy behavior-rule content.

Mitigation: Confirm the storage locations and behavior-rule changes are acceptable before enabling the plugin in a shared or production workspace.

Risk: Local script execution and recurring cron jobs can continue operating after installation.

Mitigation: Inspect the bundled scripts and back up existing OpenClaw cron jobs before installing.

Risk: External version checks and optional embedding API configuration may introduce network and credential exposure considerations.

Mitigation: Review network access expectations and provide embedding API credentials only through controlled environment configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/crusheart-7/skills/crusheart-performance-autobrain)
- [README](artifact/README.md)
- [Architecture Reference](artifact/bundle/ARCHITECTURE.md)
- [Install Guide](artifact/bundle/INSTALL_GUIDE.md)
- [Plugin Manifest](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw >= 2026.5.0, Node.js >= 18, and Python >= 3.10; runtime behavior may create persistent workspace files and recurring cron tasks.]

## Skill Version(s):

6.3.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
