## Description: <br>
Web search using Tavily's LLM-optimized API. Returns relevant results with content snippets, scores, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run Tavily web searches from an agent workflow and retrieve answer text, source links, snippets, relevance scores, and optional raw JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a live-looking Tavily API key in metadata and setup instructions. <br>
Mitigation: Use a personal Tavily API key, keep it out of committed files and screenshots, and prefer installation after the publisher replaces embedded keys with placeholders and rotates any exposed credential. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review the skill before installing and scan it again after any publisher update. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cs995279497-byte/chen-tavily-search) <br>
- [Tavily](https://tavily.com) <br>
- [Tavily Search API](https://api.tavily.com/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown search results by default, or raw JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a user-provided Tavily API key through TAVILY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
