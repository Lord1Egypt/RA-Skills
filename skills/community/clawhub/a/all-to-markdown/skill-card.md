## Description: <br>
Converts files and URLs, including documents, spreadsheets, slides, images, audio, web pages, and archives, into Markdown for agent analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert user-provided files or URLs into Markdown so the resulting content can be read, summarized, searched, or analyzed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads local files and can fetch URLs supplied by the user, which may expose sensitive local content or internal URLs if used carelessly. <br>
Mitigation: Run it only on user-approved file paths and URLs, and avoid internal or private URLs unless the user has confirmed that access is appropriate. <br>
Risk: Optional plugins or OPENAI_API_KEY-backed features may send relevant content to external services. <br>
Mitigation: Enable plugins or OpenAI-backed image description only when the plugin or external processing path is trusted and the user accepts the data handling implications. <br>
Risk: Untrusted archives may contain unexpected files for conversion. <br>
Mitigation: Use caution with archives from untrusted sources and review extracted Markdown before relying on it for downstream analysis. <br>


## Reference(s): <br>
- [Microsoft MarkItDown](https://github.com/microsoft/markitdown) <br>
- [All to Markdown on ClawHub](https://clawhub.ai/sipingme/all-to-markdown) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, files] <br>
**Output Format:** [Markdown streamed to stdout or written to a file when the -o option is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the markitdown CLI; optional plugins and OpenAI-backed image descriptions are available only when explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
