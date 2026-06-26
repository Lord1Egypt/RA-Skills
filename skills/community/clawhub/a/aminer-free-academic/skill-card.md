## Description: <br>
Free-tier AMiner academic search for lightweight paper triage, scholar identification, institution and venue normalization, patent trend scanning, and basic metadata enrichment using seven AMiner APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canxiangcc](https://clawhub.ai/user/canxiangcc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for lightweight AMiner academic discovery when they need free-tier paper, scholar, institution, venue, or patent lookups before deciding whether deeper paid APIs are warranted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AMiner API tokens or confidential research queries could be exposed if pasted into chat or sent without review. <br>
Mitigation: Keep AMINER_API_KEY in an environment variable, avoid printing tokens, and avoid submitting confidential topics or private names unless external AMiner lookup is acceptable. <br>
Risk: The routing language is broad and could steer academic questions to this free-tier skill even when the requested task needs deeper paid APIs. <br>
Mitigation: State free-tier limits in the answer and route to paid AMiner APIs only when the free endpoints cannot answer the user's request. <br>


## Reference(s): <br>
- [AMiner Free Search API Catalog](references/api-catalog.md) <br>
- [AMiner Open Platform Documentation](https://open.aminer.cn/open/docs) <br>
- [AMiner Console](https://open.aminer.cn/open/board?tab=control) <br>
- [ClawHub Skill Page](https://clawhub.ai/canxiangcc/aminer-free-academic) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, API Calls] <br>
**Output Format:** [Markdown with curl command examples and concise result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMINER_API_KEY and stays within documented free-tier AMiner endpoints unless the user explicitly asks to upgrade.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
