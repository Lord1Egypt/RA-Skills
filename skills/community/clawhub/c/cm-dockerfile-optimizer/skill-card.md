## Description:

Optimize Dockerfiles for smaller images, faster builds, better security, and production readiness - multi-stage builds, layer caching, vulnerability reduction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DevOps engineers use this skill to review Dockerfiles and receive optimization guidance for image size, build speed, layer caching, security hardening, and production readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Dockerfile changes can alter runtime behavior, base image compatibility, file inclusion, or build caching semantics.

Mitigation: Review proposed Dockerfile edits before applying them, especially base image changes, .dockerignore exclusions, cache mounts, and secret mount recommendations.

Risk: Optimization estimates may not match the actual image size, layer count, or build time for a specific project.

Mitigation: Rebuild and test the container image after applying recommendations, then verify size, security scan results, health checks, and application behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/cm-dockerfile-optimizer)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown report with Dockerfile examples, shell commands, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before-and-after estimates for image size, layer count, and build speed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
