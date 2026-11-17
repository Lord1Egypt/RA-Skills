## Description:

Set up and use Freesound API access from a local Windows OpenClaw workspace with OAuth login, local credential storage, and sound search helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users working in a local Windows OpenClaw workspace use this skill to configure Freesound API credentials, complete localhost OAuth login, search sounds, inspect sound metadata, and download original or preview audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Freesound API credentials and OAuth tokens are stored locally in plaintext.

Mitigation: Restrict the credential file to the current user account, avoid shared machines, rotate any secret already entered on the command line, and review the scripts before authenticated downloads.

## Reference(s):

- [Freesound API v2](https://freesound.org/apiv2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with PowerShell command examples and JSON or file outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local plaintext credential storage and Freesound API network calls from helper scripts.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
