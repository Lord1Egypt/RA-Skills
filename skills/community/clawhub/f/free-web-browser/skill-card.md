## Description: <br>
Browse web through OpenClaw web_search and web_fetch with Ollama as search provider, no external API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prantikmedhi](https://clawhub.ai/user/prantikmedhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search, fetch, verify, and summarize live web content with source links through OpenClaw's web_search and web_fetch tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched web content can be untrusted, outdated, or misleading. <br>
Mitigation: Check important claims against primary or reliable sources and include recency caveats when the answer is time-sensitive. <br>
Risk: The skill cannot browse live web content if the runtime does not expose web_search and web_fetch. <br>
Mitigation: Confirm the target agent runtime provides those tools before relying on this skill for live browsing. <br>


## Reference(s): <br>
- [Ollama Web Browser Notes](references/ollama-web-browser-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/prantikmedhi/free-web-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with source links and caveats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise evidence bullets and uncertainty notes for time-sensitive web results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
