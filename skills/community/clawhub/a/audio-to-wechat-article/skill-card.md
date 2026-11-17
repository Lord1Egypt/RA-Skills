## Description:

Turn meeting audio or a transcript plus optional images into a publish-ready WeChat Official Account article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, marketers, and agents use this skill to turn Chinese meeting audio, transcripts, notes, screenshots, and optional QR codes into structured WeChat Official Account drafts. It supports a repeatable workflow from source normalization through article brief, article JSON, markdown composition, image placement guidance, and optional publishing handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pipeline wrapper may execute Python files from hardcoded local paths outside the reviewed package.

Mitigation: Review and update script paths to point to trusted local copies before running the end-to-end wrapper.

Risk: Generated publish-ready Markdown may include a fixed default author name unless overridden.

Mitigation: Set or review the author metadata before publishing any WeChat draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinhuadeng/skills/audio-to-wechat-article)
- [Workflow](references/workflow.md)
- [Style Guide](references/style-guide.md)
- [Publish Handoff](references/publish-handoff.md)
- [Transcription Handoff](references/transcription-handoff.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown article drafts, article brief JSON, article JSON, and handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image placement notes, QR code CTA placement, cover image metadata, and optional WeChat draft publishing handoff.]

## Skill Version(s):

0.1.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
