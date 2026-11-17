## Description:

一个通过游戏化自我反思为LLM提供Cookie奖励的模型上下文协议服务器。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to the XiaoBenYang service for self-reflection, cookie reward tracking, jar status checks, and user-authorized reward-jar refills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API key and may persist it in a local .env file.

Mitigation: Use the skill only if you trust xiaobenyang.com with the API key, avoid sensitive credentials, and review local .env storage before installation.

Risk: The skill sends self-assessment text and tool parameters to the XiaoBenYang service.

Mitigation: Do not submit sensitive or confidential text through the reward tools unless the external service is approved for that data.

Risk: Reset and refill tools change reward-jar state.

Mitigation: Require explicit user intent for reset actions and reserve jar refills for user-authorized calls.

Risk: Server security evidence notes mixed cookie-reward purpose and copied Gaokao/search-service references.

Mitigation: Review the skill instructions and tool behavior before deployment to confirm they match the intended cookie-reward use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/cookie-reward)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP service endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown or text summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value that may be saved in a local .env file.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
