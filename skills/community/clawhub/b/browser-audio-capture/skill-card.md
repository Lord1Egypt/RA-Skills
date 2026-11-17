## Description:

Capture audio from any browser tab, including meetings, YouTube, podcasts, courses, and webinars, and stream it to an AI agent without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarvis563](https://clawhub.ai/user/jarvis563)

### License/Terms of Use:


## Use Case:

Developers and AI-agent builders use this skill to capture audio from authorized browser tabs and route PCM16 chunks to local transcription or agent pipelines for summaries, notes, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-tab audio capture can include private or sensitive conversations.

Mitigation: Use the skill only with browser profiles, meetings, and tabs that the operator is authorized to capture.

Risk: Audio chunks include tab URL and title metadata sent every few seconds to the receiver.

Mitigation: Keep the receiver bound to localhost and avoid opening sensitive tabs in a CDP-enabled browser while capture is active.

Risk: Continuous watch mode can start repeated or ongoing capture when matching browser tabs are detected.

Mitigation: Disable or avoid watch mode unless continuous auto-capture is explicitly intended and monitored.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jarvis563/skills/browser-audio-capture)
- [Extension README](artifact/scripts/extension/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, code references, configuration details, and JSON audio payload examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When run, the skill streams base64 PCM16 audio chunks with session, tab URL, and tab title metadata to a localhost receiver.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
