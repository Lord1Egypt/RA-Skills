## Description:

Explain bit-cli skill purpose, installation, required setup, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parinll](https://clawhub.ai/user/parinll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and use the Bit URL Shortener CLI for creating, listing, inspecting, updating, deleting, and reviewing click data for short links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to build an unpinned third-party CLI and move it into /usr/local/bin with sudo.

Mitigation: Review and pin the bit-cli source before installation, and prefer a user-local PATH location over a system-wide sudo install.

Risk: The CLI uses BIT_API_KEY to create, update, delete, and inspect short-link data.

Mitigation: Use a narrowly scoped Bit API key, keep it out of command history and shared scripts, and confirm link IDs with list or get before update or delete operations.

## Reference(s):

- [Bit URL Shortener on ClawHub](https://clawhub.ai/parinll/skills/bit)
- [bit-cli source module](https://github.com/ParinLL/bit-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include environment variables, CLI commands, and troubleshooting steps for Bit API operations.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
