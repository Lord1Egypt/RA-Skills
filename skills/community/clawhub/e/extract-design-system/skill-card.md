## Description:

Extract design primitives from a public website and generate starter token files for your project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arvindrk](https://clawhub.ai/user/arvindrk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to inspect a public website's visual primitives and generate starter token files for initializing a project-local design system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm commands can execute changing external code on the local machine.

Mitigation: Use pinned, lockfile-managed versions of extract-design-system and Playwright, or run extraction in a sandbox or container with minimal filesystem and credential access.

Risk: Extracted third-party website output can be incomplete or misleading if treated as an authoritative design system.

Mitigation: Review normalized extraction output before using generated token files, and do not modify existing app code or styles without explicit confirmation.

## Reference(s):

- [Skill release page](https://clawhub.ai/arvindrk/skills/extract-design-system)
- [Workflow](references/workflow.md)
- [Outputs](references/outputs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON/CSS token files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files may include .extract-design-system/raw.json, .extract-design-system/normalized.json, design-system/tokens.json, and design-system/tokens.css.]

## Skill Version(s):

0.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
