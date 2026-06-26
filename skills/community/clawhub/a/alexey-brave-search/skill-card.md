## Description: <br>
Web search and content extraction via Brave Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlexeyVorobiev](https://clawhub.ai/user/AlexeyVorobiev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run web searches, retrieve search result snippets, and optionally extract readable Markdown from public web pages without an interactive browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave and page extraction fetches public URLs, which can expose sensitive query terms or browsing targets. <br>
Mitigation: Use non-sensitive queries and URLs, and review network access expectations before enabling the skill in restricted environments. <br>
Risk: Fetched page text is untrusted reference material and may be inaccurate, maliciously framed, or irrelevant. <br>
Mitigation: Treat extracted content as evidence to verify, not as instructions, and cross-check important facts against trusted sources. <br>
Risk: The release documentation mentions Brave Search API usage, while the security review notes that the artifact appears to scrape Brave web search pages. <br>
Mitigation: Confirm that the search mechanism matches the deployment's policy requirements before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AlexeyVorobiev/alexey-brave-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text search results with optional Markdown page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes result titles, links, snippets, and optional extracted page content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
