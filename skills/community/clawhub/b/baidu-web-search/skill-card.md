## Description:

Use Baidu Qianfan web search API for real-time web retrieval when the user needs current information, latest news, fact verification, or source-backed answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhean2021](https://clawhub.ai/user/liuhean2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to run Baidu web searches for current events, factual verification, technical references, products, people, and places. The skill returns structured search results that an agent can synthesize into a concise, source-aware answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Baidu API key and can also use a local config.json file.

Mitigation: Prefer platform-injected BAIDU_API_KEY, avoid exposing credential values in logs or messages, and verify local credential files are not shared or committed.

Risk: Search queries are sent to Baidu and may include sensitive user-provided information.

Mitigation: Do not submit private, regulated, or confidential information as search queries unless the deployment has approved that data flow.

Risk: The release depends on a Node.js package and security evidence recommends review before installation.

Mitigation: Review dependency lock or pinning practices and scan the installed package before deploying the skill.

## Reference(s):

- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5)
- [ClawHub skill page](https://clawhub.ai/liuhean2021/skills/baidu-web-search)
- [ClawHub publisher profile](https://clawhub.ai/user/liuhean2021)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON search results from the script, typically synthesized by the agent into Markdown or plain-text answers with source references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a search query and optionally accepts a result count from 1 to 50; uses BAIDU_API_KEY when configured.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
