## Description:

Automates browser navigation, interaction, snapshots, and data extraction through a structured headless browser CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxw975](https://clawhub.ai/user/gxw975)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate web workflows such as navigation, form filling, UI testing, page snapshots, and structured extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned global browser automation CLI.

Mitigation: Use a pinned, local install in a sandbox or dedicated low-privilege account after verifying the npm package source.

Risk: Browser automation can interact with login sessions, credentials, cookies, and third-party sites.

Mitigation: Avoid real credentials and sensitive sessions unless the task is clearly authorized, supervised, and isolated from production accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gxw975/skills/clawhub-publish-146198)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON output guidance for programmatic browser snapshots and extraction workflows.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
