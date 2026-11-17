## Description:

Helps agents use AKShare to retrieve Chinese financial market data for stocks, funds, bonds, futures, foreign exchange, indexes, crypto, and macroeconomic indicators.

This skill is for research and development only.

## Publisher:

[anyjohn](https://clawhub.ai/user/anyjohn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance-data analysts use this skill to identify AKShare installation steps, common APIs, troubleshooting paths, and cautions for retrieving public market and macroeconomic data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AKShare and pandas are third-party Python dependencies that may change behavior across releases.

Mitigation: Use a virtual environment, avoid elevated privileges, and pin reviewed package versions where reproducibility matters.

Risk: Financial market data may be delayed, incomplete, or incorrect.

Mitigation: Verify outputs against independent data sources before relying on them for analysis or investment decisions.

Risk: Interface names and supported data endpoints may change over time.

Mitigation: Consult the AKShare changelog and current API list when calls fail or return empty results.

## Reference(s):

- [AKShare complete API list](references/api-list.md)
- [AKShare documentation](https://akshare.akfamily.xyz/)
- [AKShare GitHub](https://github.com/akfamily/akshare)
- [AKShare installation guide](https://akshare.akfamily.xyz/installation.html)
- [AKShare interface list](https://akshare.akfamily.xyz/tutorial.html)
- [AKShare changelog](https://akshare.akfamily.xyz/changelog.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AKShare API names, installation commands, troubleshooting guidance, and data-quality cautions.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
