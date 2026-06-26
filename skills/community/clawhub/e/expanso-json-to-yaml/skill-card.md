## Description: <br>
Convert JSON input into YAML format using Expanso Edge pipelines for CLI or MCP server integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert JSON strings into YAML through a local Expanso Edge CLI pipeline or an MCP-compatible HTTP pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional MCP/server pipeline listens on all network interfaces by default. <br>
Mitigation: Bind server mode to localhost or restrict network access when converting private data. <br>
Risk: Deploying the pipeline to Expanso Cloud may send conversion work to a remote Expanso job. <br>
Mitigation: Use the deploy command only when remote execution is intentional and appropriate for the input data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-json-to-yaml) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skill.yaml](skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, YAML, Shell commands, Configuration] <br>
**Output Format:** [JSON object containing YAML output, validity status, error text, and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode reads stdin with a 1 MiB buffer; MCP mode accepts POST requests on /convert.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
