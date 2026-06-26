## Description: <br>
Proactive agile metrics and team health analysis for Trello and Jira boards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OliverMonneke](https://clawhub.ai/user/OliverMonneke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Scrum Masters, Agile Coaches, and delivery teams use this skill to inspect Trello or Jira board health, compute agile flow metrics, identify bottlenecks, and prepare sprint health summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use Trello or Jira credentials to read board or project data. <br>
Mitigation: Use least-privilege tokens and confirm the exact board or project before running analysis. <br>
Risk: Agile reports may expose team workflow, blockers, or project status to unintended recipients. <br>
Mitigation: Review report destination channels before sharing output and avoid broad channels unless explicitly intended. <br>
Risk: Weekly cron scheduling can create recurring automated summaries. <br>
Mitigation: Enable recurring reports only when the user intentionally wants ongoing automated delivery. <br>


## Reference(s): <br>
- [Jira Cloud API Quick Reference](references/jira-api.md) <br>
- [Agile Metrics Reference](references/metrics.md) <br>
- [Trello API Quick Reference](references/trello-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with metric summaries, coaching suggestions, optional CSV exports, and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Trello or Jira board data and credential files when the user authorizes access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
