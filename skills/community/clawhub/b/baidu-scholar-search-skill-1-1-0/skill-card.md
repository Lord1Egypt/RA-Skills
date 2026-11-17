## Description:

Baidu Scholar Search - Search Chinese and English academic literature (journals, conferences, papers, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research teams use this skill to search Baidu Scholar for Chinese and English academic literature by keyword, paginate results, and request abstracts when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and authenticated requests are sent to Baidu Scholar/Qianfan using BAIDU_API_KEY.

Mitigation: Confirm the deployment is comfortable sharing those queries with Baidu Scholar/Qianfan and manage BAIDU_API_KEY as a secret.

Risk: The shell wrapper passes query parameters directly, so unencoded keywords or unexpected page_number and include_abstract values can create malformed or unintended authenticated requests.

Mitigation: Prefer a hardened wrapper that URL-encodes keyword values and validates page_number and include_abstract before issuing requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/skills/baidu-scholar-search-skill-1-1-0)
- [Baidu Scholar](https://xueshu.baidu.com/)
- [Baidu Scholar Search API Endpoint](https://qianfan.baidubce.com/v2/tools/baidu_scholar/search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown usage guidance and JSON search responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and BAIDU_API_KEY; abstracts are omitted unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/_meta.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
