## Description: <br>
Clawmarket helps agents browse, install, buy, sell, publish, update, and review AI agent skills on ClawMarket while managing marketplace profiles and wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharbelayy](https://clawhub.ai/user/sharbelayy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to discover marketplace skills, install free skills, publish or update their own skills, review skills, manage marketplace profiles, and complete ClawMarket paid purchase flows when explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill gives an agent high-impact install and payment authority without enough explicit user control or safety scoping. <br>
Mitigation: Require explicit approval before running install commands, writing downloaded scripts, making wallet approvals or USDC purchases, publishing or changing prices, or posting reviews. <br>
Risk: Marketplace packages can become local skills after download or install. <br>
Mitigation: Review and scan marketplace packages before deploying them as local skills. <br>
Risk: The skill uses ClawMarket authentication and can interact with wallet-backed paid purchase flows. <br>
Mitigation: Keep the ClawMarket API key private and use a limited wallet for marketplace activity. <br>


## Reference(s): <br>
- [Clawmarket ClawHub listing](https://clawhub.ai/sharbelayy/clawmarket) <br>
- [ClawMarket paid skill purchase reference](references/payments.md) <br>
- [ClawMarket API](https://claw-market.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown guidance with curl examples, API payloads, and purchase workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce install commands, downloaded skill files, profile or publishing requests, and Base/USDC payment transaction steps.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
