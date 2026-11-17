## Description:

DocsForAI crawls documentation websites into structured, persistent Markdown and helps agents read targeted official docs for libraries, frameworks, SDKs, APIs, and tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dx2331lxz](https://clawhub.ai/user/dx2331lxz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to crawl and cache official documentation websites, then read targeted docs while implementing, configuring, debugging, or upgrading software.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party documentation URLs may be crawled and saved locally.

Mitigation: Use trusted documentation URLs, run crawls in an isolated workspace when appropriate, and review or remove cached docs that should not persist.

Risk: Crawl history can persist through MEMORY.md entries across sessions.

Mitigation: Review MEMORY.md after use and remove entries when crawl history should not be retained.

Risk: The fallback install command uses an unsafe system Python path and the package install is not pinned.

Mitigation: Prefer an isolated, pinned uv tool install and avoid the pip --break-system-packages fallback unless the environment owner approves it.

## Reference(s):

- [DocsForAI PyPI Package](https://pypi.org/project/docsforai/)
- [DocsForAI ClawHub Skill](https://clawhub.ai/dx2331lxz/skills/docsforai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local documentation files and optional persistent memory entries when the agent follows the workflow.]

## Skill Version(s):

0.7.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
