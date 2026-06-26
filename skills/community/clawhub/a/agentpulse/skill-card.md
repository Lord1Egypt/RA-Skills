## Description: <br>
Track LLM API costs, tokens, latency, and errors for your AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sru4ka](https://clawhub.ai/user/sru4ka) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use AgentPulse to report LLM API usage metadata and answer questions about cost, token usage, latency, errors, and model mix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends ongoing LLM usage metadata and an API key to an endpoint that the scanner says may not match the publisher's active AgentPulse site. <br>
Mitigation: Confirm the correct AgentPulse endpoint with the publisher before setting AGENTPULSE_API_KEY or installing the skill. <br>
Risk: LLM usage metadata and error strings may leave the user's environment during reporting and statistics lookups. <br>
Mitigation: Test with a disposable AgentPulse account and API key, and avoid sending sensitive error details until the endpoint and data handling expectations are verified. <br>


## Reference(s): <br>
- [ClawHub AgentPulse release](https://clawhub.ai/sru4ka/agentpulse) <br>
- [AgentPulse dashboard](https://agentpulse.dev/dashboard) <br>
- [AgentPulse alerts dashboard](https://agentpulse.dev/dashboard/alerts) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text summaries] <br>
**Output Format:** [Markdown guidance with inline curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and AGENTPULSE_API_KEY; reports and retrieves LLM usage metadata through AgentPulse endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
