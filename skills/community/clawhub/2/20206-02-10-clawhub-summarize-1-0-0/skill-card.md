## Description:

Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pin-alt](https://clawhub.ai/user/pin-alt)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to summarize web pages, local files, PDFs, images, audio, and YouTube links through the summarize CLI. It is useful when an agent needs concise human-facing summaries or structured JSON output from supported content sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files, URLs, images, audio, PDFs, or YouTube content may be processed by the summarize CLI and configured external model or fallback providers.

Mitigation: Use the skill only with providers your organization has approved, and avoid confidential, regulated, or private inputs unless their data handling is acceptable.

Risk: Optional fallback services for blocked sites or YouTube transcription can send content to additional third-party services when configured.

Mitigation: Review optional service keys and fallback settings before use, and disable or omit services that are not approved for the data being summarized.

## Reference(s):

- [Summarize homepage](https://summarize.sh)
- [ClawHub skill page](https://clawhub.ai/pin-alt/skills/20206-02-10-clawhub-summarize-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/pin-alt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable summary length, maximum output tokens, extraction-only mode, model selection, and optional fallback services.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
