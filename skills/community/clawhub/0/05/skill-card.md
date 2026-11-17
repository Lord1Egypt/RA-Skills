## Description:

智能内容总结和项目复盘工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, teams, and external users can use this skill to summarize daily reports, meetings, projects, articles, and general text, then identify key points, completion status, issues, lessons learned, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted summaries and original content may be stored persistently in a local searchable database.

Mitigation: Avoid submitting confidential notes or sensitive project data unless the local database is protected, reviewed, and cleaned up by the user.

Risk: Markdown exports are written as plaintext files.

Mitigation: Choose export locations carefully and apply normal file access controls before sharing or retaining exported summaries.

Risk: Rule-based summaries and project review recommendations may omit context or produce generic conclusions.

Mitigation: Review generated summaries, recommendations, and action items before using them for decisions or reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/05)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured text, JSON-like summary objects, and Markdown export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores submitted content locally in ~/.ai_summary.db when a titled summary is saved; Markdown exports are plaintext files.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
