## Description:

Query China Railway 12306 for train schedules, remaining tickets, and station information for rail travel within China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danihe001](https://clawhub.ai/user/danihe001)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check China Railway train schedules, remaining ticket availability, station matches, and filtered seat options before travel planning.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill contacts China Railway 12306 and writes station cache or report files locally.

Mitigation: Run it only for intended travel queries and treat generated cache and report files as local records of those queries.

Risk: Generated HTML reports may contain travel query details and have weaker hardening than plain text output.

Mitigation: Prefer Markdown or JSON output for lower-risk display, and review or delete local HTML reports when they are no longer needed.

Risk: Installing or running an unpinned Node-based skill can make later dependency or source changes harder to audit.

Mitigation: Prefer pinned installation sources when available and review the release evidence before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danihe001/skills/12306-backup)
- [Publisher profile](https://clawhub.ai/user/danihe001)
- [China Railway 12306](https://www.12306.cn/index/)
- [12306 left-ticket query entry point](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, guidance]

**Output Format:** [Markdown tables, JSON arrays, or local HTML report file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local HTML reports and a station cache under the skill data directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
