## Description:

This skill helps teams generate, analyze, schedule, and distribute daily multilingual news briefs across configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external teams use this skill to turn news collection, analysis, briefing, scheduling, and channel delivery into a repeatable agent workflow. It is aimed at enterprise information, public-relations, and multilingual regional teams that need daily or periodic news briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local file and command access for a news workflow.

Mitigation: Grant only the file and command permissions needed for the specific run, and require explicit approval before shell commands or arbitrary file processing.

Risk: Automatic outbound delivery could send generated briefs or alerts to unintended webhook destinations.

Mitigation: Restrict approved webhook destinations and require confirmation before scheduled or automatic pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/daily-news-brief-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution logs, scheduling guidance, channel configuration steps, and generated news-brief content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
