## Description:

Vet ClawHub skills for security and utility before installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eathon](https://clawhub.ai/user/eathon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate third-party ClawHub skills before installation, combining automated pattern scanning with manual security and utility review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the skill can overrule normal security judgment with rigid scanner-driven instructions.

Mitigation: Use scanner results as advisory signals and require human review before approving, rejecting, or installing a skill.

Risk: The documented download workflow uses shared /tmp paths and direct archive extraction.

Mitigation: Use a private mktemp-created inspection directory, validate archive contents before extraction, and avoid reusing predictable temporary paths.

Risk: The scanner is regex-based and may miss semantic prompt injection, delayed behavior, context-aware behavior, or split-file obfuscation.

Mitigation: Combine automated scanning with manual code review, provenance checks, and capability review before installation.

## Reference(s):

- [Eason Skill Vetting on ClawHub](https://clawhub.ai/eathon/skills/eason-skill-vetting)
- [Prompt-Injection-Resistant Security Review Architecture](ARCHITECTURE.md)
- [Malicious Code Patterns Database](references/patterns.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and optional scanner reports in text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner findings include file, line, category, severity, description, and matched text when JSON output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
