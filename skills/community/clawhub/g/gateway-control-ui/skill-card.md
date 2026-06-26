## Description: <br>
Step-by-step guide to log into the OpenClaw Control UI, enter gateway token, approve device pairing, and verify connection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access an OpenClaw Gateway Control UI, authenticate with service credentials, enter the gateway token, approve a device pairing request, and verify connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway token and service password handling can expose credentials if copied into URLs, logs, screenshots, or shared command output. <br>
Mitigation: Treat the gateway token and service password as secrets, avoid embedding credentials in URLs when possible, and redact logs or screenshots before sharing. <br>
Risk: Approving the wrong device pairing request can authorize an unintended device. <br>
Mitigation: Approve only pairing request IDs that the operator recognizes and expects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lotfinity/gateway-control-ui) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for OpenClaw gateway login, token entry, device pairing, troubleshooting, and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
