## Description:

Guides OpenClaw agents through a knowledge crystallization loop for learning, verification, skill extraction, memory maintenance, and growth planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help OpenClaw agents structure learning, turn repeated experience into reusable skills, maintain durable memory, and plan capability growth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to preserve durable memories or propose future skill changes without a consistently mandatory review step.

Mitigation: Require explicit human approval for every memory write, MEMORY.md change, skill creation, skill update, archive action, or deletion action.

Risk: Persistent learning records may accidentally contain secrets or sensitive session details.

Mitigation: Review memory content before persistence and avoid storing secrets, credentials, personal data, or sensitive session details in durable memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/agent-nurture)
- [ClawHub publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance, checklists, templates, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent memory records, skill updates, archival actions, or deletion actions that require human review.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
