## Description:

DeckCraft helps agents generate editable PowerPoint decks through a structured 5-stage workflow with machine-readable QA gates, checkpoint recovery, native charts, icons, and multi-canvas output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simon2256928](https://clawhub.ai/user/simon2256928)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to turn briefs, outlines, source documents, and structured content into editable PPTX presentations with built-in QA checks. It is suited to business decks, reports, multi-canvas social or print presentations, and chart-heavy slide generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL and WeChat importers can fetch arbitrary or internal resources from the runtime environment.

Mitigation: Use the skill only in a constrained workspace, avoid untrusted links, and block localhost, private networks, cloud metadata endpoints, and non-HTTP(S) schemes at the environment level.

Risk: Dependency ranges are not pinned to exact versions.

Mitigation: Install in a virtual environment with pinned, reviewed dependency versions before production use.

Risk: Generated decks may contain layout, content, or rendering issues if QA gates are skipped.

Mitigation: Run the content and render gate scripts, read their JSON verdicts, and inspect rendered previews before delivery.

## Reference(s):

- [DeckCraft README](README.md)
- [DeckCraft Skill Spec](SKILL.md)
- [DeckCraft Changelog](CHANGELOG.md)
- [DeckCraft Migration Guide](MIGRATION.md)
- [DeckCraft Design Spec Template](templates/design_spec.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance, JSON outlines and content files, Python code or shell commands, QA reports, preview assets, and editable PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project files such as brief.md, outline.json, content.json, gate_content.json, gate_result.json, PPTX decks, rendered previews, and optional speaker notes.]

## Skill Version(s):

6.0.0 (source: server release metadata, SKILL.md, CHANGELOG, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
