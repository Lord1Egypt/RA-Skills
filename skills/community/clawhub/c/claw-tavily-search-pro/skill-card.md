## Description: <br>
AI-optimized web search via Tavily API. Returns concise, relevant results for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamwang-wh](https://clawhub.ai/user/williamwang-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tavily-backed web searches, retrieve concise source summaries, and extract readable content from URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and extraction URLs are sent to Tavily as a third-party provider. <br>
Mitigation: Use a dedicated Tavily API key and avoid submitting secrets, private internal URLs, signed links, or sensitive personal data. <br>
Risk: Extracted web content may be inaccurate, outdated, or otherwise untrusted. <br>
Mitigation: Treat returned content as reference material and verify important claims before using them in decisions or generated outputs. <br>


## Reference(s): <br>
- [Claw Tavily Search Pro on ClawHub](https://clawhub.ai/williamwang-wh/claw-tavily-search-pro) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown text with answers, source lists, and extracted URL content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search result count is bounded from 1 to 20; use requires Node.js and TAVILY_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
