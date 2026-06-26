## Description: <br>
Provides AI-grounded answers through Brave Search's OpenAI-compatible chat completions endpoint, with single-search and deep-research modes, streaming or blocking responses, and citation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xrichyrich](https://clawhub.ai/user/0xrichyrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to call Brave's Answers API for fast cited answers or multi-step research synthesis through an OpenAI-compatible interface. It is useful for chat integrations, cited answer generation, and web-grounded research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Questions and research-mode derived queries are sent to Brave's API using the user's Brave API key and quota. <br>
Mitigation: Use the skill only for data approved for Brave API processing, and avoid sending secrets, credentials, regulated data, or sensitive internal information unless that sharing is approved. <br>
Risk: Research mode can issue multiple queries and consume additional time, tokens, and API quota. <br>
Mitigation: Set research iteration, query, result, token, and time limits appropriate for the task, and parse usage data to monitor cost. <br>
Risk: Mode constraints can cause failed API calls when citations, research, streaming, and blocking settings are combined incorrectly. <br>
Mitigation: Use streaming for research mode and citation-enabled single-search calls, and do not enable citation tags together with research mode. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xrichyrich/answers) <br>
- [Brave Search API](https://api.search.brave.com) <br>
- [Brave Answers chat completions endpoint](https://api.search.brave.com/res/v1/chat/completions) <br>
- [Brave Search API base URL](https://api.search.brave.com/res/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with cURL, Python, HTTP, JSON, and SSE examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents single-search and research-mode API parameters, streaming tags, citations, usage reporting, and mode constraints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
