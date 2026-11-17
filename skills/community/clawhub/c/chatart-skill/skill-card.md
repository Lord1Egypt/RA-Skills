## Description:

Use when user wants to generate videos, create images from text prompts, edit existing images with AI, or replace characters in videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatart-ai](https://clawhub.ai/user/chatart-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to create AI images, edit images, generate videos from text or reference media, replace characters in videos, and check ChatArt account usage through an authenticated ChatArt account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and provided media may be sent to ChatArt cloud services.

Mitigation: Do not use the skill with sensitive, regulated, or private media unless the deployment has approved ChatArt processing and data handling.

Risk: Credentials are stored locally and security evidence reports credential logging.

Mitigation: Review and remove credential logging before use with paid accounts or sensitive environments, and restrict access to local credential storage.

Risk: The skill can download and re-upload arbitrary URLs.

Mitigation: Limit use to trusted URLs and review generated network actions before processing private links or internal resources.

Risk: The skill includes high-priority reply rules that may override normal agent communication policy.

Mitigation: Review user-facing instruction rules before installation and keep platform safety, privacy, and disclosure requirements authoritative.

## Reference(s):

- [ChatArt Skill Page](https://clawhub.ai/chatart-ai/skills/chatart-skill)
- [ChatArt Website](https://www.chatartpro.com)
- [AI Image Module](references/ai_image.md)
- [Video Generation Module](references/video_gen.md)
- [Character Replace Module](references/video_mimic.md)
- [Authentication](references/auth.md)
- [User Account](references/user.md)
- [Error Handling](references/error_handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, status text, and generated media links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit prompts and user-provided media to ChatArt cloud services and may download generated media files when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
