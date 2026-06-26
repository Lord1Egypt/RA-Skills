## Description: <br>
Detect personally identifiable information in text using Expanso Edge pipelines for CLI, MCP server, or cloud deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and privacy, security, or data engineering teams use this skill to scan text for PII before logging, storage, sharing, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive text can be sent to OpenAI during PII detection. <br>
Mitigation: Use only text you are authorized to send to OpenAI, configure approved credentials, and confirm data handling requirements before processing regulated or confidential content. <br>
Risk: MCP mode exposes an unauthenticated HTTP endpoint when run as configured. <br>
Mitigation: Run MCP mode only on trusted networks, bind it to localhost where possible, and add authentication or network controls before shared or exposed use. <br>
Risk: Artifact metadata mentions local regex detection, but the provided pipelines use OpenAI chat completion. <br>
Mitigation: Do not rely on regex-only local detection unless you verify or add a local regex pipeline path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-pii-detect) <br>
- [Artifact README](artifact/README.md) <br>
- [Expanso Edge](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [json, text, shell commands, configuration] <br>
**Output Format:** [Structured JSON findings with summary text and CLI or HTTP usage commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include PII type, value, character offsets, confidence, has_pii status, and audit metadata when returned by the pipeline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
