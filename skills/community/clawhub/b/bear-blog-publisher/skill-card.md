## Description:

Publish blog posts to Bear Blog platform. Supports user-provided markdown, AI-generated content, and auto-generated diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cattalk2](https://clawhub.ai/user/cattalk2)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to publish Markdown posts to Bear Blog, optionally generate draft content with OpenAI or Kimi, and create simple architecture diagrams for technical posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real Bear Blog account passwords and can publish public content.

Mitigation: Use isolated credentials, avoid passing passwords in chat or command-line arguments, and require manual confirmation before publishing.

Risk: Plaintext config storage is supported as an optional authentication method.

Mitigation: Prefer environment variables or runtime parameters; if a config file is used, restrict permissions to owner-only access.

Risk: Optional AI generation sends prompts to OpenAI or Kimi.

Mitigation: Avoid including secrets or sensitive unpublished material in prompts sent to external model providers.

Risk: The diagram feature uses local temporary files and Chromium with reduced browser sandboxing.

Mitigation: Avoid untrusted diagram text until HTML escaping, temp-file handling, and browser sandboxing are fixed.

## Reference(s):

- [Bear Blog](https://bearblog.dev/)
- [ClawHub Skill Page](https://clawhub.ai/cattalk2/skills/bear-blog-publisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown, status strings, published URLs, configuration snippets, shell commands, and generated diagram image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Bear Blog, OpenAI, Kimi, and local Playwright depending on the requested workflow and configured credentials.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
