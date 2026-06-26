## Description: <br>
Optimize Docker Compose configurations for development and production by auditing services, networking, volumes, health checks, and resource management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to review Docker Compose files for security, performance, production readiness, and practical configuration improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested Compose changes could be incorrect or unsuitable for the target environment. <br>
Mitigation: Review recommendations before applying them and test changes in the intended development or production environment. <br>
Risk: Docker Compose files can contain real secrets or sensitive deployment details. <br>
Mitigation: Run the skill only in the project intended for review and avoid exposing Compose files with secrets unless those values may be shared with the agent. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with issue lists, recommendations, and inline command or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides review findings for Compose services, networks, volumes, health checks, dependencies, resource limits, and development versus production posture.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
