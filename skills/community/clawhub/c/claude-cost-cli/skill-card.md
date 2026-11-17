## Description:

Query Claude API usage and cost reports from the command line. Secure macOS Keychain storage for Admin API key. Table/JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberash-dev](https://clawhub.ai/user/cyberash-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to install and run a macOS CLI that reports Anthropic Claude Admin API usage and cost data for monitoring, scripting, and spend review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to globally install an unpinned third-party CLI that handles an Anthropic Admin API key.

Mitigation: Review or pin the exact package version or source commit before installing, verify provenance or signatures where possible, and consider using an isolated environment.

Risk: A compromised package or workstation could expose an Admin API key used for organization usage and cost reporting.

Mitigation: Use the least-privileged Admin API key available and rotate it if compromise is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberash-dev/skills/claude-cost-cli)
- [claude-cost-cli source](https://github.com/cyberash-dev/claude-cost-cli)
- [Anthropic usage and cost API documentation](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline bash command examples and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs describe terminal commands for installation, key management, usage reports, and cost reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
