## Description:

Assesses a user's job tasks for AI substitution risk and creates an evidence-aware career transition plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cglt2026opc](https://clawhub.ai/user/cglt2026opc)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and career coaches use this skill to collect role, task, skills, income-structure, and anxiety context, assess AI substitution risk, and produce a practical transition plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects career, income, and anxiety details and saves them to a local report by default.

Mitigation: Review before installing, invoke only intentionally, and prefer asking before saving, using a fixed safe report directory, sanitizing filenames, and offering preview-only or redacted reports.

Risk: Career-risk assessments can be misleading if the user lacks industry, regional, or hiring-market evidence.

Mitigation: Keep ratings evidence-based, avoid unsupported predictions about job-loss timing, and pair high-risk findings with concrete transition steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cglt2026opc/skills/career-diagnostic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Files]

**Output Format:** [Markdown career diagnostic report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow defaults to saving a local Markdown report named for the diagnostic subject.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
