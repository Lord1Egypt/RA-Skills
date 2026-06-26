## Description: <br>
AI-optimized web search via the Tavily API that returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wetor](https://clawhub.ai/user/wetor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to search the web with Tavily, tune result count, depth, and topic, and extract clean page content from URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, and extracted page content are sent to Tavily. <br>
Mitigation: Use the skill only when a Tavily API key is intended and avoid private, confidential, or access-controlled URLs unless sharing that data with Tavily is acceptable. <br>
Risk: Returned web snippets or extracted content can be incomplete, stale, or misleading. <br>
Mitigation: Review source links and corroborate important information before relying on it. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com) <br>
- [ClawHub skill page](https://clawhub.ai/wetor/baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal output with answers, source links, snippets, extracted content, and failure notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; search results are capped between 1 and 20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
