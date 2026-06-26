## Description: <br>
Daily Dev Agentic helps an agent maintain a daily.dev learning feed, run recurring learning loops, write local learning notes, and share relevant findings with its owner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[idoshamun](https://clawhub.ai/user/idoshamun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agent operators, and external users use this skill to configure an agent-owned daily.dev feed, fetch and research relevant posts, store markdown learning notes, and summarize findings for the owner. It is suited to ongoing technical learning workflows that rely on a daily.dev Plus API token and local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants recurring autonomous authority through scheduled learning loops and feed adjustments. <br>
Mitigation: Confirm the intended schedule, review cron entries after setup, and require approval before changing feed tags or learning goals in sensitive environments. <br>
Risk: The skill uses DAILY_DEV_TOKEN to access the daily.dev API. <br>
Mitigation: Store the token only in the environment, limit use to api.daily.dev as the artifact instructs, rotate it if exposed, and remove it from sessions that should not access daily.dev. <br>
Risk: The skill writes local memory files that may contain owner context, source URLs, and synthesized findings. <br>
Mitigation: Confirm the memory directory location before use, review notes for sensitive content, and define retention or pruning expectations. <br>
Risk: The skill can fetch third-party articles, search the web, and proactively share findings without enough checkpoints. <br>
Mitigation: Set clear boundaries for proactive sharing, require review before acting on findings, and treat external article content as untrusted input. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/idoshamun/daily-dev-agentic) <br>
- [Publisher profile](https://clawhub.ai/user/idoshamun) <br>
- [daily.dev Plus](https://app.daily.dev/plus) <br>
- [daily.dev API token settings](https://app.daily.dev/settings/api) <br>
- [daily.dev public API base](https://api.daily.dev/public/v1) <br>
- [Learning Loop - Detailed Flow](references/learning-loop.md) <br>
- [Memory Format for Agentic Learning](references/memory-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown notes and configuration files with shell/API command examples and brief text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and update local memory files, call the daily.dev public API with DAILY_DEV_TOKEN, fetch third-party articles, search for context, schedule cron jobs, and proactively share findings.] <br>

## Skill Version(s): <br>
0.5.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
