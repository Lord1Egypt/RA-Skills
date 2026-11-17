## Description:

Feishu Cli Auth guides agents through feishu-cli OAuth authentication and User Access Token management, including non-interactive login, token status checks, scope configuration, automatic refresh behavior, and authorization troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giswilson](https://clawhub.ai/user/giswilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to authenticate feishu-cli with Feishu OAuth, obtain and refresh User Access Tokens, choose the required scopes, and troubleshoot token or permission errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad Feishu OAuth scopes and long-lived refresh access.

Mitigation: Prefer narrower scopes where practical and grant only the Feishu permissions required for the intended workflow.

Risk: OAuth callback URLs and locally stored token files can expose sensitive account access if shared or mishandled.

Mitigation: Avoid pasting callback URLs into shared logs or transcripts, protect ~/.feishu-cli/token.json, and revoke the Feishu app authorization if token exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/giswilson/skills/feishu-cli-auth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OAuth callback handling steps, token status interpretation, scope recommendations, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
