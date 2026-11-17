## Description:

Doc Analysis helps agents analyze Word (.doc/.docx) documents with MinerU and return structured Markdown that preserves headings, paragraphs, tables, lists, and layout information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, editors, and quality-assurance teams use this skill to inspect the structure, layout, and content of Word documents before processing, editing, or conversion. It is suited for local files or URLs where structured Markdown output is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be sent to an external MinerU/OpenDataLab service during analysis.

Mitigation: Confirm the documents are approved for processing with MinerU/OpenDataLab before use, and avoid submitting confidential, regulated, or private content unless that data handling is acceptable.

Risk: Global CLI installation and broad token handling can increase exposure if the installed package or credential storage is not reviewed.

Mitigation: Prefer pinned, reviewed CLI versions and least-privilege token handling for MINERU_TOKEN.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzlzyca/skills/doc-analysis)
- [MinerU homepage](https://mineru.net)
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU)
- [MinerU token management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and structured document Markdown output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api and, for full extraction, MINERU_TOKEN; document content may be processed by the MinerU/OpenDataLab service.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
