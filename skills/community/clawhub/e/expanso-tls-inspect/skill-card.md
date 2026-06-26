## Description: <br>
Inspect TLS certificates for expiry, SANs, chain validity, and cipher details using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect TLS certificate metadata for a hostname through Expanso Edge CLI or MCP pipelines. It is intended for certificate inventory and troubleshooting workflows, not as a standalone certificate assurance decision point. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that crafted host input in the CLI path may allow command execution. <br>
Mitigation: Accept only trusted, validated hostnames or host:port values, constrain execution in a sandboxed environment, and review the pipeline before deployment. <br>
Risk: The security summary reports that certificate results can be fabricated or misleading, and the valid field should not be treated as certificate assurance. <br>
Mitigation: Do not rely on the valid field for security decisions; confirm certificate status with an independent TLS validation tool before acting on results. <br>
Risk: The security guidance warns against MCP mode for real security decisions unless validation and binding behavior are changed. <br>
Mitigation: Avoid MCP mode for production certificate decisions, or modify it to perform actual TLS validation and bind only to intended network interfaces. <br>


## Reference(s): <br>
- [Expanso tls-inspect ClawHub listing](https://clawhub.ai/aronchick/expanso-tls-inspect) <br>
- [Expanso tls-inspect pipeline](https://skills.expanso.io/tls-inspect/pipeline-cli.yaml) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON certificate inspection results with shell-command usage and Expanso pipeline configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes certificate fields, validity status, host metadata, trace identifiers, and timestamps when the pipeline succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
