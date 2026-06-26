## Description: <br>
Wraps the AKShare financial data library so agents can fetch fundamental, real-time, historical, and derivative financial data for stocks, futures, options, funds, foreign exchange, bonds, indexes, and cryptocurrencies. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[codecanvas762](https://clawhub.ai/user/codecanvas762) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to install AKShare dependencies and have an agent generate examples or run helper scripts for market quotes, cryptocurrency prices, macroeconomic indicators, and financial data exploration. The artifact describes the data as intended for academic research and requiring independent verification before decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill installs AKShare and pandas from PyPI and allows AKShare to make external financial-data requests. <br>
Mitigation: Review dependency installation and network access policy before deployment. <br>
Risk: Market data may be delayed, incomplete, or unavailable from upstream public finance sources. <br>
Mitigation: Verify important values against another source before analysis or decisions. <br>
Risk: Financial outputs could be mistaken for trading or investment advice. <br>
Mitigation: Treat outputs as informational and do not use them as the sole basis for automated trading or financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codecanvas762/akshare-finance-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/codecanvas762) <br>
- [AKShare documentation](https://akshare.akfamily.xyz/) <br>
- [AKShare GitHub repository](https://github.com/akfamily/akshare) <br>
- [Skill reference README](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; bundled helper scripts print JSON when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires akshare>=1.12 and pandas>=1.5; external data availability and freshness depend on upstream financial data sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
