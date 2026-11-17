## Description:

Analyzes A-share stocks with deterministic Chan theory scripts, producing reproducible structure, buy/sell/hold/wait verdicts, invalidation prices, and human-readable guidance for an agent to relay.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to run local Chan theory analysis for Chinese A-share stocks and explain the resulting mechanical trading posture with caveats. It is useful when a user asks about Chan theory structures, buy/sell points, K-line structure, or whether to buy, hold, reduce, or wait.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if a user follows chat-based credential instructions.

Mitigation: Do not paste keys into chat; enter the key locally with `python scripts/setup_env.py --set-key` and revoke/reissue any key that was exposed.

Risk: Dependency installation and market-data retrieval contact external services.

Mitigation: Run setup in an isolated virtual environment and allow only the documented package and market-data endpoints needed for the workflow.

Risk: Stock-analysis outputs may be mistaken for personalized investment advice.

Mitigation: Present outputs as mechanical Chan theory signals, preserve caveats and invalidation prices, and keep final investment decisions with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adsorgcn/skills/chanlun-engine-skill)
- [Project homepage](https://github.com/adsorgcn/chanlun-engine-skill)
- [Chanlun core reference](references/chanlun-core.md)
- [Engine notes](references/engine-notes.md)
- [Getting started](references/getting-started.md)
- [HiThink Financial API](https://github.com/HiThink-Tech/Financial-API)
- [Chan theory source archive](https://github.com/stockServ/chzhshch-108-plus)
- [Chan.py engine](https://github.com/Vespa314/chan.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or concise text with optional shell commands and engine JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve engine caveats, invalidation prices, and the mechanical verdict from the deterministic analysis scripts.]

## Skill Version(s):

1.1.8 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
