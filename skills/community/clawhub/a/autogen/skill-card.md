## Description:

Autogen helps developers work with AutoGen multi-agent conversation orchestration, code execution, and group chat patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangifonly](https://clawhub.ai/user/zhangifonly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design AutoGen-based multi-agent workflows, configure assistant and user-proxy agents, set up group chat managers, register tools, and reason about code execution options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's examples may lead users to run agent-generated code directly on the host machine.

Mitigation: Prefer Docker or another sandbox, require human approval before execution, and use disposable work directories.

Risk: Runtime environments may expose credentials or other sensitive data to generated code.

Mitigation: Remove secrets from the execution environment before running agent-generated code.

Risk: Unpinned package installation commands may produce different behavior over time.

Mitigation: Pin package versions for production use.

## Reference(s):

- [ClawHub Autogen Skill Page](https://clawhub.ai/zhangifonly/skills/autogen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AutoGen installation commands, agent configuration snippets, and orchestration examples.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
