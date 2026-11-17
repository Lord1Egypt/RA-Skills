## Description:

Provides guidance for installing and using the code-memory MCP server for semantic code search, AST-aware symbol lookup, documentation search, Git-history search, and dead-code discovery in local Git repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimdawdy-hub](https://clawhub.ai/user/jimdawdy-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill while working in local Git repositories to set up code-memory and retrieve code, documentation, symbol, history, and candidate dead-code information. It supports code understanding and investigation workflows, with direct file reads, tests, and review still needed before risky edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned third-party MCP server code and download executable model artifacts.

Mitigation: Pin package and model versions to reviewed releases, pre-vet or pre-cache artifacts in sensitive environments, and prefer reviewed source or package installs over standalone binaries.

Risk: The MCP server can index sensitive repository content, including secrets that are present in non-ignored files.

Mitigation: Run with repository-scoped filesystem access, review .gitignore before indexing, avoid indexing unignored secrets, and add code_memory.db* to .gitignore.

Risk: SSE transport is unauthenticated if exposed beyond localhost.

Mitigation: Keep SSE bound to 127.0.0.1 and place any broader access behind an authenticated reverse proxy.

Risk: Dead-code findings are heuristic and can miss dynamic references.

Mitigation: Verify candidates with direct code inspection, tests, and human review before deleting code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimdawdy-hub/skills/code-memory-skill)
- [Upstream project link declared in skill artifact](https://github.com/kapillamba4/code-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance references local indexing state, repository paths, MCP server configuration, and security controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
