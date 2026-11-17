## Description:

Scan a third-party OpenClaw skill with ClawVet and act on its A to F grade before installing or trusting it. Use when the user says "scan this skill", "is this skill safe", "vet/check this skill", "should I install this", "audit my skills", or "clawvet", or hands you a SKILL.md from ClawHub or another untrusted source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohibshaikh](https://clawhub.ai/user/mohibshaikh)

### License/Terms of Use:

MIT

## Use Case:

Developers use ClawVet to scan third-party OpenClaw skills, review the scanner's A to F grade and coverage, and decide whether to install or trust them. It also provides commands for auditing installed skills and configuring an install gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan was partial because several local references could not be resolved, so the benign verdict does not guarantee zero risk.

Mitigation: Resolve the missing references and scan the complete local skill before relying on the result.

Risk: The security guidance notes an unpinned package reference.

Mitigation: Confirm that you trust the package source and pin its version when reproducibility is important.

## Reference(s):

- [ClawVet source repository](https://github.com/MohibShaikh/clawvet)
- [ClawVet on ClawHub](https://clawhub.ai/mohibshaikh/skills/clawvet)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and scanner findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on scan coverage and the scanner's reported grade.]

## Skill Version(s):

0.14.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
