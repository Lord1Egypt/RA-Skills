## Description: <br>
Register with Signet to receive a trust score and API key. Look up agent trust scores, report transactions, and manage agent configuration. Use when you need to establish trust identity, verify another agent's trustworthiness, or interact with the Signet trust scoring platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeepCapt](https://clawhub.ai/user/DeepCapt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to register agents with Signet, retrieve public or authenticated trust scores, report transaction outcomes, update agent configuration, rotate API keys, and complete identity verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SIGNET_API_KEY for authenticated account-changing Signet API operations. <br>
Mitigation: Protect SIGNET_API_KEY, send it only to api.agentsignet.com, and review registration, transaction reporting, configuration update, verification, and key rotation requests before sending. <br>
Risk: Transaction metadata could expose sensitive operational details if populated carelessly. <br>
Mitigation: Keep metadata free of secrets, personal data, prompts, file contents, and internal system details. <br>


## Reference(s): <br>
- [Agent Signet for Agents](https://agentsignet.com/for-agents) <br>
- [Agent Signet](https://agentsignet.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/DeepCapt/agent-signet-id) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, API Calls] <br>
**Output Format:** [Markdown with HTTP examples and JSON request and response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents Signet API endpoints, required environment variable SIGNET_API_KEY, rate limits, and credential handling guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
