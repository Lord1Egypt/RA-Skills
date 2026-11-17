## Description:

DeepVista Vistabase: View and search implicit memory context automatically accumulated from Chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for read-only DeepVista CLI commands that show or semantically search implicit memory context accumulated from Chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface private memory context from Chat through DeepVista CLI commands.

Mitigation: Run it only in trusted environments and avoid exposing unrelated sensitive files or credentials.

Risk: The skill depends on the DeepVista CLI package and the related deepvista-shared skill.

Mitigation: Prefer a pinned, reviewed CLI release and verify the dependency chain before deployment.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-vistabase)
- [Publisher profile](https://clawhub.ai/user/jingconan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only DeepVista CLI commands for showing and searching memory context.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
