## Description:

Manage a shared Windows application registry and control which agents may run registered apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregtysick](https://clawhub.ai/user/gregtysick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a shared Windows application registry, update app launch policy, validate registry entries, and launch or stop registered applications through an agent-controlled workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared app launch policies can be mutated by the skill workflow.

Mitigation: Install only where registry writers are trusted, require explicit confirmation for registry changes, and add an administrator policy for registry mutations.

Risk: Registered launch paths can start local Windows applications.

Mitigation: Review and validate launch paths before use, prefer stronger path validation, and avoid ambiguous shell launch forms where possible.

Risk: The skill can stop running applications when process metadata is stored.

Mitigation: Use explicit stop confirmation and store precise process metadata to reduce accidental termination.

## Reference(s):

- [Application Manager ClawHub Page](https://clawhub.ai/gregtysick/skills/application-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with JSON registry examples and Windows shell command shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a human-readable JSON registry at ~/.openclaw/registries/application_registry.json and may propose Windows launch or stop commands for registered applications.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
