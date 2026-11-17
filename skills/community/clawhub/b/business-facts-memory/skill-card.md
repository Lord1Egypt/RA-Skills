## Description:

Maintains approved business prices, policies, and service details with dates and sources, and flags conflicting or expired information for customer-facing agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-facing agents and business teams use this skill to record source-dated prices, policies, and service details, check them before answering customers, and flag discrepancies for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business facts are sent to a third-party service, potentially exposing sensitive information.

Mitigation: Use a least-privilege API key if available, and avoid sending secrets, customer personal data, or confidential internal rationale.

Risk: Outdated or conflicting recalled facts could lead to incorrect customer-facing answers.

Mitigation: Verify recalled facts before use, flag discrepancies, and regularly review expired or conflicting records.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/business-facts-memory)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source-dated facts and conflict flags; requires a BlueColumn API key.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
