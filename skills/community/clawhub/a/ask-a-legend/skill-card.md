## Description:

Gets one legendary trader's read on a market symbol using methods such as Wyckoff, Gann, Elliott Wave, Dow Theory, Livermore, DeMark, Wilder, Ichimoku, Weinstein stage analysis, or O'Neil CAN SLIM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxdavid-offbeatforex](https://clawhub.ai/user/fxdavid-offbeatforex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-tool operators use this skill to request a single-method market read for a symbol, timeframe, and platform. It frames the result as analysis and a second opinion rather than a trading signal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill downloads and runs external trading-analysis code.

Mitigation: Review the external code source and installation behavior before enabling the skill in a trusted environment.

Risk: The security guidance notes persistent files under ~/.tlc and local provider configuration.

Mitigation: Run the skill in an environment where local persistence is expected and inspect stored configuration before reuse.

Risk: The security guidance warns against sending API keys through chat or messaging channels.

Mitigation: Set provider secrets through an out-of-band local secret setup and rotate any key previously shared through chat.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fxdavid-offbeatforex/skills/ask-a-legend)
- [Server-resolved GitHub import](https://github.com/FXDavid-OffbeatForex/tlc-hermes-skills/tree/main/skills/ask-a-legend)
- [TLC homepage](https://github.com/FXDavid-OffbeatForex/TLC)
- [Publisher profile](https://clawhub.ai/user/fxdavid-offbeatforex)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration guidance]

**Output Format:** [Markdown analysis followed by a ballot JSON block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local TLC configuration and provider setup files before producing analysis.]

## Skill Version(s):

0.1.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
