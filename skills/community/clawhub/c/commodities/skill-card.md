## Description: <br>
Fetch commodity prices for WTI (Crude Oil), Brent, Natural Gas, and Gold using Yahoo Finance (yfinance). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youpele52](https://clawhub.ai/user/youpele52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch current Yahoo Finance commodity prices, daily movement, recent ranges, volume context, and related headlines for WTI crude oil, Brent crude, natural gas, and gold futures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yahoo Finance data and related headlines may be delayed, unavailable, or inaccurate for financial decisions. <br>
Mitigation: Verify market data and news against authoritative sources before making trading, investment, or operational decisions. <br>
Risk: The skill contacts Yahoo Finance through yfinance and returns external news links. <br>
Mitigation: Run it only in environments where Yahoo Finance network access is expected, and treat returned links as external content. <br>
Risk: Running through uv can install the yfinance dependency at execution time. <br>
Mitigation: Review dependency installation policy and pin or preinstall dependencies in controlled environments when required. <br>


## Reference(s): <br>
- [Commodities skill page](https://clawhub.ai/youpele52/commodities) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text commodity price report with headline titles and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses uv to run a Python script that installs yfinance from the inline dependency block when needed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
