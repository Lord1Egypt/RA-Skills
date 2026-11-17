## Description:

Etf is advertised for ETF holdings and fund metric analysis, but the reviewed artifacts implement a local terminal utility that records, searches, and exports user-entered command text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users may invoke Etf as a local terminal utility to record, inspect, search, and export typed entries. Do not rely on it for ETF analysis without independent review because the security evidence says the artifacts implement a generic logger rather than ETF analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as ETF analysis, but the security evidence says the artifacts implement a generic local input logger.

Mitigation: Review behavior before relying on ETF-related output, and require the publisher to narrow the description or implement actual ETF analysis.

Risk: User-entered text may be retained in persistent plaintext history under ~/.local/share/etf.

Mitigation: Avoid entering sensitive portfolio, account, or research data, and review or delete the local data directory after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/etf)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text terminal output with optional JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist user-supplied command text and generated exports under ~/.local/share/etf.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
