## Description:

Provides decision-support classifications of data as core, important, or general under cited Chinese data-grading rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-governance teams use this skill for preliminary classification of data by industry, national-core-interest relevance, and scale, with warnings when inputs are incomplete. Its results are decision support, not authoritative legal determinations.

### Deployment Geography for Use:

China (for the cited Chinese data-classification rules)

## Known Risks and Mitigations:

Risk: The skill requests broad file, shell, write, and web access despite claiming those permissions are disabled.

Mitigation: Review before installation and run only where that level of agent access is acceptable.

Risk: Classification inputs may contain personal, business, or regulated data.

Mitigation: Redact sensitive inputs unless the runtime is approved for the data, and have a qualified reviewer check results against official rules.

## Reference(s):

- [ClawHub release: data-grade-checker](https://clawhub.ai/zhaoxinghua09-cell/skills/data-grade-checker)
- [Bundled README and rule-source review checklist](README.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a data grade, suggested obligations, warnings, and a result code (0: complete; 1: warnings; 2: invalid input).]

## Skill Version(s):

1.0.3 (source: server-resolved ClawHub release; bundled documents and script report older versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
