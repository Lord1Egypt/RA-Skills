## Description: <br>
游子云旅游意外险销售平台（中国人保），适合旅行社代客出单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pythons](https://clawhub.ai/user/pythons) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travel agencies and insurance service operators use this skill to quote, purchase, manage, surrender, refund, and invoice travel accident insurance policies through the referenced API. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle bearer tokens, mobile numbers, Chinese ID numbers, policyholder details, and frequent traveler data with local persistence. <br>
Mitigation: Use it only in a dedicated workspace, restrict access to .agent-state.json, avoid committing local state, and delete retained identity or token data when no longer needed. <br>
Risk: The skill can guide purchases, cancellations, refunds, invoice creation, and red-invoice actions. <br>
Mitigation: Require explicit user confirmation before payment, surrender, refund, invoice, or red-invoice steps, and verify order and policy identifiers before each action. <br>
Risk: Privacy, retention, deletion, and data-sharing practices are not established by the provided release evidence. <br>
Mitigation: Ask the publisher for privacy, retention, deletion, and data-sharing details before using the skill with real customer information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pythons/buy-travel-accident-china) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Travel accident insurance API base URL](https://prod.uzyun.cn/api/agent/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API request guidance, JSON examples, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to persist account tokens and traveler details in .agent-state.json during use.] <br>

## Skill Version(s): <br>
2.0.4 (source: frontmatter, ClawHub release metadata, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
