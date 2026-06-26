## Description: <br>
Registers, deregisters, sends heartbeats for, and checks an OpenClaw instance as an A2A agent in an A2A API Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thearchitectit](https://clawhub.ai/user/thearchitectit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an OpenClaw instance for A2A gateway discovery, register or remove it from the gateway registry, send liveness heartbeats, and inspect registration status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts use the configured A2A gateway admin API for registration, deregistration, heartbeat, and status operations. <br>
Mitigation: Install only for trusted gateways, prefer HTTPS gateway URLs, and review gateway access expectations before running the scripts. <br>
Risk: The setup script can create or update an a2a.conf file containing gateway configuration and an API key. <br>
Mitigation: Restrict access to the generated a2a.conf file and avoid using this skill on shared machines. <br>
Risk: Status and heartbeat operations can access gateway-wide agent metadata. <br>
Mitigation: Run these operations only where gateway-wide registry visibility is acceptable. <br>
Risk: Register and deregister operations can change discoverability for the configured agent slug and URL. <br>
Mitigation: Verify the configured gateway URL, agent slug, agent URL, and capabilities before registering or removing an agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thearchitectit/a2a-register) <br>
- [Publisher profile](https://clawhub.ai/user/thearchitectit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and script-driven terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update an a2a.conf configuration file and may call A2A gateway admin endpoints when the scripts are run.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
