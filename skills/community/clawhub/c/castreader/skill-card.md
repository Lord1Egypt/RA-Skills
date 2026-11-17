## Description:

Extracts web pages, text files, and synced book chapters, then converts the content into natural-sounding MP3 audio through CastReader/Kokoro TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinxu](https://clawhub.ai/user/vinxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn article URLs, extracted text, and synced WeChat Reading or Kindle book chapters into audio for listening workflows. It is useful when a chat agent needs to summarize, present choices, generate MP3 output, and send the resulting audio file back to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad network and local-library access with under-disclosed privacy and containment risks.

Mitigation: Review before installing, run in an isolated account or container, and keep dependencies updated.

Risk: URLs, article text, or book content may be sent to the configured CastReader API for speech generation.

Mitigation: Use only URLs and book content that are acceptable to send to CastReader's API, and avoid private, internal, or sensitive content.

Risk: URL extraction can access arbitrary web targets from the runtime environment.

Mitigation: Avoid internal or localhost URLs and do not run the skill in an environment with access to sensitive internal web services.

## Reference(s):

- [CastReader OpenClaw homepage](https://castreader.ai/openclaw)
- [CastReader API Reference](references/castreader-api.md)
- [Kokoro-82M model](https://huggingface.co/hexgrad/Kokoro-82M)
- [CastReader website](https://castreader.ai)
- [Chrome Extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb)
- [Edge Add-on](https://microsoftedge.microsoft.com/addons/detail/niidajfbelfcgnkmnpcmdlioclhljaaj)
- [ClawHub skill page](https://clawhub.ai/vinxu/skills/castreader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped script results; generated MP3 files are returned by file path for message delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and network access to the configured CastReader API endpoint; generated audio is written as MP3 files, commonly under /tmp.]

## Skill Version(s):

3.2.14 (source: server release evidence; artifact SKILL.md lists 3.2.13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
