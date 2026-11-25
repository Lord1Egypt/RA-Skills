## Description:

Creates and proves a project-local e2e verification skill and feature map for an application's user-facing behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e](https://clawhub.ai/user/e2e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create a project-specific verification recipe for an app, map its user-facing features, and prove one workflow with e2e.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill refers to unpinned npx installers, which may fetch changing packages; ClawScan reports a partial scan because some referenced paths were unresolved, so the scan does not establish safety.

Mitigation: Review setup commands, use audited exact package versions, and inspect unresolved referenced paths before installing.

## Reference(s):

- [e2e project homepage](https://e2e.com)
- [create-verification-skill on ClawHub](https://clawhub.ai/e2e/skills/create-verification-skill)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Project-local Markdown skill and feature files, with test and configuration code plus runnable shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Files and instructions are tailored to the target project's observed app surface and verification setup.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
