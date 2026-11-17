## Description:

Ebook Maker guides an agent through Chinese ebook production, from requirements and research to outline creation, optional illustrations, HTML layout, PDF export, and delivery reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irenerachel](https://clawhub.ai/user/irenerachel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and publishing teams use this skill to have an agent plan, research, write, illustrate, typeset, and export ebook-style PDF manuals. It is intended for normal ebook projects where users can review the generated content, cited sources, and saved files before distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential checks can print API key values.

Mitigation: Review and revise credential checks so secrets are detected without echoing full values.

Risk: PDF generation can run Chrome without its browser sandbox.

Mitigation: Remove `--no-sandbox` unless an isolated execution environment and explicit approval justify it.

Risk: The workflow can automatically save user and request details to local reports.

Mitigation: Use the skill only with non-sensitive ebook projects or change the workflow to ask before saving reports.

Risk: Prompts and project details can be sent to external image-generation services.

Mitigation: Require user approval before submitting prompts or project details to third-party image-generation services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/irenerachel/skills/ebook-maker)
- [Main ebook workflow](artifact/SKILL.md)
- [Illustration specification](artifact/illustration.md)
- [Layout specification](artifact/layout.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTML/CSS snippets, prompt templates, shell commands, and delivery-report structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local research reports, ebook HTML/PDF files, illustrations, and delivery summaries.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
