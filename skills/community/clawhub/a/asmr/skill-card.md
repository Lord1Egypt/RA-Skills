## Description:

Provides ASMR music recommendations and playback links for sleep aid, heart rate regulation, focus enhancement, stress relief, relaxation, meditation, and optional daily listening reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashterry](https://clawhub.ai/user/ashterry)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to receive ASMR audio recommendations, playback links, and usage suggestions for sleep, relaxation, focus, stress relief, anxiety support, meditation, and nightly routine reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be invoked for broad sleep, relaxation, anxiety, or focus requests and recommend external audio links.

Mitigation: Review the recommendation and verify third-party playback links are appropriate for the user's language, region, and device before relying on them.

Risk: Daily reminder setup can create recurring notifications.

Mitigation: Enable reminders only when the user explicitly wants a recurring ASMR notification, and provide clear disable instructions.

Risk: ASMR recommendations are auxiliary wellness support and may be inappropriate during driving, machinery operation, hearing discomfort, or serious sleep or anxiety concerns.

Mitigation: Advise low volume, stop use if discomfort occurs, avoid use during safety-critical activities, and consult professionals for serious sleep or anxiety issues.

## Reference(s):

- [ASMR music reference library](references/asmr_music.md)
- [ClawHub skill page](https://clawhub.ai/ashterry/skills/asmr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with playback links, usage suggestions, and optional reminder commands or configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include third-party playback links and optional daily reminder setup instructions.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
