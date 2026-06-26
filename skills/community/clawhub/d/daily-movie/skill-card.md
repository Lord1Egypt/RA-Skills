## Description: <br>
Daily Movie recommends one movie or TV series per day by genre, mood, or theme, with a synopsis, streaming platform, and audience ratings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when they want a daily or on-demand movie and TV recommendation with ratings, spoiler-free context, and platform guidance. Users can also enable optional morning and evening pushes on supported chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily push scheduling can create recurring messages on the selected channel if enabled unintentionally. <br>
Mitigation: Enable pushes only when scheduled reminders are desired, and use node scripts/push-toggle.js off <userId> to remove the morning and evening jobs. <br>
Risk: Recommendations can include time-sensitive ratings, releases, or streaming availability that may change by region. <br>
Mitigation: Ask the agent to verify current ratings and platform availability before relying on a recommendation. <br>


## Reference(s): <br>
- [Daily Movie on ClawHub](https://clawhub.ai/jiajiaoy/daily-movie) <br>
- [Publisher profile](https://clawhub.ai/user/jiajiaoy) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text recommendations with optional shell command snippets for push scheduling.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese recommendations; optional daily push setup supports telegram, feishu, slack, and discord.] <br>

## Skill Version(s): <br>
1.0.4 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
