## Description:

Collects Amazon global-marketplace product data by product URL, category URL, keyword, or keyword plus brand through Dataify Builder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to submit and monitor Dataify Builder tasks that collect Amazon global product data, then retrieve final JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Dataify API token and may submit collection tasks that consume credits.

Mitigation: Use a rotatable Dataify token, verify token handling before installation, and review task scope before submitting high-volume collections.

Risk: Server security evidence reports bundled non-Amazon workflow scripts and runtime-shadowing risks outside the core Amazon collection flow.

Mitigation: Review or remove non-Amazon workflow scripts and prefer packaged runtime imports before deployment.

Risk: Server security guidance flags polling paths that authenticate with API keys in URLs.

Mitigation: Prefer a version that authenticates polling without placing API keys in URLs and avoid retaining request URLs in logs.

## Reference(s):

- [Modes and Parameters](references/modes-and-parameters.md)
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-amazon-global-product)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit paid Dataify collection tasks and wait for asynchronous final JSON results when a Dataify API token is configured.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
