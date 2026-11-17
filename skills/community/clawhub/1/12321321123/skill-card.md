## Description:

Generate PPT decks from prompts/block XML while preserving corporate brand style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phil-osophy-42](https://clawhub.ai/user/phil-osophy-42)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to generate corporate-style PowerPoint decks from structured block XML or presentation prompts while reusing an existing template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filename inputs can escape the skill folder and overwrite writable files.

Mitigation: Use trusted filenames only, reject absolute or parent-directory paths, and run the skill in a restricted workspace.

Risk: Template inputs may come from untrusted files.

Mitigation: Use only trusted PowerPoint template files and review generated decks before sharing.

Risk: The dependency range is not pinned for production use.

Mitigation: Pin python-pptx to an approved version before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phil-osophy-42/skills/12321321123)
- [Artifact README](artifact/README.md)
- [Demo block XML](artifact/assets/demo_blocks.xml)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [PPTX file with structured status fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns output_path, slide_count, fallback_count, and message.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact SKILL.md lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
