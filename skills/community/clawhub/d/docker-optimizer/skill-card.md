## Description: <br>
Optimize Dockerfiles with multi-stage builds, layer caching, security best practices, and size reduction techniques. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelatamuk](https://clawhub.ai/user/michaelatamuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Dockerfiles and produce optimization guidance for faster builds, smaller images, improved layer caching, and safer production container defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Dockerfiles or build commands can change build behavior, image contents, runtime users, exposed ports, or health checks. <br>
Mitigation: Review generated Dockerfile, .dockerignore, and shell commands before applying them, then test the resulting image in a project-scoped environment. <br>
Risk: Private registry credentials or package manager tokens can leak if copied into Docker build context or embedded in image layers. <br>
Mitigation: Use BuildKit secret mounts or temporary project-scoped secret files, and avoid placing real credentials in Dockerfiles, .dockerignore-excluded files, or command history. <br>


## Reference(s): <br>
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/) <br>
- [Docker development best practices](https://docs.docker.com/develop/dev-best-practices/) <br>
- [Docker multi-stage builds](https://docs.docker.com/build/building/multi-stage/) <br>
- [Moby BuildKit](https://github.com/moby/buildkit) <br>
- [GoogleContainerTools distroless](https://github.com/GoogleContainerTools/distroless) <br>
- [dive image analysis tool](https://github.com/wagoodman/dive) <br>
- [ClawHub skill page](https://clawhub.ai/michaelatamuk/docker-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/michaelatamuk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Dockerfile, .dockerignore, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optimization reports, generated Dockerfiles, .dockerignore entries, build commands, and implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
