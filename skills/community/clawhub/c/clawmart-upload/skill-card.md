## Description: <br>
Upload your current OpenClaw configuration to the ClawMart marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rxdaozhang](https://clawhub.ai/user/rxdaozhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to package their workspace configuration and submit it as a ClawMart pack for marketplace review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload OpenClaw configuration, memory, user, tools, identity, and local skill contents to an external marketplace. <br>
Mitigation: Review the file list before upload and exclude sensitive files or local skills unless their full contents are intended for submission. <br>
Risk: The built-in sensitive-data check does not cover local skill files. <br>
Mitigation: Inspect local skill files manually before including them in the upload payload. <br>
Risk: The ClawMart API token is stored in a local configuration file. <br>
Mitigation: Use a revocable token and revoke it if the local config file is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rxdaozhang/clawmart-upload) <br>
- [ClawMart marketplace](https://clawmart-gray.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON payload examples and HTTP request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user prompts, upload summaries, sensitive-data warnings, and ClawMart API request details.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
