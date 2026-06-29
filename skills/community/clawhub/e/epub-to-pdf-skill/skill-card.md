## Description: <br>
Convert EPUB e-books to PDF using ebooklib and WeasyPrint with proper CJK font support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellobigbean](https://clawhub.ai/user/hellobigbean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert trusted EPUB e-books into PDF files, including documents with Chinese, Japanese, or Korean text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires additional system and Python dependencies for EPUB parsing and PDF rendering. <br>
Mitigation: Install the listed dependencies only in environments where adding WeasyPrint, ebooklib, BeautifulSoup, and lxml is acceptable. <br>
Risk: EPUB conversion processes embedded document HTML and image references. <br>
Mitigation: Convert only EPUB files from trusted sources and review generated PDFs before relying on them. <br>
Risk: The conversion script writes to the output path supplied by the user. <br>
Mitigation: Use non-sensitive, intended output paths and avoid overwriting important files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and a Python conversion script that writes PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeasyPrint, ebooklib, BeautifulSoup, lxml, and compatible CJK font files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
