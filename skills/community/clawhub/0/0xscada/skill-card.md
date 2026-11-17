## Description:

Decentralized Industrial Control Fabric that bridges SCADA systems with blockchain-backed audit trails and Kannaka memory integration, providing a unified API for telemetry, geometry classification, and verifiable industrial state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and industrial automation engineers use this skill to start and check a local 0xSCADA node that exposes SCADA telemetry, blockchain audit anchoring, and Kannaka Flux integration when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Starting the skill may run the npm development script from the repository referenced by SCADA_DIR.

Mitigation: Install only when the local 0xSCADA repository is trusted, verify SCADA_DIR, and review the target package.json before starting the server.

Risk: The skill supports sensitive blockchain and integration credentials such as PRIVATE_KEY and FLUX_AUTH_TOKEN.

Mitigation: Keep credentials out of committed files and shared shells, and prefer read-only or test credentials for evaluation.

## Reference(s):

- [0xscada ClawHub skill page](https://clawhub.ai/nickflach/skills/0xscada)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local startup and status guidance for a configured 0xSCADA repository.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
