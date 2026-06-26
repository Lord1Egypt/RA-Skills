## Description: <br>
Generate structured daily standup reports by analyzing git commits, pull request activity, issue trackers, and project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to prepare concise daily standup or async status reports from recent repository, pull request, issue, and branch activity. It is intended for individual or team status updates that summarize yesterday's work, today's plan, and current blockers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated standups may expose private development details such as branch names, uncommitted work, pull request links, issue details, reviewer names, or internal blockers. <br>
Mitigation: Review the generated report before sharing it and redact sensitive repository, issue, pull request, or personnel details as needed. <br>
Risk: The skill reads activity from local repositories and the currently authenticated GitHub CLI account. <br>
Mitigation: Run it only against intended repositories and specify the repo paths, author, time range, and team mode explicitly when scope matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/cm-daily-standup-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured standup report with yesterday, today, and blockers sections; optional Slack, verbose, or JSON formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commit counts, file-change scope, pull request links, issue links, reviewer names, branch names, and blocker details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
