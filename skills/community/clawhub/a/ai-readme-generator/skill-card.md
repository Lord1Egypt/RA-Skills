## Description:

Generates AI-readable project documentation for OpenClaw/Cursor-style coding workflows from an existing codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjuncher](https://clawhub.ai/user/zjuncher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create or refresh AGENTS.md and Cursor rule documentation that summarize a project structure, architecture, development workflow, core flows, and human-maintained business context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated agent-facing documentation can influence future coding sessions if it contains inaccurate project facts.

Mitigation: Review the generated files and keep unverifiable claims marked with TODO verification notes.

Risk: Project-specific secrets or private local details could be summarized into generated documentation.

Mitigation: Review generated documentation before use and avoid copying environment files, credentials, tokens, private keys, or local machine paths.

Risk: Human-maintained business knowledge or lessons learned could be lost if manual documentation is overwritten.

Mitigation: Preserve existing files under .cursor/rules/ai-readme/manual/ and only create those templates when missing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Markdown, Configuration, Guidance]

**Output Format:** [Markdown files and Cursor .mdc rule files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces AGENTS.md and .cursor/rules/ai-readme documentation; manual files are created only when missing.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
