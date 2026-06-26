## Description: <br>
Create, validate, and manage portable agent identity cards using the Agent Card v1 schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryancampbell](https://clawhub.ai/user/ryancampbell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent publishers use this skill to create standardized agent.json identity cards, validate them against a bundled JSON Schema, and prepare them for hosting at well-known agent identity URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator can install external packages when local validation tools are missing. <br>
Mitigation: Review the shell scripts first and prefer installing ajv-cli or jsonschema yourself in an isolated environment. <br>
Risk: The validator has unsafe fallback path handling. <br>
Mitigation: Avoid validating files with untrusted or unusual path names. <br>
Risk: The initializer writes to the requested output path. <br>
Mitigation: Do not run init.sh on a path containing important existing data unless you intend to overwrite it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ryancampbell/agent-identity-kit) <br>
- [Agent Card specification](https://foragents.dev/spec/agent-card) <br>
- [Agent Card v1 JSON Schema](https://foragents.dev/schemas/agent-card/v1.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and JSON Schema configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and validates agent.json identity card files through bundled shell scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
