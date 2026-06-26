## Description: <br>
Formats a manuscript into a 5.5" x 8.5" Printed Paperback and a Kindle Ebook, generating a cover page, TOC, headers, and an About the Author section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vega6dev](https://clawhub.ai/user/vega6dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and authors use this skill to convert a raw text or Markdown manuscript into paperback and Kindle-ready book files with title, table of contents, chapter formatting, page numbering where appropriate, and an About the Author section. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and may run local typesetting commands to generate book files. <br>
Mitigation: Review proposed commands before execution and confirm python3, pandoc, and required PDF or EPUB tooling are installed. <br>
Risk: Generated output files may collide with existing files in the working directory. <br>
Mitigation: Run the skill from a dedicated manuscript folder and check proposed output filenames before writing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vega6dev/format-book) <br>


## Skill Output: <br>
**Output Type(s):** [files, code, shell commands, markdown, guidance] <br>
**Output Format:** [Paperback PDF or DOCX, Kindle EPUB, and a Markdown completion response with file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local manuscript output files named from the book title.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
