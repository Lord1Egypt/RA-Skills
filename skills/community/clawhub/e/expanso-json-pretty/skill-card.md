## Description: <br>
Formats and pretty-prints JSON input with indentation using Expanso Edge pipelines for easier readability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to format compact or minified JSON into readable, indented output through a local CLI pipeline or optional HTTP server pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional HTTP server mode can receive JSON over a network-facing endpoint. <br>
Mitigation: Restrict or firewall MCP/server mode when formatting private data, and prefer the local CLI pipeline for ordinary JSON formatting. <br>
Risk: Cloud deployment uses a remote pipeline URL. <br>
Mitigation: Review the remote deploy URL before deploying the pipeline to Expanso Cloud. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-json-pretty) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso Cloud pipeline](https://skills.expanso.io/json-pretty/pipeline-cli.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON object containing a formatted JSON string and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a local stdin/stdout CLI mode and an optional HTTP server mode for synchronous formatting responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
