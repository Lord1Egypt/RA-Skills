## Description:

Ancient Man is a Chinese response-compression skill that rewrites agent responses into concise modern or classical Chinese modes while preserving core technical content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garylooop](https://clawhub.ai/user/garylooop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reduce Chinese-language token usage by applying configurable compression modes to technical answers, commands, and explanations. It is most appropriate when brevity is desired and exact original wording is not required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lossy rewriting can silently change code, configuration, search queries, retrieved document text, or other wording where precision matters.

Mitigation: Gate compression behind explicit use, preserve the original text separately, and avoid default use for security, legal, medical, operational runbooks, code/config editing, and retrieval pipelines.

Risk: Broad auto-activation can compress responses when the user only loosely asks for brevity.

Mitigation: Require clear mode selection or confirmation for high-impact workflows and disable automatic compression where exact wording is important.

Risk: The decompression behavior is best-effort and may not restore the original text exactly.

Mitigation: Store mapping logs and the original source text whenever compressed content must be audited, reviewed, or reconstructed.

## Reference(s):

- [Ancientman skill definition](artifact/SKILL.md)
- [Chinese compression guide](artifact/references/caveman_zh_cn.md)
- [Classical enhancement guide](artifact/references/classical_enhancement.md)
- [Ancientman v2 update report](artifact/ancientman_v2_update_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with optional code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mode-dependent Chinese compression; output may be lossy and only partially reversible when mapping logs are preserved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
