## Description: <br>
Configure and manage Foxcode AI models in OpenClaw through guided API setup, endpoint selection, model configuration, validation, and status monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add Foxcode model providers, choose primary and fallback Claude models, validate configuration, and monitor endpoint availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Foxcode API token and writes it into OpenClaw auth profile configuration. <br>
Mitigation: Use only a token intended for this setup, keep auth profile files private, and avoid placing real tokens in shared shell startup files or shared configs. <br>
Risk: The configuration wizard can modify OpenClaw files including openclaw.json and auth-profiles.json. <br>
Mitigation: Back up OpenClaw configuration before running the wizard and review the generated provider, model, and auth profile entries before relying on them. <br>
Risk: Validation may contact custom baseUrl values from local configuration. <br>
Mitigation: Do not run validation against OpenClaw configs that contain untrusted custom baseUrl values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/foxcode-openclaw) <br>
- [Foxcode Endpoints Reference](references/foxcode-endpoints.md) <br>
- [OpenClaw Configuration Reference](references/openclaw-config.md) <br>
- [Foxcode status page](https://status.rjj.cc/status/foxcode) <br>
- [Foxcode API keys](https://foxcode.rjj.cc/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets; bundled scripts can emit text or JSON status reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When the user runs the bundled configuration script, it can write OpenClaw configuration and auth profile files on the local system.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
