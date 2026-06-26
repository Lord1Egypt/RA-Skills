## Description: <br>
AI Agent Detection and Response for real-time security monitoring with Sigma rules and optional LLM-powered triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markbriers](https://clawhub.ai/user/markbriers) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and operators use AgentShield to monitor AI agent tool calls, evaluate them against Sigma-style security rules, and optionally triage suspicious events with OpenAI or Anthropic providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation makes persistent and blocking changes to the local OpenClaw environment. <br>
Mitigation: Review install.sh before installation and confirm that a persistent security daemon and timeout_policy=block behavior are acceptable. <br>
Risk: The installer creates a local authentication token and configures OpenClaw to send tool-call evaluation requests to the AgentShield service. <br>
Mitigation: Keep the generated token private, protect the AgentShield configuration file, and rotate the token if it may have been exposed. <br>
Risk: Optional LLM triage can send security event details outside the local machine. <br>
Mitigation: Enable OpenAI or Anthropic triage only after confirming that the provider, model, and event data handling meet the deployment's security requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markbriers/agentshield) <br>
- [Publisher profile](https://clawhub.ai/user/markbriers) <br>
- [OpenClaw metadata](artifact/claw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, configuration, operation, API, and troubleshooting guidance for an AgentShield security monitor.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
