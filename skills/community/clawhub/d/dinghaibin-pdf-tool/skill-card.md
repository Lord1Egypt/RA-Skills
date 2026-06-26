## Description: <br>
Helps agents work with local PDF files by merging PDFs, splitting PDFs, extracting pages or text, and reading PDF metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to perform basic local PDF operations such as merging files, splitting pages, extracting text, extracting individual pages, and inspecting metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing untrusted or unintended PDFs can expose local PDF parser behavior to malformed files. <br>
Mitigation: Use the skill only on PDFs the user intends to process locally, and install pypdf from a trusted source. <br>
Risk: Output paths can overwrite important local files. <br>
Mitigation: Choose explicit output paths and review them before running merge, page extraction, split, or text extraction commands. <br>
Risk: Some advertised image, conversion, and compression features are not implemented in this version. <br>
Mitigation: Treat the release as a basic merge, split, page extraction, text extraction, and metadata tool until those features are added and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/dinghaibin-pdf-tool) <br>
- [Publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local PDF or text files through the bundled command-line script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
