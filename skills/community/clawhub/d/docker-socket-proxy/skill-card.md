## Description: <br>
Manage a remote Docker host through a Tecnativa docker-socket-proxy instance, using proxy-side API section controls to limit the Docker operations an agent can perform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BP602](https://clawhub.ai/user/BP602) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and administer Docker hosts through a configured docker-socket-proxy deployment while relying on proxy-side API section controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Docker through the configured proxy, including lifecycle and cleanup actions that may affect running workloads. <br>
Mitigation: Enable only the minimum docker-socket-proxy sections needed and require explicit human approval before exec, restart, kill, stop, or prune commands, especially on production hosts. <br>
Risk: Docker inspection, logs, configs, environment, mounts, and secret metadata can expose sensitive operational data. <br>
Mitigation: Limit read-oriented proxy sections to trusted use cases and handle command output as sensitive when it comes from production or shared hosts. <br>
Risk: A raw Docker daemon endpoint would be root-equivalent host access if used instead of a constrained proxy. <br>
Mitigation: Route the skill only through a tightly scoped docker-socket-proxy instance and avoid exposing a raw Docker socket or unrestricted daemon TCP endpoint. <br>


## Reference(s): <br>
- [Tecnativa docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, aligned tables, and JSON from Docker API requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on the docker-socket-proxy API sections enabled by the user; disabled sections return HTTP 403.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
