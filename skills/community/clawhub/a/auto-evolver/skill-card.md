## Description: <br>
Runs recurring inner-loop self-optimization and outer-loop value-connection workflows that monitor token use, generate repair tasks, publish or interact on platforms, and log outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run scheduled agent maintenance and outreach workflows that inspect recurring failures, generate repair or research tasks, track token budgets, perform approved publishing or connection actions, and maintain local status logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automation may publish, comment, or send private messages through user accounts without sufficiently explicit per-action approval. <br>
Mitigation: Keep dry-run review enabled by default, require explicit approval for each platform and outreach batch, and disable scheduled outer-loop activity until approvals are documented. <br>
Risk: Connection and evolution logs may retain details about outreach targets, engagement, platform activity, and local operational state. <br>
Mitigation: Define retention and redaction rules before use, avoid logging sensitive personal data, and periodically remove local records that are no longer needed. <br>
Risk: Cron-driven loops and platform tools can create repeated account activity that exceeds intended scope or rate limits. <br>
Mitigation: Set strict rate limits, monitor scheduled jobs, pause automation when token or engagement thresholds are exceeded, and require manual review before enabling optional publishing or messaging tools. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/largetool/auto-evolver) <br>
- [Publisher Profile](https://clawhub.ai/user/largetool) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [State Snapshot](artifact/STATE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cron commands, workflow checklists, task records, and local status or connection log entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown logs, pending tasks, state files, and alert records during recurring inner-loop and outer-loop runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact text also refers to v1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
