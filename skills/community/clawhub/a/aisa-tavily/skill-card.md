## Description: <br>
Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to run AIsa-backed web search and extraction, summarize recent evidence, compare tools or companies, and assemble research briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, extracted content requests, and the AIsa API key are sent to AIsa's hosted API. <br>
Mitigation: Install only if the user trusts AIsa/api.aisa.one, use a scoped or rotatable AISA_API_KEY where possible, and avoid submitting secrets, private URLs, regulated data, or internal-only research topics without organizational approval. <br>
Risk: Search or extraction providers may time out or return incomplete evidence. <br>
Mitigation: Report failed providers or missing sources honestly and avoid claiming that unqueried sources were reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-tavily) <br>
- [AIsa Tavily search API endpoint](https://api.aisa.one/apis/v1/tavily/search) <br>
- [AIsa Tavily extract API endpoint](https://api.aisa.one/apis/v1/tavily/extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown research summaries, source lists, and extracted page content from CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends submitted queries or URLs to AIsa's hosted API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
