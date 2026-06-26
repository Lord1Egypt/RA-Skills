## Description: <br>
Validates OpenClaw configuration patches or openclaw.json files locally before config changes and returns specific field-level error details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to preflight OpenClaw configuration patches or full openclaw.json files before applying changes, reducing vague validation failures by surfacing concrete schema and field-format errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The validator may query the OpenClaw gateway and cache the retrieved schema locally. <br>
Mitigation: Run it only in an environment where the local OpenClaw CLI is trusted and schema caching under the OpenClaw workspace is acceptable. <br>
Risk: Without jsonschema installed, validation falls back to basic hard-coded checks. <br>
Mitigation: Install jsonschema from a trusted package source when full JSON Schema validation is required. <br>


## Reference(s): <br>
- [Config Preflight Validator on ClawHub](https://clawhub.ai/halfmoon82/config-preflight-validator) <br>
- [Publisher profile: halfmoon82](https://clawhub.ai/user/halfmoon82) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text validation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch the OpenClaw configuration schema through the local OpenClaw CLI and cache it under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
