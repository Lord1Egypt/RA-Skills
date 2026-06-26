## Description: <br>
AMiner Data Search helps agents use the AMiner Open Platform to search papers, scholars, institutions, venues, patents, and citation data with cost-aware API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canxiangcc](https://clawhub.ai/user/canxiangcc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research-focused agents use this skill to retrieve and analyze academic entities through AMiner, including paper discovery, scholar profiles, institution analysis, venue monitoring, patent lookup, and citation-chain exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AMiner API key for external academic-search requests. <br>
Mitigation: Set AMINER_API_KEY in the environment, avoid pasting tokens into chat, and do not expose the key in outputs. <br>
Risk: Some AMiner workflows can incur paid API charges. <br>
Mitigation: Review the planned API calls and cost summary before approving paid or raw calls, especially high-cost workflows. <br>
Risk: Academic queries may include confidential unpublished research or private personal data. <br>
Mitigation: Avoid submitting confidential or private data to external AMiner APIs unless the user has approved that disclosure. <br>


## Reference(s): <br>
- [AMiner Open Platform API Catalog](references/api-catalog.md) <br>
- [AMiner Open Platform Documentation](https://open.aminer.cn/open/docs) <br>
- [AMiner API Console](https://open.aminer.cn/open/board?tab=control) <br>
- [ClawHub Skill Page](https://clawhub.ai/canxiangcc/aminer-open-academic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples, cost summaries, and structured academic search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMINER_API_KEY and may make paid external AMiner API calls.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
