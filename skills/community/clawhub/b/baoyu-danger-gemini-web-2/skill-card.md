## Description:

Generates images and text via a reverse-engineered Gemini Web API with support for prompt-based text generation, image generation, reference images for vision input, and multi-turn conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nengnengz](https://clawhub.ai/user/nengnengz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call Gemini Web for text generation, image generation, vision input with reference images, and multi-turn conversation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a reverse-engineered Gemini Web client and depends on Google browser session cookies.

Mitigation: Review the skill before installation, use it only where this authentication approach is acceptable, and prefer a dedicated Chrome profile instead of a normal browsing profile.

Risk: Cached Google session cookies and conversation sessions may expose account or prompt data if left in shared or insecure storage.

Mitigation: Protect the configured data directory and cookie cache, delete cached credentials when no longer needed, and use `--cookie-path` or `GEMINI_WEB_COOKIE_PATH` to isolate storage.

Risk: The fallback runtime command can invoke an unpinned `npx -y bun` install path.

Mitigation: Install and manage a trusted Bun runtime directly in sensitive environments instead of relying on the fallback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nengnengz/skills/baoyu-danger-gemini-web-2)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-danger-gemini-web)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Plain text or JSON responses, with optional saved PNG image files and session JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save generated images to disk and persist multi-turn session state when requested.]

## Skill Version(s):

0.1.1 (source: server release evidence; artifact frontmatter reports 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
