## Description:

A tool-neutral long-form fiction workflow for creating, continuing, importing, redirecting, rewriting, auditing, and reviewing novel projects with persistent story state and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragon-qx](https://clawhub.ai/user/dragon-qx)

### License/Terms of Use:

MIT

## Use Case:

Authors and agent operators use this skill to manage long-form fiction projects across sessions, including chapter drafting, file-based story state maintenance, continuity audits, safe rewrites, snapshots, and a local reading/progress dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is disclosed as automatically checking api.skillhub.cn and applying remote self-updates at startup, which expands trust in the remote package source.

Mitigation: Review the installed package before use, disable automatic updates with _meta.json update.auto_check=false or update.enabled=false, and apply updates manually after review.

Risk: The dashboard workflow asks the user to authorize access to local book files so it can render progress, chapters, settings, and character relationships.

Mitigation: Authorize only the intended book folder and use the documented local dashboard workflow; the artifact states the dashboard reads local files and does not modify book files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragon-qx/skills/d-writer)
- [README](README.md)
- [Skill router](SKILL.md)
- [File contract](references/file-contract.md)
- [Workflow index](references/workflow.md)
- [Chapter craft](references/chapter-craft.md)
- [Audit dimensions](references/audit-dimensions.md)
- [Dashboard workflow](references/workflow-dashboard.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose, JSON state files, HTML dashboard files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a file-based story bible, chapter index, snapshots, audit drift records, and optional local dashboard assets.]

## Skill Version(s):

3.11.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
