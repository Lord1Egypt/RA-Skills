## Description:

Audits Claude Code session memory as a knowledge graph, detecting broken wikilinks, orphan pages, hub nodes, and bridge candidates, and guiding link repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Claude Code users, and maintainers of Markdown-based personal memory systems use this skill to inspect session memory folders, identify graph-health issues in wikilinks, and plan or perform link repairs with follow-up checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect persistent Claude memory folders that may contain private or sensitive session notes.

Mitigation: Run the audit only on memory folders the user is comfortable inspecting and avoid sharing audit output that exposes sensitive memory contents.

Risk: Suggested or scripted link repairs can bulk-edit persistent memory files and introduce incorrect links or overwrite useful context.

Mitigation: Require a diff, backup, and explicit confirmation before applying repairs, then rerun the audit to verify broken links and orphan pages.

Risk: Installing mutable executable code can expose users to changes after initial review.

Mitigation: Install only a reviewed ClawHub package or a pinned, verified commit.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/heavenchenggong/skills/claude-memory-graph-audit)
- [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance and terminal-style shell output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize memory graph counts, broken links, orphan pages, hub nodes, bridge candidates, and proposed link repairs.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
