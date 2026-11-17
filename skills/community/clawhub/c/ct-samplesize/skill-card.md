## Description:

Calculates sample size and statistical power for clinical trials across 67 test types, with reproducible R code and SVG figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[medstatstar](https://clawhub.ai/user/medstatstar)

### License/Terms of Use:

MIT

## Use Case:

Clinical trial practitioners, researchers, and statisticians use the skill to estimate sample size and power across trial designs and prepare calculation outputs for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trial-design inputs and related metadata may be sent to a remote service for computation.

Mitigation: Keep confidential protocols and other sensitive material out of prompts; review the outbound data disclosure before using remote computation.

Risk: The security assessment reports file and credential access concerns, and analysis was partial.

Mitigation: Use an isolated environment, limit available credentials, and review any files the skill creates or accesses.

Risk: The security assessment flags possible output reliability issues for clinical-design calculations.

Mitigation: Have a qualified statistician independently verify calculations and assumptions before protocol, regulatory, or other consequential use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/medstatstar/skills/ct-samplesize)
- [Publisher profile](https://clawhub.ai/user/medstatstar)
- [Project homepage](https://github.com/medstatstar/ct-samplesize)
- [Project README](https://github.com/medstatstar/ct-samplesize/blob/main/README.md)
- [Statistical formulas](references/formulas.md)
- [Security model](references/security_model.md)
- [Calculation examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files]

**Output Format:** [Calculation summaries, reproducible R code, and SVG figures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include design assumptions and parameters; validate statistical results before consequential use.]

## Skill Version(s):

5.15.0 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
