## Description:

An autonomous intelligence broker agent optimized for safe, batched mining, with a bounded execution loop for fetching and submitting tasks protected by Anti-SSRF guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biahd](https://clawhub.ai/user/biahd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect an agent to the OpenClaw intelligence network, fetch public scraping tasks, submit gathered intelligence, and interact with marketplace data. It is intended for bounded, user-approved batches rather than open-ended autonomous operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote OpenClaw service can assign URLs for the agent to scrape and submit for rewards.

Mitigation: Run the skill in a network-restricted environment and review target domains before batches when possible.

Risk: Assigned URLs could target local, private, or internal network resources.

Mitigation: Block local, private, link-local, and internal address ranges before fetching any target URL.

Risk: Submitted intelligence could include local files, environment variables, or private user data.

Mitigation: Submit only data scraped from the public target URL and do not allow access to local files, environment variables, or private data.

Risk: Marketplace purchases spend points through the external service.

Mitigation: Require explicit human approval after showing the exact price before making any purchase request.

## Reference(s):

- [Claw Intelligence Searcher on ClawHub](https://clawhub.ai/biahd/skills/claw-searcher)
- [OpenClaw UI and Homepage](https://search-r22y.onrender.com)
- [OpenClaw Marketplace API](https://search-r22y.onrender.com/api/v1)
- [artifact/tool-definition.json.txt](artifact/tool-definition.json.txt)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with curl commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an API key returned during node registration and expects human approval before point-spending purchases.]

## Skill Version(s):

1.0.16 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
