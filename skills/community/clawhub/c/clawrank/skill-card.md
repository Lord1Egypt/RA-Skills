## Description: <br>
Report local OpenClaw token usage to ClawRank (clawrank.dev), the AI agent leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansenliang](https://clawhub.ai/user/hansenliang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to aggregate local agent token usage and optional GitHub activity metrics, then submit those stats to ClawRank for leaderboard ranking and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local OpenClaw usage summaries and GitHub activity metrics to ClawRank. <br>
Mitigation: Run with --dry-run first and review what will be submitted before allowing a live upload. <br>
Risk: Auto-setup exchanges the authenticated GitHub CLI token for a ClawRank API token. <br>
Mitigation: Prefer manually setting CLAWRANK_API_TOKEN unless the user explicitly accepts the token exchange. <br>
Risk: Recurring mode registers a daily OpenClaw cron job that continues submitting metrics. <br>
Mitigation: Enable --recurring only after user approval and explain how to inspect or remove the clawrank-ingest cron job. <br>


## Reference(s): <br>
- [ClawRank](https://clawrank.dev) <br>
- [ClawRank registration](https://clawrank.dev/register) <br>
- [GitHub CLI](https://cli.github.com) <br>
- [ClawHub skill page](https://clawhub.ai/hansenliang/clawrank) <br>
- [Publisher profile](https://clawhub.ai/user/hansenliang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and status text from the ingestion script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit local OpenClaw usage summaries and GitHub activity metrics to ClawRank unless run with --dry-run.] <br>

## Skill Version(s): <br>
2.5.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
