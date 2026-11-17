## Description:

Generates Instagram and social-media card-news carousels from a topic by planning content, producing HTML card layouts, capturing Playwright screenshots, and preparing upload-ready images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyeuun97](https://clawhub.ai/user/gyeuun97)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketing teams, and social-media operators use this skill to turn a topic into an Instagram-style carousel workflow with content planning, HTML design guidance, screenshot generation, captions, and posting steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags hardcoded account branding that can publish or watermark content for a specific handle.

Mitigation: Require the user to set or confirm the target brand handle before generating or publishing assets.

Risk: The release evidence flags credential-backed Instagram posting and Telegram sharing steps.

Mitigation: Require explicit upload confirmation and keep publishing credentials outside generated card assets and prompts.

Risk: The release evidence flags the JPEG conversion path as unsafe.

Mitigation: Replace the shell-based conversion path with a non-shell image conversion API or disable JPEG conversion until reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyeuun97/skills/card-news-gen)
- [Pretendard webfont stylesheet](https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces image-generation workflow guidance for 1080x1350 card screenshots and optional PNG/JPEG output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
