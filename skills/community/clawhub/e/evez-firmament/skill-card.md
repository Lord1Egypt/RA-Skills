## Description: <br>
Deploy and manage the EVEZ-OS infrastructure with 7 consciousness microservices, an API gateway, Terraform mesh, and an append-only event spine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Evez Firmament to deploy, test, and inspect a local EVEZ-OS microservice mesh with Docker Compose, Terraform-oriented infrastructure commands, health checks, and service-specific HTTP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated services can listen on ports 9111-9118 and expose service, state, health, gateway, and event-spine endpoints. <br>
Mitigation: Run only on a trusted local machine or behind a firewall, bind services to trusted interfaces, and do not expose ports 9111-9118 to untrusted networks. <br>
Risk: The invariance assertion API evaluates submitted assertion expressions and is an administrative-risk surface. <br>
Mitigation: Gate the assertion API behind trusted administrative controls or remove it before shared use. <br>
Risk: Event, replay, project, and state-inspection endpoints can reveal sensitive request or state data if private text is submitted. <br>
Mitigation: Avoid sending secrets or private text to the services and restrict access to event/state inspection endpoints. <br>
Risk: Terraform destroy targets can remove deployed infrastructure. <br>
Mitigation: Require explicit operator review and approval before running destroy commands, especially in shared or production environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/evezart/evez-firmament) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code references, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment and management guidance for Docker Compose, Terraform, Makefile targets, and local HTTP service checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
