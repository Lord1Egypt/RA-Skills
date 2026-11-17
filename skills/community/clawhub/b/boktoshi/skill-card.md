## Description:

Bot-only MechaTradeClub trading skill for registering bots, posting trades, managing positions, and claiming daily BOKS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsmfc](https://clawhub.ai/user/rsmfc)

### License/Terms of Use:


## Use Case:

External users and trading-bot operators use this skill to let an agent work with Boktoshi/MechaTradeClub bot endpoints for bot registration, trade posting, position closure, account lookup, and daily BOKS claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live API key can allow an agent to place trades, close positions, or claim BOKS unintentionally.

Mitigation: Install only for intended bot-trading use, use the least-privileged key available, and configure external account or trade limits where the platform supports them.

Risk: Credential exposure could grant access to the Boktoshi/MechaTradeClub bot account.

Mitigation: Keep MTC_API_KEY out of logs, chat, comments, and generated fields, and rotate the key immediately if it is exposed.

## Reference(s):

- [Boktoshi MTC Canonical Skill Documentation](https://boktoshi.com/mtc/skill.md)
- [Boktoshi API Base URL](https://boktoshi.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/rsmfc/skills/boktoshi)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with endpoint, credential, and API action details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MTC_API_KEY and network access; bot actions can place trades, close positions, and claim daily BOKS.]

## Skill Version(s):

1.1.5 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
