## Description:

HR Admin Assistant helps technology-company back-office teams draft HR and administrative documents, design workflows, analyze requirements, and prepare reports using bundled templates and policy references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sirutong](https://clawhub.ai/user/sirutong)

### License/Terms of Use:

MIT-0

## Use Case:

HR, administration, legal, and finance-support staff use this skill to turn back-office requests into structured documents, workflow descriptions, reports, forms, and requirement analyses for technology-company operations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The artifact includes an instruction to update its own trigger terms after use, which can create under-controlled persistent changes in shared or persistent agent environments.

Mitigation: Remove that self-modification behavior or require maintainer approval before any changes to skill instructions are made.

Risk: The document-generation helper can write to a caller-provided output path, creating a risk of unintended overwrite.

Mitigation: Constrain generated files to an approved output directory and avoid overwriting existing files by default.

Risk: HR and legal templates may be mistaken for final legal advice.

Mitigation: Treat generated HR/legal content as drafting support and require qualified legal or HR review before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sirutong/skills/admin-skills)
- [HR policies and compliance baseline](references/hr_policies.md)
- [Process library](references/process_library.md)
- [Document templates](references/doc_templates.md)
- [Report templates](references/report_templates.md)
- [API reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown documents, tables, workflow descriptions, and structured analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompts for missing business context and review notes for employee-rights or compliance-sensitive content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
