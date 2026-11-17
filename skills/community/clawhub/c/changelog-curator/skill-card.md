## Description:

Changelog Curator helps agents turn provided change logs, commit summaries, or release notes into reviewable external-facing changelog drafts that separate user-visible updates from internal changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release managers, and documentation teams use this skill to draft reviewable changelogs for product releases, announcements, or internal reporting from supplied change material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input material may contain sensitive release, customer, or internal planning details.

Mitigation: Review and redact sensitive input before use, and keep generated drafts in a review workflow until approved.

Risk: A changelog draft can become misleading if source material is incomplete or asks the skill to invent unreleased features.

Mitigation: Limit claims to the supplied change material and mark missing facts as confirmation items rather than filling gaps.

Risk: The bundled script includes inactive audit modes that can inspect local files when intentionally enabled.

Mitigation: Use the default changelog drafting mode for normal releases and enable local inspection modes only with an explicit, scoped review purpose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/changelog-curator)
- [README](README.md)
- [Output template](resources/template.md)
- [Structured specification](resources/spec.json)
- [Example input](examples/example-input.md)
- [Example output](examples/example-output.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft, with optional JSON output when the bundled local script is used with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for human review before publishing, sending, or using in compliance-sensitive release workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
