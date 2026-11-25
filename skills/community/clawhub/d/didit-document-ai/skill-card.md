## Description:

Helps developers integrate Didit Document AI to extract typed fields from documents, compare names, detect suspected tampering, and read QR codes or barcodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rosasalberto](https://clawhub.ai/user/rosasalberto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build backend integrations that submit PDFs or images to Didit, retrieve requested document fields, and handle name matching, manipulation warnings, and review statuses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and an API key are sent to the external Didit service; the security scan is marked partial because some referenced local paths could not be resolved.

Mitigation: Only send documents and credentials when you are comfortable sharing them with Didit, and review the scan gaps before use.

## Reference(s):

- [Didit Document AI API](https://docs.didit.me/standalone-apis/document-ai)
- [Document AI Feature Guide](https://docs.didit.me/core-technology/document-ai/overview)
- [Document AI Rules and Warnings](https://docs.didit.me/core-technology/document-ai/warnings-document-ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python, TypeScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples require a Didit API key supplied through DIDIT_API_KEY.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
