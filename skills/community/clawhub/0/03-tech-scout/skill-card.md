## Description:

Daily multi-source intelligence digest that scans X, YouTube, Reddit, GitHub, and web search for tools, techniques, and updates relevant to active projects, then filters results into a short actionable briefing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pingukim225](https://clawhub.ai/user/pingukim225)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical project owners use this skill to receive a daily or manually triggered briefing on fast-moving updates across their configured domains. It is suited for monitoring AI, crypto, content creation, and other technical topics without doing manual source-by-source research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may periodically query third-party services using configured project keywords.

Mitigation: Use explicit manual invocation or a clearly configured schedule when automatic morning runs are not desired, and limit keyword targets to appropriate project domains.

Risk: Local digest and seen-URL files can reveal monitored topics and previously surfaced links.

Mitigation: Store state files only in the intended workspace and delete or rotate them when the digest history is no longer needed.

## Reference(s):

- [03 Tech Scout on ClawHub](https://clawhub.ai/pingukim225/skills/03-tech-scout)
- [Publisher profile](https://clawhub.ai/user/pingukim225)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest file with ranked items, source links, relevance notes, and suggested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a dated digest and maintains a seen-URL state file for seven-day deduplication.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
