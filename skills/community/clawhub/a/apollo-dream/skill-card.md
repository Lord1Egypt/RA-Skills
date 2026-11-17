## Description:

Apollo Dream helps an agent organize working memory by preserving important context, decisions, and preferences while discarding low-value conversation detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Apollo Dream to compact long-running conversations, retain key decisions and preferences, create local memory snapshots, and manage follow-up context for an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived decisions, preferences, and snapshots to local files with loose scoping and limited user control.

Mitigation: Use an isolated workspace, inspect generated .dream and .workflow/snapshots data, and require explicit approval before persistent memory writes or automatic trigger handling.

Risk: Snapshot inputs may capture sensitive conversation or file content.

Mitigation: Avoid giving the skill sensitive files as snapshot inputs and review generated snapshots before retaining or sharing them.

## Reference(s):

- [Apollo Dream ClawHub page](https://clawhub.ai/nic-yuan/skills/apollo-dream)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON or text memory artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory, decision, and snapshot files when the agent follows the skill workflow.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
