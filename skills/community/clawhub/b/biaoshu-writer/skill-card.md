## Description: <br>
Biaoshu Writer is a bid technical proposal drafting skill that parses txt, pdf, docx, and xlsx tender files and helps generate scoring-aligned Word documents for transportation engineering bids. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuliwenjing](https://clawhub.ai/user/wuliwenjing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External bid writers, proposal teams, and developers use this skill to parse tender materials, draft technical proposal sections, check chapter word counts, merge chapter files, and convert Markdown drafts into formatted Word bid documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-authorship masking and document metadata rewriting may conflict with tender rules or organizational policy. <br>
Mitigation: Use those behaviors only when the tender rules and the organization explicitly allow them; otherwise avoid AI-trace removal and metadata-masking steps for real submissions. <br>
Risk: The skill processes bid files and writes generated outputs to user-controlled project paths. <br>
Mitigation: Use only bid files the user is authorized to process, change output paths before use, and review generated content before submission. <br>
Risk: Dependency and font installation relies on external package and font sources. <br>
Mitigation: Install Python packages and SimSun fonts from trusted sources and review the installation script before running it. <br>


## Reference(s): <br>
- [Humanizer-zh reference](references/humanizer-zh.md) <br>
- [iLovePDF OCR](https://www.ilovepdf.com/ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, generated proposal text, shell commands, and Word document files produced through bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python dependencies python-docx, pdfplumber, openpyxl, and PyPDF2; generated Word output may include document metadata rewriting.] <br>

## Skill Version(s): <br>
5.4.0 (source: server release metadata and skill changelog, released 2026-04-14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
