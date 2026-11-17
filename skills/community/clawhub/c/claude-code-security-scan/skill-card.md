## Description:

Audits Claude Code configuration for security vulnerabilities, misconfigurations, and injection risks with AgentShield.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review Claude Code project settings, MCP servers, hooks, agents, and instructions for security issues before onboarding, committing changes, or during periodic security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan depends on a third-party npm package whose code can change between releases.

Mitigation: Install the exact pinned version project-locally, keep the lockfile, and invoke it with npx --no-install.

Risk: The --fix and init commands can write changes to Claude Code configuration.

Mitigation: Review a plain scan and proposed changes first, and use a version-controlled or throwaway work tree before applying changes.

Risk: Optional deep analysis requires an Anthropic API key, and the data it sends should be understood before use.

Mitigation: Check what the analysis transmits before enabling it and use a limited API key.

## Reference(s):

- [Commands, Severity Grades, and Findings](references/commands-and-findings.md)
- [ClawHub release](https://clawhub.ai/djc00p/skills/claude-code-security-scan)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown security findings and guidance with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings may be emitted as text, JSON, or Markdown by the scanner.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
