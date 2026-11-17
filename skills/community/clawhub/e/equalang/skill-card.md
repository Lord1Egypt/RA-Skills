## Description:

Helps agents translate documents, images, subtitles, and recordings, and transcribe audio or video through Equalang's cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[equalang-ai](https://clawhub.ai/user/equalang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to translate files or batches of text, preserve document layout where supported, and produce timed transcripts or translated subtitles from recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files, text, or public URLs are sent to Equalang's cloud for processing.

Mitigation: Share only material approved for cloud processing and check Equalang's privacy terms before using sensitive content.

Risk: Translations and transcriptions can spend Equalang credits.

Mitigation: Estimate costs and obtain user approval before starting paid jobs.

Risk: The API key is stored locally and an endpoint override can redirect requests.

Mitigation: Keep the key private and review any EQUALANG_BASE_URL override before use.

## Reference(s):

- [Equalang developer documentation](https://equalang.com/developers)
- [Equalang API reference](https://equalang.com/llms.txt)
- [Equalang Translation on ClawHub](https://clawhub.ai/equalang-ai/skills/equalang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-text instructions and JSON command results; translated or transcribed content is saved to files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports output paths and credits charged; file contents need not appear in the conversation.]

## Skill Version(s):

0.2.0 (source: ClawHub release and bundled script)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
