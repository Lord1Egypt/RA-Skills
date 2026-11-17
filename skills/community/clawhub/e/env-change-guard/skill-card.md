## Description:

Helps users record environment or system variable changes and explains their impact in beginner-friendly language, while checking logs, errors, or visible clues first when troubleshooting unclear environment issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marerlee](https://clawhub.ai/user/marerlee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when changing PATH, JAVA_HOME, Python, Node, ADB, Android SDK, or related environment settings, and when troubleshooting unclear command, tool, log, or system behavior. The skill guides the agent to record what changed and explain the likely impact and next troubleshooting steps in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext environment-variable logs can expose API keys, passwords, cloud credentials, database URLs, private paths, or sensitive troubleshooting details.

Mitigation: Use the skill only with clear user direction and redact secret values, or record only variable names, timestamps, reasons, and success status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marerlee/skills/env-change-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and environment-change log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update logs/env-change-log.md when environment variables are changed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
