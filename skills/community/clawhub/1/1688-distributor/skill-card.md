## Description:

Automate 1688.com product search, AI selection, batch distribution to your shop, and view distribution logs in one seamless workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeppaura](https://clawhub.ai/user/zeppaura)

### License/Terms of Use:


## Use Case:

External merchants and operators use this skill to search 1688.com, apply product criteria, select matching items, submit distribution to a target shop, and review distribution logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk distribution actions may submit listings to an authenticated 1688 shop from broad or vague product criteria.

Mitigation: Require explicit confirmation of the target shop, product count, selected filters, and final distribution action before submitting.

Risk: Copied distribution logs may include sensitive shop or product details.

Mitigation: Review and redact copied logs before sharing them outside the operating environment.

## Reference(s):

- [1688 AI product selection and distribution workspace](https://air.1688.com/app/channel-fe/distribution-work/ai-assistant.html#/multi-agent)
- [ClawHub skill page: 1688 Distributor](https://clawhub.ai/zeppaura/skills/1688-distributor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with JavaScript code blocks and structured status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include target shop name, selected product count, distribution status, and copied distribution-log content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
