## Description:

Cron Task helps agents convert a nearly finished recurring workflow into a scheduled daily automation by running readiness checks, generating an executor script, writing the Schedule prompt, configuring Feishu notification, and archiving outputs to Feishu Drive, Obsidian, and IMA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill after debugging a data pipeline, skill workflow, or repeated task to package it as a recurring Schedule job with readiness validation, fallback instructions, notification, and archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create recurring jobs that run local Python commands.

Mitigation: Review the generated command, fallback commands, local paths, and cron schedule before enabling the task, and periodically audit or remove created Schedule entries.

Risk: Generated workflows may archive reports to Feishu Drive, Obsidian, and IMA.

Mitigation: Confirm cloud folders, local inbox paths, knowledge-base IDs, and sensitive-data scope before use; use dedicated least-privilege Feishu and IMA credentials.

## Reference(s):

- [Cron Task ClawHub Page](https://clawhub.ai/edwardwason/skills/cron-task)
- [9-Point Readiness Checklist](references/readiness-checklist.md)
- [Schedule Prompt Template](references/schedule-prompt-template.md)
- [Three-Destination Archiving Guide](references/archiving-guide.md)
- [Executor Script Template](assets/executor_template.py)
- [Archive Metadata Header Template](assets/metadata_header.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables and inline shell commands, plus generated Python executor scripts and Schedule prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files, Schedule task definitions, Feishu card notification instructions, and archive configuration for Feishu Drive, Obsidian, and IMA.]

## Skill Version(s):

1.0.1 (source: server release, SKILL.md frontmatter, CHANGELOG; released 2026-07-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
