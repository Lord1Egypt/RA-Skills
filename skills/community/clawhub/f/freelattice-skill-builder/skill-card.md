## Description:

Drafts FreeLattice form fields and, when the runtime supports artifacts, packages the resulting skill as a zip for import-style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neomagnetar](https://clawhub.ai/user/neomagnetar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and FreeLattice users use this skill to turn plain-language skill ideas into copy-ready FreeLattice form fields and, when supported, a minimal import-style zip package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts or triggers may be too broad for the intended FreeLattice skill.

Mitigation: Review generated prompts, triggers, and package contents before importing or publishing the skill.

Risk: The skill may create a local zip package containing generated skill.json and README.md files.

Mitigation: Inspect the generated files before use and confirm they match the displayed form fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neomagnetar/skills/freelattice-skill-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration]

**Output Format:** [Markdown sections with optional JSON package files or zip artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a minimal local zip package containing skill.json and README.md when the runtime supports file creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
