## Description: <br>
Extract Tables From Pdf helps agents extract structured tables from native or scanned PDF files and URLs using MinerU's table detection and OCR capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, financial teams, and researchers use this skill to extract table data from PDF reports, papers, and documents for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF files and URLs processed through this skill may be sent to MinerU's external service. <br>
Mitigation: Avoid confidential, regulated, or proprietary documents unless MinerU's terms, retention policy, and privacy controls meet the deployment requirements. <br>
Risk: The skill requires a MinerU token for extraction and crawl operations. <br>
Mitigation: Store MINERU_TOKEN as a secret or environment variable and do not commit it to source control or shared prompts. <br>
Risk: Table extraction quality can vary for scanned files, complex layouts, merged cells, and nested tables. <br>
Mitigation: Review extracted table structure before using the output for financial, research, or operational decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mzlzyca/extract-tables-from-pdf) <br>
- [MinerU homepage](https://mineru.net) <br>
- [MinerU API token management](https://mineru.net/apiManage/token) <br>
- [MinerU GitHub repository](https://github.com/opendatalab/MinerU) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mineru-open-api output, which may be written to stdout or to an output directory depending on flags.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
