## Description: <br>
Extracts web page or synced book text and converts it to natural AI speech with Kokoro TTS, producing MP3 audio for delivery by an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinxu](https://clawhub.ai/user/vinxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn article URLs, text files, or synced WeChat Reading and Kindle book chapters into MP3 narration. It supports extraction-first review flows before generating full-article, summary, paragraph, chapter, or full-book audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Article, book, or text-file content may be sent to the default CastReader TTS endpoint or a configured endpoint. <br>
Mitigation: Use the skill only with content approved for that endpoint, avoid confidential or copyrighted material unless permitted, and configure CASTREADER_API_URL deliberately. <br>
Risk: Generated audio and cached extraction data are written to local temporary paths. <br>
Mitigation: Clear /tmp/castreader-* and /tmp/castreader-book-* after sensitive use and avoid shared temporary directories for private content. <br>
Risk: The skill reads local synced book content from ~/castreader-library/books/ when book mode is used. <br>
Mitigation: List books first, use exact server-returned book IDs, and limit use to library content the user is authorized to process. <br>
Risk: The security verdict is suspicious because the skill has weak scoping around URLs, local library access, and command templates. <br>
Mitigation: Review commands before execution, prefer trusted URLs, and avoid expanding the provided command templates beyond documented flows. <br>


## Reference(s): <br>
- [CastReader API Reference](references/castreader-api.md) <br>
- [CastReader OpenClaw Homepage](https://castreader.ai/openclaw) <br>
- [CastReader Website](https://castreader.ai) <br>
- [Kokoro-82M Model Card](https://huggingface.co/hexgrad/Kokoro-82M) <br>
- [ClawHub Release Page](https://clawhub.ai/vinxu/castreader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON command output, and MP3 audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is written to local MP3 files, typically under /tmp/castreader-* or next to the source text file.] <br>

## Skill Version(s): <br>
3.2.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
