## Description:

Review a Dockerfile for layer hygiene, least-privilege users, pin practices, and clearer build structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmahmadcs](https://clawhub.ai/user/hmahmadcs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Dockerfiles for build efficiency, maintainability, and security, with prioritized fixes and suggested snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted Dockerfiles may reveal secrets or sensitive internal image details.

Mitigation: Remove credentials and sensitive image details before sharing a Dockerfile for review.

Risk: Suggested Dockerfile changes may not work with private base images or distribution-specific packages.

Mitigation: Review proposed changes and validate builds and runtime behavior in the target environment before deployment.

## Reference(s):

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [ClawHub skill release](https://clawhub.ai/hmahmadcs/skills/dockerfile-best-practice-reviewer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Dockerfile snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings, suggested changes, and a verification checklist; builds are not run by default.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
