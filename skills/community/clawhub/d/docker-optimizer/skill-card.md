## Description:

Optimize Dockerfiles with multi-stage builds, layer caching, security best practices, and size reduction techniques.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelatamuk](https://clawhub.ai/user/michaelatamuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to review Dockerfiles, identify build, size, caching, and container security issues, and produce optimized production-oriented Dockerfile changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Dockerfile changes can alter production container behavior through base image swaps, dependency changes, user permissions, health checks, exposed ports, or package removals.

Mitigation: Review each generated Dockerfile change as production code, then build and run the image in a representative environment before deployment.

Risk: Optimization patterns can unintentionally affect secret handling, especially when build inputs or environment files are copied into images.

Mitigation: Verify that secrets are not copied into image layers and prefer BuildKit secret mounts or runtime secret injection where applicable.

## Reference(s):

- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [BuildKit documentation](https://github.com/moby/buildkit)
- [Dive image layer explorer](https://github.com/wagoodman/dive)
- [Distroless images](https://github.com/GoogleContainerTools/distroless)
- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with Dockerfile, .dockerignore, and shell command code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include before-and-after estimates for image size, build speed, caching behavior, and security posture.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
