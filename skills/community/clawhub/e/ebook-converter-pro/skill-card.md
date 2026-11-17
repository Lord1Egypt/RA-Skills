## Description:

電子書轉換工具箱：支援 EPUB / PDF / MOBI / AZW3 / FB2 -> TXT / Markdown / HTML / JSON；批量轉換、封面萃取、元資料讀寫、圖書館自動分類。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

Developers and ebook library maintainers use this skill to convert EPUB and PDF files into text-oriented formats, extract covers and metadata, export bibliographic data, and organize local ebook collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review reports unsafe handling of untrusted EPUB/HTML content and temporary files.

Mitigation: Use only ebooks from trusted sources, keep output directories explicit, and avoid opening generated HTML from unknown EPUBs in a browser.

Risk: Security review notes that MOBI, AZW3, and FB2 support may be less complete than advertised.

Mitigation: Expect EPUB and PDF workflows to be more reliable, and verify converted output before relying on it.

Risk: Optional dependency installation may require package-manager or sudo commands.

Mitigation: Review dependency installation as a separate system-level choice before running those commands.

Risk: Library organization can create or change files in output locations.

Mitigation: Use dry-run mode for organization workflows before applying changes to a library directory.

## Reference(s):

- [README.md](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/xuan905/skills/ebook-converter-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and generated ebook output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local conversion outputs, metadata exports, cover files, image files, and batch reports; OCR and PDF image workflows depend on optional system packages.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
