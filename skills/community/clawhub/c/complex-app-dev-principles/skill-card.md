## Description:

Guides modular complex app development using five principles for controlled planning, module boundaries, developer confirmation, sequential testing, and final verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smxtx](https://clawhub.ai/user/smxtx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, build, refactor, test, and verify complex app modules with documented module boundaries, API contracts, lock records, and delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts can create directories, README files, source and test folders, and lock records in the working tree.

Mitigation: Run the skill in a version-controlled workspace, constrain output paths, and review diffs before accepting generated files.

Risk: The skill text includes an under-scoped automatic cleanup instruction for code that is inconsistent with confirmed functionality.

Mitigation: Require explicit user confirmation and a reviewed change plan before any cleanup, deletion, or lock operation.

Risk: Untrusted module names or output paths could create files in unintended locations.

Mitigation: Use trusted module names and project-local output directories, and reject path traversal or unexpected absolute paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smxtx/skills/complex-app-dev-principles)
- [Module design template](references/module_design_template.md)
- [API interface specification](references/api_specification.md)
- [Test case template](references/test_case_template.md)
- [Delivery checklist](references/delivery_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with optional generated files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create module scaffold directories, README files, source and test folders, and lock record files when bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
