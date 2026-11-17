## Description:

Dotfiles helps an agent provide command-line guidance for recording local system configuration and operations entries, reviewing recent activity, and exporting collected logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sysops practitioners, and external users can use this skill to ask an agent for help operating a local Bash logbook for configuration checks, backup or restore notes, incident timelines, benchmarks, and activity exports. Security evidence indicates the inspected artifact should be treated as plaintext logging utility rather than real dotfile backup, sync, restore, or version tracking software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is presented as dotfile backup, sync, restore, and version tracking software, but security evidence says the inspected artifacts implement a local plaintext logging utility instead.

Mitigation: Use and describe the skill as a local logbook unless independent review confirms real backup, sync, restore, or version tracking behavior.

Risk: Local logs and exports may retain sensitive configuration details in plaintext under ~/.local/share/dotfiles.

Mitigation: Avoid entering secrets, tokens, private configuration contents, or other sensitive values; review and clear local logs before sharing or deploying outputs.

Risk: The scanner verdict is suspicious because the advertised capability does not match the inspected artifact behavior.

Mitigation: Review the artifact carefully before installation and validate expected behavior in an isolated test environment.

## Reference(s):

- [Dotfiles on ClawHub](https://clawhub.ai/bytesagain1/skills/dotfiles)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands; the bundled script writes plaintext logs and optional JSON, CSV, or TXT exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies or API keys are required; local data is stored under ~/.local/share/dotfiles.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
