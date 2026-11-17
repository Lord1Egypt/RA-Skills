## Description:

DocCraft helps agents create source-grounded professional documents from existing materials and generate, edit, review, or redline .docx deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bloom-u](https://clawhub.ai/user/bloom-u)

### License/Terms of Use:

Anthropic service agreement terms

## Use Case:

Developers, employees, and external users can use this skill to turn source files, outlines, and templates into formal long-form deliverables, then prepare Word outputs with formatting, review, comments, or tracked changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unpinned global npm install path can change the local environment or make DOCX generation less reproducible.

Mitigation: Install in an isolated workspace and prefer a pinned local docx dependency with a lockfile.

Risk: Processing malicious or oversized Office archives can exhaust disk, memory, or CPU.

Mitigation: Process trusted Office files only, or run archive handling with size and time limits.

Risk: The skill reads selected source files and writes or modifies document outputs.

Mitigation: Review selected inputs and generated or modified documents before external delivery.

## Reference(s):

- [DocCraft Skill Page](https://clawhub.ai/bloom-u/skills/doccraft)
- [DocCraft Skill Instructions](SKILL.md)
- [DOCX JavaScript Workflow](docx-js.md)
- [OOXML Editing Workflow](ooxml.md)
- [Source Manifest](references/source-manifest.md)
- [Section Briefs](references/section-briefs.md)
- [Drafting Rules](references/drafting-rules.md)
- [Consistency Review](references/consistency-review.md)
- [Word Delivery Brief](references/word-delivery-brief.md)
- [Word Assembly Plan](references/word-assembly-plan.md)
- [Word Format Profile](references/word-format-profile.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or text drafts, generated .docx files, review notes, configuration JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected source files and write or modify local document outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
