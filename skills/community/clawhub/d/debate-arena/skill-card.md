## Description:

Debate Arena helps a host agent orchestrate configurable multi-agent debates with chat commands, role assignment, round progression, local archiving, and multi-voter scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[updatedb](https://clawhub.ai/user/updatedb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run structured debate workflows in group chats, including setup of pros, cons, host, judge, voters, rounds, prompts, and persisted debate records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Participant or user-provided debate text can influence later agents that are asked to send group messages.

Mitigation: Restrict spawned agents to the intended group-message capability, bind channel and target outside the model prompt where possible, and review host integration before installation.

Risk: Debate transcripts, votes, logs, and default configuration are retained as local records.

Mitigation: Avoid sensitive debate topics unless local retention is acceptable, and configure state and archive paths with appropriate access controls and cleanup procedures.

Risk: Debater and judge agents could gain unnecessary local capabilities if the host exposes broad tools.

Mitigation: Do not expose shell, filesystem, or broad messaging tools to debaters; use the direct content-recording helpers and keep file-import helpers disabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/updatedb/skills/debate-arena)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text chat responses with JSON-like command results and Node.js API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local state, log, default configuration, and archive files under the configured Debate Arena data paths.]

## Skill Version(s):

1.2.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
