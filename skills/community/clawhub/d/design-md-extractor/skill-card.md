## Description:

Design.md Extractor generates AI-friendly DESIGN.md or design.md files from a user-provided webpage URL or local HTML file by running a local Playwright-based design token extractor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei1125](https://clawhub.ai/user/liuwei1125)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI coding agents use this skill to inspect visible webpage styles from an explicitly provided URL or local file and produce reusable design documentation for frontend implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can open arbitrary URLs or local files provided by the user.

Mitigation: Use it only with trusted public pages or intentionally selected local files, and confirm the exact target before running extraction.

Risk: Generated snapshots may include page URLs, selectors, metadata, and visible text snippets.

Mitigation: Review design-snapshot.json before sharing or committing it, especially when extracting from private or sensitive pages.

Risk: Rule-based sampling can miss hidden states, authenticated content, responsive variants, animation details, and brand rules that are not visible in the loaded page.

Mitigation: Treat generated design tokens as a practical starting point and review DESIGN.md before using it as implementation guidance.

## Reference(s):

- [Extraction Rules](references/extraction-rules.md)
- [Design Snapshot Schema](references/snapshot-schema.md)
- [ClawHub Skill Page](https://clawhub.ai/liuwei1125/skills/design-md-extractor)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown design guide and optional JSON snapshot, with shell commands in agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on an explicitly provided URL or file; optional snapshots may include page URLs, selectors, and visible text snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
