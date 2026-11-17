## Description:

The fast auto-invest function of Gate Exchange Earn. Use this skill whenever you need to create, update, stop, or top up invest plans and to query supported coins, minimum amounts, records, orders, and plan detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and their agents use this skill to manage Gate Exchange Earn auto-invest plans, including DCA plan creation, updates, stops, top-ups, and account-specific plan queries. It is intended for workflows that require explicit confirmation before live financial account actions.

### Deployment Geography for Use:

Global, subject to Gate account eligibility and regional product availability.

## Known Risks and Mitigations:

Risk: The security summary flags live financial account actions combined with runtime rules delegated to an unbundled mutable file.

Mitigation: Review the skill before installing it on an account with trading permissions, and bundle or pin the shared runtime rules to an immutable version before deployment.

Risk: Create, update, stop, and top-up operations can change a user's financial account state.

Mitigation: Require a clear Action Draft showing amount, cadence, fund source, and destination, then wait for fresh explicit confirmation before every write action.

Risk: A repeated top-up call can cause duplicate deductions.

Mitigation: Call the add-position tool exactly once per confirmed top-up request and invalidate the confirmation if the amount or plan changes.

Risk: Incorrect time-zone conversion can schedule purchases at an unintended UTC hour.

Mitigation: Convert local execution times to UTC where possible and show both UTC and local time in the confirmation draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-exchange-autoinvest)
- [Gate exchange runtime rules](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md)
- [Auto-invest plan lifecycle workflows](references/autoinvest-plans.md)
- [Auto-invest compliance and funding rules](references/autoinvest-compliance.md)
- [Auto-invest scenario index](references/scenarios.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown-style conversational responses with structured action drafts, query summaries, and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require a fresh explicit confirmation; create and top-up flows include amount, cadence, funding, destination, balance, and eligibility checks.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version 2026.4.2-3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
