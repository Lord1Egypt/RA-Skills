## Description:

Discovers, scores, and monitors Chinese GitHub developers using GitHub signals, rule-based processing, optional OpenClaw AI evaluation, shortlist queries, cron management, workspace export, and controlled configuration-change requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huandu](https://clawhub.ai/user/huandu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect GitHub signals, process candidate records, evaluate talent fit, query shortlists, manage scheduled runs, and export local workspace results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill profiles and scores Chinese GitHub users at scale and may process identity or location signals.

Mitigation: Install only for a legitimate, reviewed recruiting or analysis need; use a test workspace first and review candidate exports before sharing them.

Risk: Optional AI evaluation and channel delivery can share candidate data with external OpenClaw agents or configured channels.

Mitigation: Prefer --skip-ai when external AI processing is unnecessary, keep provider and channel credentials outside the skill, and dry-run config messages before enabling delivery.

Risk: Recurring cron jobs can repeatedly collect and evaluate public GitHub data.

Mitigation: Do not enable cron until collection scope, schedules, credentials, and review processes have been approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huandu/skills/chinese-talent-scout)
- [Repository](https://github.com/presence-io/talent-scout)
- [Architecture](references/architecture.md)
- [Credential Model](references/credentials.md)
- [Data Sources](references/data-sources.md)
- [Identity Detection](references/identity.md)
- [Evaluation Model](references/evaluation.md)
- [Security Notes](references/security.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text or Markdown-style command output with local file paths and workspace artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace-data outputs and local ZIP exports; AI evaluation and channel delivery depend on external CLI configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
