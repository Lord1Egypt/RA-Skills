## Description: <br>
0xSCADA bridges SCADA systems with blockchain-backed audit trails and Kannaka memory integration through a unified API for telemetry, geometry classification, and verifiable industrial state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickFlach](https://clawhub.ai/user/NickFlach) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial automation engineers use this skill to configure, start, and check a local 0xSCADA server that connects SCADA telemetry with blockchain audit and Kannaka Flux integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The startup wrapper runs an external 0xSCADA project with npm run dev from the configured SCADA_DIR. <br>
Mitigation: Inspect and trust the configured 0xSCADA repository before running the skill, and prefer an isolated development environment. <br>
Risk: Optional configuration can expose sensitive SCADA data, database URLs, blockchain private keys, and Flux tokens to the local server. <br>
Mitigation: Use test or least-privilege credentials and avoid production telemetry or funded keys until the server behavior is verified. <br>
Risk: The wrapper starts a background server but does not define a stop command. <br>
Mitigation: Confirm process management and shutdown steps before using it in a long-running or shared environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NickFlach/0xscada) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start or check a local 0xSCADA server using SCADA_DIR, SCADA_PORT, and optional database, blockchain, and Flux environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
