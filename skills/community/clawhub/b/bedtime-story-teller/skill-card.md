## Description:

睡前故事精靈，用溫暖聲音為 2-6 歲孩童講床邊故事。20+ 故事模板、免 API、支援 TTS 朗讀、故事收藏、睡前引導。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and caregivers use this agent to generate age-appropriate Traditional Chinese bedtime stories for children ages 2-6. It can provide story text, TTS-oriented reading prompts, favorites/history support, and bedtime routine guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented cron setup can create persistent daily execution.

Mitigation: Review the cron command before installing it, run it only when a persistent daily reminder is intended, and confirm how to inspect or remove the crontab entry.

Risk: Favorites, playback history, and bedtime routine settings are stored locally under ~/.qclaw/kids.

Mitigation: Avoid saving sensitive personal details in story inputs or routine settings, and review or delete the local JSON files when they are no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Traditional Chinese conversational text and Markdown, with optional JSON story records and shell commands when scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store favorites, playback history, and routine settings locally under ~/.qclaw/kids.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
