## Description:

CastReader extracts readable text from web pages and converts full articles or summaries into MP3 audio with natural TTS voices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinxu](https://clawhub.ai/user/vinxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn article URLs into spoken audio, with a choice between full-article playback and summary-only playback. Developers can also use its Node.js scripts to extract web page text or generate MP3 audio from text files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted page text and generated summaries may be sent to a remote TTS service and delivered through Telegram.

Mitigation: Use only public, non-sensitive URLs unless the deployment has reviewed and approved the remote service and messaging path.

Risk: The skill processes arbitrary URLs and page content.

Mitigation: Restrict use to trusted URLs and avoid private, authenticated, paywalled, business, chat, document, and ebook content.

Risk: Security evidence flags review-level risks around URL handling, Chromium sandboxing, temporary files, and shell interpolation for summaries.

Mitigation: Review the implementation before deployment and require HTTPS, URL validation, Chromium sandboxing, safe temporary-file handling, and shell-safe summary handling.

## Reference(s):

- [CastReader OpenClaw homepage](https://castreader.ai/openclaw)
- [Castreader API Reference](references/castreader-api.md)
- [CastReader Chrome extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb)
- [CastReader Edge add-on](https://microsoftedge.microsoft.com/addons/detail/niidajfbelfcgnkmnpcmdlioclhljaaj)
- [ClawHub skill page](https://clawhub.ai/vinxu/skills/castreader-openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output; generated audio is written as MP3 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and sends extracted text to a remote TTS service when generating audio.]

## Skill Version(s):

2.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
