## Description:

Create a thread-based recovery summary when an agent loses the thread by reading the relevant conversation and canonical files, summarizing what was done, where it is documented, and what the real next step is, then writing a compressed reorientation snapshot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wroadd](https://clawhub.ai/user/wroadd)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to recover orientation during long, fragmented, or resumed tasks by summarizing completed work, source-of-truth documentation, and the actual next step before further action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read prior conversation context or state files that contain sensitive information.

Mitigation: Avoid invoking it on threads or files containing secrets unless the agent is instructed to redact sensitive content.

Risk: The skill writes a reorientation snapshot to state/ORIENT.md.

Mitigation: Review the generated snapshot before sharing or committing it, especially when task history includes private details.

## Reference(s):

- [Context Rescue on ClawHub](https://clawhub.ai/wroadd/skills/context-rescue)
- [Publisher profile](https://clawhub.ai/user/wroadd)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reorientation summary and snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a compressed reorientation snapshot to state/ORIENT.md when used as directed.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
