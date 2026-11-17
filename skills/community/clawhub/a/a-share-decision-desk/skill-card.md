## Description:

Build next-session A-share game plans from market structure, overnight macro shocks, policy timing, and watchlist leadership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangrichao2020](https://clawhub.ai/user/huangrichao2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to convert A-share market structure, overnight macro news, policy timing, watchlists, and capital-flow signals into a next-session pre-open decision plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-line remote installation may run code before a user has reviewed the checkout.

Mitigation: Use manual copy installation from a reviewed checkout or pinned release instead of the one-line git clone and install command.

Risk: Eastmoney/MX integrations require EM_API_KEY and make recurring external network calls.

Mitigation: Configure EM_API_KEY only after reviewing and trusting the integration and expected data access.

Risk: Optional background polling can continue running locally and write state under ~/.uwillberich.

Mitigation: Enable launchd or nohup polling only when intentional, and monitor or remove the local service when it is no longer needed.

## Reference(s):

- [Project homepage](https://github.com/huangrichao2020/uwillberich)
- [ClawHub skill page](https://clawhub.ai/huangrichao2020/skills/a-share-decision-desk)
- [methodology.md](references/methodology.md)
- [data-sources.md](references/data-sources.md)
- [trading-mode-prompt.md](references/trading-mode-prompt.md)
- [opening-window-template.md](references/opening-window-template.md)
- [message-iterator.md](references/message-iterator.md)
- [cross-cycle-watchlist.md](references/cross-cycle-watchlist.md)
- [event-regime-watchlists.md](references/event-regime-watchlists.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown desk reports, checklists, command snippets, and optional local data artifacts from scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows require EM_API_KEY and may save reports or polling state locally.]

## Skill Version(s):

0.1.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
