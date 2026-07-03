## Description: <br>
Queries A-share industry, concept, and regional sector performance and capital flow for realtime or historical dates using EastMoney data through akshare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yituwangpeng](https://clawhub.ai/user/yituwangpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market analysts use this skill to retrieve A-share sector rankings, fund-flow leaderboards, and constituent-stock tables for current or historical dates. It supports research-style market summaries and does not provide investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime dependency installation may fetch unreviewed or newer package versions. <br>
Mitigation: Preinstall reviewed, pinned versions of akshare and pandas in managed environments, and disable runtime installation if policy requires controlled dependencies. <br>
Risk: The script removes proxy environment variables for its own process, which may bypass expected network routing controls. <br>
Mitigation: Run the skill in a network-controlled environment and confirm EastMoney access policy before use. <br>
Risk: Market data from public third-party interfaces may be delayed, unavailable, or incomplete on non-trading days. <br>
Mitigation: Present source and date context with outputs, treat results as research reference only, and avoid using the skill as investment advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yituwangpeng/skills/a-share-sector) <br>
- [EastMoney market data](https://quote.eastmoney.com/) <br>
- [AkShare documentation](https://akshare.akfamily.xyz/) <br>
- [AkShare GitHub repository](https://github.com/akfamily/akshare) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables with concise narrative summaries and disclaimer text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses network calls to EastMoney through akshare; historical queries can be slow and concurrent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
