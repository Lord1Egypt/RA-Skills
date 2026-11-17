## Description:

Converts PDFs, images, scanned documents, and Office files into structured Markdown with preserved headings, tables, lists, paragraphs, and page structure using Laiye ADP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laiye-adp](https://clawhub.ai/user/laiye-adp)

### License/Terms of Use:

Commercial License Agreement

## Use Case:

Developers, knowledge workers, and agent builders use this skill to convert local, remote, or Base64-encoded documents into Markdown for documentation migration, publishing, archive digitization, and LLM context preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are processed by the ADP cloud service, which may expose document contents to an external provider.

Mitigation: Use the skill only for documents approved for ADP processing and confirm organizational data-handling requirements before sending sensitive files.

Risk: The artifact documents curl-to-shell and PowerShell pipe-to-execute installer options that can run unreviewed remote code.

Mitigation: Prefer a pinned npm package version or reviewed release binary, and inspect installer scripts before execution.

Risk: The bundled CLI supports broader ADP account actions, including custom application creation, update, and deletion.

Mitigation: Allow an agent to run extraction or custom-app management commands only after explicit user approval for those account changes.

Risk: The skill requires ADP API credentials and application identifiers.

Mitigation: Store API keys securely, avoid logging or sharing them, and verify the configured endpoint before running document parsing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/laiye-adp/skills/adp-pdf-to-structured-markdown)
- [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- [Public Cloud Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- [ADP CLI Releases](https://github.com/laiye-ai/adp-cli/releases)
- [Laiye ADP Product Page](https://laiye.com/en/product/agentic-document-processing)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text, with JSON summaries or structured error objects for batch and failure cases.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ADP API key, an ADP document parsing app_id, supported document input, and ADP CLI availability.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
