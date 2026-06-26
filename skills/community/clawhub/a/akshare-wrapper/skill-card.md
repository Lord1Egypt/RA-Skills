## Description: <br>
A-share analysis wrapper based on akshare data sources for natural-language queries about market quotes, stock analysis, sector rotation, and capital flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiaping2010-coder](https://clawhub.ai/user/hongjiaping2010-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask natural-language questions about A-share market data, individual securities, sector movement, capital flows, market statistics, financial news, and simple portfolio analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The wrapper delegates execution to a separate local akshare-stock skill. <br>
Mitigation: Install and use it only when that underlying local skill is trusted and available. <br>
Risk: Portfolio features may process private holdings information. <br>
Mitigation: Avoid entering private holdings unless storage and deletion behavior of the underlying skill is understood. <br>
Risk: Market data and stock recommendations may be delayed or unsuitable for personal financial decisions. <br>
Mitigation: Treat outputs as informational research and verify important investment decisions with authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiaping2010-coder/akshare-wrapper) <br>
- [Publisher profile](https://clawhub.ai/user/hongjiaping2010-coder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chat-optimized text with concise sections, highlighted key data, and timestamps when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates queries to a separately installed local akshare-stock skill and may return delayed market data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
