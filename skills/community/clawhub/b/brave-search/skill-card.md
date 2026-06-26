## Description: <br>
Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to run headless web searches, retrieve search snippets, and extract readable webpage content as Markdown without interactive browsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Brave and requested page URLs are sent to target websites. <br>
Mitigation: Avoid searching for secrets, proprietary internal terms, or other sensitive data. <br>
Risk: Extracted webpage content may be inaccurate, hostile, or otherwise untrusted. <br>
Mitigation: Treat extracted content as reference material and verify it before using it for decisions or commands. <br>
Risk: The documentation asks for a Brave API key, but the implementation does not use that key in this version. <br>
Mitigation: Do not provide a Brave API key unless the implementation is corrected to use it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/brave-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Plain text search results with titles, links, snippets, and optional extracted page content in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search extraction can include fetched webpage content truncated to 5,000 characters per result.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
