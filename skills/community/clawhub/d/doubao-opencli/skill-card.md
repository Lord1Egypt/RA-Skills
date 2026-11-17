## Description:

doubao-opencli automates a logged-in Doubao session through opencli browser to support chat, batch questions, backups, image generation, AI podcast generation, PPT generation, and meeting summaries.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to automate Doubao tasks from a CLI or scripts, including asking questions, batch processing prompts, generating images, podcasts, and PPT files, and backing up conversations. It requires an existing Edge browser session logged into Doubao and the opencli browser bridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Doubao browser session.

Mitigation: Use a dedicated browser profile or account with only the data needed for the task, and review browser actions before running automation.

Risk: The skill can export chat history, uploaded document content, generated media, and logs to local plaintext outputs.

Mitigation: Avoid confidential documents, secrets, regulated data, and private chat history; delete generated outputs when no longer needed.

Risk: The security evidence flags unsafe command and browser-eval patterns.

Mitigation: Review and pin dependencies, remove Invoke-Expression usage, and safely serialize browser-eval input before broader use.

Risk: Generated podcasts trim the opening seconds by default, which may remove or alter source service branding or notices.

Mitigation: Confirm rights and service terms for generated media, and set trimming to zero when preserving original output is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclawzhangchong/skills/doubao-opencli)
- [Doubao chat](https://www.doubao.com/chat)
- [Doubao image creation](https://www.doubao.com/chat/create-image)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with PowerShell commands and generated local files such as Markdown, JSON, JPG, WAV, and PPTX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Edge logged into Doubao, opencli browser bridge, and optional ffmpeg for podcast trimming.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
