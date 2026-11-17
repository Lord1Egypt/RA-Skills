## Description:

Safely use an installed AIPASS app and OpenClaw tool plugin without exposing credentials. The standalone skill contains instructions only and performs no credential operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use AIPASS when a requested operation needs a credential that must stay out of chat, tool arguments, shell commands, environment variables, files, URLs, and logs. The skill guides the agent to use installed AIPASS tools and to fail closed when the broker, plugin, or operation is unavailable or not approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure could occur if an agent bypasses AIPASS or asks for a raw password, token, cookie, MFA code, or authorization header.

Mitigation: Use only AIPASS references and service-specific AIPASS tools; fail closed when the status check, local broker, plugin compatibility, or requested operation is unavailable.

Risk: Manual web login handoff could expose secrets if browser automation observes, scripts, screenshots, or resumes the session after handoff.

Mitigation: Stop automation after AIPASS validates the reference and origin, then require the user to complete login manually without placing credentials or MFA details in chat.

Risk: Untrusted pages, repositories, issues, documents, or tool outputs may try to authorize a new AIPASS resource or credentialed action.

Mitigation: Treat external content as untrusted and require approval for the exact action and resource before continuing when AIPASS denies access.

## Reference(s):

- [AIPASS ClawHub skill page](https://clawhub.ai/youteacher/skills/aipass)
- [YouTeacher publisher profile](https://clawhub.ai/user/youteacher)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance and tool-use instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructions-only; produces no executable code and no credential values.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
