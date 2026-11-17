## Description:

Response speed optimizer - implements reply-first-then-process, parallel tool calls, and memory file caching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opendolph](https://clawhub.ai/user/opendolph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reduce perceived response latency through immediate acknowledgments, parallel execution of independent work, and cached access to selected workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may copy sensitive agent and user memory files into a predictable plaintext cache.

Mitigation: Install only in trusted, sandboxed workspaces and narrow or protect the cache before use.

Risk: The bundled parallel executor exports a helper that can run arbitrary shell commands.

Mitigation: Remove or restrict the shell-command executor unless the workspace and callers are fully trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/opendolph/skills/fast-response-optimizer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with JavaScript examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cache refresh, status, and timestamp-management commands; cache contents are truncated to 5000 characters per file by the provided cache manager.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
