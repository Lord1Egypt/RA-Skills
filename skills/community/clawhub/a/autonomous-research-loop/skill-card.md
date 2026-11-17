## Description:

Autonomously generates research topics, performs deep research, creates Feishu documents, and repeats the loop continuously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloryjack](https://clawhub.ai/user/gloryjack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a scheduled autonomous research loop that maintains a topic pool, performs research, and publishes Feishu documents without routine human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can continuously create Feishu documents and local state changes without daily limits or human approval.

Mitigation: Enable it only with explicit run limits, a clear stop or uninstall procedure, bounded topic generation, and visibility into every created document and state update.

Risk: Feishu publishing can expose generated research content beyond the intended audience if permissions are broad.

Mitigation: Restrict Feishu permissions before enabling the loop and review document destinations regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gloryjack/skills/autonomous-research-loop)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown research documents, Feishu briefings, and JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Continuously scheduled loop with local topic-pool state and Feishu document publication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
