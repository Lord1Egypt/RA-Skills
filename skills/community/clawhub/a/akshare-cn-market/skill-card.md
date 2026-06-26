## Description: <br>
Provides AKShare-based access to Chinese A-share market data, index data, financial summaries, macroeconomic indicators, bond yields, and trading-calendar utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoion](https://clawhub.ai/user/geoion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent builders use this skill to retrieve public Chinese equity-market and macroeconomic datasets through AKShare scripts for research, reporting, and workflow automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retrieves market and macroeconomic data from public financial data providers, so availability, latency, or provider-side field quality can affect results. <br>
Mitigation: Confirm that AKShare and pandas are installed, allow expected outbound access, and validate important results against source-provider data before relying on them. <br>
Risk: Financial data returned by the skill can be mistaken for investment advice. <br>
Mitigation: Use outputs as research material only and require independent human judgment for investment decisions. <br>


## Reference(s): <br>
- [AKShare reference notes](references/README.md) <br>
- [AKShare official documentation](https://akshare.akfamily.xyz/) <br>
- [AKShare GitHub repository](https://github.com/akfamily/akshare) <br>
- [ClawHub skill page](https://clawhub.ai/geoion/akshare-cn-market) <br>


## Skill Output: <br>
**Output Type(s):** [JSON data, Shell commands, Python code, Guidance] <br>
**Output Format:** [JSON arrays from command-line scripts, with Markdown guidance and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may contact public financial data providers through AKShare and require akshare and pandas.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
