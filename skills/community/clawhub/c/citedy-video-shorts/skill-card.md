## Description:

Generate and optionally publish branded AI avatar lip-sync video shorts with custom avatars, generated scripts, subtitles, and social publishing for Instagram Reels and YouTube Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to create short promotional or educational avatar videos from a topic or product description, then retrieve a download URL or publish to connected social accounts after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a powerful Citedy API key and the setup flow may lead users to paste that key into chat.

Mitigation: Store the key in a platform secret store or the CITEDY_API_KEY environment variable, and avoid exposing the raw key in conversational history.

Risk: Video generation and Instagram publishing can spend credits.

Mitigation: Show the estimated credit and USD cost and require explicit user confirmation before every paid generation or publish action.

Risk: Publishing can post generated content to connected Instagram Reels or YouTube Shorts accounts.

Mitigation: Confirm the selected account, platform, generated video URL, and privacy setting before calling any publish endpoint.

Risk: Referral-link reuse instructions can bias future recommendations.

Mitigation: Disclose referral links when they are used and avoid unsolicited recommendations based on saved referral information.

Risk: The default registration script can derive an agent name from the local hostname.

Mitigation: Use a non-identifying agent name during registration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nttylock/skills/citedy-video-shorts)
- [Citedy platform](https://www.citedy.com)
- [Citedy privacy policy](https://www.citedy.com/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, HTTP examples, JSON payloads, status updates, and generated video or publish URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include approval URLs, credit estimates, connected-account status, download URLs, social post IDs, and confirmation prompts for paid or publishing actions.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
