## Description: <br>
文旅公众号信息源 searches cultural tourism WeChat Official Account articles, ranks popular content by read count, clusters results by topic, and generates an HTML report for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, tourism marketers, team managers, and researchers use this skill to find trending cultural tourism WeChat articles, compare topics or destinations, and receive concise category summaries with downloadable HTML reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily subscription can create persistent scheduled jobs. <br>
Mitigation: Prefer one-time report generation unless daily delivery is required; when subscribing, verify the created LaunchAgent or crontab entry and remove it when no longer needed. <br>
Risk: API keys may be stored on disk for scheduled use. <br>
Mitigation: Avoid long-lived API keys in environment-backed plist files, verify key scope and revocation support, and do not expose keys in code, prompts, logs, or output files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/cultural-tourism-wechat-feed) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown chat summary plus terminal output and generated HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; supports optional keyword, start date, end date, output directory, and daily subscription controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
