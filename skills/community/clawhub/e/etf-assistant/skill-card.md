## Description: <br>
ETF投资助理 / ETF Investment Assistant - 查询行情、筛选ETF、对比分析、定投计算。支持沪深300、创业板、科创50、纳指等主流ETF。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[franky0617](https://clawhub.ai/user/franky0617) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External investors and agents use this skill to list common ETFs, look up ETF quotes, compare pairs, search by code or name, and calculate DCA estimates. Its results are informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quote and comparison commands send user-entered ETF symbols to Yahoo Finance. <br>
Mitigation: Inform users about the outbound request before use and avoid entering symbols or queries they consider sensitive. <br>
Risk: Investment summaries, popular ETF lists, quote output, and DCA estimates could be mistaken for financial advice or trading instructions. <br>
Mitigation: Treat outputs as informational only and verify investment decisions with authoritative market data and qualified financial guidance. <br>


## Reference(s): <br>
- [ETF投资助理 ClawHub release page](https://clawhub.ai/franky0617/etf-assistant) <br>
- [Yahoo Finance chart endpoint used for ETF quotes](https://query1.finance.yahoo.com/v8/finance/chart/${code}.SS) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output with ETF lists, quote summaries, comparisons, and DCA estimates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote and comparison commands make outbound Yahoo Finance requests with user-entered ETF symbols.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
