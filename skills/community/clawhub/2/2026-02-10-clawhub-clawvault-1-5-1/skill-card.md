## Description:

Structured memory system for OpenClaw agents. Context death resilience (checkpoint/recover), structured storage, Obsidian-compatible markdown, local semantic search, and session transcript repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pin-alt](https://clawhub.ai/user/pin-alt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use ClawVault to maintain local, structured memory across OpenClaw sessions, including checkpoint recovery, handoffs, typed memory capture, search, wiki-linking, and transcript repair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The global CLI and OpenClaw hook can persist local memory, index Markdown, and modify vault files.

Mitigation: Install only after reviewing this boundary, keep the vault in a dedicated directory, and avoid storing secrets or regulated data.

Risk: Bulk linking and session repair can modify many local files.

Mitigation: Use dry-run modes before bulk linking or repairing session transcripts.

Risk: An unpinned qmd installation can change search behavior or dependency exposure over time.

Mitigation: Use a pinned qmd version when installing or updating the search dependency.

Risk: The sleep workflow may prompt for a whole-repository git commit.

Mitigation: Use --no-git unless a repository-wide commit is explicitly intended.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [qmd](https://github.com/Versatly/qmd)
- [ClawVault npm package](https://www.npmjs.com/package/clawvault)
- [Auto-linking documentation](docs/auto-linking.md)
- [Context death resilience documentation](docs/context-death.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text with shell command examples and local vault file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist local memory, update Markdown files, index vault contents, and repair session transcript files.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json, CHANGELOG released 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
