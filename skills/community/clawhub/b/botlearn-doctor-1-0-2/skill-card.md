## Description:

Autonomously inspects a live OpenClaw instance across hardware, configuration, security, skills, and autonomy domains, then delivers a quantified traffic-light health report with actionable fix guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1215656](https://clawhub.ai/user/1215656)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw installations, inspect system health signals, and produce prioritized remediation guidance. It supports full and targeted checks across hardware resources, configuration health, security risks, skills completeness, and autonomous intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive local data may be over-collected during diagnostics.

Mitigation: Limit collection to redacted metrics, avoid raw config or identity-file contents, and review reports before sharing.

Risk: Remediation guidance may include curl-to-shell or forced install commands.

Mitigation: Remove curl-to-shell and --force recommendations, and require explicit approval before any fix command is executed.

Risk: Report delivery can send or open reports outside the terminal when channels are configured.

Mitigation: Disable external report delivery and browser auto-open unless the user explicitly requests them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1215656/skills/botlearn-doctor-1-0-2)
- [Publisher profile](https://clawhub.ai/user/1215656)
- [OpenClaw Health Doctor instructions](artifact/SKILL.md)
- [Data collection protocol](artifact/data_collect.md)
- [Security risk checks](artifact/check_security.md)
- [Setup and prerequisites](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON diagnostic reports, with optional HTML rendering and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports use traffic-light status labels and domain scores; credential values should be redacted.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter says 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
