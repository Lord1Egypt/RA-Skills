## Description: <br>
Agentic Commerce News scans recent agentic commerce activity from X/Twitter, industry media, VC announcements, and conference coverage, then produces a structured news briefing about startups, products, funding rounds, partnerships, and influential opinions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuxinmaxen](https://clawhub.ai/user/xuxinmaxen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, founders, investors, and commerce teams use this skill to monitor recent agentic commerce market signals and receive concise, source-linked briefings. It can also help set up a recurring digest when the user's runtime supports scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring digest setup can create persistent or background jobs if the user approves scheduling. <br>
Mitigation: Review every scheduling request before approving it, especially OpenClaw cron or system crontab requests. <br>
Risk: News briefings can include stale or weakly sourced market claims if search results are not checked carefully. <br>
Mitigation: Require recent source links for included items and avoid padding quiet weeks with older news. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuxinmaxen/agentic-commerce-news) <br>
- [README](README.md) <br>
- [Evaluations](evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with source links, event cards, summary tables, trend takeaways, and optional scheduling commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on the past 7 days of activity and filters for credible endorsements or official announcements.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
