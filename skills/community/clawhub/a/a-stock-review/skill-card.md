## Description: <br>
A-stock-review helps agents produce A-share stock review reports using AkShare market, financial, fund-flow, sector, and technical-analysis data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianxiangbing](https://clawhub.ai/user/tianxiangbing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate A-share stock review reports from market, financial, fund-flow, sector, announcement, and technical data. Outputs should be treated as research support, not as a standalone basis for trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce trade-ready buy, sell, stop-loss, target-price, and position guidance that may be mistaken for personalized investment advice. <br>
Mitigation: Treat outputs as research only, do not trade solely from generated recommendations, and seek qualified financial advice where appropriate. <br>
Risk: Reports depend on third-party market-data calls and may contain stale, mismatched, unavailable, or incorrectly dated prices, stock identities, sector data, or source data. <br>
Mitigation: Manually verify stock code, market, dates, prices, volume, sector information, and source accuracy against reliable market-data sources before relying on the report. <br>
Risk: Running the bundled scripts can make network requests to third-party market-data services. <br>
Mitigation: Review the scripts before execution and run them only in an environment where those outbound requests are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianxiangbing/a-stock-review) <br>
- [Sina Finance quote endpoint used by artifact](https://hq.sinajs.cn/list={self.market}{self.stock_code}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain-text stock review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include buy, sell, stop-loss, target-price, and position-sizing guidance; depends on third-party market-data calls and requires manual verification.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
