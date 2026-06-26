## Description: <br>
Purchase and manage prepaid virtual Visa cards usable at US online merchants for secure AI agent payments via the agentcard CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florrdv](https://clawhub.ai/user/florrdv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, power users, and agents use this skill to create and manage prepaid virtual Visa cards for online purchases such as API credits, SaaS subscriptions, domains, and cloud resources. <br>

### Deployment Geography for Use: <br>
Global use, with card transactions limited to US-based online merchants. <br>

## Known Risks and Mitigations: <br>
Risk: An agent can create prepaid cards or initiate refund workflows that affect real funds. <br>
Mitigation: Keep user confirmation enabled and set a low maximum purchase amount before using the skill. <br>
Risk: Payment card details and local AgentCard session data are sensitive. <br>
Mitigation: Retrieve card details only when needed, avoid local persistence, and protect the local AgentCard session file. <br>
Risk: The CLI package, terms, or payment workflow may change before real purchases are made. <br>
Mitigation: Verify the AgentCard CLI package and confirm current AgentCard terms and commands before use. <br>
Risk: Transactions at non-US merchants are expected to fail. <br>
Mitigation: Confirm the merchant is US-based before using a card for checkout. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/florrdv/agentcardai) <br>
- [AgentCard website](https://agentcard.ai) <br>
- [Alchemy](https://alchemy.com) <br>
- [agentcard npm package code](https://www.npmjs.com/package/agentcard?activeTab=code) <br>
- [npm provenance documentation](https://docs.npmjs.com/generating-provenance-statements) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes payment workflow guidance, user-confirmation expectations, and CLI command examples.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
