## Description:

Automatically generates optimized Dockerfiles for common application types with multi-stage builds and container best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honestqiao](https://clawhub.ai/user/honestqiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate Dockerfile starting points for Node.js, Python, Go, and Java applications. It helps standardize container setup with common build, dependency, port, and command patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted version or port values may be embedded directly into generated Dockerfile instructions, which could create unsafe builds.

Mitigation: Review generated Dockerfiles before building them, use trusted simple version and port values, and avoid automated pipelines until version and port validation is enforced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honestqiao/skills/dockerfile-generator)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Plain text Dockerfile content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Dockerfiles should be reviewed before build or deployment.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
