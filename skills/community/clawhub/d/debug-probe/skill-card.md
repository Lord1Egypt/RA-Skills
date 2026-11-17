## Description:

Guides agents through hypothesis-driven runtime debugging with precise temporary instrumentation to diagnose bugs, confirm root causes, apply minimal fixes, and clean up diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zelixag](https://clawhub.ai/user/zelixag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to debug bugs, anomalies, and unexpected behavior when static code analysis is insufficient. It structures the workflow around hypotheses, targeted instrumentation, reproduction, log review, root-cause confirmation, minimal fixes, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic logging or dump endpoints could expose secrets, tokens, cookies, full payloads, or personal data.

Mitigation: Use local or non-production reproductions where possible, log only narrow key-value diagnostics, avoid sensitive values, and require strong access controls for any diagnostic export path.

Risk: Temporary instrumentation can remain in deployed code after debugging.

Mitigation: Require all temporary code to be marked for removal, search for those markers during cleanup, remove diagnostic imports and buffers, and verify the build after cleanup.

Risk: The global unpinned install command can introduce supply-chain uncertainty.

Mitigation: Prefer a reviewed local or project-level installation when evaluating or adopting the skill.

## Reference(s):

- [Debug Probe README](README.md)
- [Diagnostic Buffer Templates](TEMPLATES.md)
- [ClawHub Skill Page](https://clawhub.ai/zelixag/skills/debug-probe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with code snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary diagnostic instrumentation should be removed after debugging.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
