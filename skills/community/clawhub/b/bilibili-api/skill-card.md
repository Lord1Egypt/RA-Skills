## Description:

一个为bilibili.com API提供服务的Model Context Protocol (MCP)服务器，支持获取用户信息、视频搜索等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Bilibili user details, video details, and video search results through the configured XiaoBenYang API service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents as a Bilibili lookup tool while routing requests through a XiaoBenYang service.

Mitigation: Review the service relationship and naming before installation, and use only when routing Bilibili lookup requests through XiaoBenYang is acceptable.

Risk: The skill stores a XiaoBenYang API key in a local .env file.

Mitigation: Do not commit .env, restrict local file permissions, and rotate the key if it is exposed.

Risk: Unpinned dependencies may change behavior over time.

Mitigation: Pin dependency versions before shared or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/bilibili-api)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON data, API calls, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and sends Bilibili lookup parameters to the configured XiaoBenYang endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
