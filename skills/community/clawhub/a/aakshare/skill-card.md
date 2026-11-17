## Description:

AKShare helps agents use a free Python financial data API library for equities, funds, bonds, futures, options, foreign exchange, and macroeconomic datasets without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and work with AKShare financial market and macroeconomic data in Python workflows. It is useful for data exploration, analysis scripts, and examples that return pandas DataFrames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AKShare and pandas dependencies may change behavior if installed with broad or upgraded version ranges.

Mitigation: Install in a virtual environment and pin exact reviewed versions before deployment.

Risk: AKShare calls contact external financial data providers and returned data may be unavailable, stale, incomplete, or unsuitable for investment decisions.

Mitigation: Validate returned DataFrames, handle empty results and exceptions, cross-check important data, and do not treat outputs as investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coderwpf/skills/aakshare)
- [AKShare Documentation](https://akshare.akfamily.xyz/)
- [AKShare API Reference](https://akshare.akfamily.xyz/data/index.html)
- [AKShare GitHub Project](https://github.com/akfamily/akshare)
- [AKTools HTTP API Wrapper](https://aktools.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs commonly describe AKShare calls that return pandas DataFrames.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
