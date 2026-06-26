## Description: <br>
A five-step A-share stock screening skill that uses AkShare market data to filter candidates, generate screening reports, export Excel stock pools, and support custom screening criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to run a structured A-share screening workflow, draft stock analysis reports, and export a candidate stock pool for further review. It is research support and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock lists may be incomplete because several fundamental and capital-flow checks are simplified or depend on third-party financial data availability. <br>
Mitigation: Verify candidates manually against official filings, trusted financial data terminals, and current market data before making decisions. <br>
Risk: Users may mistake screening output for investment advice. <br>
Mitigation: Treat the output as research support only and perform independent review before trading or portfolio allocation. <br>
Risk: The script retrieves public financial data from third-party sources and writes a local Excel file. <br>
Mitigation: Install and run it only in an environment where those dependencies, network calls, and file outputs are acceptable. <br>


## Reference(s): <br>
- [A-share Industry Guide](artifact/references/industry_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nodermachine/a-stock-screener) <br>
- [Eastmoney](https://www.eastmoney.com/) <br>
- [iWencai](https://www.iwencai.com/) <br>
- [CNINFO](http://www.cninfo.com.cn/) <br>
- [Tushare](https://tushare.pro/) <br>
- [Baostock](http://baostock.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and Excel spreadsheet output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an .xlsx stock pool when the screening script is run with an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
