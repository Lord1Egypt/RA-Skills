## Description:

Helps agents save work checkpoints before restarts or model changes and restore them in a later session using BlueColumn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and teams use this skill to save completed work, pending tasks, decisions, blockers, and next steps before a restart or model change, then resume from that checkpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved checkpoints may disclose sensitive work details to BlueColumn.

Mitigation: Only store approved summaries; redact secrets, credentials, customer data, private URLs, security details, and internal ticket information unless your organization approves their storage.

## Reference(s):

- [ClawHub agent-resume release](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/agent-resume)
- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown text with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checkpoints summarize completed work, unfinished tasks, decisions, blockers, and next steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
