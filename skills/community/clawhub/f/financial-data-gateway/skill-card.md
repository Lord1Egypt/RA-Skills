## Description:

Downloads Chinese A-share annual report PDFs from CNInfo and extracts structured consolidated financial statement data for downstream financial analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shihugh5-lab](https://clawhub.ai/user/shihugh5-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and financial analysts use this skill to download public Chinese A-share annual report PDFs, extract balance sheet, income statement, and cash flow data, and prepare validated JSON for financial databases or analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends PDF page summaries to the OpenAI API for page-location assistance.

Mitigation: Avoid confidential or sensitive PDFs unless that external processing is acceptable for the use case.

Risk: CNInfo discovery endpoints are documented as plaintext HTTP, which can affect transport confidentiality and integrity.

Mitigation: Use an isolated environment and validate downloaded report metadata and contents before relying on extracted data.

Risk: Financial statement extraction can produce incorrect or incomplete structured data due to PDF layout, scanner quality, or source-report complexity.

Mitigation: Review the generated validation fields and verify key figures against the source report before downstream analysis.

Risk: Runtime dependencies may change behavior across installations.

Mitigation: Pin dependencies and run the skill in a controlled environment before production use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/shihugh5-lab/skills/financial-data-gateway)
- [CNInfo announcement search endpoint](http://www.cninfo.com.cn/new/hisAnnouncement/query)
- [CNInfo company search endpoint](http://www.cninfo.com.cn/new/information/topSearch/query)
- [CNInfo static report downloads](https://static.cninfo.com.cn/{adjunctUrl})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead the agent to create downloaded PDF files and structured financial statement JSON.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
