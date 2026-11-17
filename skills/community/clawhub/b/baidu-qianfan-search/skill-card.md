## Description:

Baidu Search helps agents run Baidu Qianfan Web Search queries through a Node.js CLI using a user-supplied Baidu Qianfan API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsall357357](https://clawhub.ai/user/lsall357357)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to perform Baidu Qianfan enterprise web, image, and video searches with filters for recency, sites, blocked sites, safe search, and resource types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Baidu Qianfan's external search service.

Mitigation: Avoid submitting secrets, regulated personal data, or other sensitive information in search queries.

Risk: The skill requires a Baidu Qianfan API key and supports loading credentials from a local .env file.

Mitigation: Prefer the BAIDU_QIANFAN_API_KEY environment variable over persistent local files and keep credentials out of shared artifacts.

Risk: The release does not include a dependency lockfile.

Mitigation: Pin dependencies with a lockfile before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lsall357357/skills/baidu-qianfan-search)
- [Baidu Cloud](https://cloud.baidu.com/)
- [Baidu Qianfan API Reference](references/api-reference.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and text or JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-supplied BAIDU_QIANFAN_API_KEY and sends search queries to Baidu Qianfan.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
