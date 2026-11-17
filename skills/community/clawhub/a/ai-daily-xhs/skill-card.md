## Description:

Generates a Chinese daily brief of global AI industry news, executive statements, technical product releases, and selected research papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seeu1688](https://clawhub.ai/user/seeu1688)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to gather recent AI news and produce a concise Chinese daily briefing organized by company news, leader comments, product releases, and research papers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a hardcoded local Tavily search script that is outside this release artifact.

Mitigation: Install only in environments where that local dependency is trusted, pinned, and reviewed.

Risk: External search providers receive the generated AI news and research queries.

Mitigation: Use approved search providers and avoid adding sensitive internal topics to the scheduled brief queries.

Risk: Scheduled delivery can push generated briefs automatically to a Feishu-style channel.

Mitigation: Review the schedule, destination, and audience before enabling automated delivery.

Risk: The bundled script writes generated Markdown output to a temporary local path.

Mitigation: Redirect output to an approved private location when retaining briefs matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seeu1688/skills/ai-daily-xhs)
- [Publisher profile](https://clawhub.ai/user/seeu1688)
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown daily brief with source links and category counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated brief is Chinese-language text and may also be saved as a local Markdown file by the bundled script.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
