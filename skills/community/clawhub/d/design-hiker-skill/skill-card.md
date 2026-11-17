## Description:

Generates and verifies UI design deliverables, including interactive prototypes, annotated HTML, design tokens, machine-readable specs, assumptions logs, browser measurement evidence, screenshots, and acceptance tests from text, screenshots, Sketch, or Figma inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilper](https://clawhub.ai/user/hilper)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, product teams, developers, and AI coding agents use this skill to turn UI requirements or design inputs into high-fidelity prototypes and implementation-ready design specifications for mobile H5 and web PC projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated files may expose private designs, repositories, or customer product plans.

Mitigation: Review the skill before installation and run it only in an isolated workspace for sensitive projects.

Risk: Preview servers and mutable browser code may expose generated files or execute prototype code.

Mitigation: Bind preview servers to localhost and the active project folder, then review generated HTML, scripts, reports, and acceptance tests before broader use.

Risk: Remote CDN imports and external sync can retain or transmit sensitive prototype artifacts.

Mitigation: Avoid remote CDN imports for sensitive prototypes and keep cross-session approved-design storage or external sync disabled unless artifact retention is acceptable.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/hilper/design-hiker-skill)
- [ClawHub skill page](https://clawhub.ai/hilper/skills/design-hiker-skill)
- [Skill definition](artifact/SKILL.md)
- [Core methodology](artifact/system-prompt.md)
- [Codex harness reference](artifact/references/codex.md)
- [Claude harness reference](artifact/references/claude.md)
- [Cursor harness reference](artifact/references/cursor.md)
- [Design profile registry](artifact/design-system/profiles/registry.json)
- [Universal component specs](artifact/design-system/universal/components.md)
- [Universal usage guidelines](artifact/design-system/universal/usage-guidelines.md)
- [Visual critic checklist](artifact/design-system/universal/references/visual-critic.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Design package files: HTML, CSS, JSON, Markdown/text logs, PNG screenshots, and JavaScript acceptance tests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under designs/<project-name>/ and include browser measurement reports plus an executable acceptance contract when verification completes.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact metadata release.version is v0.6.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
