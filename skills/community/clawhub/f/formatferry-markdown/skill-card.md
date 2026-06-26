## Description: <br>
Local-first document-to-Markdown converter supporting HTML, DOCX, PDF, XLSX, CSV, JSON, XML, and PPTX inputs with GitHub, CommonMark, Slack, Discord, Reddit, Confluence, R Markdown, and custom Markdown outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[britrik](https://clawhub.ai/user/britrik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert local documents, pasted HTML, web URLs, or batches of files into Markdown tailored for common publishing and collaboration platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL extraction can send sensitive or internal link content to server-side processing. <br>
Mitigation: Use local file or stdin conversion for private material, and avoid --url unless server-side processing is acceptable. <br>
Risk: Optional API and license keys may be used for URL extraction and premium batch mode. <br>
Mitigation: Prefer environment variables or temporary credentials until the CLI documents how stored credentials are protected. <br>
Risk: The skill depends on an external Node.js CLI being installed and trusted. <br>
Mitigation: Install only from trusted package sources and review conversion commands before execution. <br>


## Reference(s): <br>
- [FormatFerry homepage](https://github.com/britrik/FormatFerry) <br>
- [FormatFerry CLI Reference](references/cli-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/britrik/formatferry-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown text or Markdown files with optional shell commands for conversion workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports selectable Markdown flavours and optional file, stdin, URL, or batch inputs.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
