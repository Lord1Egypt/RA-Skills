## Description:

Query China Railway 12306 for train schedules, remaining tickets, and station information for rail travel within China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirorab](https://clawhub.ai/user/kirorab)

### License/Terms of Use:


## Use Case:

Travelers, support teams, and agent developers use this skill to check China Railway train schedules, remaining ticket availability, station resolution, and seat-specific filters from 12306 data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README install command does not pin a package or revision.

Mitigation: Install only from a trusted source and reviewed revision, and pin the installer or source version where possible.

Risk: The skill contacts China Railway 12306 web endpoints during ticket and station lookups.

Mitigation: Use it only in environments where outbound access to those endpoints is expected and acceptable.

Risk: Default HTML mode writes output files and station lookup caches local station data for up to 7 days.

Mitigation: Review output paths, manage generated files, and clear the station cache when stale local data is undesirable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirorab/skills/12306)
- [Publisher profile](https://clawhub.ai/user/kirorab)
- [China Railway 12306 ticket query](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc)
- [China Railway 12306 station data](https://www.12306.cn/index/)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables, JSON, HTML files, and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default ticket-query mode writes an HTML file; markdown and JSON modes write to stdout.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
