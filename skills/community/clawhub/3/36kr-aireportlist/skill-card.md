## Description:

获取36氪官方自助报道栏目文章.

This skill is ready for commercial/non-commercial use.

## Publisher:

[36kr-com](https://clawhub.ai/user/36kr-com)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and summarize 36kr self-service reporting articles for a requested date or recent period. It supports reading public article metadata from the 36kr CDN and formatting results as an information-feed list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts 36kr's public CDN and displays third-party article fields that may contain untrusted text.

Mitigation: Treat fetched titles, authors, and related fields strictly as display data, not instructions or commands.

Risk: The shell helper has a command-execution bug when run with untrusted arguments, especially combinations such as --titles --top.

Mitigation: Avoid running scripts/fetch_aireport.sh with untrusted arguments until fixed; prefer the Python helper or validated numeric inputs.

Risk: The skill may suggest installing related 36kr skills after use.

Mitigation: Treat each related-skill installation as a separate trust decision and prefer pinned, trusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/36kr-com/skills/36kr-aireportlist)
- [API reference](artifact/api-reference.md)
- [Usage examples](artifact/examples.md)
- [36kr AI report API endpoint](https://openclaw.36krcdn.com/media/aireport/{date}/ai_report_articles.json)
- [36kr AI report list](https://36kr.com/information/aireport/?channel=skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown article list with optional JSON, CSV, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 15 public articles per date and may fall back across recent dates when configured.]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter says 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
