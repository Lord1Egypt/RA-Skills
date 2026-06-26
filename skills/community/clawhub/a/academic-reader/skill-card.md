## Description: <br>
PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other users use this skill to convert local PDFs or PDF URLs into Markdown for reading, extraction, summarization, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDF files or PDF links are sent to MinerU for conversion and may contain sensitive content. <br>
Mitigation: Use only documents appropriate for third-party processing; avoid confidential, regulated, or sensitive business documents unless MinerU's privacy and retention practices meet requirements. <br>
Risk: Images, tables, formulas, or larger documents may be incomplete or replaced with placeholders in the Markdown output. <br>
Mitigation: Review the generated Markdown against the source PDF before relying on it, and use the authenticated extraction flow only when higher-fidelity processing is approved. <br>


## Reference(s): <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with CLI command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MinerU Open API through the mineru-open-api CLI; flash extraction is limited to 10 MB or 20 pages per document.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
