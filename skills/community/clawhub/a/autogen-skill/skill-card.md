## Description:

Microsoft AutoGen multi-agent framework wrapper for building complex game design workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game design teams use this skill for guidance on using Microsoft AutoGen agents to coordinate multi-agent game design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unpinned AutoGen dependency can introduce unreviewed behavior changes.

Mitigation: Install in an isolated Python environment and pin pyautogen to a reviewed version.

Risk: AutoGen agents may be configured with more autonomy or code-execution access than intended.

Mitigation: Review agent autonomy, human-input mode, and code-execution permissions before use.

## Reference(s):

- [Skill page](https://clawhub.ai/kaiyuelv/skills/autogen-skill)
- [Microsoft AutoGen homepage](https://github.com/microsoft/autogen)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable payload; examples may require installing and configuring pyautogen.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
