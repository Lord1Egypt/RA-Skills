## Description: <br>
Infrastructure for AI agents: phone, email, social accounts, compute, domains, and voice calling, paid with USDC on Solana or Base via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xartex](https://clawhub.ai/user/0xartex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to provision and manage AgentOS resources such as phone numbers, encrypted email inboxes, compute, domains, wallets, and voice calls through CLI or HTTP API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate paid AgentOS operations such as buying phone numbers, sending messages, placing calls, deploying compute, registering domains, and reading paid resources. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit human confirmation before any paid action. <br>
Risk: The skill includes destructive or persistent infrastructure actions such as deleting compute servers, changing DNS records, registering webhooks, and managing wallet-owned resources. <br>
Mitigation: Review each target resource identifier and operation before execution, and restrict agents to the minimum resources needed for the task. <br>
Risk: Phone, voice, email, webhooks, attachments, and call recording can handle privacy-sensitive communications. <br>
Mitigation: Use messaging, recording, and outbound communication only with appropriate consent, retention controls, and clear user authorization. <br>
Risk: The decryption helper reads a local Solana keypair to decrypt AgentOS email content. <br>
Mitigation: Keep private keys out of prompts and untrusted environments, and run the helper only on trusted machines with reviewed inputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xartex/agents-infra) <br>
- [AgentOS API](https://agntos.dev) <br>
- [AgentOS API docs](https://agntos.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with CLI commands, API endpoint tables, and a JavaScript decryption helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes paid service costs and operational commands for wallet-owned AgentOS resources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
