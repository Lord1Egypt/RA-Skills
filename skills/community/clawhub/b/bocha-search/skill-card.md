## Description: <br>
博查搜索 API 插件，从全网搜索网页信息，结果准确、摘要完整，适合 AI 使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunjingji](https://clawhub.ai/user/sunjingji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run Bocha web searches from an agent workflow, with optional result summaries and time-range filters. It is suited for gathering structured web-search results that an AI agent can consume directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Bocha's API and may reveal sensitive user intent, private identifiers, secrets, regulated data, or personal information. <br>
Mitigation: Use the skill only for search terms that are acceptable under Bocha's data handling terms, and avoid submitting secrets, private internal identifiers, regulated data, or sensitive personal information. <br>
Risk: The skill requires a Bocha API key or account quota, so misuse can expose credentials or consume paid service capacity. <br>
Mitigation: Provide the API key through a controlled environment variable or local configuration, restrict access to that secret, and monitor account quota or rate-limit errors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunjingji/bocha-search) <br>
- [Publisher Profile](https://clawhub.ai/user/sunjingji) <br>
- [博查开放平台](https://open.bochaai.com) <br>
- [博查 API 文档](https://bocha-ai.feishu.cn/wiki/RXEOw02rFiwzGSkd9mUcqoeAnNK) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured JSON search results or structured JSON error responses from a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include query text, total and returned result counts, titles, URLs, descriptions, optional summaries, site names, and publication or crawl dates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
