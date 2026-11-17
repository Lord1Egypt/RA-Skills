## Description:

Generates complete PRD Markdown documents through interactive requirements analysis, structured domain questions, and data-flow validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lf951515851](https://clawhub.ai/user/lf951515851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and technical teams use this skill to turn early product ideas into structured PRD documents with clarified requirements, recommended technology choices, and validated core data flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify Markdown files in the workspace, including through a custom output path.

Mitigation: Review the target path before execution and keep generated files under docs/prd unless a different destination is intentional.

Risk: The workflow may continue into design generation after PRD creation.

Mitigation: Explicitly decline, pause, or require confirmation before allowing follow-on gen-design work.

## Reference(s):

- [Gen Prd ClawHub skill page](https://clawhub.ai/lf951515851/skills/gen-prd)
- [README.md](artifact/README.md)
- [prompt.md](artifact/prompt.md)
- [prd-template.md](artifact/prd-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown PRD file with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is docs/prd/YYYY-MM-DD-{project-name}.md, with support for a custom Markdown output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
