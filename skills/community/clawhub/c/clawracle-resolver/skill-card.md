## Description:

Clawracle Oracle Resolver enables AI agents to resolve oracle queries on Monad by monitoring requests, fetching data from configured APIs, submitting on-chain resolutions, and validating answers for reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deeakpan](https://clawhub.ai/user/deeakpan)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure agents that monitor Clawracle oracle requests, answer supported data queries with APIs, and participate in dispute validation on Monad.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous wallet signing can spend gas or lose bonded CLAWCLE tokens when answers are wrong, disputed, or submitted unexpectedly.

Mitigation: Use a fresh low-value wallet, prefer testnet where possible, cap funds, and add transaction approval plus maximum bond limits before running with real value.

Risk: LLM-constructed API calls can expose credentials or send requests to unintended destinations.

Mitigation: Use fixed allowlisted API destinations, validate requests before credentials are injected, and never send raw API keys to an LLM.

Risk: Unpinned dependencies and continuous autonomous network activity can make runtime behavior harder to control.

Mitigation: Pin dependencies and add rate limits, monitoring, and operational approval gates before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deeakpan/skills/clawracle-resolver)
- [Setup Guide](artifact/references/setup.md)
- [API Integration Guide](artifact/references/api-guide.md)
- [Contract ABIs](artifact/references/abis.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Technical Reference](artifact/TECHNICAL_REFERENCE.md)
- [Complete Agent Example](artifact/COMPLETE_AGENT_EXAMPLE.md)
- [API Configuration](artifact/api-config.json)
- [TheSportsDB API Documentation](artifact/api-docs/thesportsdb.md)
- [NewsAPI Documentation](artifact/api-docs/newsapi.md)
- [OpenWeather Documentation](artifact/api-docs/openweather.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions and example scripts; runtime behavior depends on configured API keys, wallet funding, Monad RPC access, and oracle request data.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
