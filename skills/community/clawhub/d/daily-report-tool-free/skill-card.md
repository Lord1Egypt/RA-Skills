## Description:

根据输入生成日报 Markdown 草稿并写入 reports 目录，适合个人工作记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and lightweight teams use this skill to turn dates, highlights, and blockers into daily Markdown work-report drafts for personal records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill can guide an agent to run commands and inspect API-related environment variables.

Mitigation: Require review before shell execution, secret reads, file writes, or environment inspection.

Risk: The security evidence flags unclear network, API key, and credential-adjacent instructions for a daily-report workflow.

Mitigation: Review network and API behavior before installation and avoid sending sensitive work notes to external services unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/daily-report-tool-free)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report file with structured status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a daily report under the reports directory and may return a nextAction status.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
