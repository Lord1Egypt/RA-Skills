## Description: <br>
Fetches, ranks, and summarizes top AI news stories from trusted editorial, official, research, and community sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brunovu20](https://clawhub.ai/user/brunovu20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate concise daily or weekly briefings on current AI launches, research, industry news, and trend signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Python or Bash with outbound network access to fetch public AI news feeds and APIs. <br>
Mitigation: Install only in environments where outbound public news access is acceptable, and review network behavior before deployment. <br>
Risk: Fresh AI news may include rumors, weak sourcing, duplicated coverage, or incomplete early reporting. <br>
Mitigation: Prefer primary and reputable sources, deduplicate related stories, and label or exclude low-confidence items. <br>
Risk: News queries can reveal sensitive internal interests or priorities. <br>
Mitigation: Avoid including sensitive internal topics in queries and keep briefings limited to public information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brunovu20/ai-trending-news) <br>
- [Ranking model](references/ranking.md) <br>
- [Source tiers for AI trending news](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown numbered briefing with source links, dates, short summaries, and ranking notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exactly 10 items when at least 10 credible candidates exist; otherwise returns the highest-confidence subset and says so.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
