## Description:

Query Claude API usage and cost reports from the command line with macOS Keychain storage for an Admin API key and table or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberash-dev](https://clawhub.ai/user/cyberash-dev)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to install and run a macOS CLI that reports Anthropic API token usage and costs across selected periods, models, API keys, and workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned, deprecated third-party CLI that handles an Anthropic Admin API key.

Mitigation: Prefer the maintained replacement named by the skill, or audit and pin a trusted package version before installation.

Risk: The CLI requires an Admin API key with read-only access to organization usage and cost reports.

Mitigation: Enter the key only after trusting the installed CLI code and confirming that this access is acceptable for the organization.

## Reference(s):

- [claude-usage-cli source repository](https://github.com/cyberash-dev/claude-usage-cli)
- [Anthropic Usage and Cost API documentation](https://platform.claude.com/docs/en/build-with-claude/usage-cost-api)
- [Maintained replacement: claude-cost-cli](https://clawhub.com/skills/claude-cost-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced CLI can produce terminal tables or JSON usage and cost reports.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
