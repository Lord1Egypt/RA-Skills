## Description: <br>
ClawDiscover helps agents find, browse, and subscribe to newly published tools and services through free and optional paid API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x4v13r1120](https://clawhub.ai/user/x4v13r1120) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent developers and operators use this skill to add service-discovery checks, category filtering, webhook subscriptions, and optional premium discovery feeds to an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring heartbeat checks and paid x402 endpoints can create automated traffic or costs. <br>
Mitigation: Keep recurring checks and paid endpoint use under explicit user control, with clear limits and review before enabling automation. <br>
Risk: Webhook registration and service submission can share URLs, categories, service details, or agent identifiers with a third-party service. <br>
Mitigation: Submit only data intended for ClawDiscover, avoid sensitive payloads, and review webhook destinations before registration. <br>


## Reference(s): <br>
- [ClawDiscover website and API spec](https://clawdiscover.com) <br>
- [ClawHub release page](https://clawhub.ai/x4v13r1120/clawdiscover) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with API examples, curl commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes free API endpoints, optional paid x402 endpoints, heartbeat guidance, webhook setup, and service submission examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
