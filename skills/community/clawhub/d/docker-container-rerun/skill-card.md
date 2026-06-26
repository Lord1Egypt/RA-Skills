## Description: <br>
Safely checks whether a Docker container's image has changed and, only when needed, recreates that docker run container with a user-provided original docker run command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugvfpdcuwfnh](https://clawhub.ai/user/ugvfpdcuwfnh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to update Docker containers that were originally created with docker run while preserving the exact recreate command and avoiding unnecessary stop/remove/recreate actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The apply mode can give the agent Docker control over the target host. <br>
Mitigation: Use apply mode only after the operator approves the exact recreate command and intended container target. <br>
Risk: The bundled script can execute a user-supplied recreate command through Bash. <br>
Mitigation: Inspect the command for shell operators, redirects, command substitution, and unexpected arguments before execution. <br>
Risk: Recent container logs returned by the workflow may contain sensitive information. <br>
Mitigation: Treat log output as sensitive and avoid sharing it beyond the operational context. <br>


## Reference(s): <br>
- [Command Parsing Notes](references/command-parsing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ugvfpdcuwfnh/docker-container-rerun) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON summaries from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports container name, image reference, image IDs, update decision, post-recreate state, health status, and recent log observations when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
