## Description: <br>
使用必应中文搜索引擎进行网络搜索和网页抓取。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dej4vu](https://clawhub.ai/user/dej4vu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Bing China and fetch public webpage content for research, retrieval, and source-gathering workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching private, internal, localhost, or account-specific URLs can expose returned content to the agent context and sends network requests from the user's environment. <br>
Mitigation: Use the skill only for public web searches and public webpage extraction, and avoid private, internal, localhost, or authenticated URLs. <br>
Risk: Fetched web pages may contain untrusted or misleading content. <br>
Mitigation: Review extracted content before relying on it, especially when it is used for decisions, citations, or downstream automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dej4vu/bing-search-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON returned by a Node.js command-line tool, with guidance in Markdown skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search returns result counts plus titles, URLs, snippets, and site names; fetch returns a page title and cleaned text content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
