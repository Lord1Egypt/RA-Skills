## Description: <br>
Install and run Aperture, the L402 Lightning reverse proxy from Lightning Labs, for creating L402 paywalls, configuring paid API endpoints, hosting paid content for other agents, or testing L402 authentication flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install Aperture, generate local configuration, and run an L402-aware reverse proxy in front of backend APIs or paid content services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aperture configuration can expose paid endpoints without intended payment enforcement if authentication is disabled or TLS is disabled on public or shared networks. <br>
Mitigation: Review ~/.aperture/aperture.yaml before starting Aperture, avoid --insecure and --no-auth outside local development, and use explicit production TLS settings. <br>
Risk: Overbroad host matching can route unintended requests through the proxy. <br>
Mitigation: Replace hostregexp ".*" with explicit hostnames for production services. <br>
Risk: Using overly powerful LND credentials increases blast radius if local configuration or mounted credentials are exposed. <br>
Mitigation: Use an invoice-only macaroon rather than admin credentials and confirm the configured macdir before launch. <br>
Risk: The start script can leave Aperture running as a background service. <br>
Mitigation: Stop the service with scripts/stop.sh when finished and check the configured log file if startup fails. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Roasbeef/aperture) <br>
- [Aperture source and documentation](https://github.com/lightninglabs/aperture) <br>
- [Go downloads](https://go.dev/dl/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Aperture configuration under ~/.aperture when its setup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
