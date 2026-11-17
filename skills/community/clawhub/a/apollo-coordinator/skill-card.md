## Description:

Coordinates complex tasks by splitting them across multiple helper agents and summarizing the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to coordinate complex work by decomposing a task into independent spoke-agent assignments and consolidating structured results, timeouts, and conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The support script reads local OpenClaw workflow and task metadata and writes coordinator state.

Mitigation: Run it only in the intended local OpenClaw workspace and review the generated coordinator state before relying on it.

Risk: Server security guidance flags under-disclosed local state handling and non-JSON-safe output generation.

Mitigation: Require publisher documentation of the script behavior and JSON-safe state output before deployment in stricter environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nic-yuan/skills/apollo-coordinator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese-language Markdown guidance with structured task and result templates; optional shell status output from the coordinator check script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The status script reads local OpenClaw workflow and task metadata and writes coordinator state JSON.]

## Skill Version(s):

2.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
