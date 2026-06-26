## Description: <br>
Analyzes nested JSON through Expanso Edge CLI or HTTP pipeline modes and returns the parsed object, top-level keys, key count, and run metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to inspect JSON payload structure from the command line or through an HTTP endpoint backed by Expanso Edge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTTP mode listens broadly by default and returns submitted JSON in the response. <br>
Mitigation: Use CLI mode for sensitive JSON, or bind and firewall the HTTP endpoint so it is not exposed to untrusted networks. <br>
Risk: The published metadata describes flattened dot-notation output, while the pipeline behavior reports the original object and top-level structure metadata. <br>
Mitigation: Validate the returned JSON shape against downstream expectations before relying on it as a fully flattened object. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-json-flatten) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON object from CLI stdout or HTTP sync response, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI mode reads stdin with a 1 MiB buffer; HTTP mode accepts POST requests at /flatten on the configured port, defaulting to 8080.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
