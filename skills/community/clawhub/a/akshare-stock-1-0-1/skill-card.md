## Description: <br>
Akshare Stock helps agents retrieve and analyze A-share market quotes, historical K-line data, financial data, sector information, fund flows, IPO data, margin trading data, and related stock lookup results through AkShare. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-data analysts use this skill to answer A-share stock lookup, market data, financial analysis, and screening questions. The artifact states that returned data is for academic research and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on AkShare as a third-party market-data dependency, and upstream interfaces or network availability can affect results. <br>
Mitigation: Use a virtual environment, pin a reviewed AkShare version, test in the local target environment, and add retry and error handling around data calls. <br>
Risk: Returned financial data may be incomplete, delayed, or unsuitable for trading decisions. <br>
Mitigation: Treat outputs as informational research data, verify important values against authoritative sources, and do not use the skill output alone as investment advice or trading authority. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with Python snippets and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses AkShare public market-data calls; local network and upstream data-source availability may affect results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
