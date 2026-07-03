## Description: <br>
Generates API-backed 3D-styled chart illustrations from user-provided data, supporting line, bar, pie, and other chart types with 13 material styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn tabular chart data into 3D visualization illustrations through the aitubiao service. It guides authentication, chart-type selection, quota confirmation, API invocation, and result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled CLI stores a persistent aitubiao API key in the user's home directory. <br>
Mitigation: Use a dedicated, revocable API key, restrict file permissions, and rotate or revoke the key when the skill is no longer needed. <br>
Risk: User-provided chart data is sent to a third-party service. <br>
Mitigation: Avoid submitting sensitive or regulated datasets unless the user trusts the service and the use is allowed by applicable policy. <br>
Risk: The bundled script includes broader chart, PPT, Sankey, and export commands beyond the advertised 3D chart illustration workflow. <br>
Mitigation: Review the script before installation and execute only the commands required for the 3D illustration workflow. <br>
Risk: Create operations may consume paid credits and should not be repeated automatically after timeouts or server errors. <br>
Mitigation: Check quota, show the cost, require explicit user confirmation before creation, and let the user decide whether to retry failed create operations. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/aitubiao/ai-3d-illustration) <br>
- [Publisher profile](https://clawhub.ai/user/aitubiao) <br>
- [爱图表 application](https://app.aitubiao.com) <br>
- [API key management](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style responses with Bash commands and JSON API payloads; final results include image URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.aitubiao.com, Bash, curl, jq, and a user-provided aitubiao API key.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release metadata; artifact frontmatter reports 1.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
