## Description:

Use this skill when the user wants to put a Binance trade thesis on trial, review whether a long or short idea deserves risk, get an APPROVE / REVIEW / REJECT verdict, inspect the three juror opinions, receive an execution playbook, or generate a Binance Trade Jury share card link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review Binance long or short trade ideas before acting on them. It returns a verdict, juror-style rationale, concerns, approval conditions, an execution playbook, and an optional share-card link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade thesis text and any bankroll amount are sent to a third-party API.

Mitigation: Invoke the skill only when the user accepts that data sharing, and avoid sending confidential strategy, account, or portfolio details.

Risk: The documented curl example embeds user-supplied trade text in a shell command.

Mitigation: Use structured HTTP and JSON serialization from the agent runtime instead of interpolating raw user text into shell commands.

Risk: The skill produces trading guidance that may be incorrect or incomplete.

Mitigation: Treat verdicts and execution playbooks as decision support, not financial advice or authorization to place trades.

## Reference(s):

- [Binance Trade Jury skill page](https://clawhub.ai/richard7463/skills/binance-trade-jury)
- [Binance Trade Jury Review API](https://binance-trade-jury.vercel.app/api/trade-jury)
- [Binance Trade Jury Share Image API](https://binance-trade-jury.vercel.app/api/trade-jury/share-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with verdict, juror opinions, execution playbook, and optional share-card URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses returned JSON from the public review API and may include a generated share-image link.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
