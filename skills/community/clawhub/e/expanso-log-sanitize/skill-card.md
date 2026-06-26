## Description: <br>
Sanitize log entries by removing passwords, tokens, and other sensitive patterns using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to redact common secrets from logs before sharing, documenting, or sending logs to downstream systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP HTTP mode exposes an unauthenticated endpoint on all network interfaces while handling sensitive logs. <br>
Mitigation: Prefer CLI mode for local-only sanitization. If MCP mode is used, bind it to localhost or protect it with firewall rules and authentication before sending real logs. <br>
Risk: Cloud deployment may process logs outside the local environment. <br>
Mitigation: Avoid cloud deployment unless the remote pipeline content and log processing location have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-log-sanitize) <br>
- [Expanso website](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [Sanitized log text and JSON objects with redaction counts and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode reads logs from standard input; MCP mode returns synchronous HTTP responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
