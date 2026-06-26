## Description: <br>
Generate daily internship logbook drafts and weekly internship reports from GitHub and GitLab commit activity, with Indonesian MIS-friendly summaries, Telegram approval requests, and OpenClaw cron delivery for daily and weekly reporting flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozaldy](https://clawhub.ai/user/mozaldy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering interns, and supervisors use this skill to turn same-day GitHub and GitLab commit activity into Indonesian internship logbook drafts, weekly reports, and approval-ready status messages. It supports repo-aware activity summaries and approval-before-submit workflows for MIS logbook reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install persistent scheduled reporting automation. <br>
Mitigation: Review generated cron jobs before enabling them and disable jobs that are no longer needed. <br>
Risk: MIS submission helpers can change account data if run after approval. <br>
Mitigation: Do not run submission helpers until the pending draft and the related MIS submission behavior have been reviewed and explicitly approved. <br>
Risk: Commit-derived summaries and local configuration may contain sensitive project or account details. <br>
Mitigation: Keep the local .env file private, review Telegram-bound messages before sending, and back up HEARTBEAT.md before enabling recurring flows. <br>


## Reference(s): <br>
- [Indonesian Logbook Formatting Guide](references/format-guide.md) <br>
- [Repository Context Overrides](references/repo-contexts.json) <br>
- [Daily Commit Logbook release page](https://clawhub.ai/mozaldy/daily-commit-logbook) <br>
- [MIS portal referenced by the skill](https://online.mis.pens.ac.id/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, Indonesian text snippets, Telegram-ready messages, shell commands, and local configuration entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes daily and weekly report artifacts, pending MIS drafts, and optional recurring OpenClaw cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
