## Description:

Wrap long lines of text to a specified width for formatting text files within column limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to wrap long text lines so files fit terminal columns, documentation margins, or project formatting limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper may read file contents that are explicitly passed to it.

Mitigation: Pass only intended files and avoid using the skill on sensitive paths unless that access is expected.

Risk: The bundled helper may not fully match the documented command-line options.

Mitigation: Verify option behavior in the target environment before relying on flags such as space-only or byte-count wrapping.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/fold-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and plain text wrapping output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper wraps stdin or an explicitly supplied file to a specified line width.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
