## Description: <br>
User-approved 96Push desktop client publishing helper that queries platforms and accounts, creates content, inspects platform rules, and publishes only after explicit confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xsxs89757](https://clawhub.ai/user/xsxs89757) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to work with a local 96Push desktop client for multi-platform social publishing workflows. It helps inspect connected accounts and platform rules, prepare article, image, or video content, upload supported images, and submit approved publish, queue, or settings actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved actions can publish, delete, cancel queued publishing, upload files, or change platform settings for logged-in social media accounts. <br>
Mitigation: Require explicit approval for each high-impact action and review the content ID or title, content type, target accounts and platforms, draft or live state, visibility, and settings before execution. <br>
Risk: PUSH_API_KEY is a sensitive credential for the 96Push workflow. <br>
Mitigation: Keep the key local in an environment variable or local .env file and avoid echoing or pasting it into chat. <br>
Risk: Uploading a file sends that runtime-accessible file to 96Push. <br>
Mitigation: Upload only files the user intends to send to 96Push and require immediate approval before upload. <br>
Risk: Repeated publish attempts can create duplicate or conflicting browser automation tasks. <br>
Mitigation: Submit one publish command per approved content and account batch, then report the result or ask the user to check the local 96Push client if a timeout occurs. <br>


## Reference(s): <br>
- [96Push homepage](https://push.96.cn) <br>
- [ClawHub skill page](https://clawhub.ai/xsxs89757/96push) <br>
- [Platform settings reference](references/platform-settings.md) <br>
- [Platform rules index](references/platform-rules/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the 96Push API through a local desktop-client workflow when the user has configured PUSH_API_KEY and approved high-impact actions.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
