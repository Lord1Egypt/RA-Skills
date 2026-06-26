## Description: <br>
Automated daily planning and reflection system with morning briefs, wind-down prompts, sleep nudges, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, professionals, and founders use this skill to configure recurring daily planning, task syncing, morning briefings, evening reflection prompts, sleep nudges, and weekly reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional business metrics syncing uses broad subscription access and can store customer identifiers locally. <br>
Mitigation: Enable ARR tracking only when needed, do not set SKILLBOSS_API_KEY otherwise, and protect or periodically delete local memory files containing ARR and customer data. <br>
Risk: The skill requires sensitive credentials such as Google OAuth files, API keys, and optional calendar URLs. <br>
Mitigation: Keep credentials and ICS URLs out of shared folders and repositories, use least-privilege access where possible, and review scheduled jobs before enabling them. <br>
Risk: Cron jobs can run scripts repeatedly and persist personal planning, task, and reflection data. <br>
Mitigation: Review cron entries before installation, scope paths to the intended workspace, and monitor generated memory files for sensitive content. <br>


## Reference(s): <br>
- [Daily Rhythm Configuration Guide](references/CONFIGURATION.md) <br>
- [Daily Rhythm ClawHub Release](https://clawhub.ai/alvisdunlop/abe-daily-rhythm) <br>
- [Publisher Profile](https://clawhub.ai/user/alvisdunlop) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, cron examples, and generated daily or weekly planning prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files containing tasks, reflections, calendar-derived data, ARR, and customer identifiers when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
