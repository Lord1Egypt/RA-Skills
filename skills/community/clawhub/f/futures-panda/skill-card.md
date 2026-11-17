## Description:

Provides AKShare-based access to Chinese futures and options market data, including live quotes, historical bars, contract details, positions, basis data, fees, and trading calendars.

This skill is for research and development only.

## Publisher:

[mabtush13](https://clawhub.ai/user/mabtush13)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve futures-market data through AKShare-backed Python commands for research, learning, integration, and data analysis workflows. It is not a source of investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned market data may be delayed, incomplete, or affected by upstream AKShare and public financial website changes.

Mitigation: Cross-check important results against additional data sources, handle JSON error responses, and do not use the output as investment advice or for high-frequency trading.

Risk: Documented commands or capabilities may be inaccurate for some AKShare versions.

Mitigation: Install in an isolated Python environment, pin reviewed dependency versions, and verify commands against the AKShare documentation before relying on them.

## Reference(s):

- [AKShare Futures Data Skill README](references/README.md)
- [AKShare Official Documentation](https://akshare.akfamily.xyz/)
- [AKShare GitHub Repository](https://github.com/akfamily/akshare)
- [ClawHub Skill Page](https://clawhub.ai/mabtush13/skills/futures-panda)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; the bundled script returns JSON arrays or JSON error objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python dependencies akshare>=1.12 and pandas>=1.5.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
