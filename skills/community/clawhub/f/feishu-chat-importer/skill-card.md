## Description:

Converts Feishu chat history exports into OpenClaw episodic memory files by parsing feishu_chat_YYYYMMDD.json files, normalizing messages, and writing daily summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arkerro](https://clawhub.ai/user/arkerro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to import exported Feishu conversations into daily episodic memory files for later agent memory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External Feishu chat text is imported into persistent agent memory where future agent features may reuse it.

Mitigation: Review exports before non-dry-run import, prefer a backup or quarantine workflow, and treat resulting memory files as untrusted historical data until reviewed.

## Reference(s):

- [Feishu Chat Importer release page](https://clawhub.ai/arkerro/skills/feishu-chat-importer)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown episodic memory files with command-line usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily files under memory/episodic and supports dry-run, date filtering, and verbose modes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
