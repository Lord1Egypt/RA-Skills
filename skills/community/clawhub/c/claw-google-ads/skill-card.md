## Description:

Manages Google Ads campaigns by helping an agent list campaign metrics, prepare basic reports, and invoke script commands for campaign budget or status changes through the Google Ads API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3824108-cell](https://clawhub.ai/user/3824108-cell)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to inspect Google Ads campaign performance and coordinate controlled account-management actions such as budget or status changes. It is intended for workflows where the user can provide Google Ads credentials and confirm business-impacting changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local Google Ads credential configuration, including ~/.google-ads.yaml.

Mitigation: Use owner-only file permissions, avoid shared workspaces for real secrets, and install only where agent access to those credentials is acceptable.

Risk: The artifact selects the first accessible Google Ads customer account, which can target the wrong account in multi-account environments.

Mitigation: Require explicit confirmation of the target Google Ads customer account before any operation.

Risk: Budget and status-management features are advertised but incomplete in this artifact.

Mitigation: Treat budget and status changes as proposals until implementation behavior is verified against a test account.

## Reference(s):

- [Google ads for OpenClaw on ClawHub](https://clawhub.ai/3824108-cell/skills/claw-google-ads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local Google Ads credential configuration and may propose business-impacting account operations that require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
