## Description:

Advanced security validation for Clawdbot agents, including pattern detection, command sanitization, and threat monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonyrw](https://clawhub.ai/user/sonyrw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to validate commands, URLs, paths, and external content before agent actions, and to monitor local security events for suspicious activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic hook behavior and broad tool-call monitoring can introduce security and privacy risk when enabled.

Mitigation: Review the hook before use, enable it only where needed, and keep validation behavior pinned to a trusted release.

Risk: Local security logs may contain sensitive command, URL, path, or content details.

Mitigation: Redact or restrict logs, set appropriate retention, and review log storage before using the skill in shared environments.

Risk: High-risk validation failures may still allow execution depending on hook configuration or runtime errors.

Mitigation: Configure high-risk checks to fail closed and test command, URL, path, and content validation before relying on the skill.

Risk: Promotional social-media guidance is not required security guidance.

Mitigation: Treat promotional links as optional community material and base deployment decisions on reviewed release evidence and security policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sonyrw/skills/clawdbot-security-suite-bak)
- [Publisher Profile](https://clawhub.ai/user/sonyrw)
- [Artifact README](README.md)
- [Security Skill Reference](skills/security/SKILL.md)
- [Installation Guide](skills/security/INSTALL.md)
- [Security Policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local validation guidance and command outputs; requires jq according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
