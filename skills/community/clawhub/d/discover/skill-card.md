## Description:

Discover new ideas, sources, opportunities, and angles with durable watchlists, novelty rules, and heartbeat-backed finding logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Discover to maintain durable discovery watchlists for topics where novelty over time matters, then log only findings that change a decision, risk, opportunity, or next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include a permission-command typo that targets ~/discover.

Mitigation: Correct the chmod target to ~/Clawic/data/discover before running setup.

Risk: Recurring discovery can create unwanted monitoring noise or scope drift if enabled too broadly.

Mitigation: Enable heartbeat only for explicitly approved watchlist topics with a clear novelty bar, and return HEARTBEAT_OK when nothing materially new appears.

Risk: Public lookups may send topic names, query variants, and source lookups to external search, news, community, or topic-specific sources.

Mitigation: Keep lookup scope narrow, avoid secrets or sensitive private details in watchlist topics, and require approval before broader tools or external actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/discover)
- [Discover homepage](https://clawic.com/skills/discover)
- [Discovery loop](artifact/discovery-loop.md)
- [Novelty test](artifact/novelty-test.md)
- [Heartbeat rules](artifact/heartbeat-rules.md)
- [Setup](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local discovery state under ~/Clawic/data/discover/ when the user approves setup or recurring checks.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
