## Description: <br>
Performs web searches using DuckDuckGo to retrieve real-time information for current events, documentation, tutorials, and other information that requires web search capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[10e9928a](https://clawhub.ai/user/10e9928a) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and agent users use this skill to search the web through DuckDuckGo for current information, documentation, tutorials, news, images, videos, maps, suggestions, and instant answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent through a network-backed search package and may include sensitive user-provided text. <br>
Mitigation: Avoid entering secrets, confidential business information, or sensitive personal data into search queries. <br>
Risk: The skill may install and run the duckduckgo-search Python package. <br>
Mitigation: Install only in environments where running that package is acceptable and review package installation behavior before deployment. <br>
Risk: The optional save-results example can leave query text and search results on disk. <br>
Mitigation: Store result files only in approved locations and delete them when they are no longer needed. <br>
Risk: Batch searches or large result counts can trigger rate limits or unreliable results. <br>
Mitigation: Use modest result counts, add delays between repeated searches, and handle search exceptions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/10e9928a/duckduckgo-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; executed searches can return text summaries, links, and optional JSON result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses network-backed DuckDuckGo searches through the duckduckgo-search Python package and can optionally write search result files to disk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
