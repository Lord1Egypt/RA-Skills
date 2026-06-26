## Description: <br>
Verifiable human ownership for OpenClaw agents. Register your agent under your human owner via VeryAI palm verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oyyblin](https://clawhub.ai/user/oyyblin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Clawkey to register an OpenClaw or compatible agent under a verified human owner and to let third parties check whether a device ID or Ed25519 signature is tied to that verified registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using the skill links a persistent agent device ID and public key to ClawKey and a human verification flow. <br>
Mitigation: Use the skill only when that association is intended, and review ClawKey and VeryAI privacy terms before completing verification. <br>
Risk: The registration flow depends on local private-key signing; exposing the private key would compromise the agent identity. <br>
Mitigation: Keep the private key local and send only the device ID, public key, message, signature, and timestamp to the API. <br>
Risk: Heartbeat and status checks create recurring contact with ClawKey services. <br>
Mitigation: Disable or avoid heartbeat and status checks if recurring service contact is not desired. <br>


## Reference(s): <br>
- [Clawkey on ClawHub](https://clawhub.ai/oyyblin/clawkey) <br>
- [ClawKey Homepage](https://clawkey.ai) <br>
- [ClawKey API Base](https://api.clawkey.ai/v1) <br>
- [ClawKey Skill Document](https://clawkey.ai/skill.md) <br>
- [ClawKey Heartbeat Document](https://clawkey.ai/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands, JavaScript examples, and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides registration, polling, device lookup, and signature verification while keeping private keys local.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
