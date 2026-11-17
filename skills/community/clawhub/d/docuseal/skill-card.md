## Description:

Manage DocuSeal e-signature workflows from the terminal via the DocuSeal CLI, including creating templates from PDF, DOCX, and HTML files, sending documents for signing, tracking submissions, and updating submitters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[docuseal](https://clawhub.ai/user/docuseal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run DocuSeal CLI workflows from shells, scripts, and CI/CD pipelines for document template management, signing requests, submission tracking, and signer updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing a mutable DocuSeal CLI executable package.

Mitigation: Pin and verify the DocuSeal CLI version before production use.

Risk: The skill uses DocuSeal API credentials and may operate on sensitive document files.

Mitigation: Use a narrowly scoped API key where possible and run the skill with only the required files and environment variables.

Risk: The skill can trigger high-impact e-signature actions such as sending notifications, archiving or replacing documents, and marking signers as completed.

Mitigation: Review commands carefully before execution, especially commands that send messages, alter document state, or complete signer workflows.

## Reference(s):

- [DocuSeal Homepage](https://www.docuseal.com)
- [DOCX Dynamic Content Variables](references/docx-variables.md)
- [PDF / DOCX Field Tags](references/field-tags.md)
- [HTML Field Tags](references/html-fields.md)
- [Submissions](references/submissions.md)
- [Submitters](references/submitters.md)
- [Templates](references/templates.md)
- [DocuSeal DOCX Variables Guide](https://www.docuseal.com/guides/use-dynamic-content-variables-in-docx-to-create-personalized-documents)
- [DocuSeal Embedded Field Tags Guide](https://www.docuseal.com/guides/use-embedded-text-field-tags-in-the-pdf-to-create-a-fillable-form)
- [DocuSeal HTML Fillable Form Guide](https://www.docuseal.com/guides/create-pdf-document-fillable-form-with-html-api)
- [DocuSeal Field Tags Example PDF](https://www.docuseal.com/examples/fieldtags.pdf)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-oriented CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [DocuSeal CLI command output is described by the artifact as JSON.]

## Skill Version(s):

1.0.8 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
