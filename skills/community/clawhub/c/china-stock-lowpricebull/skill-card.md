## Description: <br>
Screens China A-share stocks for low-price candidates using public East Money market data and approximate capital-strength criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run a public-data China A-share stock screener and receive structured candidate results for reference. The output is not investment advice. <br>

### Deployment Geography for Use: <br>
Global; market data and screening criteria focus on China A-shares. <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script and makes a network request to East Money for market data. <br>
Mitigation: Install and run it only in environments where local script execution and outbound requests to East Money are acceptable. <br>
Risk: Screening results can be mistaken for financial advice. <br>
Mitigation: Treat the output as reference screening data only and review results independently before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luyao-inc/china-stock-lowpricebull) <br>
- [Publisher profile](https://clawhub.ai/user/luyao-inc) <br>
- [East Money public quote API](https://push2.eastmoney.com/api/qt/clist/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, guidance] <br>
**Output Format:** [JSON stock-screening results with status, strategy metadata, ranked stocks, and messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 or python and makes a network request to East Money for public market data.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
