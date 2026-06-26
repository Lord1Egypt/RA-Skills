## Description: <br>
Convert XML input into JSON using Expanso Edge pipelines for CLI, MCP server, or cloud deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert XML strings into JSON through a local CLI pipeline, an MCP-style HTTP server pipeline, or a deployable Expanso Cloud pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server pipeline listens for XML conversion requests and may accept input from other machines if exposed on a network interface. <br>
Mitigation: Bind the service to localhost or protect the port unless remote submissions are intended. <br>
Risk: Cloud deployment could run a remote pipeline that differs from the reviewed local artifact. <br>
Mitigation: Prefer the reviewed local pipeline, or verify the Expanso Cloud pipeline URL and contents before deployment. <br>
Risk: Large or untrusted XML input may consume runtime resources during parsing. <br>
Mitigation: Keep input-size limits in place and review the pipeline before accepting untrusted XML at scale. <br>


## Reference(s): <br>
- [Expanso xml-to-json on ClawHub](https://clawhub.ai/aronchick/expanso-xml-to-json) <br>
- [Publisher profile](https://clawhub.ai/user/aronchick) <br>
- [Expanso Cloud pipeline](https://skills.expanso.io/xml-to-json/pipeline-cli.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON output and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode reads XML from stdin; server mode accepts POST requests and returns json, valid, error, and metadata fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
