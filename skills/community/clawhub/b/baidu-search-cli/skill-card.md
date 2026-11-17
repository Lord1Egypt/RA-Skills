## Description:

Provides a CLI-oriented workflow for querying Baidu AI Search Engine (BDSE) with curl and a JSON request file, without requiring Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zfeng1982](https://clawhub.ai/user/zfeng1982)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Baidu AI Search web searches by editing search_request.json and issuing the documented curl request with BAIDU_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, filters, and API authorization are sent to Baidu's AI search API.

Mitigation: Use the skill only when Baidu AI Search is intended, and avoid confidential, regulated, or internal-only content in search_request.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zfeng1982/skills/baidu-search-cli)
- [Baidu AI Search API endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with a curl command and JSON request configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends the configured search request to Baidu's AI search API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
