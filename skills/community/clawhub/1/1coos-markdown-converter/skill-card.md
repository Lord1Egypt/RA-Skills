## Description: <br>
Converts files such as PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, images, audio, ZIP archives, EPub files, and YouTube URLs into formatted Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1coos](https://clawhub.ai/user/1coos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to convert local documents and media into Markdown and apply consistent formatting styles for repositories, notes, or downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses uvx to download and run the markitdown[all] converter dependencies. <br>
Mitigation: Install and use it only in environments where those converter dependencies are acceptable. <br>
Risk: Selected documents are parsed into Markdown, which can expose sensitive content or process untrusted file data. <br>
Mitigation: Avoid highly sensitive or untrusted files unless the conversion environment and converter behavior are understood. <br>
Risk: The artifact instructions mention main.ts while the packaged executable file is main.js. <br>
Mitigation: Confirm the packaged script path before execution or correct the invocation to match the artifact. <br>


## Reference(s): <br>
- [Supported Formats](references/supported-formats.md) <br>
- [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) <br>
- [ClawHub skill page](https://clawhub.ai/1coos/1coos-markdown-converter) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files plus concise status or error text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports style selection, output directory selection, convert-only mode, and optional config file overrides.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
