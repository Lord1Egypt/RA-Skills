## Description:

Analyzes Douyin transcript text by cleaning obvious transcription errors, removing filler language, segmenting topics, extracting key points, and generating tags and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[don068589](https://clawhub.ai/user/don068589)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Whisper transcript text from Douyin videos into structured Markdown transcripts with corrected wording, topic sections, key points, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper script reads OpenClaw user configuration even though transcript analysis does not require it.

Mitigation: Review before installation and prefer a version that removes config access or restricts it to an explicit dedicated config file.

Risk: Transcript text is incorporated into generated LLM prompts and may contain untrusted or adversarial content.

Mitigation: Treat transcript input as untrusted and review generated prompts and summaries before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/don068589/skills/douyin-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Structured Markdown transcript with headings, key points, and tags; the optional helper script can emit JSON for full analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes user-provided transcript text and may generate an LLM prompt for deeper analysis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
