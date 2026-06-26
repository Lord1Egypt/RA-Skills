## Description: <br>
Remove watermarks from local image files or remote image URLs through the Airemovewatermark API, with support for task polling and credit checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isees](https://clawhub.ai/user/isees) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to process images they own or are authorized to edit through Airemovewatermark, poll asynchronous tasks, check credits, and optionally save completed results locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image files or image URLs are sent to the Airemovewatermark remote service for processing. <br>
Mitigation: Install and use the skill only if you trust Airemovewatermark with the selected images, and confirm the user wants to process each image through the remote API. <br>
Risk: The skill depends on an API key and supports overriding the API base URL. <br>
Mitigation: Keep API_KEY private, avoid untrusted API_BASE_URL or --base-url values, and continue only after credential errors are fixed. <br>
Risk: Watermark removal can be inappropriate when the user lacks rights to edit the image. <br>
Mitigation: Use the skill only for images the user owns or is authorized to edit. <br>


## Reference(s): <br>
- [AI Remove Watermark on ClawHub](https://clawhub.ai/isees/airemove-watermark) <br>
- [Airemovewatermark OpenClaw documentation](https://airemovewatermark.net/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script returns structured JSON and can save an image file when download is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires API_KEY. Local image files or image URLs are sent to a remote service, and local downloads are opt-in.] <br>

## Skill Version(s): <br>
0.1.7 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
