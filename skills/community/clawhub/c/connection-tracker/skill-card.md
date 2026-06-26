## Description: <br>
Tracks connection activity across human, resource, and memory interactions, scores connection value, and produces local Markdown dashboards and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to record and review connection-building activity across social, tool, resource, and memory workflows. It helps summarize activity into daily and weekly Markdown reports while keeping records local to the OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local activity logs may capture sensitive or private connection details if users enter them. <br>
Mitigation: Keep entries high level and avoid secrets, private conversation text, account details, API keys, or other sensitive content. <br>
Risk: Automatic triggers or cron jobs can create ongoing records beyond a one-time manual action. <br>
Mitigation: Enable scheduled reporting only when persistent tracking is intentional and periodically review the generated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/largetool/connection-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/largetool) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown dashboards and reports, with JSON summaries from CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local connection records under ~/.openclaw/workspace/connections when the handler is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
