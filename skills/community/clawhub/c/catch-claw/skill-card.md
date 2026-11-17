## Description:

Search, install, and export agentars from the CatchClaw marketplace when the user wants to find, install, or package agent templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovelcp](https://clawhub.ai/user/lovelcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search the CatchClaw marketplace, install selected agentar archives into OpenClaw workspaces, export local agents as distributable agentar ZIP packages, and restore workspace backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install remote agentar packages and persistently modify local OpenClaw workspaces, including overwrite operations.

Mitigation: Review the skill and selected agentar before installation, use trusted registries, and avoid overwrite mode unless replacing the main workspace is intentional.

Risk: API keys can be passed to the CLI and written into a workspace credentials file.

Mitigation: Do not pass API keys on the command line unless necessary, and review any generated workspace for credentials before sharing or exporting.

Risk: Server security guidance notes a path validation issue for agent names.

Mitigation: Use simple alphanumeric agent names until the path validation issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovelcp/skills/catch-claw)
- [CatchClaw repository homepage](https://github.com/OpenAgentar/catchclaw)
- [CatchClaw marketplace service](https://catchclaw.me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local OpenClaw workspaces, backups, credentials, and agentar ZIP exports through the bundled Node.js CLI.]

## Skill Version(s):

3.5.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
