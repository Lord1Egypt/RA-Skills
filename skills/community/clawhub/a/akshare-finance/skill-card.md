## Description: <br>
Provides AKShare-based access to public financial market, macroeconomic, cryptocurrency, foreign exchange, precious metals, and fundamental data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BenAngel65](https://clawhub.ai/user/BenAngel65) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to retrieve public financial datasets through AKShare and produce code, commands, and data-handling guidance for market analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on AKShare and pandas packages from pip. <br>
Mitigation: Install dependencies only from trusted package indexes and use an isolated Python environment. <br>
Risk: The skill makes outbound requests to public financial-data sources through AKShare. <br>
Mitigation: Run it only in environments where outbound financial-data requests are allowed. <br>
Risk: Returned market data may be delayed, incomplete, or unsuitable for financial decisions. <br>
Mitigation: Treat outputs as informational and cross-check important results with authoritative data sources before use. <br>


## Reference(s): <br>
- [AKShare Reference README](references/README.md) <br>
- [AKShare Documentation](https://akshare.akfamily.xyz/) <br>
- [AKShare GitHub Repository](https://github.com/akfamily/akshare) <br>
- [ClawHub Skill Page](https://clawhub.ai/BenAngel65/akshare-finance) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python and bash examples; helper scripts emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AKShare calls typically return pandas DataFrame objects; included helper scripts serialize selected results as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
