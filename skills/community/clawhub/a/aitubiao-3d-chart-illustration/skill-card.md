## Description: <br>
Generates 3D-style chart illustrations from user-provided tabular data through the Aitubiao API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn validated table data into 3D chart illustration images after authenticating with Aitubiao, selecting a supported chart type, checking quota, and approving the generation cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an Aitubiao API key and sends chart data to api.aitubiao.com. <br>
Mitigation: Use a dedicated or low-quota API key, avoid regulated or confidential datasets unless third-party processing is approved, and rotate or delete the key when no longer needed. <br>
Risk: The bundled CLI includes account-backed project, PPT, Sankey, and export capabilities beyond the advertised 3D chart feature. <br>
Mitigation: Review intended command use before deployment and restrict usage to the documented 3D chart workflow unless the broader account-backed capabilities are acceptable. <br>
Risk: Generation may consume account credits and create calls should not be retried automatically after timeouts or server errors. <br>
Mitigation: Require quota checks and explicit user cost confirmation before generation, and let the user decide whether to retry failed create requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aitubiao/aitubiao-3d-chart-illustration) <br>
- [Aitubiao application](https://app.aitubiao.com) <br>
- [Aitubiao API key management](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with shell commands and returned image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns 3D illustration image URLs and a short summary when generation succeeds.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
