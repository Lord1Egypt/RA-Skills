## Description: <br>
Performs web searches using DuckDuckGo to retrieve real-time information from the internet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macdesire](https://clawhub.ai/user/macdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web, news, image, video, instant-answer, suggestion, and map search results through DuckDuckGo-backed Python examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install and use the duckduckgo-search Python dependency. <br>
Mitigation: Review or pin the dependency before use, and install it only in environments where package-manager access is acceptable. <br>
Risk: Search queries may disclose sensitive private information to an external search service. <br>
Mitigation: Avoid putting secrets, private data, customer data, or confidential project details into search queries. <br>
Risk: Frequent or large batches of searches can trigger request limits or unreliable results. <br>
Mitigation: Limit result counts, add delays for batch searches, and handle DuckDuckGo search exceptions as shown by the artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macdesire/duckduckgo-search-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may print search result titles, links, snippets, metadata, or save JSON search results to a local file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
