## Description: <br>
Convert CSV input with a header row into a JSON array of objects using Expanso Edge CLI or MCP pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to transform CSV data from imports, spreadsheets, logs, or API workflows into structured JSON for downstream automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional MCP/HTTP mode can expose CSV conversion over a network listener. <br>
Mitigation: Bind the service to localhost or restrict network access before processing private CSV data. <br>
Risk: The artifact includes a command to deploy the pipeline through Expanso Cloud. <br>
Mitigation: Run the deploy command only when you intentionally want to publish or operate the skill through that service. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aronchick/expanso-csv-to-json) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso](https://expanso.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON objects returned on stdout or synchronous HTTP response, with Markdown usage guidance and shell commands in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON output includes data, row_count, columns, and metadata fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
