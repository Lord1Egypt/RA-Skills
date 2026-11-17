## Description:

AI Stem Splitter guides agents through splitting audio into vocals, drums, bass, guitar, piano, and other stems using the hosted AI Stem Splitter API, SDKs, or web app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeugar](https://clawhub.ai/user/codeugar)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and music production workflows use this skill to separate local audio files or supported audio URLs into named stems, create karaoke or instrumental versions, extract acapellas, and integrate with the AI Stem Splitter API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio files or source URLs are sent to a hosted third-party service for stem separation.

Mitigation: Use the skill only for audio the user is comfortable uploading to AI Stem Splitter, and avoid sensitive or unauthorized source material.

Risk: API keys may expose paid credits or service access if printed, stored, or used from browser code.

Mitigation: Keep AISTEMSPLITTER_API_KEY server-side, never print or persist it in logs, and use isolated environments for sensitive workflows.

Risk: Generated stems do not grant copyright or usage rights for the original audio.

Mitigation: Confirm the user has rights or permission to process and use the source audio before creating or distributing stems.

Risk: SDK installation can introduce dependency and version drift into production workflows.

Mitigation: Prefer direct REST calls or pinned SDK versions when reliability and supply-chain control matter.

## Reference(s):

- [AI Stem Splitter API Reference](artifact/references/api.md)
- [AI Stem Splitter ClawHub Listing](https://clawhub.ai/codeugar/skills/ai-stem-splitter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API guidance, JSON request examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include split status, source filename or URL, stem model, stem names, returned download URLs, and saved local file paths when requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
