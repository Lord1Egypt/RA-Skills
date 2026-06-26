## Description: <br>
Helps agents provide python-docx guidance and examples for creating, reading, and modifying Word .docx documents with text, paragraphs, tables, styles, and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adtomato](https://clawhub.ai/user/adtomato) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate practical python-docx snippets and guidance for working with .docx files, including document creation, reading, tables, formatting, images, and existing-document edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands and code snippets that install packages and read or write local .docx and image files. <br>
Mitigation: Review generated commands and file paths before execution, and run examples in a controlled project directory. <br>
Risk: The artifact notes that complex formatting can vary across Word versions. <br>
Mitigation: Validate generated documents in the target Word processor before relying on layout or style fidelity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adtomato/docx-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples target python-docx and .docx files; .doc format is not supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
