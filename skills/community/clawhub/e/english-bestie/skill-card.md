## Description: <br>
A friendly AI English teacher that runs daily lessons via Telegram voice messages and teaches grammar, vocabulary, and conversation with a casual buddy style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Haiku54](https://clawhub.ai/user/Haiku54) <br>

### License/Terms of Use: <br>


## Use Case: <br>
English learners and agent operators use this skill to run proactive Telegram-based English practice, including onboarding, level assessment, daily lessons, correction cards, spaced vocabulary review, and weekly progress reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores learner profile, mistake, progress, and conversation-history data in local tracking files. <br>
Mitigation: Deploy only with a consenting student and define how tracking files will be reviewed, retained, or deleted. <br>
Risk: The skill creates ongoing automated Telegram outreach and scheduled follow-ups. <br>
Mitigation: Use a dedicated OpenClaw workspace and Telegram bot, then review or reduce cron jobs after setup. <br>
Risk: Telegram bot setup requires a bot token and allowed user configuration. <br>
Mitigation: Protect the Telegram token, restrict allowed users, and review openclaw.json after installation. <br>


## Reference(s): <br>
- [English Bestie ClawHub Release](https://clawhub.ai/Haiku54/english-bestie) <br>
- [OpenClaw](https://openclaw.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram voice/text tutoring messages, Markdown correction cards, JSON tracking updates, and inline shell commands for scheduling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, a dedicated Telegram bot, a student Telegram user ID, and OPENAI_API_KEY for text-to-speech.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
