## Description:

Detects and fixes Feishu channel configuration conflicts in OpenClaw by keeping the complete channel, merging allowlists and dmPolicy, removing duplicate channel entries, and prompting a Gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuxuebin20260309](https://clawhub.ai/user/liuxuebin20260309)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to repair Feishu bot non-response caused by duplicate feishu and openclaw-feishu channel entries, while preserving complete app credentials and merging access policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change access-control settings, merge allowlists, change dmPolicy, delete a duplicate channel, and re-enable the retained Feishu channel.

Mitigation: Review the planned OpenClaw configuration changes before running the skill, keep the generated backup, and restore the backup if access becomes too broad or the bot behaves unexpectedly.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update ~/.openclaw/openclaw.json and create ~/.openclaw/openclaw.json.bak when executed.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
