## Description:

Turn a Bilibili video URL or BV number into a human-like XMind mind map. Use when the user wants to collect subtitles, comments, AI summary, and transcript fallback, then generate structured notes or mind maps for a Bilibili video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pzc163](https://clawhub.ai/user/pzc163)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and video analysts use this skill to turn a Bilibili URL or BV id into structured notes and an XMind mind map. It collects video metadata, subtitles, comments, AI summary, and ASR fallback material, then prepares or renders an outline for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Bilibili video content can be passed into the host model and may lead to incorrect, misleading, or prompt-influenced outlines.

Mitigation: Review the generated context and outline before relying on them, and preserve uncertainty markers when the source material is weak or incomplete.

Risk: The skill can fetch Bilibili content, use a Bilibili login session, and write local audio, transcript, context, and output files.

Mitigation: Run it only for videos and login sessions the user intends to use, and inspect the generated output directory before sharing artifacts.

Risk: Audio may be sent to configured ASR services such as Aliyun or a Parakeet-compatible endpoint when transcription fallback is enabled.

Mitigation: Prefer existing subtitles when available, disable ASR when audio privacy matters, or use a trusted local ASR endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pzc163/skills/bili-mindmap)
- [Host LLM Outline Spec](references/host-llm-outline-spec.md)
- [Mindmap Outline Template](references/mindmap-outline-template.md)
- [Third-Party Notices](THIRD_PARTY_NOTICES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated local files can include context.md, host_outline_prompt.md, outline.md, transcripts, JSON metadata, and .xmind output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses subtitles as the preferred evidence source, can fall back to ASR, and writes local output files for the selected Bilibili video.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
