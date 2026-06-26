## Description: <br>
Issue virtual Visa/MC cards funded by USDT, check balance, get card credentials, and fetch OTP codes via REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elvismusli](https://clawhub.ai/user/elvismusli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and operators use AgentFin to inspect prepaid virtual card balance and status, retrieve payment credentials and OTPs, top up a card, and review transactions for online purchases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose live payment-card credentials and OTP codes to an agent. <br>
Mitigation: Require explicit approval before retrieving or revealing card credentials or OTPs, prevent logging or long-term memory storage of card data, and keep the API key revocable. <br>
Risk: The skill supports fund-moving actions such as card top-ups and can enable real purchases. <br>
Mitigation: Use a dedicated low-balance prepaid account and require explicit approval for every purchase and top-up. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elvismusli/agentfin) <br>
- [AgentFin homepage](https://agentfin.tech) <br>
- [AgentFin API base URL](https://agentfin.tech/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with REST endpoint guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTFIN_API_KEY and access to the AgentFin REST API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
