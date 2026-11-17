## Description:

Review and optimize Dockerfiles to reduce layer count, minimize image size, and improve build times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to review Dockerfiles, receive an optimized Dockerfile, and understand changes that reduce image size, improve build caching, and strengthen container best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dockerfile recommendations may not match the application's base-image, operating-system, or dependency requirements.

Mitigation: Review suggested base-image changes, package-manager commands, and dependency assumptions before applying the optimized Dockerfile.

Risk: The skill may propose Dockerfile commands or configuration changes that need project-specific validation.

Mitigation: Test the resulting image build and runtime behavior in the target environment before release.

## Reference(s):

- [Dockerfile Optimizer on ClawHub](https://clawhub.ai/sunny0826/skills/dockerfile-optimizer)
- [Publisher profile](https://clawhub.ai/user/sunny0826)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration guidance]

**Output Format:** [Markdown report with Dockerfile code blocks and explanatory sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in Chinese or English based on the user's prompt language.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
