## Description: <br>
Extracts detailed financial statement note tables from China A-share annual-report PDFs for analyses that need data beyond the primary financial statements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts and data engineers use this skill to locate and extract financial note tables from Chinese A-share annual reports for CapEx, receivables aging, goodwill impairment, related-party transactions, and R&D expense analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes local annual-report PDFs using host Python tools. <br>
Mitigation: Keep input PDFs in a limited project folder and install pdfplumber or OCR tools only from trusted sources. <br>
Risk: Downloaded financial reports may be untrusted or unsuitable for broad processing. <br>
Mitigation: Review downloaded reports before broad processing. <br>
Risk: Multi-page tables or scanned PDFs can produce incomplete extraction results. <br>
Mitigation: Review extracted tables, merge split tables when needed, and use OCR only after confirming the PDF requires it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python code and structured data output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides extraction into Dict[List] or DataFrame-style structures from local annual-report PDFs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
