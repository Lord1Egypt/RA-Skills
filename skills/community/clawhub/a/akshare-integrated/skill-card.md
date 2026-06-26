## Description: <br>
Akshare Integrated helps agents use AKShare-based stock data workflows to retrieve market data, screen equities, score opportunities, and describe risk controls across multiple stock markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haosongyi-star](https://clawhub.ai/user/haosongyi-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to ask an agent for AKShare-backed market data retrieval, stock screening, scoring, and risk-control guidance for A-share, Hong Kong, and U.S. equities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce confident BUY, HOLD, REDUCE, SELL, position-size, stop-loss, and take-profit guidance that may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as research support only, require human review, and do not use the skill to place trades or make automated investment decisions. <br>
Risk: The artifact describes use of AKShare, pandas, numpy, and a stock-selector-akshare command or module, but the release artifact does not include implementation code. <br>
Mitigation: Verify package sources and installed commands before use, and review dependency provenance in the target environment. <br>
Risk: Market data from free or third-party data sources may be delayed, unavailable outside trading hours, rate limited, or intermittently fail. <br>
Mitigation: Use caching, retries, source validation, and freshness checks before relying on generated analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haosongyi-star/akshare-integrated) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, Python, API, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock ratings, position suggestions, stop-loss and take-profit guidance, caching guidance, and operational cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
