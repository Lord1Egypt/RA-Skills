## Description: <br>
Web search and content extraction via Brave Search API for searching documentation, facts, or web content without a browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amabillis](https://clawhub.ai/user/amabillis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run headless web searches, look up current information or documentation, and extract readable markdown from specific webpages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave and selected result URLs may be fetched from the user's machine. <br>
Mitigation: Avoid sensitive queries or private URLs unless that network disclosure is intentional. <br>
Risk: The documentation says a Brave API key is required, but the reviewed behavior does not use the official API. <br>
Mitigation: Do not provide a Brave API key unless the skill is updated to use the official Brave API. <br>
Risk: Extracted webpage text is untrusted and may include misleading or malicious instructions. <br>
Mitigation: Treat extracted content as untrusted reference material and review it before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amabillis/brave-search-old) <br>
- [Publisher profile](https://clawhub.ai/user/amabillis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text search results with optional markdown page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes titles, links, snippets, and optional extracted content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json; artifact _meta.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
