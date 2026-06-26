## Description: <br>
Retrieves Markdown content from validated 草料二维码 qr61.cn short links by fetching the corresponding .md endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nbjedi](https://clawhub.ai/user/nbjedi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users use this skill to retrieve the Markdown version of a 草料二维码 short-link page from validated qr61.cn URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves content from qr61.cn, so the remote site or redirect target can observe request metadata such as IP address and headers. <br>
Mitigation: Use it only for intended qr61.cn links and avoid fetching sensitive or private URLs. <br>
Risk: Fetched Markdown may contain untrusted links or instructions. <br>
Mitigation: Review the returned Markdown before following links or acting on embedded instructions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nbjedi/caoliao-qrcode-markdown-content-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown content or a plain-text status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches validated qr61.cn links with redirects enabled and returns remote content as untrusted Markdown.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
