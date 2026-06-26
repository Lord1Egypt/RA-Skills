## Description: <br>
Automate DolphinDB Docker deployment with auto architecture detection (ARM64/x86_64), smart memory allocation (50% rule), and full data persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy and operate DolphinDB in Docker on macOS or Linux with architecture detection, memory sizing, persistent data storage, and version selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker container can receive broad host configuration access through the /etc mount. <br>
Mitigation: Remove the /etc mount when possible, narrowly scope it when required, and make any required mount read-only. <br>
Risk: The deployment script changes Docker state and can stop or replace an existing container named dolphindb. <br>
Mitigation: Check for an existing dolphindb container before running the skill and use a dedicated container name and data directory for this deployment. <br>
Risk: DolphinDB service ports may be reachable beyond the intended host. <br>
Mitigation: Bind service ports to localhost or firewall them unless remote access is intentionally required. <br>


## Reference(s): <br>
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) <br>
- [DolphinDB Documentation](https://dolphindb.cn/) <br>
- [DolphinDB Docker Hub](https://hub.docker.com/u/dolphindb) <br>
- [DolphinDB GitHub](https://github.com/dolphindb) <br>
- [ClawHub Skill Page](https://clawhub.ai/ugpoor/dolphindb-docker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Docker deployment guidance for macOS and Linux hosts that have Docker available.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
