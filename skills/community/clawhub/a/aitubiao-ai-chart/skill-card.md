## Description: <br>
Generates AI chart visualization projects from pasted tables or uploaded data through the aitubiao API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn pasted tables or uploaded CSV, TXT, or spreadsheet data into chart projects hosted by aitubiao. It guides authentication, data confirmation, quota checking, fee confirmation, chart creation, optional screenshots, and project export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a persistent aitubiao API key on the user's machine. <br>
Mitigation: Use the skill only if you trust aitubiao with the key, keep the credentials file private, and revoke or delete the key after use when appropriate. <br>
Risk: Chart data is sent to a third-party service for generation. <br>
Mitigation: Avoid sensitive, confidential, or regulated datasets unless that use has been approved for aitubiao. <br>
Risk: The bundled CLI exposes broader aitubiao API commands than chart generation alone. <br>
Mitigation: Review the command being invoked and keep use scoped to the intended chart workflow unless the user explicitly requests a supported follow-up action. <br>
Risk: Project exports write files to local paths. <br>
Mitigation: Confirm export paths before downloading and avoid paths that could overwrite important local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitubiao/aitubiao-ai-chart) <br>
- [aitubiao application](https://app.aitubiao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request bodies, API response summaries, project links, and downloaded file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.aitubiao.com, Bash, curl, jq, and a user-provided aitubiao API key.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
