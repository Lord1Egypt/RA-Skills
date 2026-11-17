## Description:

Compresses PDFs and images to reduce storage and transfer size using Python-first workflows with Node.js fallback utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexavi8](https://clawhub.ai/user/hexavi8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to shrink PDF and image files for upload, sharing, or storage while balancing quality and size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing compression dependencies can introduce normal supply-chain risk.

Mitigation: Review and approve pip, npm, brew, or apt commands before execution, preferably in an isolated environment with pinned dependency versions.

Risk: Compression can increase file size or reduce quality for already optimized or unsuitable inputs.

Mitigation: Compare before and after sizes, keep the original input file, and retry with an alternate preset, quality, format, resize setting, or backend when the result is poor.

Risk: Sensitive documents may be processed by local third-party compression libraries and tools.

Mitigation: Process sensitive files only in trusted local environments and avoid installing unreviewed dependencies while handling confidential content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexavi8/skills/file-compression)
- [Publisher profile](https://clawhub.ai/user/hexavi8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and compression result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports output path, before and after sizes, saved percentage, and backend used.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
