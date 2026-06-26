## Description: <br>
Conducts industry, keyword, search-intent, audience-question, content-gap, competitor-keyword, and SERP research using Ahrefs, Firecrawl, and Exa to produce a comprehensive intelligence brief. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, content, and campaign teams use this skill to understand search demand, map keyword intent, collect audience questions and pain points, identify content gaps, and summarize competitor positioning before campaign planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client details, proprietary strategy, or campaign inputs may be sent to external research services. <br>
Mitigation: Use only information approved for third-party research tools, and avoid confidential or sensitive client material unless that sharing is acceptable. <br>
Risk: The skill saves a local research brief under .agents, which may retain client or campaign context. <br>
Mitigation: Review the generated brief before sharing or committing it, and remove sensitive details that should not persist in local artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/abm-industry-research) <br>
- [Ahrefs API v3](https://api.ahrefs.com/v3) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research brief with tables and concise synthesized findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local .agents/industry-research-{client}.md brief and records per-section research dates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
