## Description:

Checks year-end bonus pool worksheets by recalculating allocation, net bonus, one-time annual bonus tax, totals, duplicate people, and blanks, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Payroll, finance, and HR staff use this skill at year-end to review copied bonus worksheet text for bonus allocation, net bonus, annual one-time bonus tax arithmetic, totals, duplicate people, and blanks before manual approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is used with payroll or bonus worksheet text, which can contain sensitive compensation data.

Mitigation: Run it only in a trusted local environment and provide only the worksheet text needed for the check.

Risk: The free release covers only the listed checks and should not be treated as complete tax advice.

Mitigation: Review the checks that were not run and have payroll or tax reviewers confirm results before using them for decisions.

Risk: Incomplete or unrecognized input can prevent the checker from producing a supported conclusion.

Mitigation: Provide a table with recognizable headers and review any missing-field guidance before rerunning the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bonus-pool-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Console text or JSON report with findings, summary totals, executed checks, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input returns missing requirements instead of a conclusion.]

## Skill Version(s):

1.0.55 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
