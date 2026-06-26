## Description: <br>
Use this skill when the user asks to search the web, look up recent information, check current events, gather online sources, or research a topic using Tavily search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuxindavid](https://clawhub.ai/user/liuxindavid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run lightweight Tavily web searches for current information, news, source gathering, and research without installing Python packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and API credentials are sent to Tavily as part of normal operation. <br>
Mitigation: Use a dedicated Tavily API key, keep the .secrets key file private, and avoid submitting secrets, confidential business data, or sensitive personal information in queries. <br>


## Reference(s): <br>
- [Cliby Tavily Search on ClawHub](https://clawhub.ai/liuxindavid/cliby-tavily-search) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include answer summaries, ranked result snippets, URLs, scores, images, and raw JSON when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
