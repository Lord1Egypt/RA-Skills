## Description: <br>
Queries Google Antigravity quota data and reports remaining model usage percentages and reset times for configured accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[T-Atlas](https://clawhub.ai/user/T-Atlas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI tool users with a Google Antigravity or OpenClaw OAuth profile use this skill to check model quota status, remaining percentage, and refresh times from the local agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a stored Google Antigravity or OpenClaw OAuth token and uses it for remote quota queries. <br>
Mitigation: Install and run it only with explicit consent to use that local OAuth profile for Google quota requests. <br>
Risk: The public framing as local CodexBar cost reporting may mislead users about the credential and network behavior. <br>
Mitigation: Review the skill before deployment and treat it as Google Antigravity quota reporting, not as a local cost-summary tool. <br>


## Reference(s): <br>
- [Google Antigravity Quota API Reference](references/codexbar-cli.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/T-Atlas/ag-model-usage) <br>
- [Fetch Available Models Endpoint](https://daily-cloudcode-pa.sandbox.googleapis.com/v1internal:fetchAvailableModels) <br>
- [Google Cloud Platform OAuth Scope](https://www.googleapis.com/auth/cloud-platform) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a local Google Antigravity or OpenClaw OAuth profile.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
