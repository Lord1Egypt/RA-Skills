## Description:

Helps agents troubleshoot and fix WorkBuddy connector OAuth authorization failures on Windows, including diagnosis, HKCU browser ProgId repair guidance, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Support engineers and WorkBuddy users use this skill when third-party connector OAuth flows fail with errors such as 0x800401F5, missing application messages, SSE 405 responses, or authorization timeouts. It guides the agent through log review, network checks, Windows default-browser diagnosis, registry repair, and post-fix validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a persistent HKCU registry change for browser ProgId handling that can affect how links open for the current user.

Mitigation: Confirm the affected ProgId and browser executable path before applying the change, record or export the existing HKCU value, and proceed only with user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwenqi123123/skills/connector-oauth-fix)
- [Publisher profile](https://clawhub.ai/user/liuwenqi123123)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language troubleshooting workflow for Windows WorkBuddy connector OAuth failures.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
