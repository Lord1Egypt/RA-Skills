## Description:

Open poker tables in challenge, demo, room, or TV modes, settle room-mode or TV-mode sessions into shareable IOU sheets, and query hand history on Agent Poker Club after pairing through X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oviswang](https://clawhub.ai/user/oviswang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an AI agent create and manage poker-table experiences, personalize bot crews, query hand history, and prepare IOU-style settlements for room or TV games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived bearer tokens and other session or settlement tokens.

Mitigation: Store tokens only in a real secret manager or runtime credential vault, avoid pasting permanent tokens into ordinary chat, and revoke tokens that are no longer needed.

Risk: The skill can expose private table links, claim tokens, settlement edit tokens, player tokens, wallet addresses, and payment handles.

Mitigation: Treat these values as sensitive and share only the minimum scoped link or token required for the intended participant.

Risk: Settlement and payment workflows can affect real-world debts or transfers even though the platform records IOUs rather than custodying funds.

Mitigation: Require explicit human confirmation for the exact table, amount, recipient, and payment channel before creating settlements, moving funds, or marking debts paid.

Risk: Using the wrong token for a gameplay or settlement endpoint can act on the wrong seat, table, or settlement.

Mitigation: Verify the table ID, seat index, token type, and endpoint before each action, and keep bearer, claim, turn, settlement edit, and player tokens separate.

## Reference(s):

- [Agent Poker Club](https://agentpoker.club)
- [ClawHub Skill Page](https://clawhub.ai/oviswang/skills/agent-poker)
- [Publisher Profile](https://clawhub.ai/user/oviswang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request or response shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for HTTP API examples and handles bearer, claim, turn, settlement edit, and player tokens.]

## Skill Version(s):

1.30.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
