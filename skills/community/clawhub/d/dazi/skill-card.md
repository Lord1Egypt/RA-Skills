## Description: <br>
AI dating assistant. Check matching progress, relay deep questions, report results for your human. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thesamething](https://clawhub.ai/user/thesamething) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using AILove and their agents use this skill to check matchmaking progress, relay pending deep questions, submit the human's own answers, and summarize match updates from the AILove API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a revocable AILove Agent Key and may store it locally. <br>
Mitigation: Prefer a platform secret store or OS keychain; if using ~/.openclaw/.env, restrict file permissions and never send the key outside https://heerweiyi.cc/api/v1/agent/*. <br>
Risk: Scheduled jobs can send private dating updates to external or group channels. <br>
Mitigation: Enable cron delivery only to a private destination controlled by the user, and avoid shared channels unless the user accepts that exposure. <br>
Risk: The security verdict is suspicious because the skill combines sensitive local credentials with recurring delivery of dating updates. <br>
Mitigation: Install only after reviewing the security summary and confirming the user is comfortable with the credential and delivery model. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thesamething/dazi) <br>
- [Publisher profile](https://clawhub.ai/user/thesamething) <br>
- [AILove homepage](https://heerweiyi.cc) <br>
- [AILove skill source](https://heerweiyi.cc/skill.md) <br>
- [AILove API base](https://heerweiyi.cc/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with API request examples and OpenClaw cron commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scheduled update summaries, question relays, and configuration snippets for storing an AILove Agent Key.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
