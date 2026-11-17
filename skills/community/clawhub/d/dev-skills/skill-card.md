## Description:

A Chinese-language full-stack development workflow skill that uses living specifications, atomic task decomposition, parallel implementation, and snapshot regression testing to plan and deliver software changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weedfire](https://clawhub.ai/user/weedfire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure new projects, feature work, bug fixes, and change requests into specification-backed units that can be implemented, tested, integrated, and documented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create or update project documentation, code, tests, and database migration snippets.

Mitigation: Review generated changes before applying them, especially database ALTER and ROLLBACK statements and any commands that affect the working tree.

Risk: Parallel task decomposition can miss hidden coupling between files, APIs, components, or database tables.

Mitigation: Use the skill's conflict checks and full snapshot regression testing before merging parallel changes.

Risk: Security claims such as OWASP coverage, input validation, observability, and zero-defect testing depend on the user's implementation environment.

Mitigation: Treat those outputs as review requirements and verify them with project-specific security scans, unit tests, integration tests, and browser-based regression tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weedfire/skills/dev-skills)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with plans, code blocks, file-change summaries, commands, and documentation updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce living specifications, architecture notes, tests, database migration and rollback snippets, changelog entries, API documentation, and browser-test instructions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
