## Description:

Transform one source asset into a coordinated pack for multiple channels such as WeChat, Xiaohongshu, TikTok, email, and slides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams use this skill to turn one source article, video, or transcript into channel-specific drafts, a shared facts block, a launch checklist, and a reuse matrix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional helper script reads a source text file and writes a JSON draft file.

Mitigation: Run it only on content intended for processing and choose an output path that will not overwrite an important file.

Risk: Repurposed public-facing content can preserve or amplify unsupported claims from the source material.

Mitigation: Keep assumptions explicit and review channel drafts, facts, metrics, legal claims, and CTAs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/content-repurpose-studio)
- [README](artifact/README.md)
- [Channel specifications](artifact/resources/channel_specs.yaml)
- [Smoke test](artifact/tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses and optional JSON draft files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local Python helper to read an explicit source text file and write a channel-pack JSON draft.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
