## Description:

Query ocean freight rates and search shipping prices via the Eyun freight assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobofrivia](https://clawhub.ai/user/bobofrivia)

### License/Terms of Use:

MIT-0

## Use Case:

Freight operations users and agents use this skill to query Eyun for ocean or air freight rates, route-specific shipping quotes, and structured rate information. It relies on a configured Eyun endpoint and company ID to submit the user's freight question and return the remote answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw business queries may send sensitive shipment or customer details to the configured Eyun endpoint.

Mitigation: Use only a trusted Eyun endpoint, require HTTPS, validate EYUN_BASE_URL, and avoid sending unnecessary sensitive shipment or customer details.

Risk: Remote answers are relayed verbatim without attribution or safety checks.

Mitigation: Review responses before acting on them and update the skill so remote answers are attributed and can be safety-checked.

Risk: Endpoint and company ID values affect shell-based curl calls and can create insecure HTTP or command-handling exposure.

Mitigation: Validate EYUN_BASE_URL and require a numeric EYUN_COMPANY_ID before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bobofrivia/skills/eyun-freight)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown freight-rate response with optional structured table data from the Eyun API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl plus EYUN_BASE_URL and EYUN_COMPANY_ID configuration.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
