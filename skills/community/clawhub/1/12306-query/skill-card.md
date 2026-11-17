## Description:

Query China Railway 12306 for train schedules, remaining tickets, and station info.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangsaizz](https://clawhub.ai/user/zhangsaizz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to check China Railway 12306 train schedules, ticket availability, station matches, and filtered train options for travel within China.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The README installation command is unpinned, so users could install a different release than the reviewed artifact.

Mitigation: Install a pinned or verified skill version before using it in production workflows.

Risk: The skill contacts the live 12306 service and returns travel availability that can change quickly.

Mitigation: Treat results as current lookup data and verify critical itinerary or purchase decisions through the official 12306 flow.

Risk: HTML output can write to a caller-provided path and may overwrite an existing file.

Mitigation: Use deliberate output paths, preferably under a temporary or dedicated reports directory.

Risk: Station data is cached locally for 7 days.

Mitigation: Review or clear the local cache when workspace retention or data freshness requirements matter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangsaizz/skills/12306-query)
- [China Railway 12306 left-ticket query](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc)
- [China Railway 12306 station data](https://www.12306.cn/index/)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML files, shell commands, guidance]

**Output Format:** [Markdown tables, JSON, generated HTML reports, and stdout text from Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default HTML mode writes a local report file; station data is cached locally for 7 days.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
