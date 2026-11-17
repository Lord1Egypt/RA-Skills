## Description:

Security engineer skill for backend ACL structure, menu visibility control, and administrative access safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, repair, and review WelineFramework backend ACL definitions, menu visibility, and controller permission wiring for administrative features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect ACL or menu wiring can expose administrative features or hide required controls.

Mitigation: Review changes against menu.xml and controller permission annotations, then test allowed and denied admin roles through the real admin path.

Risk: Menu visibility can be mistaken for access control.

Mitigation: Enforce controller-level permission checks and verify denied backend paths fail safely.

Risk: The skill guides production permission changes but contains no executable validation.

Mitigation: Treat outputs as proposed changes and run project-specific admin ACL tests before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/acl)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with code or configuration snippets and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on ACL, menu, and controller permission alignment with allowed and denied admin-role validation evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
