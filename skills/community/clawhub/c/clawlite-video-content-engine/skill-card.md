## Description:

Converts third-party educational YouTube videos into ClawLite-oriented educational marketing content packs, including summaries, short-video scripts, social posts, blog summaries, source notes, and reusable marketing assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users can use this skill to turn a source video into a compliant ClawLite content pack with attribution, beginner framing, channel-specific drafts, and reusable marketing notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party video, transcript, or notes may be uploaded to NotebookLM during ingestion.

Mitigation: Confirm the source material is allowed to be uploaded to NotebookLM before using that optional ingestion path.

Risk: Reusable CTA, positioning, hook, or proof text may persist in video-content/ or marketing-assets/ and shape future marketing outputs.

Mitigation: Review generated folders and promoted marketing assets before reuse or publication.

Risk: Draft marketing content could over-copy, overstate endorsement, or reuse source material beyond commentary and educational framing.

Mitigation: Apply the compliance guidance: credit the source creator, add original explanation, avoid long transcript reuse, and keep ClawLite bridges soft.

## Reference(s):

- [Angle Framework](artifact/references/angle-framework.md)
- [Asset Promotion Guide](artifact/references/asset-promotion-guide.md)
- [Compliance and Positioning](artifact/references/compliance-and-positioning.md)
- [Content Pack Template](artifact/references/content-pack-template.md)
- [JK Marketing Asset Template](artifact/references/jk-marketing-asset-template.md)
- [NotebookLM Automation Guide](artifact/references/notebooklm-automation-guide.md)
- [Short Video Template](artifact/references/short-video-template.md)
- [Source Note Template](artifact/references/source-note-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown files plus metadata JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reusable, auditable outputs under video-content/<videoId>/ and may promote reusable notes into marketing-assets categories.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
