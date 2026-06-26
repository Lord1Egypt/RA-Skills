## Description: <br>
Query China Railway 12306 for train schedules, remaining tickets, and station info. Use when user asks about train/高铁/火车 tickets, schedules, or availability within China. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirorab](https://clawhub.ai/user/kirorab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up China Railway 12306 train schedules, ticket availability, station details, and filtered route options for travel within China. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Train searches contact official 12306 websites and send the queried stations and travel date to those services. <br>
Mitigation: Use the skill only when that network disclosure is acceptable for the requested travel query. <br>
Risk: The default HTML mode writes output files, and station metadata is cached locally. <br>
Mitigation: Use an explicit output path only when intended, and review or remove generated output and cached station data when no longer needed. <br>
Risk: Server-resolved GitHub import provenance is unavailable for this release. <br>
Mitigation: Review future updates and publisher release notes before installing or upgrading. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirorab/12306) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [China Railway 12306 Ticket Query](https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc) <br>
- [China Railway 12306 Station Data](https://www.12306.cn/index/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML files, Shell commands] <br>
**Output Format:** [Markdown tables, JSON stdout, station lookup text, or generated HTML files depending on options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; defaults to writing HTML output and caches station metadata locally for 7 days.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
