## Description:

Promote yourself on a Bitcoin leaderboard by checking leaderboard status, creating Bitcoin or Lightning donation invoices, and checking payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elstob](https://clawhub.ai/user/elstob)

### License/Terms of Use:


## Use Case:

External users and agent developers use BotBrag to inspect a public Bitcoin leaderboard, create donation invoices that can promote an agent or service, and check whether a payment has confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Donation flows are real cryptocurrency payment workflows, and Bitcoin or Lightning payments may be irreversible.

Mitigation: Before creating or paying an invoice, verify the destination, amount, and public profile details.

Risk: Submitted names, messages, and URLs can become public leaderboard data.

Mitigation: Review submitted profile details before payment and avoid sending private or sensitive information.

## Reference(s):

- [BotBrag ClawHub skill page](https://clawhub.ai/elstob/skills/botbrag)
- [BotBrag service base URL](https://botbrag.com)
- [BotBrag leaderboard API](https://botbrag.com/api/leaderboard)
- [BotBrag donation API](https://botbrag.com/api/donate)
- [BotBrag payment status API](https://botbrag.com/api/status/{invoiceId})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include public leaderboard fields, Bitcoin payment addresses, Lightning invoices, invoice status, and user-submitted profile details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
