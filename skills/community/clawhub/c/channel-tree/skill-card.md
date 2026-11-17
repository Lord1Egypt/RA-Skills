## Description:

Channel Tree helps an agent organize OpenClaw work into a persistent Hall, Universe, World, Forest, Tree, and Channel hierarchy with inheritance, context switching, and monitoring commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to split work into named session hierarchies, create task, QA, and branch channels, switch context, and inspect channel status. It is useful when an agent needs lightweight local organization across multiple conversations or workstreams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local state under /root/.openclaw/workspace/channel_tree.

Mitigation: Use it only in environments where that local path is acceptable, and review or back up the state file before relying on it for important work.

Risk: Some documented commands, including sessions and ->0, are not implemented in the bundled script.

Mitigation: Verify available commands against the script before building workflows around documented command names.

Risk: The command-line output is primarily Chinese-language text.

Mitigation: Use it with operators who can interpret the output or translate command results before acting on them.

## Reference(s):

- [Channel Tree on ClawHub](https://clawhub.ai/kukuxnd/skills/channel-tree)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command guidance and status text for managing a JSON-backed channel hierarchy.]

## Skill Version(s):

3.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
