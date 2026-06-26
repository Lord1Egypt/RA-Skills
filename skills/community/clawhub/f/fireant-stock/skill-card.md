## Description: <br>
Automated Vietnamese stock price and index checking on FireAnt.vn for Vietnamese stocks and market indices, returning formatted price, market statistic, and financial metric summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aholake](https://clawhub.ai/user/aholake) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check current Vietnamese equity and index information from FireAnt.vn for symbols such as VCB, FPT, DPM, VNINDEX, VN30, and HNX30. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes a hard-coded local Agent Browser binary path, so the resolved executable may be missing, stale, or untrusted on another system. <br>
Mitigation: Verify or replace the Agent Browser path before use, install Agent Browser only from a trusted source, and run the skill in an isolated environment first. <br>
Risk: The skill retrieves live financial data from an external website, so results depend on site availability, page structure, and current market data presentation. <br>
Mitigation: Review returned values against an authoritative financial source before using them for decisions. <br>


## Reference(s): <br>
- [FireAnt stock and index pages](https://fireant.vn/ma-chung-khoan/{SYMBOL}) <br>
- [ClawHub release page](https://clawhub.ai/aholake/fireant-stock) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Markdown-formatted text with stock or index metrics and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one formatted result block per requested stock symbol or index.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
