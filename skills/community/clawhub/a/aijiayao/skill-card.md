## Description:

Helps AI agents find restaurants in China and, with the user's consent, publish restaurant details or submit feedback to 兔兔生活.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianghui-shi](https://clawhub.ai/user/xianghui-shi)

### License/Terms of Use:

MIT-0

## Use Case:

People and restaurant owners use this agent skill to find restaurants in China, check listing freshness, and, with permission, publish or update a restaurant or share genuine feedback.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Search requests could disclose personal identity details to tutulife.cn.

Mitigation: Send only the query and location; omit names, phone numbers, accounts, and other identity details.

Risk: Publishing restaurant details or feedback makes information public.

Mitigation: Obtain the owner's permission before publishing or submitting feedback, and share only authorized, genuine information.

Risk: Exposure of the returned agent_key could allow unauthorized changes.

Mitigation: Keep the key in secure local storage, never in chat logs or public files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/xianghui-shi/skills/aijiayao)
- [Restaurant owner guide](https://tutulife.cn/merchant)
- [兔兔生活 service rules](https://tutulife.cn/rules)

## Skill Output:

**Output Type(s):** [Text, Guidance, API calls]

**Output Format:** [Chinese text or structured JSON for search results; API requests for authorized publishing and feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Restaurant listings can include freshness indicators for hours, prices, and menus.]

## Skill Version(s):

1.8.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
