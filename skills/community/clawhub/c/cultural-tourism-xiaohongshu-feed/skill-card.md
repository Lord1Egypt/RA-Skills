## Description: <br>
Searches Xiaohongshu for popular cultural-tourism posts, filters them by engagement, clusters results by topic, and generates an HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, tourism marketers, and researchers use this skill to monitor popular Xiaohongshu cultural-tourism posts, compare topic activity, and produce shareable daily reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional daily subscription changes local scheduler settings through a macOS LaunchAgent or crontab. <br>
Mitigation: Review subscription behavior before enabling it, prefer one-time report generation when recurring output is not needed, and remove the scheduled task with the provided unsubscribe flow when no longer required. <br>
Risk: The skill requires REDFOX_API_KEY and subscription setup can store the key in local scheduler configuration. <br>
Mitigation: Use a limited and revocable API key, avoid exposing it in prompts, logs, or shared files, and rotate or revoke the key after use if it may have been stored in plaintext. <br>
Risk: Queries and report generation depend on RedFoxHub/Xiaohongshu data handling. <br>
Mitigation: Install only when that data handling is acceptable for the intended use, and avoid submitting sensitive or confidential search terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/cultural-tourism-xiaohongshu-feed) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown summary with a category table plus a generated HTML report file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; optional subscription creates recurring scheduled reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
