## Description: <br>
Daily Rhythm automates daily planning and reflection with morning briefs, wind-down prompts, sleep nudges, and weekly reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnthonyFrancis](https://clawhub.ai/user/AnthonyFrancis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, founders, and professionals use this skill to set up recurring personal planning workflows, morning brief generation, task synchronization, optional ARR tracking, wind-down prompts, and weekly reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Google Tasks and optional Stripe credentials, which can expose personal task data and business subscription data if stored or shared carelessly. <br>
Mitigation: Use restricted Google and Stripe credentials, keep token files and .env.stripe out of source control, and enable only the integrations needed. <br>
Risk: Some scripts and cron examples include hard-coded local paths under /Users/tom, which can fail or write data to unexpected locations in another workspace. <br>
Mitigation: Edit scripts and cron entries to use the target workspace paths before installation or scheduled execution. <br>
Risk: Recurring cron automation can run API syncs and planning prompts without further review once installed. <br>
Mitigation: Install only cron jobs the user understands, review their schedules and commands, and keep removal steps available. <br>


## Reference(s): <br>
- [Daily Rhythm Configuration Guide](references/CONFIGURATION.md) <br>
- [Daily Rhythm ClawHub Release](https://clawhub.ai/AnthonyFrancis/daily-rhythm) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Stripe Dashboard API Keys](https://dashboard.stripe.com/apikeys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, cron examples, and local JSON state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local planning artifacts and optional synced task and ARR data when configured with user credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
