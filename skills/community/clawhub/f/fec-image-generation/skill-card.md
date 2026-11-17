## Description:

Helps agents create and edit images and diagrams, retain editable sources, and review exported PNGs for visual issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers, designers, and other creators use this skill to make diagrams and visual assets, export images, and check PNG quality while retaining editable sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local diagram server can retain or change sessions without authentication, potentially exposing sensitive diagram content to other local users.

Mitigation: Avoid sensitive architecture, personal data, credentials, and unreleased details; use unique session IDs, keep the server on 127.0.0.1, and stop it when finished.

Risk: Export helpers run local Node tools, a browser, and image converters.

Mitigation: Review the bundled scripts and local tool execution before installing or running the skill.

Risk: Automated PNG checks may miss incorrect labels or misleading visual details.

Mitigation: Inspect final images and confirm names, figures, brand details, and compliance-sensitive content manually.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/bovinphang/skills/fec-image-generation)
- [Project homepage (package metadata; provenance not verified)](https://github.com/bovinphang/frontend-craft)
- [Diagram workflows](references/diagram-workflows.md)
- [HTML technical diagrams](references/html-technical-diagrams.md)
- [PNG QA and repair](references/png-qa-autofix.md)

## Skill Output:

**Output Type(s):** [Images, Code, Configuration instructions, Guidance]

**Output Format:** [Editable diagram sources and PNG/SVG/HTML images with Markdown guidance and QA results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains editable sources and records QA findings; final images need visual review.]

## Skill Version(s):

2.9.0 (source: ClawHub release, README.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
