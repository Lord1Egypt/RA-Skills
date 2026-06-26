## Description: <br>
Convert YAML input into JSON format using Expanso Edge pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to convert YAML strings into JSON through a local CLI pipeline or an optional HTTP server pipeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional server mode listens for HTTP requests and may expose YAML conversion over the network if deployed broadly. <br>
Mitigation: Prefer CLI mode for private data; when using server mode, bind locally or otherwise restrict network exposure before processing sensitive YAML. <br>
Risk: The skill depends on the Expanso Edge runtime to execute its pipelines. <br>
Mitigation: Install and run it only in environments where the Expanso Edge dependency is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-yaml-to-json) <br>
- [README.md](README.md) <br>
- [skill.yaml](skill.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON object with parsed output, validity flag, error text, and metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode reads YAML from stdin; server mode accepts POST requests to /convert.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
