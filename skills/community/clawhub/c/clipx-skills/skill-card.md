## Description:

Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain (no scraping code, no API keys).

This skill is ready for commercial/non-commercial use.

## Publisher:

[clipxonchain](https://clawhub.ai/user/clipxonchain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch BNB Chain protocol rankings, market snapshots, network metrics, and address or block data through the ClipX API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected analytics requests and any entered public BNB address to the private ClipX API.

Mitigation: Avoid submitting addresses unless that disclosure is acceptable for the user or organization using the skill.

Risk: Returned rankings, market snapshots, and announcements are external financial or market content.

Mitigation: Treat the output as informational analytics and verify material decisions against trusted primary sources.

Risk: Some API responses are intended to be reproduced exactly, which can preserve misleading or unexpected external content.

Mitigation: Review outputs before relying on them and do not treat pass-through API text as agent-authored advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clipxonchain/skills/clipx-skills)
- [ClipX publisher profile](https://clawhub.ai/user/clipxonchain)
- [ClipX API base URL](https://skill.clipx.app)
- [BNB Chain](https://bnbchain.org)
- [OpenClaw](https://openclaw.ai)
- [Python downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown code blocks, plain Markdown announcements, and compact JSON from a Python CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill uses pre-formatted 40-character tables for most analysis outputs and leaves Binance announcements as plain Markdown.]

## Skill Version(s):

1.0.20 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
