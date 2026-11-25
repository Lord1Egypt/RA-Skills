## Description:

Give a terminal agent a Cooper Email inbox with the Cooper CLI. Use when installing the CLI, signing up, creating an inbox, sending, reading unread mail, replying, waiting for mail, or waiting for a verification code. The CLI reads the API key from the environment or the saved credentials file, so the key stays off the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-o-x11](https://clawhub.ai/user/f-o-x11)

### License/Terms of Use:

MIT

## Use Case:

Terminal agents and their operators use this skill to set up a Cooper Email inbox and manage messages, drafts, and verification codes from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the remotely hosted CLI installation guidance as a supply-chain risk because it does not pin a version or verify integrity.

Mitigation: Review the download source and inspect the CLI before running it; use a pinned release and verify its integrity when available.

Risk: The CLI can access email credentials and other sensitive files in its runtime environment.

Mitigation: Run it only in an environment you trust, keep the API key out of command-line arguments, and store credentials in the protected credentials file or environment.

## Reference(s):

- [Cooper CLI documentation](https://cooperemail.com/docs/cli)
- [Cooper Email](https://cooperemail.com)
- [Cooper Email CLI on ClawHub](https://clawhub.ai/f-o-x11/skills/cooper-email-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions for installation, account setup, inbox and message operations, drafts, and waiting for mail or verification codes.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
