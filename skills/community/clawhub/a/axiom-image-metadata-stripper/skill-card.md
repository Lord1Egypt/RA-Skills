## Description:

A local Python image metadata stripping skill for removing EXIF, GPS, camera, and related metadata from supported image files before sharing or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to propose local commands or Python calls that strip metadata from photos before web publication or external sharing. It is most relevant when reducing accidental disclosure of GPS coordinates, camera identifiers, or similar image metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill overstates its privacy guarantees for image metadata removal.

Mitigation: Treat it as best-effort metadata reduction, keep original backups, and verify cleaned outputs with a mature metadata inspection tool before publishing sensitive photos.

Risk: Supported formats are narrower than the skill description suggests.

Mitigation: Use it only for the demonstrated JPEG and PNG workflows unless separate validation proves additional format support.

Risk: Untrusted or malformed image files may trigger parser edge cases.

Mitigation: Run it in a controlled local environment and avoid relying on it as the only control for hostile or malformed inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/axiom-image-metadata-stripper)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell and Python examples; CLI output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced local tool can write stripped image files and analysis results for supported inputs.]

## Skill Version(s):

0.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
