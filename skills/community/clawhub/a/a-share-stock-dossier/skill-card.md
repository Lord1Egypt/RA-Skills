## Description: <br>
Analyze A-share stocks and portfolios with analyst-grade, evidence-first reports. Use when the user asks for 个股分析、持仓复盘、逻辑是否还在、行业龙头、盘前/盘后策略、情绪+技术综合判断, especially when they want deep web verification and full process transparency (检索过程摘要 + 证据逐条分析) via web_search/web_fetch/browser plus Eastmoney/Tencent quote data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[T-Atlas](https://clawhub.ai/user/T-Atlas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to produce process-transparent A-share stock and portfolio dossiers with structured quote data, multi-source verification, evidence-bound conclusions, and portfolio action guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce portfolio actions or trading guidance from web-heavy market research. <br>
Mitigation: Treat recommendations as analysis, not automatic trading instructions, and independently verify important facts before acting. <br>
Risk: Prompts may include personal financial details or portfolio holdings. <br>
Mitigation: Avoid sharing unnecessary personal financial information and limit inputs to the minimum needed for the analysis. <br>
Risk: Market data and web evidence can change quickly during active trading sessions. <br>
Mitigation: Use fresh quote data, preserve timestamps in the retrieval log, and resolve conflicts with official or preferred sources first. <br>


## Reference(s): <br>
- [A Share Stock Dossier on ClawHub](https://clawhub.ai/T-Atlas/a-share-stock-dossier) <br>
- [Eastmoney Core Fields](references/eastmoney-fields.md) <br>
- [Report Template](references/report-template.md) <br>
- [Search Depth Protocol](references/search-depth-protocol.md) <br>
- [Source Checklist](references/source-checklist.md) <br>
- [Eastmoney Quote API](https://push2.eastmoney.com/api/qt/ulist.np/get) <br>
- [Tencent Kline API](https://web.ifzq.gtimg.cn/appstock/app/fqkline/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with retrieval log, structured market baseline, evidence cards, stock-by-stock analysis, and portfolio guidance; helper script output is JSON when used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current web and market-data retrieval; conclusions should be reviewed before any investment or trading decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
