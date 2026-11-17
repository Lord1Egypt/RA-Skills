## Description:

Generate ASCII art from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert text prompts into ASCII art through the configured generate-ascii-art capability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases and messy merged content may cause activation for adjacent ASCII-related requests.

Mitigation: Review or narrow trigger phrases before deployment.

Risk: The artifact delegates execution to local capability_executor.py and mentions MetaClaw and SEAL components that were not included in the artifact.

Mitigation: Confirm the local dispatcher and related components are trusted before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/generate-ascii-art)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Bilibili: ascii-image-converter](https://www.bilibili.com/video/BV19R22YyEuz)
- [Bilibili: x ascii](https://www.bilibili.com/video/BV16myLYwEKT)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text ASCII art, with optional Markdown usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on a trusted local capability_executor.py dispatcher.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
