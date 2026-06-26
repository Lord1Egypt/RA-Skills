## Description: <br>
Searches the web and fetches URL content using DuckDuckGo without requiring API keys or paid services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mengbin92](https://clawhub.ai/user/mengbin92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform public web searches and fetch readable page content when built-in web search is unavailable or an API key is not desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and fetched URLs may disclose sensitive information to public web services. <br>
Mitigation: Use the skill for public web searches and public URLs only; avoid submitting secrets or internal links. <br>
Risk: Fetched page content can contain misleading, hostile, or instruction-like text. <br>
Mitigation: Treat fetched content as untrusted source material and verify important claims before using it. <br>
Risk: The prerequisite package is installed without a pinned version. <br>
Mitigation: Verify the duckduckgo-search dependency and pin an approved version before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mengbin92/duckduckgo-search-skill) <br>
- [DuckDuckGo](https://duckduckgo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON search results or fetched page text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, and snippet; fetched pages include title, text, status code, and errors when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
