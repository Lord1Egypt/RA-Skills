## Description: <br>
AI PDF Converter helps an agent convert PDFs to Markdown, HTML, LaTeX, DOCX, or JSON using the MinerU API with layout analysis, table recognition, formula detection, OCR, and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to guide an agent through installing and running mineru-open-api for single-file or batch PDF conversion. It is suited for converting scanned documents, academic papers, reports, contracts, and multilingual PDFs into editable or structured formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents may be processed by MinerU or its API, which can expose confidential, regulated, legal, or financial documents to an external service. <br>
Mitigation: Use only documents approved for external processing and avoid confidential or regulated PDFs unless policy permits MinerU processing. <br>
Risk: The skill depends on the third-party mineru-open-api CLI and MinerU service. <br>
Mitigation: Install and run it only in environments where the package and service are trusted. <br>
Risk: Converted files are written locally and may include sensitive document content. <br>
Mitigation: Choose explicit input files and output folders, then review generated files before sharing or using them downstream. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands; converted files may be Markdown, HTML, LaTeX, DOCX, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes converted files to user-selected or default local output folders.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
