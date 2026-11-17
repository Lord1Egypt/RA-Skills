## Description:

Posts text, images, videos, and long-form X Articles to X through a real Chrome browser session, with support for preview-first composition and optional live publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praguepp](https://clawhub.ai/user/praguepp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and social-media operators use this skill to compose X posts, quote posts, video posts, and long-form articles from an agent-assisted workflow while retaining browser review before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real logged-in X session and may publish live posts when submission is enabled.

Mitigation: Use a dedicated Chrome profile, keep preview mode as the default, review every composed post in the browser, and use --submit only for intentional live publishing.

Risk: Markdown and media inputs can affect what is posted and may include local paths or remote image downloads.

Mitigation: Use trusted Markdown and media files, inspect generated article content before publishing, and avoid untrusted paths or remote assets.

Risk: Chrome automation and debug-process handling can affect local browser sessions.

Mitigation: Run the pre-flight permission check, isolate the browser profile, and avoid automatic termination of Chrome debugging processes unless that behavior is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/praguepp/skills/baoyu-post-to-x-enhanced)
- [OpenClaw Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-x)
- [Regular Posts Guide](references/regular-posts.md)
- [X Articles Guide](references/articles.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and browser automation status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open a local Chrome session, prepare draft content, upload media, and publish only when the user explicitly requests live submission.]

## Skill Version(s):

3.0.0 (source: frontmatter, ClawHub release, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
