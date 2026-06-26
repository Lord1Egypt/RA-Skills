## Description: <br>
Generate images using Coze AI platform with automatic Base64 encoding for inline preview from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pgyppp](https://clawhub.ai/user/pgyppp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to send text prompts to a configured Coze image project and receive generated images as inline Base64 data URIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, request metadata, and a bearer token can be sent to an external Coze endpoint, including a caller-configured URL without host validation. <br>
Mitigation: Use a limited Coze token, configure a trusted endpoint, project ID, and session ID, and avoid allowing untrusted callers to override api_url. <br>


## Reference(s): <br>
- [Coze Image Skill Payload](references/payload-shape.md) <br>
- [ClawHub skill page](https://clawhub.ai/pgyppp/coze-image) <br>
- [Repository listed in skill metadata](https://github.com/openclaw/skills) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Image data URI, Error object] <br>
**Output Format:** [JSON object containing a Base64 image data URI, MIME type, filename, source URL, optional answer text, or structured error fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include debug fields with endpoint, project ID, and session ID when debug mode is requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, package.json, and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
