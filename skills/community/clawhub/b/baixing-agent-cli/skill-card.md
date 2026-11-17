## Description:

Installs and uses the Baixing Agent CLI from npm to run Baixing listing, category, search, detail, and posting workflows from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install baixing-agent-cli, initialize configuration, inspect Baixing categories and metadata, publish listings, and retrieve listing/search details through documented CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install executable npm code that is not pinned to an exact version.

Mitigation: Use a pinned, trusted version of baixing-agent-cli where possible and prefer local installation when global installation is not required.

Risk: The skill can publish real Baixing listings and may use fabricated contact details if user-provided details are missing.

Mitigation: Require explicit user confirmation of contact details and listing intent before publishing.

Risk: A misconfigured Baixing API base URL could point requests at an unintended endpoint.

Mitigation: Verify BX_API_BASE_URL or configured baseUrl before using non-default Baixing endpoints.

## Reference(s):

- [Baixing Agent CLI npm Package](https://www.npmjs.com/package/baixing-agent-cli)
- [Baixing Agent CLI Complete Reference](reference.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON parsing expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command-line options, environment variables, expected stdout and stderr behavior, and exit-code handling guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
