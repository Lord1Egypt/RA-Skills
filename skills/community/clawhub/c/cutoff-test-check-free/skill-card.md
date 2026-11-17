## Description:

Runs a local Chinese-language cutoff check for revenue and cost working papers, including recalculation, period/date consistency checks, duplicate-row checks, blank-value checks, and source-cited findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, audit, and month-end close teams use this skill before period close or audit sampling to check whether cutoff working-paper rows have internally consistent dates, periods, amounts, document types, and required fields. Results are advisory checks and do not replace accounting judgment, audit procedures, or assurance opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat deterministic cutoff findings as audit opinions or accounting conclusions.

Mitigation: Present results as advisory checks and require professional review for revenue recognition, cutoff conclusions, audit evidence, and assurance reporting.

Risk: Working-paper text may contain sensitive accounting or customer data.

Mitigation: Run the skill locally as documented and avoid using it in environments where user-supplied materials may be logged or shared outside the review workflow.

Risk: Duplicate-document findings may be repeated because the duplicate check runs twice.

Mitigation: De-duplicate repeated duplicate-document messages during review and confirm the underlying document rows before remediation.

Risk: The free version omits some cutoff checks, including long cross-period delays and post-period amount comparisons.

Mitigation: Review the reported executed-check scope and use additional procedures for checks listed as not run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/cutoff-test-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON containing cutoff findings, summary counts, executed-check scope, and omitted-check notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Node.js execution; reads user-supplied working-paper text and reports deterministic findings without network use or persistence.]

## Skill Version(s):

1.0.25 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
