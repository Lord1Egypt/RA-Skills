## Description: <br>
Bridge to external vertical agents (Google ADK, VeADK, etc.) for specialized tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqsge](https://clawhub.ai/user/sqsge) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to delegate user requests to trusted external specialized agents through a configured HTTP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and context sent through this skill are shared with the configured remote service. <br>
Mitigation: Use only remote agents you control or trust, and avoid sending sensitive data unless the endpoint is approved for that data. <br>
Risk: A misconfigured endpoint or untrusted authentication token can expose requests or credentials. <br>
Mitigation: Verify REMOTE_AGENT_URL before use and use a scoped, revocable REMOTE_AGENT_KEY when authentication is needed. <br>
Risk: Disabling TLS verification can allow traffic interception in non-controlled environments. <br>
Mitigation: Avoid --insecure except during controlled testing with non-sensitive data. <br>


## Reference(s): <br>
- [Google Agent Development Kit documentation](https://google.github.io/adk-docs/) <br>
- [ClawHub skill page](https://clawhub.ai/sqsge/clawhub-skill-remote-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REMOTE_AGENT_URL; REMOTE_AGENT_KEY is optional for bearer-token authentication.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
