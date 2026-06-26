## Description: <br>
Daily Self Improvement automatically collects an agent's daily failures, corrections, and notes, analyzes recurring problems, searches ClawHub for improvement suggestions, writes a Markdown report, and can send it to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to schedule or manually run a daily reflection workflow that summarizes recent issues, identifies repeated failure patterns, suggests relevant ClawHub skills, and records a daily improvement report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a hardcoded local gateway token and prefilled Discord delivery from local notes and logs. <br>
Mitigation: Remove and rotate the hardcoded token, replace the Discord channel with one controlled by the deploying user, and disable Discord delivery until the exact payload has been reviewed. <br>
Risk: Scheduled runs can read local failure logs, corrections, and daily notes and write daily reports. <br>
Mitigation: Review configured data sources and report paths before enabling cron, and run manually first to confirm the collected content is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/daily-self-improvement) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>
- [Configuration example](config/settings.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report, console text, and optional Discord message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; optional ClawHub search and Discord delivery are controlled by configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
