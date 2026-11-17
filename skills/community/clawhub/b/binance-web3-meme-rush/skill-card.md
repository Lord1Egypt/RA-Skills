## Description:

Provides agents with a Binance Web3 CLI for live meme-token launchpad lifecycle feeds and AI-detected hot market topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binance-skills-hub](https://clawhub.ai/user/binance-skills-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query public Binance Web3 meme-token feeds for new, finalizing, or migrated launchpad tokens and AI-detected market narratives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live crypto market data may be mistaken for financial advice.

Mitigation: Present results as market data only and avoid trading recommendations or investment advice.

Risk: The local Node CLI sends selected filter parameters to Binance Web3 public API endpoints.

Mitigation: Review parameters before execution and avoid sending sensitive or personal data.

## Reference(s):

- [CLI Reference](references/cli.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Guidance]

**Output Format:** [JSON from CLI calls, with markdown guidance for selecting commands and interpreting fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI returns live Binance Web3 public market data and uses a 10 second request timeout.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
