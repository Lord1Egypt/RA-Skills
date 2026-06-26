## Description: <br>
Run Clawbridge discovery from OpenClaw chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeeTheBuilder](https://clawhub.ai/user/LeeTheBuilder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to trigger the Clawbridge CLI from OpenClaw chat and receive a candidate count with a Vault review link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an external Clawbridge CLI and depends on the user's trust in that runner and its cloud Vault handling. <br>
Mitigation: Install only after reviewing and trusting Clawbridge, and use an appropriately scoped workspace or profile. <br>
Risk: The documented install path uses a shell installer fetched from the Clawbridge website. <br>
Mitigation: Review the installer before running the command where possible. <br>
Risk: Discovery results may involve sensitive workspace data or uploads to the Clawbridge Vault. <br>
Mitigation: Avoid running discovery on sensitive data unless the Clawbridge cloud and Vault handling are acceptable for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/LeeTheBuilder/clawbridge-skill-latest) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/LeeTheBuilder) <br>
- [Clawbridge homepage](https://clawbridge.cloud) <br>
- [Clawbridge install script](https://clawbridge.cloud/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown chat response with parsed CLI output and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a candidate count and Vault URL when the external Clawbridge CLI emits machine-readable output.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
