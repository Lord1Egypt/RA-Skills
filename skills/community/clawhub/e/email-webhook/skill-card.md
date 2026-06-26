## Description: <br>
Receive incoming emails via JSON webhooks and wake the agent. Built for AI Commander. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lksrz](https://clawhub.ai/user/lksrz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run an authenticated email webhook that stores incoming message payloads locally and wakes a specific OpenClaw agent for follow-up handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The webhook receives and stores sensitive email content in a local inbox file. <br>
Mitigation: Protect and rotate inbox.jsonl, restrict filesystem access, and delete retained email data when it is no longer needed. <br>
Risk: The service is intended to run as a public Node HTTPS webhook. <br>
Mitigation: Use a strong WEBHOOK_SECRET, limit network exposure to the intended email worker or proxy, and monitor unauthorized requests. <br>
Risk: Incoming email events can wake an agent and trigger downstream notification behavior. <br>
Mitigation: Set OPENCLAW_AGENT_ID, configure an explicit safe notification channel, and review agent handling before deployment. <br>
Risk: The server can use an undeclared OPENCLAW_GATEWAY_TOKEN and performs automatic public-IP diagnostics. <br>
Mitigation: Review token handling and external diagnostics before running the server in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lksrz/email-webhook) <br>
- [Publisher profile](https://clawhub.ai/user/lksrz) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for Node, OpenClaw, webhook authentication, local inbox storage, and agent wake-up handling.] <br>

## Skill Version(s): <br>
2.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
