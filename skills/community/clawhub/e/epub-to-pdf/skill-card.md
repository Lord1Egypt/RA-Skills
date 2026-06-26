## Description: <br>
Convert EPUB ↔ PDF bidirectionally. EPUB→PDF preserves layout for analysis; PDF→EPUB compresses and reflows for distribution and ereaders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bunsdev](https://clawhub.ai/user/bunsdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and document workflow users use this skill to convert EPUB books or papers into PDFs for layout-preserving analysis, and to convert PDFs into reflowable EPUBs for distribution or ereaders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager and sudo examples can change the local system if run without review. <br>
Mitigation: Review installation commands before execution and install Calibre only through package sources you trust. <br>
Risk: Document conversion writes local output files and may overwrite or produce unexpected results when paths are reused. <br>
Mitigation: Confirm input and output filenames before running commands, then inspect converted files before relying on them. <br>
Risk: Converted documents may be redistributed without appropriate rights. <br>
Mitigation: Convert or distribute only documents you have permission to use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bunsdev/epub-to-pdf) <br>
- [Calibre Handbook](https://manual.calibre-ebook.com/) <br>
- [pdftotext manual page](https://manpages.ubuntu.com/manpages/xenial/man1/pdftotext.1.html) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local PDF or EPUB files through Calibre; users choose source documents and output paths.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
