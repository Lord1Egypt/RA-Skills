## Description: <br>
Guides agents through building, pushing, remotely deploying, and health-checking Docker images for TPAIP project releases on Linux servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lky115](https://clawhub.ai/user/lky115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to deploy new or patched TPAIP service versions by confirming deployment inputs, building and pushing a Docker image, updating a remote Linux server, and validating service health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect deployment inputs could build, push, or run the wrong image or target the wrong server. <br>
Mitigation: Confirm the project path, Dockerfile path, image registry, tag, SSH target, deployment directory, ports, environment file, volumes, backup, and rollback plan before running deployment commands. <br>
Risk: Deployment requires sensitive SSH and registry access. <br>
Mitigation: Use least-privilege SSH and registry credentials, and verify access scope before invoking build, push, pull, or remote container commands. <br>
Risk: The server security summary notes a mismatched registry summary that could confuse operators. <br>
Mitigation: Verify the exact registry address and image tag against the intended TPAIP release before pushing or pulling images. <br>
Risk: The skill is designed for one-step container replacement and is not suited to complex database migrations or data rollback. <br>
Mitigation: Use a separate migration or release process when database changes, staged rollout, or data rollback planning is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lky115/deploy-docker-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the user to confirm deployment-specific paths, registry details, SSH target, runtime configuration, health checks, and rollback decision points before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
