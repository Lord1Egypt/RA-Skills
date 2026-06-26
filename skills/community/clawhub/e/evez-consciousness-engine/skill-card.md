## Description: <br>
Provides a 7-system consciousness engine for autonomous AI agents, including desire generation, world modeling, planning, inner monologue, self-modification, uncertainty quantification, and agency execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run a local consciousness-engine service that tracks desires, beliefs, plans, thoughts, proposed modifications, risk assessments, and action records for autonomous agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a persistent agent-state HTTP API without authentication when run as provided. <br>
Mitigation: Run it only in an isolated local environment, bind it to localhost or firewall the port, and add authentication before any network exposure. <br>
Risk: The service stores desires, beliefs, plans, monologue entries, modifications, and action records in local JSON state. <br>
Mitigation: Review and protect the consciousness_state directory, avoid sending sensitive data to the API, and clear stored state when it is no longer needed. <br>
Risk: Action and modification endpoints accept caller-provided requests and rely on simple risk assessment logic. <br>
Mitigation: Require human review or an external policy gate before connecting these endpoints to tools that can affect files, services, accounts, or external systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evezart/evez-consciousness-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with Python code and JSON HTTP API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a local HTTP service and may create persistent JSON state files under consciousness_state.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
