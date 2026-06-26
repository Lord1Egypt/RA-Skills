## Description: <br>
Routes Chinese futures and options questions to free AKShare-compatible data sources, recipes, and helper scripts for real-time boards, intraday indicators, options Greeks, implied volatility, and RR25 estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forevershu](https://clawhub.ai/user/forevershu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users working with Chinese market data use this skill to classify futures and options requests by frequency, asset type, and computation need, then select the matching AKShare source, recipe, and local helper command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local helper scripts may depend on akshare and pandas and make network requests to public financial-data providers through AKShare. <br>
Mitigation: Review proposed commands before execution, install dependencies only from trusted package sources, and run scripts in an environment appropriate for public market-data access. <br>
Risk: Public AKShare-backed provider fields and availability can change, which may make routed recipes fail or produce incomplete market-data outputs. <br>
Mitigation: Check failed interface names and returned columns, verify results against the referenced AKShare index, and update routing or field mappings when upstream data structures change. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/forevershu/akshare-router-cn) <br>
- [AKShare interface index](artifact/references/INDEX.md) <br>
- [AKShare source selection notes](artifact/sources/akshare.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML routing references and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Python script execution that uses akshare and pandas to query public financial-data providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
