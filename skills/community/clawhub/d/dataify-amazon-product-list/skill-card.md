## Description:

Collect Amazon product-list records by keyword and marketplace domain through Dataify Builder and return the collected JSON result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to submit Dataify Amazon product-list collection jobs by keyword and Amazon marketplace domain, then monitor the task and retrieve final JSON results. It is intended for list-style Amazon collection, not single-ASIN details, reviews, or global brand collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Dataify account token and can submit paid or credit-consuming Dataify jobs.

Mitigation: Configure DATAIFY_API_TOKEN through the local environment, do not expose token values in chat or logs, and confirm high-volume or multi-page collection scopes before execution.

Risk: Security evidence reports credential and import-handling risks, including token-in-query and external import-path behavior.

Mitigation: Review, fix, or explicitly accept these behaviors before installation; run the skill in a least-privileged environment until resolved.

Risk: Security evidence reports broader under-disclosed scraping and business-intelligence helper code beyond the advertised Amazon-list workflow.

Mitigation: Review the bundled scripts before deployment and restrict invocation to the advertised Amazon product-list workflow unless the additional helpers are intentionally approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-amazon-product-list)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON task/result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN; normal execution can submit credit-consuming Dataify jobs and may wait for asynchronous task completion.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
