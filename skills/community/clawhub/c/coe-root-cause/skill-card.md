## Description:

Run a Correction of Error root-cause analysis for recurring failures, false success, missed work, data loss, and brittle automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghitafilali](https://clawhub.ai/user/ghitafilali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and operators use this skill to produce structured Correction of Error reports after recurring failures, false success, missed work, data loss, or brittle automation incidents. It guides impact, timeline, evidence, root-cause analysis, corrective actions, and verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated postmortems may include sensitive logs, customer data, tokens, or private workspace details if source evidence is copied directly.

Mitigation: Review reports before sharing and redact secrets, personally identifying information, customer data, and private workspace details.

Risk: A generated COE may overstate the root cause or corrective action if evidence is incomplete.

Mitigation: Require concrete evidence, state uncertainty plainly, and include verification evidence for every corrective action.

## Reference(s):

- [COE Root Cause on ClawHub](https://clawhub.ai/ghitafilali/skills/coe-root-cause)
- [ghitafilali ClawHub profile](https://clawhub.ai/user/ghitafilali)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown report with structured sections and optional tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include evidence summaries, 5 Whys analysis, corrective actions, verification evidence, and residual risk.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
