## Description: <br>
Manage Google Calendar, Google Drive, and Google Sheets through MyBrandMetrics-connected Google data sources and the local Google Workspace CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Workspace users use this skill to perform Google Calendar, Drive, and Sheets actions through a local CLI wrapper backed by MyBrandMetrics-managed Google access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Google access through a MyBrandMetrics API key and token endpoint. <br>
Mitigation: Set GWS_TOKEN_URL only to the legitimate MyBrandMetrics token endpoint, connect only needed Google data sources, and protect the API key or use GWS_SKILL_API_KEY instead of a plaintext file. <br>
Risk: Calendar, Drive, and Sheets operations can delete, share, move, or bulk-update user content. <br>
Mitigation: Manually confirm delete, share, move, and bulk-update actions before running generated commands. <br>
Risk: The install script may fetch or build the Google Workspace CLI before use. <br>
Mitigation: Review the installation steps and trust the MyBrandMetrics and Google Workspace CLI sources before installing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawbus/clawbus-google-workspace) <br>
- [Clawbus Website](https://www.clawbus.com/) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>
- [Google Workspace CLI Releases](https://api.github.com/repos/googleworkspace/cli/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local CLI commands that call Google Workspace APIs using MyBrandMetrics-managed access tokens.] <br>

## Skill Version(s): <br>
1.2.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
