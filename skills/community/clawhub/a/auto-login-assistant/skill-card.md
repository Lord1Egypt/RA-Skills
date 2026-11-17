## Description:

Help the agent recover from login walls on websites by detecting sign-in states, collecting user-approved credentials, filling common login forms, and handling verification codes safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddmmddmm](https://clawhub.ai/user/ddmmddmm)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent is blocked by a login wall and the user wants guided sign-in assistance with explicit credential and verification-code consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Passwords can be exposed through agent-visible command output or reusable plaintext credential examples.

Mitigation: Prefer credentials provided for the current session, avoid reusable plaintext files or exported environment variables when possible, and redact or avoid stdout output containing secrets.

Risk: Agent-assisted login and verification-code handling can exceed the user's intended account-access scope.

Mitigation: Use the skill only for accounts where agent-assisted login is acceptable, require explicit user approval for mailbox access, and prefer manual OTP entry.

## Reference(s):

- [Credential Config Example](references/config-example.md)
- [Auto Login Assistant on ClawHub](https://clawhub.ai/ddmmddmm/skills/auto-login-assistant)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with optional shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May normalize credential inputs to JSON and extract candidate verification codes when explicitly authorized.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
