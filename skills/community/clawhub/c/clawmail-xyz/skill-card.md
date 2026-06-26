## Description: <br>
Email service for AI agents with wallet authentication and crypto payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrickshuff](https://clawhub.ai/user/patrickshuff) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to give AI agents ClawMail inboxes, authenticate with wallet signatures, and manage mailbox messages through MCP or REST workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet authentication and USDC payment prompts can authorize identity or paid mailbox actions. <br>
Mitigation: Use a dedicated wallet where practical and require explicit review of wallet signatures and payment prompts before approval. <br>
Risk: Mailbox session tokens can grant access to list, read, or delete messages. <br>
Mitigation: Keep JWT tokens private and avoid exposing them in shared logs, prompts, or configuration files. <br>
Risk: The delete message tool can permanently remove mailbox content. <br>
Mitigation: Require explicit approval before allowing an agent to delete messages. <br>
Risk: The npm package and linked source repository are not verified by server-resolved provenance for this release. <br>
Mitigation: Before installing, verify the npm package and linked source repository through trusted channels. <br>


## Reference(s): <br>
- [ClawMail website](https://clawmail.xyz) <br>
- [ClawHub skill page](https://clawhub.ai/patrickshuff/clawmail-xyz) <br>
- [Publisher profile](https://clawhub.ai/user/patrickshuff) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes MCP tools for mailbox availability, wallet login, message listing, message reading, and message deletion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
