## Description: <br>
Convert JSON arrays of objects into CSV format using local Expanso Edge pipelines for CLI or MCP workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to convert JSON object arrays into CSV output for data export, spreadsheet generation, report creation, and API response formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP mode starts an HTTP server that binds to 0.0.0.0 by default. <br>
Mitigation: Restrict or firewall MCP mode, choose an appropriate port, and stop the background server when finished. <br>
Risk: Remote deployment depends on the Expanso Cloud pipeline URL. <br>
Mitigation: Verify the Expanso Cloud pipeline URL before deploying. <br>
Risk: The skill depends on Expanso Edge tooling to execute pipelines. <br>
Mitigation: Install and run it only in environments where the Expanso tooling is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-json-to-csv) <br>
- [Expanso publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso](https://expanso.io) <br>
- [Expanso Cloud json-to-csv pipeline](https://skills.expanso.io/json-to-csv/pipeline-cli.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The pipeline returns CSV text with row count, detected columns, and metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
