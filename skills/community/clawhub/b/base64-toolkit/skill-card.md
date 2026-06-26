## Description: <br>
Base64 encoding and decoding toolkit. Encode/decode text, URL-safe Base64, and image to Base64 conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeter226](https://clawhub.ai/user/freeter226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to encode and decode Base64 text, work with URL-safe Base64 strings, and convert image files into Base64 data URIs for API, URL, and embedding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Base64 output may expose credentials, tokens, private files, or JWT payloads when copied into shared terminals, logs, or tickets. <br>
Mitigation: Use the tool only with data safe to display, and avoid processing secrets or private files in shared environments. <br>
Risk: Base64 encoding may be mistaken for encryption. <br>
Mitigation: Treat encoded output as reversible text and use appropriate encryption or secret-management controls for sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freeter226/base64-toolkit) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands] <br>
**Output Format:** [JSON printed to stdout with encoded or decoded strings, URL-safe strings, or image data URIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes only user-provided strings or local files; no external dependencies are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
