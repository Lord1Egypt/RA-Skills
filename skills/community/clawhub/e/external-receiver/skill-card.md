## Description: <br>
External Receiver starts an HTTP service that receives file uploads, text messages, and JSON webhooks and forwards them into an OpenClaw session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kriouerlia](https://clawhub.ai/user/kriouerlia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to bridge external systems into OpenClaw by receiving uploads, messages, or webhook payloads and surfacing them in an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The receiver can expose uploads and agent-visible messages to anyone who can reach the HTTP server if deployed without access controls. <br>
Mitigation: Bind the service to localhost or a private interface, set RECEIVER_SECRET, and place it behind firewall, VPN, or TLS controls before accepting external traffic. <br>
Risk: Received files and webhook payloads are external input and may be untrusted. <br>
Mitigation: Treat all received content as untrusted, review files before use, and restrict public access to status and download endpoints. <br>


## Reference(s): <br>
- [External Receiver on ClawHub](https://clawhub.ai/kriouerlia/external-receiver) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces server setup instructions, endpoint examples, and agent-visible received message or file notifications.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
