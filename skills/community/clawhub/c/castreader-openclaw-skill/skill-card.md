## Description: <br>
Read any web page aloud with natural AI voices by extracting article text from a URL and converting it to MP3 audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinxu](https://clawhub.ai/user/vinxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn web articles, documents, and supported reading surfaces into spoken audio. It is useful when a user sends a URL and wants either the full extracted content or a concise summary delivered as audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted webpage, document, chat, or ebook text may be sent to CastReader's remote TTS service and through a messaging channel. <br>
Mitigation: Use the skill only with content the user is authorized to process and share; avoid private, internal, legal, medical, financial, copyrighted, or logged-in pages unless policy explicitly allows it. <br>
Risk: The default CastReader API endpoint uses an insecure connection. <br>
Mitigation: Configure a trusted HTTPS CastReader API endpoint before processing sensitive or business content. <br>


## Reference(s): <br>
- [CastReader OpenClaw homepage](https://castreader.ai/openclaw) <br>
- [Castreader API Reference](references/castreader-api.md) <br>
- [CastReader Chrome Extension](https://chromewebstore.google.com/detail/castreader-tts-reader/foammmkhpbeladledijkdljlechlclpb) <br>
- [ClawHub skill page](https://clawhub.ai/vinxu/castreader-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Agent guidance with inline shell commands; scripts return JSON metadata and write MP3 audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send generated audio through a messaging channel after the user chooses full article or summary audio.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release metadata; artifact frontmatter lists 2.1.0 and package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
