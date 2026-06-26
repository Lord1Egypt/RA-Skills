## Description: <br>
Analyzes Chinese A-share capital flows using main-force net inflow and northbound holding data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBABYZS](https://clawhub.ai/user/GBABYZS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investment-analysis agents use this skill to query and summarize Chinese A-share capital-flow signals for stock research workflows. It supports main-force flow and northbound holding checks for a supplied stock code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes may be queried through akshare and its upstream market-data sources. <br>
Mitigation: Use the skill only with stock codes that are appropriate to send to those data providers. <br>
Risk: Dependencies are not version-pinned. <br>
Mitigation: Pin and review akshare and pandas versions in the consuming environment before deployment. <br>
Risk: The advertised Dragon Tiger List export appears missing in this version. <br>
Mitigation: Use only the implemented analyze_main_force and analyze_northbound functions until the missing export is added or the manifest is corrected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBABYZS/capital-flow-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Python dictionary results and agent-facing explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on akshare and upstream market-data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
