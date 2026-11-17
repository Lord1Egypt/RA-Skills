## Description:

Generate viral TikTok photo carousels using AI with a 6-slide formula and a learning loop for continuous improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g0atfac3](https://clawhub.ai/user/g0atfac3)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, content creators, and influencers use this skill to plan TikTok photo carousels, generate AI image prompts or images, and track post performance for future optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok cookies are treated as full account credentials and may be stored locally in plaintext during the posting flow.

Mitigation: Avoid using an important TikTok account, review the posting flow before running it, and prefer a delegated posting method or an OS secret manager for credential storage.

Risk: Browser automation can act on a TikTok account using the provided session cookies.

Mitigation: Run posting commands only after reviewing the carousel content and confirming that automated account activity is acceptable for the account and platform policies.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/g0atfac3/skills/g0atbot-tiktok-carousel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples and JSON-backed carousel records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY for image generation and TIKTOK_COOKIES for posting workflows. Generated records may include carousel metadata, slide prompts, image URLs, and performance metrics.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
