## Description: <br>
Generate a daily AI news newsletter from fresh web sources for current AI digests, roundups, curated newsletters, or daily briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI practitioners use this skill to collect fresh AI/ML news, verify candidate articles, and produce a concise daily newsletter with source links and structured article data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Brave and Firecrawl API keys, which can expose service access, quota, or cost if over-scoped. <br>
Mitigation: Use dedicated low-privilege API keys with usage limits and rotate them according to the owning organization's credential policy. <br>
Risk: Search queries, article URLs, and fetched article content are sent through the configured search and fetch services. <br>
Mitigation: Avoid using the skill for sensitive internal topics or private URLs, and review data-sharing requirements before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/ai-newsletter) <br>
- [Publisher profile](https://clawhub.ai/user/j3ffyang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON] <br>
**Output Format:** [Markdown newsletter plus JSON newsletter object and article item list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes article titles, URLs, domains, publication dates, concise summaries, relevance scores, source queries, and actionable warnings when fetches or validation checks fail.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
