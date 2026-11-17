## Description:

A local checker for expense and budget worksheets that runs 14 built-in checks per client directory and prints one conclusion line per client with source file and line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

Finance staff, management accountants, expense reviewers, and bookkeeping providers use this skill before monthly expense close and operating reviews to check exported Chinese-language expense and budget worksheets for arithmetic and consistency issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on worksheet results as audit approval, invoice authenticity verification, legal advice, or accounting judgment.

Mitigation: Treat output as arithmetic and consistency checks only, and have qualified finance or audit staff review conclusions before relying on them.

Risk: The free release explicitly lists checks and sub-checks that are not executed.

Mitigation: Review the not-run checks in the output scope before using the result to support monthly close or review decisions.

Risk: The checker operates on exported Chinese-language financial worksheets that may contain sensitive business data.

Mitigation: Run it only in an environment approved for those worksheets and provide exported copies rather than direct access to finance systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/fee-budget-pack-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console text, with optional JSON output when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result stream per run; findings cite the source file and line where available.]

## Skill Version(s):

1.0.29 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
