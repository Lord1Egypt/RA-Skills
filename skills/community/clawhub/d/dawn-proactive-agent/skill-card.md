## Description: <br>
Dawn Proactive Agent helps an OpenClaw agent move from passive responses to scheduled proactive work by combining Gateway Cron triggers, decision follow-up tracking, and a proactive engine script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure scheduled proactive agent checks, decision backtracking, workspace memory logging, and optional Feishu notifications. It is suited for workflows where cron-triggered agent reminders and follow-up records need to run without waiting for a user prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled cron tasks may notify the wrong Feishu recipient or channel if copied without editing routing values. <br>
Mitigation: Confirm each cron schedule, Feishu recipient or channel, timezone, and session target before installing; use a test recipient first. <br>
Risk: The helper writes local session-state, decision-registry, and proactive-log files under the configured OpenClaw workspace. <br>
Mitigation: Run it only in a workspace where OPENCLAW_WORKSPACE and the memory files are under the user's control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/dawn-proactive-agent) <br>
- [Publisher profile](https://clawhub.ai/user/chen6896qqwee) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact dawn_proactive.py](artifact/dawn_proactive.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown documentation with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace state, decision registry, and proactive log files when the Python helper is installed and run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
