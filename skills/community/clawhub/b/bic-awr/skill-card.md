## Description:

Submits database AWR or compatible performance reports to the BIC-QA AWR API for asynchronous analysis delivered by email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbsyd2](https://clawhub.ai/user/bbsyd2)

### License/Terms of Use:

MIT-0

## Use Case:

External users, database administrators, and engineers use this skill to submit AWR-compatible database performance reports to BIC-QA for remote asynchronous analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWR reports may contain sensitive database, host, SQL, or workload details and are uploaded to BIC-QA for remote analysis.

Mitigation: Review or redact sensitive details before upload and submit reports only when the user explicitly wants remote analysis.

Risk: The BIC-QA API key is required for authentication and could be misused if exposed.

Mitigation: Store the API key only on trusted machines, use protected configuration or environment variables, and rotate the key if exposure is suspected.

## Reference(s):

- [BIC-QA homepage](https://www.bic-qa.com)
- [BIC-QA AWR API endpoint](https://api.bic-qa.com/skills/awr)
- [ClawHub skill page](https://clawhub.ai/bbsyd2/skills/bic-awr)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provisioned BIC-QA API key; uploads AWR reports to BIC-QA for asynchronous email delivery.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
