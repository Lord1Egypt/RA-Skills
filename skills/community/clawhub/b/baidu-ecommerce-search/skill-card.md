## Description:

Baidu ecommerce one-stop service, including product knowledge, product comparison, brand and category knowledge, product specifications, rankings, search, order placement, and after-sales support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossallen](https://clawhub.ai/user/crossallen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research Baidu ecommerce products, compare options, inspect rankings and specifications, search purchasable items, manage addresses, place orders, and check after-sales status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create ecommerce orders and store delivery addresses.

Mitigation: Require explicit user approval before address changes or order creation, and summarize product, address, and amount before running purchase commands.

Risk: The Baidu ecommerce API token is sent in URL query strings and may appear in terminal output, shell history, or infrastructure logs.

Mitigation: Use a tightly scoped token where available, avoid sharing logs that contain command output or URLs, and rotate the token if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossallen/skills/baidu-ecommerce-search)
- [Publisher profile](https://clawhub.ai/user/crossallen)
- [Baidu Open Platform](https://openai.baidu.com)
- [Baidu Youxuan skill API endpoint](https://mcp-youxuan.baidu.com/skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_EC_SEARCH_TOKEN; order and address workflows require explicit user confirmation.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
