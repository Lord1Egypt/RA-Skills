## Description:

MinerU document extraction CLI converts PDFs, images, and web pages into Markdown, HTML, LaTeX, or DOCX via the MinerU API, with support for single and batch extraction, web crawling, async tasks, and piped workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[decrystal](https://clawhub.ai/user/decrystal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to convert PDFs, images, DOCX files, and web pages into text-oriented outputs through mineru CLI commands, including batch extraction, OCR, crawling, async status checks, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples execute mutable remote scripts directly.

Mitigation: Inspect installer contents first or use pinned, checksummed downloads before installing mineru.

Risk: Confidential documents, internal URLs, or token-bearing requests may be sent to the MinerU API or configured endpoint.

Mitigation: Avoid confidential inputs unless the endpoint and data policy allow it; use only approved private deployments when required.

Risk: Extraction output can be incomplete or inaccurate for corrupted files, scanned content, formulas, complex layouts, or oversized documents.

Mitigation: Review generated outputs before relying on them; use OCR, page ranges, model selection, and longer timeouts where appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/decrystal/skills/ade-mineru-api-skills)
- [Publisher profile](https://clawhub.ai/user/decrystal)
- [MinerU website](https://mineru.net)
- [MinerU CLI installer for Linux and macOS](https://cdn-mineru.openxlab.org.cn/open-api-cli/install.sh)
- [MinerU CLI installer for Windows](https://cdn-mineru.openxlab.org.cn/open-api-cli/install.ps1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide mineru CLI usage for Markdown, JSON, HTML, LaTeX, and DOCX extraction outputs.]

## Skill Version(s):

1.2.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
