## Description: <br>
Docker Analyzer helps agents inspect Docker images, containers, layers, build history, disk usage, compose files, and optimization opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect local Docker images and containers, review layer and history information, and get cleanup or optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted image name passed to the optimization command may execute local code. <br>
Mitigation: Avoid image names or arguments copied from untrusted text until the optimize argument-handling issue is fixed. <br>
Risk: The skill runs Docker inspection commands against the local Docker context. <br>
Mitigation: Use it only with Docker contexts and image metadata that are acceptable to expose to the agent. <br>


## Reference(s): <br>
- [Docker Analyzer on ClawHub](https://clawhub.ai/xueyetianya/docker-analyzer) <br>
- [wagoodman/dive](https://github.com/wagoodman/dive) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text Docker inspection and optimization reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Docker CLI access for most commands] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
