## Description:

博客写作助手基础版 helps users draft 800-1500 word blog posts, match personal writing-style examples, integrate research materials, and iterate on titles, structure, and paragraphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and individual creators use this skill to turn topics, research links, and writing-style samples into draft blog or marketing content for review and revision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags broad file, shell, and network/API behavior.

Mitigation: Install only with human supervision and restrict the agent to the files, commands, and network destinations needed for the writing task.

Risk: The skill includes credential-related setup and environment inspection examples.

Mitigation: Do not allow the agent to enumerate unrelated environment variables or handle credentials outside the specific API keys required by the task.

Risk: The skill claims local-only data handling while also describing callback URLs and external APIs.

Mitigation: Treat the local-data privacy claim as incomplete and review any callback or external API use before sending user content or research materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/blog-writer-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown and text with optional JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference input_params, output_format, callback_url, style samples, research links, and local agent configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
