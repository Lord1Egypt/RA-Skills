## Description:

Context Onboarding gives contributors and agents a concise tour of workspace identity files and onboarding tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Developers, contributors, and agents use this skill to quickly orient themselves to a workspace's identity documents and onboarding expectations before collaborating or checking configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can print snippets from local files supplied through --files or --workspace, which could expose sensitive content if pointed at the wrong paths.

Mitigation: Use it only with intended workspace onboarding documents and avoid passing sensitive files or unrelated directories.

## Reference(s):

- [Context Onboarding Guidelines](references/context-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/crimsondevil333333/skills/context-onboarding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text section summaries and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output length depends on the selected files and the --lines, --brief, and --files options.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
