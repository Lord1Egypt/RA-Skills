## Description: <br>
Set up APort guardrails for OpenClaw with local-first policy enforcement that checks tool calls against a passport before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aporthq](https://clawhub.ai/user/aporthq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install, configure, and verify APort Agent Guardrails for OpenClaw so tool calls are evaluated before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent OpenClaw policy-enforcement hook that changes agent tool execution. <br>
Mitigation: Install only when this behavior is intended, review the generated ~/.openclaw configuration and wrapper scripts, and confirm how to disable or reset the plugin before relying on it in a sensitive environment. <br>
Risk: Cloud mode and data handling may be ambiguous during setup. <br>
Mitigation: Choose local mode during setup if tool-call metadata should not be sent to APort, and review any APORT_API_URL and APORT_AGENT_ID configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aporthq/aport-agent-guardrail) <br>
- [Source code](https://github.com/aporthq/aport-agent-guardrails) <br>
- [Security Model](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/SECURITY_MODEL.md) <br>
- [OAP Specification](https://github.com/aporthq/aport-spec) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.1.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
