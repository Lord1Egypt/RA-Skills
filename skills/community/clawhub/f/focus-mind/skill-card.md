## Description:

FocusMind helps agents analyze context health, extract goals, and generate concise summaries so long-running conversations stay focused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiaoni](https://clawhub.ai/user/hongjiaoni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to check whether a long conversation is becoming unfocused, summarize important context, extract active goals, and decide when cleanup is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read context from files and export reports to user-specified paths.

Mitigation: Use explicit, trusted input and output paths and review generated reports before sharing them.

Risk: HTML export is reported to have unsafe output escaping for untrusted or shared conversation content.

Mitigation: Prefer Markdown or JSON export for untrusted content until HTML escaping is fixed and reviewed.

Risk: Optional webhook and file notifications may send or store context-derived report data.

Mitigation: Keep webhook and file notifications disabled unless the destination is trusted and the data-sharing impact is acceptable.

## Reference(s):

- [FocusMind Design Patterns](references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/hongjiaoni/skills/focus-mind)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown and JSON reports, with optional exported Markdown, JSON, or HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read context from stdin or explicit input files; optional export and notification outputs should be configured deliberately.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
