## Description:

Provides routed access to China and U.S. macroeconomic indicators from market.ft.tech, including GDP, prices, credit, trade, labor, housing, and interest-rate datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts can use this skill through an agent to answer China and U.S. macroeconomic data questions and present the returned indicators in concise tables or notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged Python dispatcher can be steered toward unintended handler paths if arbitrary subskill names or path-like values are passed.

Mitigation: Install only after review, use packaged subskill names, and harden the dispatcher with an explicit allowlist and canonical path checks before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-macro-economy-data)
- [market.ft.tech data service](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text summaries with optional tables and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns macroeconomic indicator data selected by country, indicator, and, for U.S. data, a type value.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
