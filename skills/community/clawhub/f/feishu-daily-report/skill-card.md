## Description:

Generates daily and weekly Markdown work reports from structured JSON or parsed text data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Teams and individual contributors use this skill to turn completed work, in-progress tasks, plans, risks, and metrics into Chinese-oriented daily or weekly status reports. It is suited to Feishu-style reporting workflows where the final output is copied or sent as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied file paths can cause the local scripts to read input data or write generated JSON where the user points them.

Mitigation: Review command arguments before execution and use expected workspace-local paths for input and output files.

Risk: Promotional links in the skill text are informational and are not required for report generation.

Mitigation: Treat those links as optional references and verify them separately before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/feishu-daily-report)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports and JSON data produced by local Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily or weekly report type, optional target date, optional JSON data path, and output target selection.]

## Skill Version(s):

1.8.2 (source: server release metadata; artifact frontmatter says 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
