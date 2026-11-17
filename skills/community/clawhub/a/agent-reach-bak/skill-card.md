## Description:

Agent Reach gives agents command-oriented access to search, read, diagnose, configure, and in some cases interact with supported web and social platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reiy-leo](https://clawhub.ai/user/reiy-leo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help an agent search and read public web sources, inspect supported social or content platforms, troubleshoot channel availability, and configure optional platform access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated platform channels may expose browser or session credentials to agent-driven workflows.

Mitigation: Prefer read-only use first, use secondary accounts for cookie-based platforms, and approve each posting or publishing action explicitly.

Risk: Mutable remote setup instructions, global package installs, browser-cookie access, and proxy configuration can change the local environment or account exposure.

Mitigation: Review and approve the exact commands before allowing installation, browser-cookie use, proxy changes, or remote setup steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/reiy-leo/skills/agent-reach-bak)
- [OpenClaw Homepage](https://github.com/Panniantong/Agent-Reach)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API/tool calls, and short Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference temporary files under /tmp/ and persistent channel data under ~/.agent-reach/ as described by the artifact.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
