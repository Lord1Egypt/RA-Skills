## Description: <br>
Detects hardcoded secrets like API keys, tokens, and passwords in text or code using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to scan code, configuration, logs, pull requests, and CI inputs for hardcoded credentials before release or deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanned text, source code, and possible secrets can be sent to OpenAI when this skill is used. <br>
Mitigation: Use only with data flows approved by the organization, and avoid scanning private repositories, production logs, or real credentials unless that transfer is authorized. <br>
Risk: MCP mode can expose an unauthenticated network scan endpoint. <br>
Mitigation: Bind the service to localhost or restrict access with firewall rules before use. <br>
Risk: Secret matches can be exposed through logs or CI output. <br>
Mitigation: Avoid storing or printing full secret matches, and review logging behavior before CI or shared-environment deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aronchick/expanso-secrets-scan) <br>
- [Expanso Edge](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, analysis] <br>
**Output Format:** [JSON object with findings, has_secrets, summary, and metadata fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may include secret type, partial value, line number, severity, context, and audit metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
