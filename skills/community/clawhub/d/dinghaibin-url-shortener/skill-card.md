## Description: <br>
Create and manage short URLs with custom aliases and tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to create local short aliases for long URLs, optionally with custom aliases, QR code files, and basic saved-link statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored URLs may contain tokens, private query parameters, or sensitive internal addresses. <br>
Mitigation: Use the skill as a local helper and avoid saving sensitive URLs because mappings are written to ~/.url_shortener.json. <br>
Risk: QR code output can overwrite an existing file if the chosen output path already exists. <br>
Mitigation: Choose QR output paths deliberately and check existing files before writing QR code images. <br>
Risk: The helper is not designed to operate as a hosted short-link service. <br>
Mitigation: Keep usage local and do not rely on it for public redirect hosting or production analytics. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output is plain text with optional PNG QR code files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores URL mappings locally in ~/.url_shortener.json when the helper script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
