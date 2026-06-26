## Description: <br>
Run macOS in Docker on a Linux host with Docker and KVM so developers can access a macOS environment for iOS builds and macOS-only software. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NightVibes3](https://clawhub.ai/user/NightVibes3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, and connect to a Docker-OSX macOS VM on Linux for iOS build workflows or macOS-only tools. It is intended for hosts with Docker, KVM, and sufficient CPU, memory, and disk resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose SSH and VNC access to a privileged macOS VM. <br>
Mitigation: Run it only on a trusted Linux host, bind SSH and VNC to localhost or firewall them, and change the default password immediately. <br>
Risk: Docker and KVM access can affect host security boundaries. <br>
Mitigation: Review the Docker-OSX image source and use the skill only where Docker and KVM risks are acceptable. <br>
Risk: Stopping or restarting the VM may remove unpersisted VM state. <br>
Mitigation: Back up or persist important VM work before stopping or recreating the container. <br>


## Reference(s): <br>
- [Docker-OSX project homepage](https://github.com/sickcodes/Docker-OSX) <br>
- [ClawHub release page](https://clawhub.ai/NightVibes3/docker-osx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with status text, connection commands, and troubleshooting details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SSH/VNC connection details, a default password, Docker status, and recent container logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
