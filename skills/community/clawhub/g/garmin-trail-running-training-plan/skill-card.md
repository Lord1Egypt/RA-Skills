## Description: <br>
Creates trail race roadmaps and dynamic training plans from Garmin activity data and race GPX tracks, with optional calendar synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtroymatt](https://clawhub.ai/user/mtroymatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External runners and training-plan builders use this skill to analyze Garmin activity history and race GPX files, then produce trail-race pacing guidance, taper plans, calendar events, and optional social sharing copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Garmin credentials, sensitive health history, and stored session tokens. <br>
Mitigation: Install only when that access is acceptable, avoid putting a Garmin password in config.json, prefer a temporary user-controlled login method, scope wellness/profile queries to what is needed, and delete stored tokens under ~/.clawdbot/garmin when finished. <br>
Risk: The skill can generate calendar synchronization scripts that write to macOS/iOS calendars. <br>
Mitigation: Review any generated calendar script before running it and confirm the target calendar, event contents, and date range. <br>


## Reference(s): <br>
- [Garmin Trail-Running Roadmap & Training Plan Guide](references/roadmap_standard.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/mtroymatt/garmin-trail-running-training-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated HTML, JSON, Python, AppleScript, and shell command snippets where needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce calendar synchronization scripts and Garmin data queries that require local review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
