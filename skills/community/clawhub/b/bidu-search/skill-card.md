## Description:

Perform web searches using the Baidu API with a focus on Chinese content, customizable result counts, and OpenClaw integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Baidu web searches, especially for Chinese-language queries, from Python or CLI workflows and return formatted search results.

### Deployment Geography for Use:

Global, subject to Baidu API availability and regional restrictions.

## Known Risks and Mitigations:

Risk: Baidu API key material may be exposed in returned error text when HTTP exception strings include request details.

Mitigation: Review before installing when the API key has billing, quota, or account privileges; redact the ak parameter from errors or use safer provider-supported authentication.

Risk: Runtime behavior depends on external Baidu API access, credentials, quota, and regional availability.

Mitigation: Install in an isolated environment, pin dependencies, and verify API account permissions, quotas, and regional terms before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leohuang8688/skills/bidu-search)
- [Baidu AI Open Platform](https://ai.baidu.com/)
- [Baidu Search API Reference](https://ai.baidu.com/ai-doc/SEARCH)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown-formatted text with result titles, URLs, and snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; result count is caller-configurable.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
