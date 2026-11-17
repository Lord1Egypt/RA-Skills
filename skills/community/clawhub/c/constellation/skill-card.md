## Description:

一个功能完整的星座 MCP (Model Context Protocol) 服务，提供星座信息查询、运势分析、配对测试等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query constellation information, daily horoscope data, zodiac compatibility, zodiac lookup by date, and rising-sign information through the XiaoBenYang service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use it only where plaintext local credential storage is acceptable, limit the key's scope where possible, and replace plaintext storage with a secure credential store before routine use.

Risk: Birth time and precise location used for rising-sign calculations are sent to an external service.

Mitigation: Share only data the user is comfortable sending externally and document this data flow before deploying the skill for regular users.

Risk: Inconsistent gaokao or school-search leftovers may confuse review and operation.

Mitigation: Remove stale gaokao references and verify the documented constellation behavior matches the shipped artifact before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/constellation)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, configuration, guidance]

**Output Format:** [Markdown text summarizing JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and sends requested constellation parameters to an external service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
