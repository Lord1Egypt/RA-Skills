## Description:

Coordinate multiple agents with minimal token waste by using direct agent-to-agent spawning and file-based handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wewehg](https://clawhub.ai/user/wewehg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate work across specific agents while preserving detailed handoff state in local markdown files. It is suited for multi-agent tasks where concise chat coordination and durable takeover notes reduce repeated context transfer and omission risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local handoff files can retain sensitive or unnecessary private context.

Mitigation: Store only the context needed for takeover, avoid secrets, and periodically clean up ~/.openclaw/shared-handoffs/ when retained notes are no longer needed.

Risk: A stale or ambiguous handoff can cause the next agent to misunderstand scope or redo completed work.

Mitigation: Use explicit sections for completed work, remaining tasks, risks, next owner, and files to inspect before transfer.

## Reference(s):

- [Handoff Template](references/handoff-template.md)
- [ClawHub Skill Page](https://clawhub.ai/wewehg/skills/agents-efficient-workflow)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance and handoff templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to create or update local markdown handoff files.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
