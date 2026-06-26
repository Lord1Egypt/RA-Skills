## Description: <br>
Build your AI Company - 8 models across 4 providers act as your CEO, CTO, CMO, CFO, and Workers. Crypto-native, pay-as-you-go with USDC/USDT. No GPU needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawapiorg](https://clawhub.ai/user/clawapiorg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to configure ClawAPI as a pay-as-you-go OpenAI-compatible model provider. It provides setup, model-selection, balance-monitoring, funding, and troubleshooting guidance for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes guidance for wallet private keys and automatic crypto deposits. <br>
Mitigation: Do not give an agent wallet private keys or authorize automatic deposits; create keys and fund the account manually. <br>
Risk: Crypto funding mistakes can send funds to the wrong token, network, amount, or destination address. <br>
Mitigation: Verify token, network, amount, and destination address yourself, and keep only limited funds exposed. <br>
Risk: Configuration changes can expose API keys or point agents at an unintended paid provider. <br>
Mitigation: Store CLAWAPI_KEY as a secret and review OpenClaw configuration file changes before applying them. <br>


## Reference(s): <br>
- [Clawapi Skill on ClawHub](https://clawhub.ai/clawapiorg/clawapi-skill) <br>
- [ClawAPI homepage](https://clawapi.org) <br>
- [ClawAPI skill documentation](https://clawapi.org/api/skill) <br>
- [ClawAPI structured skill documentation](https://clawapi.org/api/skill?format=json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON, environment variable, shell, and API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLAWAPI_KEY for configured use; crypto funding steps should be manually reviewed before action.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
