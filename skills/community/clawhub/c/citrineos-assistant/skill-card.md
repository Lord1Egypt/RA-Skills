## Description: <br>
Install, configure, and manage CitrineOS (EV charging / OCPP) via natural language. Supports Docker, cloud hosting, and API operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enenkov](https://clawhub.ai/user/enenkov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, operators, and engineers use this skill to install, configure, deploy, troubleshoot, and administer CitrineOS for EV charging and OCPP environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated commands or API calls may affect live CitrineOS, Docker, cloud firewall, or charging-station state. <br>
Mitigation: Review generated commands and explicitly confirm the target server, charging station, and operation before running mutating actions such as start, reset, stop, or firewall changes. <br>
Risk: Production deployments may be exposed or unstable if service ports, sudo commands, npm commands, or dependency versions are accepted without review. <br>
Mitigation: Review Docker, npm, sudo, and cloud firewall commands before use, and prefer pinned CitrineOS releases for production deployments. <br>


## Reference(s): <br>
- [ClawHub CitrineOS Assistant](https://clawhub.ai/enenkov/citrineos-assistant) <br>
- [CitrineOS Core Repository](https://github.com/citrineos/citrineos-core) <br>
- [Docker Get Docker Documentation](https://docs.docker.com/get-docker/) <br>
- [Docker Engine Installation Documentation](https://docs.docker.com/engine/install/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, HTTP request descriptions, tables, and configuration paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that affect Docker services, cloud firewall settings, or charging-station APIs; users should review commands before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
