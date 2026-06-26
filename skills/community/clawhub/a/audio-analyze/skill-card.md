## Description: <br>
High-performance audio transcription and analysis using Gemini 3.1 Pro. Powered by Evolink.ai <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to transcribe meeting recordings, long-form audio, and audio or video files, then summarize or analyze the resulting content through Evolink's Gemini-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The transcription helper uploads user media to a third-party API for processing. <br>
Mitigation: Use it only with media you are allowed to send to Evolink or Gemini processing, and avoid confidential or regulated recordings unless that use is approved. <br>
Risk: The transcription helper can be abused through crafted filenames or option values. <br>
Mitigation: Run it only on trusted local files and arguments until the helper is patched to pass inputs safely. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evolinkai/audio-analyze) <br>
- [Evolink API reference](https://docs.evolink.ai/en/api-manual/language-series/gemini-3.1-pro-preview-customtools/openai-sdk/openai-sdk-quickstart?utm_source=github&utm_medium=skill&utm_campaign=audio-analyze) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript or analysis returned by a shell command, with setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY, can use EVOLINK_MODEL, and sends the selected media file to api.evolink.ai.] <br>

## Skill Version(s): <br>
1.0.7 (source: release evidence; artifact _meta.json lists 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
