## Description:

Build and operate a crypto signal trading automation using RapidAPI cryptexAI Buy & Sell Signals as signal source and dYdX v4 for execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdann1992](https://clawhub.ai/user/mdann1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation operators use this skill to assemble a RapidAPI-to-dYdX crypto signal workflow, configure credentials and risk controls, and test signal fetching before scheduled execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading can place live dYdX orders using high-impact exchange credentials.

Mitigation: Start on testnet or dry-run, require explicit human approval before live execution or cron enablement, and cap leverage, margin, and open positions.

Risk: RapidAPI keys, dYdX signing material, passphrases, and Telegram tokens are collected during setup.

Mitigation: Keep secrets out of chat and source control, store local env files with chmod 600, avoid passing secrets on the command line, and rotate any exposed credentials.

Risk: External trading signals may be stale, duplicated, inaccurate, or unsuitable for the operator's risk profile.

Mitigation: Filter for fresh active signals, deduplicate by signal ID, test one symbol in controlled mode first, and review strategy behavior before expanding symbol coverage.

## Reference(s):

- [RapidAPI cryptexAI mapping](references/rapidapi-cryptexai.md)
- [Setup checklist](references/setup-checklist.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, JSON examples, shell commands, and generated configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API connectivity checks, environment templates, cron/runtime guidance, and trading risk settings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
