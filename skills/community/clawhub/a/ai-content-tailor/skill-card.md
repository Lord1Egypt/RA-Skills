## Description:

Repurposes one article into platform-specific versions for WeChat Official Account, Xiaohongshu, Zhihu, and Douyin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utopiabenben](https://clawhub.ai/user/utopiabenben)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators and operators use this skill to turn a Markdown or text article into channel-ready drafts for WeChat Official Account, Xiaohongshu, Zhihu, and Douyin while preserving the source article's main ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and uninstaller behavior can write or delete files outside the skill directory.

Mitigation: Review install.sh and uninstall.sh before use, verify the exact .env and output paths they affect, and avoid running uninstall.sh until the BASE_DIR path issue is fixed or manually checked.

Risk: Input articles are sent to OpenAI for rewriting.

Mitigation: Use only articles you are comfortable sending to OpenAI, and remove sensitive drafts, secrets, or confidential material before processing.

Risk: The provided setup installs Python packages globally and creates a plaintext .env template for the API key.

Mitigation: Prefer a virtual environment and store the API key in a securely permissioned environment file or shell environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/utopiabenben/skills/ai-content-tailor)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown and plain text content, optionally written as platform-specific Markdown files or shown in a terminal preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenAI API key; supports single-article and batch processing, platform selection, model selection, tone selection, and preview mode.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
