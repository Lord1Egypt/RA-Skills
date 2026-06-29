## Description: <br>
AI抖音信息源 scans AI-related Douyin posts, ranks them by engagement, clusters topics, and generates an HTML daily report with cover images, metrics, direct links, and subscription support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, AI creators, and industry analysts use this skill to monitor AI trends on Douyin, review historical hot topics, and generate local daily reports for market or creative research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and can expose sensitive credentials if the key is hardcoded, logged, or stored insecurely. <br>
Mitigation: Provide the key through REDFOX_API_KEY only, verify the key source, scope, expiry, and reset path, and avoid placing the key in prompts, code, logs, or generated reports. <br>
Risk: The optional subscription feature persists a scheduled task and may store the API key on disk. <br>
Mitigation: Avoid subscription mode unless that persistence is acceptable; review and remove the LaunchAgent or crontab entry when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/redfox-data/douyin-ai-feed) <br>
- [RedFoxHub API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, HTML, shell commands, configuration] <br>
**Output Format:** [Terminal text plus generated HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; optional subscription creates a daily scheduled task.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
