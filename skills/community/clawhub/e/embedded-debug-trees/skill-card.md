## Description:

Provides symptom-driven decision trees for diagnosing common MCU hardware and firmware faults, with evidence-gathering steps and likely causes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT

## Use Case:

Developers and embedded engineers use the decision trees to gather evidence and troubleshoot MCU faults across startup, peripherals, RTOS, data transfer, and low-power operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One local reference could not be resolved, leaving some review evidence incomplete; hardware-specific guidance may not cover every device or variant.

Mitigation: Review the unresolved reference and verify device-specific steps against the official datasheet and reference manual before applying them.

## Reference(s):

- [Decision Trees Reference](references/trees.md)
- [ClawHub skill page](https://clawhub.ai/liujycode/skills/embedded-debug-trees)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with diagnostic steps and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static reference material; does not execute code. Verify hardware-specific recommendations against the official datasheet for the target part.]

## Skill Version(s):

1.4.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
