## Description: <br>
Provides free web search using Bing results with Jina.ai content extraction, without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azzazhang](https://clawhub.ai/user/azzazhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run lightweight web searches and retrieve summarized search-result links from Bing through Jina.ai. It is suited for quick lookup tasks where no search API key is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and fetched pages are sent to third-party web services. <br>
Mitigation: Use only for non-sensitive searches, and do not submit secrets, private URLs, or internal hostnames. <br>
Risk: The security review reports that outside web content is handled in a way that could run code locally. <br>
Mitigation: Review before installing, pin a fixed version, and replace parsing that embeds web responses in executable code with safer data parsing. <br>
Risk: The release does not clearly declare network and tool requirements. <br>
Mitigation: Confirm outbound access to Bing and Jina.ai, plus local jq, curl, bc, and Python availability, before enabling the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/azzazhang/bing-search-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [JSON search results with query, result entries, and response time; documentation includes Markdown and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search input accepts a required query string and optional max_results value from 1 to 10.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
