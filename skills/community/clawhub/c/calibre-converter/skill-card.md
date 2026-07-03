## Description: <br>
Calibre Converter helps an agent request conversion of books or documents already registered in Calibre by identifying the item, confirming the target format, and calling a local calibre-openclaw-server API to convert, register, and report the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[carlosdelfino](https://clawhub.ai/user/carlosdelfino) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users operating a Calibre-based library use this skill to ask an agent to convert a uniquely identified ebook or document into a requested format and return the conversion status, generated format, and registered output path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a broader local Calibre gateway that can mutate the library, index content, and manage downloads. <br>
Mitigation: Install only when those gateway capabilities are intended, review configuration before use, and keep destructive or automated features disabled unless needed. <br>
Risk: Network-facing features and third-party integrations can expose content metadata, files, or API keys if configured loosely. <br>
Mitigation: Bind the service to localhost, require a strong API key, avoid putting API keys in URLs, and enable VirusTotal, OpenLibrary, direct download, or network binding features only after accepting their privacy and network exposure. <br>
Risk: Format conversion, especially PDF to EPUB, can produce layout, table-of-contents, or page-break issues. <br>
Mitigation: Review converted files in Calibre or a compatible reader before relying on the output. <br>


## Reference(s): <br>
- [Calibre Converter skill page](https://clawhub.ai/carlosdelfino/calibre-converter) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Calibre gateway README](artifact/calibre-openclaw-gateway/README.md) <br>
- [OpenLibrary](https://openlibrary.org) <br>
- [VirusTotal](https://www.virustotal.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON API payloads and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report server-returned status, title, source format, target format, registered output path, and conversion errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
