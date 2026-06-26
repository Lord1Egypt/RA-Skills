## Description: <br>
Provides a config-driven wrapper around gcalcli plus optional CalDAV integration to generate JSON reminder plans for scheduling one-shot OpenClaw reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adorostkar](https://clawhub.ai/user/adorostkar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to read configured Google Calendar and optional CalDAV calendars, produce a reminder plan, and wire one-shot OpenClaw reminders through their own scheduler or agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Calendar tools can access configured calendar data and may expose private event metadata in reminder plans. <br>
Mitigation: Keep calendar configuration private and install only when comfortable letting trusted local gcalcli, khal, and vdirsyncer binaries read the configured calendars. <br>
Risk: Configurable binary paths or scheduler wiring could run unintended local commands if pointed at untrusted executables or shell strings. <br>
Mitigation: Prefer absolute paths to trusted binaries and review cron or agent wiring before enabling automatic reminder creation. <br>
Risk: Automatic reminder scheduling can create duplicates or stale reminders if state handling is not wired correctly. <br>
Mitigation: Use the planner state file and review the generated JSON plan before enabling recurring unattended scheduling. <br>


## Reference(s): <br>
- [OpenClaw calendar example configuration](references/openclaw-calendar.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON reminder plan with Markdown setup guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Planner output includes reminder times, event metadata, skip counts, config path, and state path.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
