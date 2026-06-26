## Description: <br>
Register and manage ICANN domains for AI agents with wallet authentication, USDC payments on Base or Solana, and DNS management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibrant](https://clawhub.ai/user/vibrant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to check and register domains, create ICANN registrant profiles, and manage DNS or nameserver settings through the AgentNS client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real USDC for domain registration. <br>
Mitigation: Use a dedicated low-balance wallet and confirm each domain, price, and registration term before execution. <br>
Risk: The skill can change live DNS records and nameservers. <br>
Mitigation: Review every DNS and nameserver change before execution and keep a backup of existing DNS settings for rollback. <br>
Risk: The workflow depends on the external agentns-client package. <br>
Mitigation: Pin and review the package version before allowing an agent to use it. <br>
Risk: Wallet files may authorize payment or domain administration actions. <br>
Mitigation: Protect wallet files and limit access to the credentials needed for the intended task. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vibrant/agentns) <br>
- [AgentNS Website](https://agentns.xyz) <br>
- [AgentNS API Docs](https://agentns.xyz/docs) <br>
- [agentns-client on PyPI](https://pypi.org/project/agentns-client/) <br>
- [agentns-client GitHub Repository](https://github.com/vibrant/agentns_client) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, payment, registrant, DNS, and nameserver setup steps.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
