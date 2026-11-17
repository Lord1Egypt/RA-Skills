## Description:

High-fidelity HTML design and prototype skill for landing pages, slide decks, mobile mockups, interactive prototypes, dashboard explorations, design-direction advising, and design review work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and product teams use this skill to turn visual design requests into reviewable HTML artifacts such as landing pages, slide decks, dashboards, mobile mockups, interactive prototypes, and design reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An export helper can unintentionally bundle sensitive local files when HTML contains unsafe asset paths.

Mitigation: Use export tools only on trusted HTML, inspect asset paths before creating self-contained output, and avoid packaging projects that contain nearby secrets.

Risk: Export workflows that process third-party HTML or sensitive project files can increase exposure if run in a broad workspace.

Mitigation: Run exports in a sandboxed workspace and prefer pinned dependencies with a lockfile before installation.

## Reference(s):

- [CC Design ClawHub Skill](https://clawhub.ai/cellinlab/skills/cell-cc-design)
- [Source Homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/cc-design)
- [Design Excellence Guide](references/design-excellence.md)
- [Frontend Design](references/frontend-design.md)
- [Design Patterns Library](references/design-patterns.md)
- [Interactive Prototype](references/interactive-prototype.md)
- [Platform Tool Reference](references/platform-tools.md)
- [Verification Protocol](references/verification-protocol.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, generated HTML/CSS/JS files, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce export-ready HTML, PDF, or PPTX workflows when the user requests export.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
