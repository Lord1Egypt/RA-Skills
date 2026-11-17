## Description:

Extracts structured table data from native or scanned PDF documents using MinerU's table detection and OCR-capable CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, financial teams, and researchers use this skill to guide agents in extracting structured tables from PDF reports, papers, and documents. It is suited for workflows that need CLI-based table extraction from local files or URLs with MinerU authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local PDFs or URLs through a third-party tokenized MinerU CLI without a clear privacy disclosure.

Mitigation: Use it only with approved documents and URLs, avoid confidential, regulated, or customer data unless external processing is authorized, and review MinerU terms before deployment.

Risk: The install examples use global latest-version package installation.

Mitigation: Prefer a pinned and reviewed local install, verify the package source, and scan the resolved dependency before use.

Risk: The referenced CLI also supports broader extraction and crawl workflows beyond table extraction.

Mitigation: Limit agent usage to the documented table extraction commands and review proposed commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/extract-tables-from-pdf)
- [MinerU homepage](https://mineru.net)
- [MinerU token management](https://mineru.net/apiManage/token)
- [MinerU GitHub project](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include install commands, authentication setup, extraction flags, and notes about stdout, output directories, OCR, language hints, and page ranges.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
