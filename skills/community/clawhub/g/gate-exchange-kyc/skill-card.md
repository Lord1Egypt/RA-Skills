## Description: <br>
Routes Gate users who ask about KYC, identity verification, or withdrawal blocks to the official KYC portal with brief completion guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users use this skill to find the identity verification portal and understand that KYC must be completed on Gate's official web flow. It also helps agents redirect KYC status or document-submission requests away from chat and toward the portal or support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on external runtime rules that can change outside the reviewed package. <br>
Mitigation: Install only when the publisher is trusted and review the current runtime guidance before using the skill in sensitive account workflows. <br>
Risk: KYC workflows involve sensitive identity and account information. <br>
Mitigation: Direct users to complete verification only on the official Gate portal and do not ask them to paste identity documents, API keys, passwords, or account credentials into chat. <br>
Risk: Users may expect the agent to approve KYC, check status, or accept documents in chat. <br>
Mitigation: State that verification is completed only on the portal and route status questions to the portal or Gate support. <br>


## Reference(s): <br>
- [Gate Exchange KYC Portal Skill on ClawHub](https://clawhub.ai/gate-exchange/gate-exchange-kyc) <br>
- [MCP execution specification](references/mcp.md) <br>
- [Scenarios](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text guidance with an official portal URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not process identity documents, approve KYC, or mutate account status.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter: 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
