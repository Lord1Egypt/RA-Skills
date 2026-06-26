## Description: <br>
Capture audio from browser tabs, including meetings, videos, podcasts, courses, and webinars, and stream it to an AI agent or local transcription pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jarvis563](https://clawhub.ai/user/jarvis563) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to give an AI agent access to audio playing in a Chrome tab for meeting summaries, media notes, course notes, call analysis, or transcription workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records browser-tab audio and tab metadata, which can include sensitive meeting, call, course, or media content. <br>
Mitigation: Use it only when recording is intentional, obtain appropriate consent, and stop captures when finished. <br>
Risk: Audio is sent to a local transcription pipeline and relies on local Chrome debugging or extension capture controls. <br>
Mitigation: Keep the receiver and Chrome debugging interface bound to localhost, use a separate Chrome profile, and avoid leaving watch mode running. <br>


## Reference(s): <br>
- [Browser Audio Capture on ClawHub](https://clawhub.ai/jarvis563/browser-audio-capture) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill streams base64-encoded PCM16 audio chunks with tab metadata to a local HTTP receiver.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
