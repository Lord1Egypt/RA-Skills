## Description: <br>
Complete integration guide for the Fliz REST API, an AI-powered video generation platform that transforms text content into professional videos with voiceovers, AI-generated images, and subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jb-fliz](https://clawhub.ai/user/jb-fliz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to integrate with the Fliz REST API, create videos from text, monitor generation status, translate or duplicate videos, and handle completion webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source text, and video metadata are sent to the external Fliz API. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive content in prompts, and review Fliz account and data-handling requirements before deployment. <br>
Risk: The Fliz API key can grant access to create and manage video resources. <br>
Mitigation: Keep the key in environment variables such as FLIZ_API_KEY, avoid committing credentials, and rotate exposed or unneeded keys. <br>
Risk: The sample webhook handler is example code and records received payloads without production-grade controls. <br>
Mitigation: Add authentication, HTTPS, payload validation, redaction, retention limits, and durable storage policies before deploying webhook handling. <br>


## Reference(s): <br>
- [Fliz API Reference](references/api-reference.md) <br>
- [Fliz API Enum Values](references/enums-values.md) <br>
- [Fliz API Documentation](https://app.fliz.ai/api-docs) <br>
- [Fliz Website](https://fliz.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/jb-fliz/fliz-ai-video-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and Python, Node.js, cURL, and Flask code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Fliz API request payloads, polling guidance, webhook handling patterns, and generated video identifiers or URLs returned by the external Fliz API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
