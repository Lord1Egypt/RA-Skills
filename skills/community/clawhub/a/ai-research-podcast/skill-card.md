## Description:

Converts research reports, long-form articles, and technical documents into summarized podcast audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn URLs, PDFs, Markdown or text files, and pasted text into short spoken research briefings for hands-free review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch URLs, read supplied local documents, write generated files under /tmp, and optionally send generated audio through external messaging services.

Mitigation: Review sources, destination channels, credentials, and generated files before enabling delivery or using sensitive documents.

Risk: Scheduled mode can create recurring network-fetch-and-send workflows.

Mitigation: Treat scheduled execution as opt-in and verify the source list, destinations, credentials, and disable path before enabling it.

Risk: The artifact claims offline and privacy-safe operation while the workflow can fetch network sources and send audio to external services.

Mitigation: Do not rely on the offline/privacy claim for sensitive or internal documents until dependencies, network behavior, and delivery settings are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-research-podcast)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated audio file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3 or WAV audio files and optional delivery status when messaging is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
