## Description: <br>
Searches Douyin cultural tourism content, ranks popular videos by likes, clusters topics, and generates an HTML report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content operators, tourism professionals, and researchers use this skill to monitor trending Douyin cultural tourism videos, compare hotspots, and produce reports for selected keywords and date ranges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The subscription feature can install persistent scheduled jobs and may store REDFOX_API_KEY in a macOS LaunchAgent. <br>
Mitigation: Prefer one-off report generation unless recurring reports are required; inspect LaunchAgents or crontab after enabling subscription and rotate the API key if it was written to disk. <br>
Risk: The security evidence reports unsafe shell-built crontab commands in subscription handling. <br>
Mitigation: Avoid --subscribe until the scheduling implementation is reviewed or fixed; use a chosen output directory for one-off reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/cultural-tourism-douyin-feed) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, HTML, Files] <br>
**Output Format:** [Markdown summary with category counts, terminal table output, and a generated HTML report file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY. Optional subscription mode creates recurring local report jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
