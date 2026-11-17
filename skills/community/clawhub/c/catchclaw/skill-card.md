## Description:

Search, install, and export agentars and teams from the CatchClaw marketplace. Use when the user wants to find, install, or package agent templates or teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovelcp](https://clawhub.ai/user/lovelcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use CatchClaw to search the CatchClaw marketplace, install single agentars or teams, export local agents as distributable ZIP packages, and roll back workspace changes when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing remote agentars or teams can change future agent behavior by adding instructions, skills, or team coordination files to live OpenClaw workspaces.

Mitigation: Install only trusted CatchClaw releases, prefer a new named agent over overwriting the main workspace, and review installed AGENTS.md and skill changes before use.

Risk: Overwrite installs, team installs, exports, API-key use, custom API base URLs, or untrusted PATH configurations can affect local workspace integrity or expose sensitive material.

Mitigation: Require explicit user confirmation for install modes and team installs, avoid --api-key unless necessary, review exported ZIPs, and use only trusted AGENTAR_API_BASE_URL and executable paths.

## Reference(s):

- [CatchClaw ClawHub listing](https://clawhub.ai/lovelcp/skills/catchclaw)
- [CatchClaw repository homepage](https://github.com/OpenAgentar/catchclaw)
- [CatchClaw marketplace service](https://catchclaw.me)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update local OpenClaw workspaces, team registries, exports, backups, and optional credential files through the bundled CLI.]

## Skill Version(s):

3.7.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
