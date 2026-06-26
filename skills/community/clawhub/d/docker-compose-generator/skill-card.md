## Description: <br>
Generates a Docker Compose YAML file for a development MySQL and Redis stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to quickly create a local Docker Compose configuration for common development services. The bundled generator currently emits MySQL and Redis service definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes to docker-compose.yml by default and can overwrite an existing file at the chosen output path. <br>
Mitigation: Run it in the intended project directory, pass a non-conflicting output path when needed, and review any existing compose file before generation. <br>
Risk: The documentation lists several services, but the bundled generator currently emits only MySQL and Redis. <br>
Mitigation: Review the generated compose file and add or adjust services manually before relying on it for a broader stack. <br>
Risk: The generated MySQL example uses default local-development credentials. <br>
Mitigation: Change credentials and environment values before using the compose file outside a disposable local development environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/docker-compose-generator) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, text] <br>
**Output Format:** [Docker Compose YAML plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes docker-compose.yml by default unless the caller supplies another output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
