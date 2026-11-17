## Description:

Distill Self-Improving indexes user-selected local files into a local knowledge base and creates navigable inventories, per-file summaries, and project or topic summaries without modifying the source files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzusp](https://clawhub.ai/user/zzusp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill when they explicitly want selected files, directories, projects, or document collections added to a local knowledge base with audit tables, file-level distillations, and optional project or topic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected folders can contain secrets, private records, regulated data, or sensitive filenames, and paths, metadata, and sanitized summaries may be retained locally.

Mitigation: Use the skill only on intentionally selected local files and avoid sensitive folders unless retaining that local metadata and summary content is acceptable.

Risk: Generated indexes and summaries can become stale or be mistaken for the source of truth.

Mitigation: Treat knowledge-base entries as navigation and summary aids, and recheck the original files and current filesystem state before relying on conclusions.

## Reference(s):

- [Batch Migration, Exceptions, and Real Scenarios](references/distillation-scenarios.md)
- [ClawHub Skill Page](https://clawhub.ai/zzusp/skills/distill-self-improving)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, CSV inventories, validation command guidance, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local knowledge-base navigation, audit tables, per-file distillation files, and optional summaries under ~/.agent-knowledge while keeping source files read-only.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-08-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
