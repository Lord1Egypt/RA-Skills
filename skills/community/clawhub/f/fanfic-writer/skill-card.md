## Description:

Fanfic Writer is an automated novel-writing assistant that plans, drafts, reviews, and assembles long-form fiction with state tracking, multi-perspective QC, atomic file writes, and human confirmation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanson515](https://clawhub.ai/user/tanson515)

### License/Terms of Use:

MIT

## Use Case:

Writers and agent users use this skill to create serialized fiction by generating outlines, world-building notes, chapter plans, draft chapters, QC feedback, backpatch plans, and final manuscript files with human review points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual approval gates may not be enforced before model calls and persistent writes.

Mitigation: Review the code before installation, run it only in a dedicated novel workspace, avoid auto mode and large chapter ranges, and keep --run-dir away from sensitive directories.

Risk: The skill writes generated drafts, state, logs, and final manuscript files to disk.

Mitigation: Use a purpose-built workspace with limited contents and inspect generated files before reuse or publication.

## Reference(s):

- [Fanfic Writer ClawHub listing](https://clawhub.ai/tanson515/skills/fanfic-writer)
- [Prompt reference](references/prompts.md)
- [Installation guide](INSTALL_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated prose, JSON state files, text manuscript files, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a dedicated novel run directory; model selection is supplied by OpenClaw configuration.]

## Skill Version(s):

2.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
