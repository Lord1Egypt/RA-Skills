## Description:

Event Manager helps Architect agents create, edit, query, and export Chinese novel event profiles with causality chains, timelines, and multi-thread narrative tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and story-planning agents use this skill during AutoNovel Writer v5.0 Phase 2 to convert outlines and world files into events/*.yml causality records. It supports creating event files, listing and querying events, updating or deleting records, and exporting a Markdown timeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency versions are lower-bounded rather than pinned, which can make installs less reproducible.

Mitigation: Install in a virtual environment and use pinned or locked dependency versions before production use.

Risk: Create and export commands write local files and may overwrite selected output paths.

Mitigation: Run file-changing commands only inside the intended novel project directory and review output paths before execution.

Risk: Delete removes local event files after confirmation.

Mitigation: Keep project backups or version control enabled and verify the target event title before confirming deletion.

## Reference(s):

- [Event Manager ClawHub Release](https://clawhub.ai/yuzhihui886/skills/event-manager)
- [Reference Documentation for Event Manager](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, YAML event files, and optional Markdown timeline exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local project files such as events/*.yml and timeline Markdown when the CLI is executed.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
