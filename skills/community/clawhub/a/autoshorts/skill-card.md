## Description:

Turn long videos into viral TikTok, Instagram Reels & YouTube Shorts with a daily human-gated pipeline that transcribes with Whisper, uses Gemini 3 Flash to select short-form moments, renders clips with hook overlays, and schedules approved posts through Upload-Post.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutonby](https://clawhub.ai/user/mutonby)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, and agent users use this skill to turn already prepared vertical long-form videos into short-form clip candidates, review rendered outputs, and schedule approved posts across TikTok, Instagram Reels, and YouTube Shorts. It is intended for a human-in-the-loop publishing workflow rather than fully autonomous posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires Gemini and Upload-Post credentials and may store them in a local plaintext .env file.

Mitigation: Configure secrets through a protected terminal or local secret manager, restrict .env file permissions, avoid pasting keys into chat, and rotate any keys exposed in conversation logs.

Risk: Full videos and transcripts are sent to Gemini for multimodal clip selection.

Mitigation: Use the skill only with videos the user is comfortable sending to Gemini, and avoid processing sensitive, private, or regulated footage without an approved data-handling review.

Risk: Upload-Post credentials can schedule content to connected social media accounts.

Mitigation: Review connected Upload-Post profiles, keep the human approval and dry-run steps in place, and use TikTok draft mode unless direct posting is explicitly required.

Risk: Learning and history files can retain persistent local records of clip decisions and performance analytics.

Mitigation: Treat the learning directory as persistent local history and manage access, retention, and backups according to the user's privacy expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mutonby/skills/autoshorts)
- [Skill homepage](https://github.com/mutonby/skill-autoshorts)
- [Upload-Post](https://upload-post.com)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON command output, shell commands, rendered media file paths, and platform-specific publishing copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local transcript, clip, preview, state, and learning files; approved clips may be scheduled through Upload-Post after human confirmation.]

## Skill Version(s):

2.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
