## Description: <br>
Monitors the Codex Reset Radar current.json feed for Codex usage reset-window changes and helps an OpenClaw cron send chat alerts only when state changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[advnljs](https://clawhub.ai/user/advnljs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Codex users use this skill to monitor reset-window status without repeatedly checking the dashboard by hand. It is intended for scheduled OpenClaw runs that fetch a public JSON feed, compare it with local cached state, and produce a concise change notice when an alert is warranted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts codex-reset-radar.pages.dev, so alert quality depends on that public feed being reachable and accurate. <br>
Mitigation: Review the external URL before scheduling the cron job and treat alerts as monitoring signals rather than authoritative quota guarantees. <br>
Risk: Frequent cron schedules can create unnecessary network traffic and chat noise when monitoring is not urgent. <br>
Mitigation: Choose a cron frequency appropriate for the user's needs and prefer the documented hourly waking-hours schedule for normal monitoring. <br>
Risk: The detector stores a small local cache in the OpenClaw workspace to compare state across runs. <br>
Mitigation: Run it from the intended workspace and review the cache path and permissions before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/advnljs/codex-reset-radar) <br>
- [Codex Reset Radar dashboard](https://codex-reset-radar.pages.dev/) <br>
- [Codex Reset Radar current JSON feed](https://codex-reset-radar.pages.dev/current.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON diff output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script emits has_changes status, event details, and current status; no-change runs are designed to stay silent.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
