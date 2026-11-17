## Description:

Active research intelligence: track questions you're pursuing, log findings as they arrive, and close the loop when you figure it out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Digs to help an agent maintain local research threads, synthesize findings, track open questions, and close resolved inquiries in markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to maintain persistent research notes based on inferred conversation.

Mitigation: Require confirmation before writing, updating, or moving research notes when the user's intent is ambiguous.

Risk: The skill includes instructions for recurring automation through HEARTBEAT or cron.

Mitigation: Remove or disable recurring automation instructions before use unless the user explicitly approves them.

Risk: The skill includes update and install paths that reference mutable remote instructions or unpinned commands.

Mitigation: Install or update from a pinned, reviewed release rather than a mutable main-branch URL or unpinned npx command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilyabelikin/skills/digs)
- [Publisher profile](https://clawhub.ai/user/ilyabelikin)
- [Cities for People](https://islandpress.org/books/cities-people)
- [Walk Score methodology](https://www.walkscore.com/methodology.shtml)
- [Peeps companion skill](https://github.com/haah-ing/peeps-skill)
- [Pages companion skill](https://github.com/haah-ing/pages-skill)
- [Haah companion skill](https://github.com/haah-ing/haah-skill)
- [Nooks companion skill](https://github.com/haah-ing/nooks-skill)
- [Vibes companion skill](https://github.com/haah-ing/vibes-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes and concise conversational guidance with occasional shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under mind/digs/; may move resolved notes to mind/digs/closed/.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
