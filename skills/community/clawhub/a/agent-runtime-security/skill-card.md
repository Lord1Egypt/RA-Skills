## Description:

Agent Runtime Security helps OpenClaw agents harden storage and runtime behavior against data leaks, prompt injection, and unintended command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linuxying](https://clawhub.ai/user/linuxying)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure OpenClaw security boundaries, protect local workspace secrets, and add checklists and tests that distinguish copied command text from explicit execution requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security scan reports credential-like values in tests/pre-submit-check.sh.

Mitigation: Remove the credential-like values before installation or publication, rotate any matching real credentials, and rerun security checks before using the skill.

Risk: The skill includes commands that can change local configuration, schedule jobs, install packages, or rewrite Git history.

Mitigation: Review each command against the target OpenClaw workspace and run only commands that match the user's explicit intent and environment.

## Reference(s):

- [OpenClaw Security Documentation](https://docs.openclaw.ai/security)
- [GnuPG Manual](https://www.gnupg.org/gph/en/manual.html)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [ClawHub Skill Page](https://clawhub.ai/linuxying/skills/agent-runtime-security)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and test cases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes security checklists, OpenClaw configuration examples, and manual validation cases.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
