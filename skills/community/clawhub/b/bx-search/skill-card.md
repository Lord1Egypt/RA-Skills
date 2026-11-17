## Description:

Provides agent-facing web search, RAG grounding, news, images, videos, local places, and AI-synthesized answers through the Brave Search CLI (`bx`).

This skill is ready for commercial/non-commercial use.

## Publisher:

[brave-skills](https://clawhub.ai/user/brave-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route external search, documentation lookup, troubleshooting research, news, media, local-place lookup, and RAG grounding tasks through Brave Search CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries routed through `bx` may disclose secrets, private code, or sensitive context to Brave Search.

Mitigation: Use `bx` only for queries intended for Brave Search and avoid sending secrets or private code in search prompts.

Risk: The skill documents remote-script installation commands that execute downloaded shell or PowerShell content.

Mitigation: Do not run the pipe-to-shell or Invoke-Expression install commands directly; prefer verified, pinned release artifacts with checksums or signatures.

Risk: The skill broadly redirects search behavior through a local third-party executable.

Mitigation: Review the skill before installing and keep the built-in search tool available unless intentionally choosing Brave for the task.

## Reference(s):

- [Brave Search API](https://brave.com/search/api/)
- [Brave Search Skills Repository](https://github.com/brave/brave-search-skills/tree/main/clawhub/bx-search)
- [Brave Search Skills Issues](https://github.com/brave/brave-search-skills/issues)
- [Brave Search API Registration](https://api-dashboard.search.brave.com/register)
- [Brave Goggles Quickstart](https://github.com/brave/goggles-quickstart)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command examples and JSON response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the `bx` executable and `BRAVE_SEARCH_API_KEY`; context results can be token-budgeted with CLI flags.]

## Skill Version(s):

1.4.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
