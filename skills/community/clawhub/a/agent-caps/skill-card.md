## Description:

Define, validate, and audit agent capability manifests for safe skill installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and security reviewers use this skill to validate, scaffold, and cross-check agent capability manifests before publishing or installing agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path fetches mutable remote Python code without verification.

Mitigation: Use the packaged agent_caps.py from the release, or require a pinned release and checksum verification before execution.

Risk: The validator alone is not sufficient as a security gate.

Mitigation: Use it as one manifest-quality check and pair it with review and scanning before granting machine access.

## Reference(s):

- [Agent Caps ClawHub listing](https://clawhub.ai/itspremkumar/skills/agent-caps)
- [README](artifact/README.md)
- [Agent Caps CLI source](artifact/agent_caps.py)
- [Hermes example manifest](artifact/examples/hermes.json)
- [OpenClaw example manifest](artifact/examples/openclaw.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON manifest files and Python CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs offline with Python 3.8+ and no third-party dependencies.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
