## Description: <br>
Converts document files (.pdf, .docx, .xlsx, .pptx) to Markdown using the `markitdown` command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ytyytt520](https://clawhub.ai/user/ytyytt520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and other agent users use this skill to convert user-selected PDF, DOCX, XLSX, and PPTX files into Markdown text for reading, summarization, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted document contents may be exposed in the agent conversation. <br>
Mitigation: Use the skill only on documents whose contents are intended to be shared with the agent session. <br>
Risk: The skill depends on the local `markitdown` command and inherits trust from that installed converter. <br>
Mitigation: Install and run it only in environments where the local converter is trusted, and review converted output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ytyytt520/doc-converter) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text produced by a local document conversion command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects an input file path and relies on the local `markitdown` command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
