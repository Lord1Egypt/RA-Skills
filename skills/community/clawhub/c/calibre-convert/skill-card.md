## Description: <br>
Use this skill when the user wants to convert ebook or document files between formats with Calibre, including EPUB to PDF, Markdown to EPUB, MOBI to EPUB, AZW3 to EPUB, HTML to EPUB, DOCX to EPUB, and similar source/target format pairs supported by ebook-convert. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shake](https://clawhub.ai/user/shake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supported ebook and document files with a local Calibre ebook-convert installation, including common EPUB, PDF, Markdown, MOBI, AZW3, HTML, and DOCX workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion reads the selected source file and writes the selected output path through Calibre, which can overwrite existing files. <br>
Mitigation: Confirm the source file, destination path, and any extra Calibre options before execution. <br>
Risk: A missing Calibre ebook-convert binary or unsupported format pair can cause conversion failure. <br>
Mitigation: Check ebook-convert availability and verify the output file exists before reporting success. <br>


## Reference(s): <br>
- [Calibre Convert Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or overwrite a user-selected output file through Calibre.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
