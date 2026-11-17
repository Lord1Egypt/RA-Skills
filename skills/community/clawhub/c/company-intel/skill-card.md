## Description:

Build structured company intelligence for interview preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanghong5233](https://clawhub.ai/user/wanghong5233)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to gather structured company research for interview preparation, including business direction, likely technology stack, funding or team-stage signals, interview style, risks, and preparation suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends company names, role titles, job descriptions, and focus keywords to a local service.

Mitigation: Use it only with a trusted service on 127.0.0.1:8010, and avoid confidential hiring context unless storage and retention behavior are understood.

Risk: The include_search option may cause the local service to perform external searches.

Mitigation: Disable external search or review the service policy before using sensitive or internal company research inputs.

Risk: Company intelligence can be incomplete or uncertain.

Mitigation: Preserve confidence and uncertainty in the final summary and do not present inferred facts as certain.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional curl command template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a local company-intelligence service and summarize its response with confidence and uncertainty noted.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
