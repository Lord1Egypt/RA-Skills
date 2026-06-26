## Description: <br>
Formats a manuscript into a 6" x 9" Printed Paperback and a Kindle Ebook, generating a cover page, TOC, headers, and an About the Author section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vega6dev](https://clawhub.ai/user/vega6dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authors, editors, and publishing workflows use this skill to turn raw text or Markdown manuscripts into a 6x9 paperback file and a Kindle EPUB. The skill requests missing title, author, or About the Author details before generating the outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated manuscript files are written into the current working directory and may conflict with similarly named files. <br>
Mitigation: Run the skill from the intended output folder, check for existing files with similar names, and use a clean book title before generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vega6dev/format-book-6x9) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with generated local PDF, DOCX, or EPUB files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written into the user's current working directory using filenames derived from the book title.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
