## Description: <br>
Sync one or more source Google calendars into private Busy hold events in one or more target calendars using gog. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tdewitt](https://clawhub.ai/user/tdewitt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and calendar operators use this skill to configure an agent to mirror source Google Calendar events into private Busy holds on target calendars for double-booking prevention, backfill, drift reconcile, and scheduled sync. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, and delete Busy holds on configured target Google calendars. <br>
Mitigation: Start with dry-run on test calendars, verify mappings, and keep maxChangesPerRun conservative before enabling live automation. <br>
Risk: Calendar metadata may include source account, calendar, event ID, timing, and title information in managed hold descriptions. <br>
Mitigation: Avoid shared target calendars when source titles or account identifiers are sensitive. <br>
Risk: Custom gog command templates can change how calendar commands are executed. <br>
Mitigation: Keep custom commands disabled unless the configuration is fully trusted and audited. <br>
Risk: Cron or watch mode can continue applying calendar changes after initial setup. <br>
Mitigation: Enable scheduled operation only after confirming mappings and documenting how to disable the scheduled job. <br>


## Reference(s): <br>
- [Calendar Hold Sync on ClawHub](https://clawhub.ai/tdewitt/calendar-hold-sync) <br>
- [gog CLI homepage](https://gogcli.sh/) <br>
- [gog CLI source](https://github.com/steipete/gogcli) <br>
- [gog skill on ClawHub](https://clawhub.ai/steipete/gog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing instructions for config-driven calendar reconciliation, backfill, status checks, cron installation, and polling watch mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
