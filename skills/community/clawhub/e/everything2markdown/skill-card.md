## Description:

Convert almost anything (PDF, DOCX, PPTX, XLSX, images, audio, YouTube, etc.) to Markdown using Microsoft MarkItDown. Optimized for AGENT and LLM workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsm0826](https://clawhub.ai/user/xsm0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert documents, media, web content, and archives into Markdown that is easier to inspect, summarize, chunk, or feed into LLM workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a broad third-party converter bundle.

Mitigation: Install it in an isolated environment, avoid administrator privileges, and pin dependencies when reproducibility or supply-chain control matters.

Risk: Converted documents, media, or URLs may contain confidential content.

Mitigation: Use caution with sensitive inputs and confirm that enabled converters, plugins, and storage locations meet the deployment's data-handling requirements.

Risk: Untrusted or large files may stress converters or produce misleading extraction results.

Mitigation: Validate file types, apply size and runtime limits, and review generated Markdown before using it in downstream decisions.

## Reference(s):

- [Microsoft MarkItDown homepage](https://github.com/microsoft/markitdown)
- [ClawHub skill page](https://clawhub.ai/xsm0826/skills/everything2markdown)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with shell command and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include extracted document metadata and preserved structure when using the Python API.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
