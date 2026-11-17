## Description:

Translate user-supplied text PDFs into Simplified Chinese and bilingual PDFs. Reads the PDF and only explicitly selected local LaTeX, sends extracted text to an explicitly approved OpenAI-compatible endpoint, runs local PDF/Python subprocesses, and writes outputs, diagnostics, and the default runtime cache under the chosen directory. Local proxy, arXiv download, Docker compilation, and external cache paths require explicit command-line opt-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[double6-ai](https://clawhub.ai/user/double6-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to translate non-scanned English text PDFs into Simplified Chinese while preserving layout, producing a Chinese PDF, a bilingual PDF, diagnostics, and quality-gate evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are sent to the selected model provider.

Mitigation: Use only a trusted HTTPS endpoint, confirm the destination before sending documents, and avoid highly sensitive PDFs unless the provider and handling controls are acceptable.

Risk: The security summary flags API-key exposure and insecure endpoint handling as review-worthy.

Mitigation: Use explicit per-run credentials, keep keys out of logs and outputs, and review API-key handling before production use.

Risk: The security summary flags unpinned executable dependencies.

Mitigation: Install in a dedicated virtual environment and review or pin the pdf2zh_next dependency and PDF tooling before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/double6-ai/skills/double6-pdf-translation)
- [Metadata homepage](https://github.com/double6-ai/double6-skills/tree/main/skills/double6-pdf-translation)
- [Workflow](references/workflow.md)
- [Runtime dependencies](references/runtime-dependencies.md)
- [Academic translation policy](references/academic-translation-policy.md)
- [Known pitfalls](references/known-pitfalls.md)
- [Provider base URLs](references/provider-base-urls.md)
- [Glossary template](references/glossary-template.tsv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated PDF, JSON, and diagnostic files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese and bilingual PDFs, a render manifest, and diagnostic artifacts under the selected output directory.]

## Skill Version(s):

1.0.5 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
