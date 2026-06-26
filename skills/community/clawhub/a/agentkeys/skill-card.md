## Description: <br>
Secure credential proxy for AI agents. Make API calls through AgentKeys - real secrets never leave the vault. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexandr-belogubov](https://clawhub.ai/user/alexandr-belogubov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure AI agents to call external APIs through the AgentKeys proxy while keeping real service credentials outside the agent runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Covered API calls and request data are routed through the AgentKeys proxy service. <br>
Mitigation: Confirm the service trust and privacy terms, and route only API traffic approved for that proxy before installing. <br>


## Reference(s): <br>
- [AgentKeys Skill Page](https://clawhub.ai/alexandr-belogubov/agentkeys) <br>
- [AgentKeys Documentation](https://agentkeys.io/docs) <br>
- [AgentKeys Dashboard](https://app.agentkeys.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTKEYS_PROXY_URL and either AGENTKEYS_API_KEY or AGENTKEYS_PROXY_TOKEN.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
