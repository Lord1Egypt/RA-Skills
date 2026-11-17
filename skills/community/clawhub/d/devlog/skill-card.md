## Description:

Generate narrative blog posts from AI coding session transcripts, selecting relevant sessions and producing agent-narrated builder's log, tutorial, or technical deep-dive Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lordshashank](https://clawhub.ai/user/lordshashank)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to turn AI coding-session transcripts into publishable developer blog posts that explain goals, decisions, implementation work, and collaboration dynamics. It can optionally publish generated Markdown to a supported platform after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private AI coding-session transcripts that may contain sensitive project details, prompts, file paths, or secrets.

Mitigation: Limit the requested project, platform, sessions, and time range before use, then review and redact the generated Markdown before sharing or publishing it.

Risk: The skill can publish transcript-derived posts online using account credentials.

Mitigation: Treat publishing as a separate high-impact step, confirm the exact destination and content first, and use temporary environment variables or a secret manager for tokens.

## Reference(s):

- [Blog Writing Guide](references/blog-writing-guide.md)
- [Claude Code Platform Reference](references/platforms/claude-code/claude-code.md)
- [Codex Platform Reference](references/platforms/codex/codex.md)
- [Gemini CLI Platform Reference](references/platforms/gemini-cli/gemini-cli.md)
- [OpenClaw Platform Reference](references/platforms/openclaw/openclaw.md)
- [OpenCode Platform Reference](references/platforms/opencode/opencode.md)
- [Hashnode Publishing Reference](references/publishing/hashnode/hashnode.md)
- [ClawHub Skill Page](https://clawhub.ai/lordshashank/skills/devlog)
- [Publisher Profile](https://clawhub.ai/user/lordshashank)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown blog post with optional Mermaid diagrams and a short completion report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local devlog file and, with user confirmation and credentials, publish the generated Markdown to Hashnode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
