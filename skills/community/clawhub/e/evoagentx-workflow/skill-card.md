## Description:

EvoAgentX Workflow helps agents provide EvoAgentX setup guidance, status checks, examples, and starter workflow templates for self-evolving agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylechen26](https://clawhub.ai/user/kylechen26)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to check EvoAgentX availability, get installation guidance, view example workflow patterns, and create editable Python workflow templates for multi-agent systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate Python workflow files that may overwrite existing files in the current working directory.

Mitigation: Run it in a dedicated or disposable directory and review generated files before importing or executing them.

Risk: Workflow names and descriptions are inserted into generated Python code.

Mitigation: Avoid untrusted workflow names or descriptions and inspect generated code for syntax or injection issues before use.

Risk: The skill depends on the external EvoAgentX package.

Mitigation: Pin and verify the EvoAgentX dependency through the organization's normal dependency review process before installation.

Risk: The artifact claims broad EvoAgentX/OpenClaw integration capabilities that may exceed the provided CLI behavior.

Mitigation: Treat the skill as setup guidance and template generation unless additional reviewed integration code is supplied.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylechen26/skills/evoagentx-workflow)
- [EvoAgentX GitHub](https://github.com/EvoAgentX/EvoAgentX)
- [EvoAgentX documentation](https://evoagentx.github.io/EvoAgentX/)
- [EvoAgentX arXiv paper](https://arxiv.org/abs/2507.03616)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and generated Python code templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a Python workflow template file in the current working directory when the create-workflow command is used.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
