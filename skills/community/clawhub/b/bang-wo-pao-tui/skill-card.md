## Description: <br>
UU跑腿同城配送服务，用于订单询价、发单下单、订单查询、订单取消和骑手实时追踪。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uupt-mcp](https://clawhub.ai/user/uupt-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to estimate prices, create and manage UU跑腿 same-city delivery or on-site help orders, and track couriers after registration and configuration. <br>

### Deployment Geography for Use: <br>
China; service availability follows UU跑腿 platform coverage. <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill can create real-world paid orders without final confirmation. <br>
Mitigation: Require explicit final user confirmation before creating or cancelling any order, including price, addresses, phone number, help note, payment method, and order code. <br>
Risk: The security guidance notes sensitive phone number, address, order, payment-link, and credential handling. <br>
Mitigation: Use environment or platform-managed secrets, minimize persisted local configuration, and avoid sharing logs or outputs that contain sensitive user or order data. <br>
Risk: The security guidance flags optional WeChat QR-code handling through a third-party QR service. <br>
Mitigation: Avoid the WeChat QR path unless third-party QR exposure is acceptable; otherwise provide the original payment link through an approved channel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uupt-mcp/skills/bang-wo-pao-tui) <br>
- [UU跑腿开放平台](https://open.uupt.com) <br>
- [UU跑腿 API 文档](https://open.uupt.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order identifiers, payment links, QR-code file paths, registration prompts, and courier-tracking details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter/package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
