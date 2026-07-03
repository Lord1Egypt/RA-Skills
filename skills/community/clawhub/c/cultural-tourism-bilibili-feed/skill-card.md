## Description: <br>
文旅B站信息源 searches Bilibili cultural-tourism videos, filters popular content by likes, clusters results by topic, and generates a polished HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, tourism professionals, and tourism researchers use this skill to monitor Bilibili cultural-tourism hotspots, compare topic activity, and generate shareable HTML trend reports from RedFox data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional daily subscription path can create persistent scheduled jobs through LaunchAgents or crontab. <br>
Mitigation: Prefer manual report generation or a user-managed scheduler unless the operator has reviewed and accepted the persistence behavior. <br>
Risk: The optional subscription path can store a RedFox API key on disk without enough safeguards. <br>
Mitigation: Use a revocable RedFox API key, avoid high-value credentials, and confirm key scope, expiration, and reset support before use. <br>
Risk: Generated reports include data returned from an external service and may contain untrusted video metadata. <br>
Mitigation: Review generated HTML reports before sharing and avoid treating report contents as verified facts without source validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/cultural-tourism-bilibili-feed) <br>
- [Publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=github) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Analysis] <br>
**Output Format:** [Markdown summary with category counts plus an HTML report file and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; normal report generation writes an HTML file, and optional subscription can create scheduled jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
