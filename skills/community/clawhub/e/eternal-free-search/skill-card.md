## Description: <br>
Free web search using DuckDuckGo with web, news, image, instant-answer, and suggestion modes, without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eternal0404](https://clawhub.ai/user/eternal0404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run DuckDuckGo searches for public web information, recent news, images, instant answers, and search suggestions from a command-line helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to an external web service. <br>
Mitigation: Avoid submitting secrets, private company data, personal identifiers, or sensitive conversation context in search queries. <br>
Risk: The skill imports the third-party ddgs package at runtime. <br>
Mitigation: Verify the ddgs package source and pinned version before use in managed or sensitive environments. <br>
Risk: Search results, news, images, and instant answers may be incomplete, stale, or misleading. <br>
Mitigation: Review returned sources and verify important facts before using results in decisions or generated work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eternal0404/eternal-free-search) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/eternal0404) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text search results or JSON arrays from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports web, news, Q&A, image, and suggestion modes with optional max result count, region, time filter, and JSON output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
