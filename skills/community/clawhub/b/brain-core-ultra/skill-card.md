## Description:

Guides agents through deeper reasoning before acting on complex, dependency-heavy tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users apply this meta-skill when they need structured reasoning, decomposition, hypothesis testing, tool selection, anti-hallucination checks, and completion verification for complex or risky tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad reasoning guidance can make an agent more structured and verification-heavy than needed for simple tasks.

Mitigation: Scope use to difficult, risky, or multi-step work and avoid activating the framework for trivial requests.

Risk: A meta-skill that shapes decision-making can affect many downstream responses.

Mitigation: Keep memory, observability, security, and approval behavior under the platform's normal controls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pmuhammadagus-byte/skills/brain-core-ultra)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown or text guidance with task-specific plans, checks, and command suggestions when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only reasoning framework; no direct tool calls, filesystem changes, or network access are performed by the skill itself.]

## Skill Version(s):

1.0.1 (source: metadata.openclaw.version and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
