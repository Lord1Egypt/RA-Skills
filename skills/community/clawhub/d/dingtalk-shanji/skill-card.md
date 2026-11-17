## Description:

Extracts DingTalk Shanji meeting records, transcripts, AI summaries, todos, and keywords using the dws CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and DingTalk users use this skill to find and extract authorized DingTalk Shanji meeting data for review, export, and follow-up workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs installation of external CLI software, including pipe-to-shell or Invoke-Expression installer paths.

Mitigation: Install a pinned and verified dingtalk-workspace-cli version outside the skill workflow, and avoid pipe-to-shell or Invoke-Expression installers.

Risk: Documented dws commands can update meeting titles, summaries, transcript text, mind maps, or upload recordings.

Mitigation: Require explicit user confirmation before running any update, replace-text, mind-graph, or upload command.

Risk: Retrieved meeting transcripts, summaries, todos, and participant metadata may contain confidential business or personal information.

Mitigation: Limit access to authorized DingTalk records and handle extracted content according to confidentiality and data retention requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/156554395/skills/dingtalk-shanji)
- [DingTalk Workspace CLI GitHub repository](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli)
- [DingTalk Workspace CLI command documentation](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/docs/command-index.md)
- [DingTalk Workspace CLI Chinese documentation](https://github.com/DingTalk-Real-AI/dingtalk-workspace-cli/blob/main/README_zh.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that retrieve confidential meeting transcripts, summaries, todos, and metadata from DingTalk.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
