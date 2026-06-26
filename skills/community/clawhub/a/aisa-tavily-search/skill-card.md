## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research users use this skill to run AIsa-backed web searches, recent-news searches, URL extraction, competitor scans, and trend discovery, then turn retrieved results into concise research briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and submitted URLs are sent to AIsa. <br>
Mitigation: Avoid confidential or regulated data in searches and URL extraction requests unless AIsa use is approved for that data. <br>
Risk: The skill requires an AIsa API key. <br>
Mitigation: Use a dedicated, revocable API key and rotate it if exposure is suspected. <br>
Risk: Search or extraction results can be incomplete, unavailable, or provider-dependent. <br>
Mitigation: Report timeouts or missing provider results honestly and verify important findings against the returned sources. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/bibaofeng/aisa-tavily-search) <br>
- [AIsa Homepage](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown research answers, source lists, and extracted URL content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and AISA_API_KEY; search result count is capped by the bundled script.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
