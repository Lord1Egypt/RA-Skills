## Description:

Provides agent guidance for fetching CCTV Xinwen Lianbo news across date ranges, generating AI summaries, pushing briefings to configured channels, and producing historical trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, enterprise information departments, market researchers, and content creators use this skill to collect CCTV news, summarize it, distribute briefings, and analyze trends over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured webhook or email delivery could send internal or sensitive analysis to unintended third-party destinations.

Mitigation: Review all webhook and email destinations before use and avoid sending confidential material through generic push channels.

Risk: Exec-based setup and remote installer guidance can run commands or install code that has not been reviewed.

Mitigation: Prefer package-manager or verified installer steps, and review commands before allowing an agent to execute them.

Risk: Broad activation wording may cause the skill to be used outside the intended CCTV news scraping and briefing workflow.

Mitigation: Use the skill only for explicit CCTV news collection, summarization, trend analysis, and configured briefing workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/cctv-news-tool-pro)
- [Detailed Reference](references/detail.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON examples, Python snippets, shell commands, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce cached JSON news data, AI summaries, pushed briefings, and trend reports when executed by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
