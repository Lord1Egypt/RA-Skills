## Description:

Claw Recall indexes local agent conversations and configured external sources into searchable memory so agents can recover context after compaction and search prior work across OpenClaw and Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodbland2021](https://clawhub.ai/user/rodbland2021)

### License/Terms of Use:


## Use Case:

Developers and agent users use Claw Recall to search session transcripts, recover pre-compaction context, and share findings across agents. When configured, it can also search captured thoughts, markdown files, Gmail, Google Drive, and Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private agent transcripts and external sources may be centralized into a searchable local database.

Mitigation: Index only authorized sources, avoid secrets or regulated data, and apply explicit access controls before using the database with sensitive accounts.

Risk: Remote SSE access could expose searchable memory if the endpoint is made directly reachable.

Mitigation: Do not expose the SSE endpoint directly; place it behind reviewed network controls and use a pinned release or reviewed commit.

Risk: Semantic search can send content to an external embedding provider when enabled.

Mitigation: Keep keyword-only mode unless external embedding processing is acceptable for the indexed data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rodbland2021/skills/claw-recall)
- [Project homepage](https://github.com/rodbland2021/claw-recall)
- [Quick start](https://github.com/rodbland2021/claw-recall#quick-start)
- [Full guide](https://github.com/rodbland2021/claw-recall/blob/master/docs/guide.md)
- [Changelog](https://github.com/rodbland2021/claw-recall/blob/master/CHANGELOG.md)
- [Community](https://discord.gg/4wGTVa9Bt6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration snippets, and MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return search results, recent transcript excerpts, activity summaries, source status, database statistics, or saved-memory acknowledgements depending on the MCP tool used.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
