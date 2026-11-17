## Description:

Guides an agent to operate the eppie-console email CLI for account, folder, message, sync, send, and local vault workflows using deterministic commands and structured output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eppieapp](https://clawhub.ai/user/eppieapp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an autonomous or semi-autonomous agent needs to inspect email accounts and folders, read or send messages, synchronize folders, and manage a local eppie-console vault with machine-readable output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run a downloaded eppie-console executable.

Mitigation: Use only a trusted, verified build and prefer a pinned release with an independently checked digest or signature.

Risk: The skill includes destructive operations such as reset and delete-message.

Mitigation: Run in an isolated working directory and require explicit user approval before destructive mail or vault actions.

Risk: The skill can send mail and provide account or vault credentials to the CLI.

Mitigation: Require explicit user approval before sending mail or supplying credentials, and pass secrets only through the documented standard-input paths.

## Reference(s):

- [Eppie CLI latest release](https://github.com/Eppie-io/Eppie-CLI/releases/latest)
- [Eppie CLI repository](https://github.com/Eppie-io/Eppie-CLI)
- [ClawHub skill page](https://clawhub.ai/eppieapp/skills/eppie-email-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers eppie-console JSON envelopes with type, code, data, meta, and message fields for agent automation.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
