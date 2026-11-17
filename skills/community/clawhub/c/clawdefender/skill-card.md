## Description:

ClawDefender provides shell-based scanning and sanitization helpers for agent workflows to detect prompt injection, command injection, SSRF, credential exfiltration, and path traversal patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nukewire](https://clawhub.ai/user/nukewire)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to scan skills and scripts, sanitize untrusted text, validate URLs before fetching, and flag suspicious content in automation pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scanner may be mistaken for a complete security boundary.

Mitigation: Treat it as a lightweight regex helper and require additional review, policy controls, and testing for security-sensitive workflows.

Risk: The --install mode installs from ClawHub before scanning the installed skill.

Mitigation: Avoid using --install for untrusted skills; scan and review artifacts before allowing them into agent workspaces.

Risk: Sanitizer and URL validation checks are weaker than advertised.

Mitigation: Use strict blocking for agent-facing input pipelines and do not rely on this URL validator as the only SSRF protection before fetching external URLs.

## Reference(s):

- [ClawDefender ClawHub listing](https://clawhub.ai/nukewire/skills/clawdefender)
- [Nukewire publisher profile](https://clawhub.ai/user/nukewire)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON status output, Markdown guidance, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can pass through clean input, wrap flagged input with warning markers, or exit non-zero in strict mode.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
