## Description:

Author a new trading legend/persona from a famous trader's name or plain-English strategy description, then lint and live-audition it before it joins the user's roster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxdavid-offbeatforex](https://clawhub.ai/user/fxdavid-offbeatforex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-system developers use this skill to create a TLC trading legend/persona from a named public methodology or strategy description, lint the generated spec, and run a live audition before adding it to a roster.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and run code from GitHub under the user's account.

Mitigation: Install only from trusted publisher releases and review the source, dependency changes, and generated local files before use.

Risk: The optional TradingView integration involves an API key.

Mitigation: Configure secrets locally when possible, avoid sending API keys through chat, and leave the integration disabled when the key is not needed.

Risk: Generated trading specs and live-audition output may be unsuitable for live trading decisions.

Mitigation: Review the generated config, roster changes, legend spec, and ballot output before relying on any trading result.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/FXDavid-OffbeatForex/tlc-hermes-skills/tree/main/skills/forge-legend)
- [TLC project homepage](https://github.com/FXDavid-OffbeatForex/TLC)
- [ClawHub skill page](https://clawhub.ai/fxdavid-offbeatforex/skills/forge-legend)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration changes, generated skill spec files, and JSON ballot validation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local TLC config, environment scaffolding, legend specs, roster changes, and validation artifacts inside the TLC workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
