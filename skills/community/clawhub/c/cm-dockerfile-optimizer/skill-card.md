## Description: <br>
Optimize Dockerfiles for smaller images, faster builds, better security, and production readiness through multi-stage builds, layer caching, and vulnerability reduction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to review Dockerfiles, reduce container image size, improve build caching, harden runtime configuration, and prepare containers for production deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Dockerfile changes can alter build behavior, runtime permissions, health checks, or base image compatibility. <br>
Mitigation: Review base image swaps, non-root user changes, health checks, package pinning, and runtime configuration before applying changes to production. <br>
Risk: Build secret handling recommendations may be applied incorrectly and expose sensitive values in image layers or logs. <br>
Mitigation: Use BuildKit secret mounts or runtime environment injection, and inspect generated Dockerfiles for secrets in ARG, ENV, RUN, or copied files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/cm-dockerfile-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with inline Dockerfile, shell command, and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include before-and-after size estimates, issue severity groupings, optimization recommendations, and sample Dockerfile output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
