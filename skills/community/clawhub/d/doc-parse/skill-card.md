## Description: <br>
Parse Word documents into structured Markdown using MinerU while preserving headings, lists, tables, paragraphs, and document hierarchy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content managers use this skill to extract structured Markdown from Word documents for downstream processing, content analysis, and document migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some parsing workflows may send document data or URLs to MinerU/OpenDataLab services. <br>
Mitigation: Avoid confidential files, secrets, customer data, or internal-only URLs unless the provider's data handling and retention practices are acceptable for the use case. <br>
Risk: The skill depends on the external mineru-open-api binary and a MINERU_TOKEN for token-required parsing modes. <br>
Mitigation: Install mineru-open-api from the declared package source and provide MINERU_TOKEN only in environments approved for document parsing. <br>


## Reference(s): <br>
- [Doc Parse on ClawHub](https://clawhub.ai/mzlzyca/doc-parse) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured Markdown to stdout or save it to an output directory through mineru-open-api.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
