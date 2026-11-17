## Description:

Generate images with the user's own Chrome session and Gemini web UI for article covers, illustrations, and social media visuals when the user explicitly requests image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiao1yin2he3](https://clawhub.ai/user/jiao1yin2he3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate Gemini web image generation through their own authorized Chrome session, then download and copy generated image assets for articles, covers, social posts, and product or concept visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives temporary browser automation control over a Chrome profile that may already be logged in to Gemini.

Mitigation: Use a dedicated low-privilege Chrome profile, keep remote debugging local, and stop the MCP server after use.

Risk: The browser-control dependency is invoked with a mutable `@latest` package reference.

Mitigation: Pin or review the browser-control dependency before installation or execution.

Risk: Downloaded image handling is weakly scoped and can confuse newly generated assets with other files in Downloads.

Mitigation: Verify downloaded files before copying them from Downloads and copy only assets generated for the current user-requested task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiao1yin2he3/skills/gemini-browser-image)
- [Gemini Web UI](https://gemini.google.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with PowerShell and mcporter command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through browser-based image generation and local download handling; generated image files are produced by Gemini in the user's browser session.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
