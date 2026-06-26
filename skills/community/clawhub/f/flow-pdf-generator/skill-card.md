## Description: <br>
Generates styled PDF documents from structured JSON data, including titles, tables, lists, highlights, images, and page breaks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flexrox](https://clawhub.ai/user/flexrox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn structured JSON content into styled PDF reports or exports, including documents with text, headings, tables, lists, highlights, images, and page breaks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted JSON or image paths may cause the local helper to read unexpected local files or fail during PDF generation. <br>
Mitigation: Use trusted input files, review image paths before execution, and run the helper in a virtual environment. <br>
Risk: A caller-controlled output path can overwrite an unintended local PDF file. <br>
Mitigation: Check the output path before generation and write into a project-specific directory. <br>


## Reference(s): <br>
- [PDF Generator Schema Reference](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/flexrox/flow-pdf-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with JSON examples and shell commands; generated artifact is a PDF file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads JSON data and optional local image paths, then writes a PDF to the requested output path.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
