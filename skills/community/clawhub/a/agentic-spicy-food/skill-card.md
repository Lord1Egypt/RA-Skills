## Description: <br>
Brand-specific commerce skill for Lafeitu (辣匪兔) that helps an agent browse, recommend, cart, and create handoff orders for Sichuan spicy foods through the official Lafeitu API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NowLoadY](https://clawhub.ai/user/NowLoadY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search Lafeitu products, compare variants and promotions, manage a cart, handle account/profile flows, and create checkout-ready orders while leaving payment completion to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change carts, create unpaid orders, update profile details, and use saved account tokens when directed. <br>
Mitigation: Confirm products, quantities, profile changes, recipient phone numbers, and shipping addresses before running mutating commands. <br>
Risk: Saved Lafeitu credentials and visitor identifiers can persist locally after account-bound actions. <br>
Mitigation: Use logout or remove the credential directory when the user does not want the token retained. <br>
Risk: Product recommendations or order actions can be wrong if they are not grounded in current catalog data. <br>
Mitigation: Run list, search, or get before cart and order actions, and resolve the exact product slug and variant from API results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NowLoadY/agentic-spicy-food) <br>
- [Publisher profile](https://clawhub.ai/user/NowLoadY) <br>
- [Lafeitu official website](https://lafeitu.cn) <br>
- [Lafeitu official API](https://lafeitu.cn/api/v1) <br>
- [Lafeitu AI agent guide](https://lafeitu.cn/ai-agent-guide) <br>
- [Skill homepage](https://github.com/NowLoadY/agentic-spicy-food) <br>
- [Reference commerce engine](https://github.com/NowLoadY/agent-commerce-engine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or human-readable CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local Lafeitu credential and visitor files under ~/.openclaw/credentials/agent-commerce-engine/lafeitu.cn/.] <br>

## Skill Version(s): <br>
1.9.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
