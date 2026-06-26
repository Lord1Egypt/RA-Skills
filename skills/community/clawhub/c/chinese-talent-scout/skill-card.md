## Description: <br>
Discover, score, and monitor Chinese GitHub developers with GitHub signals, rule-based processing, optional OpenClaw AI evaluation, shortlist queries, cron management, workspace export, and controlled config-change requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huandu](https://clawhub.ai/user/huandu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and recruiting or talent intelligence operators use this skill to collect public GitHub signals, process candidate records, evaluate fit, query shortlists, and manage scheduled talent-scouting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill profiles a nationality-linked developer group using public GitHub and ranking signals. <br>
Mitigation: Review the intended use, data sources, scoring thresholds, and evaluation outputs before deployment; use the results as decision-support rather than sole decision criteria. <br>
Risk: The skill can send OpenClaw messages and manage OpenClaw cron jobs. <br>
Mitigation: Use least-privileged GitHub and OpenClaw accounts, review channel targets, inspect config-request payloads with dry runs, and confirm cron definitions before syncing or enabling jobs. <br>
Risk: Workspace exports may include local configuration from workspace-data/talents.yaml. <br>
Mitigation: Review generated ZIP contents before sharing and remove local-only routing or configuration values that should not leave the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huandu/chinese-talent-scout) <br>
- [Publisher profile](https://clawhub.ai/user/huandu) <br>
- [Repository metadata](https://github.com/presence-io/talent-scout) <br>
- [Architecture](references/architecture.md) <br>
- [Credential Model](references/credentials.md) <br>
- [Security Notes](references/security.md) <br>
- [Data Sources](references/data-sources.md) <br>
- [Identity Detection](references/identity.md) <br>
- [Evaluation Model](references/evaluation.md) <br>
- [China Ranking](https://china-ranking.aolifu.org) <br>
- [GitHubRank](https://githubrank.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text, local workspace files, ZIP archive paths, and optional OpenClaw-delivered messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on local GitHub CLI, OpenClaw CLI, workspace configuration, and enabled cron jobs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
