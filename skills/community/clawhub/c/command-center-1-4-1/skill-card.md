## Description:

Mission control dashboard for OpenClaw - real-time session monitoring, LLM usage tracking, cost intelligence, and system vitals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcdentoncore](https://clawhub.ai/user/jcdentoncore)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run a local OpenClaw dashboard for monitoring AI sessions, LLM usage, costs, scheduled jobs, and system health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard can expose sensitive OpenClaw session activity, transcript excerpts, operator identities, memory metadata, vitals, and job state if run without appropriate access controls.

Mitigation: Bind the service to loopback, enable authentication, and avoid exposing port 3333 to LAN, VPN, or public networks unless access controls are in place.

Risk: The quick-start flow uses an unpinned npx installer.

Mitigation: Review the package source and prefer pinned, trusted versions before installing in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jcdentoncore/skills/command-center-1-4-1)
- [OpenClaw Command Center Documentation](https://github.com/jontsai/openclaw-command-center#readme)
- [Architecture Overview](docs/architecture/OVERVIEW.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts a local dashboard service for OpenClaw visibility.]

## Skill Version(s):

1.4.1 (source: SKILL.md frontmatter and package.json); ClawHub release version 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
