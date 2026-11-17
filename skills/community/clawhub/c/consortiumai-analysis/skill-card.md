## Description:

Gets the latest AI-generated crypto trading analysis (BUY / SELL / WAIT) for spot trading pairs from the Consortium AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webcraft3r](https://clawhub.ai/user/webcraft3r)

### License/Terms of Use:


## Use Case:

External users, developers, and trading analysts use this skill to retrieve the latest Consortium AI spot crypto trading signal overall or for a specific base token. It supports read-only BUY, SELL, or WAIT analysis with confidence, setup score, summary, and reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users must trust Consortium AI with TRADING_ANALYSIS_API_KEY handling.

Mitigation: Scope the API key to this service where possible and avoid pasting it into chats, logs, or shared files.

Risk: The skill returns crypto trading signals that may be incorrect, stale, or unsuitable for a user's risk tolerance.

Mitigation: Treat returned BUY, SELL, or WAIT analysis as informational input and review confidence, setup score, reasoning, and current market context before acting.

Risk: Users may mistake the read-only analysis retrieval for trade execution.

Mitigation: Confirm downstream workflows do not execute trades automatically; this skill retrieves signals only.

## Reference(s):

- [Consortium AI Analysis on ClawHub](https://clawhub.ai/webcraft3r/skills/consortiumai-analysis)
- [Consortium AI](https://consortiumai.org/)
- [Trading Analysis API Endpoint](https://api.consortiumai.org/api/trading-analysis)
- [Consortium AI API Key Contact](https://x.com/Consortium_AI)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRADING_ANALYSIS_API_KEY; optional token input filters results by base token.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
