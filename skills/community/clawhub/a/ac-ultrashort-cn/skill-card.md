## Description: <br>
A股超短线交易策略。用于 Peter 的游牧型超短线交易风格：只做主线、只做最强、1-2天T+1套利。当需要分析A股盘面、筛选热点板块、寻找龙头股、制定买卖策略时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbmchina](https://clawhub.ai/user/xbmchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for educational A-share ultra-short-term trading analysis, including sector review, hot-theme screening, candidate leader identification, entry and exit planning, risk controls, and trade journaling. It does not place trades or connect to brokerage systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short-term A-share trading guidance can be wrong, stale, or financially harmful. <br>
Mitigation: Treat outputs as educational analysis only, verify current market data independently, and make trading decisions outside the skill. <br>
Risk: Connecting strategy guidance directly to brokerage APIs or credentials could enable unintended automated trading. <br>
Mitigation: Keep the skill text-only unless a separate reviewed execution workflow controls credentials, approvals, and order placement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xbmchina/ac-ultrashort-cn) <br>
- [Eastmoney Concept Sector Capital Flows](https://data.eastmoney.com/bkzj/gn.html) <br>
- [CLS Hot Stocks](https://www.cls.cn/hot-stock) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, tables, checklists, and trade journal templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only; no code, installer, credentials, persistence, or automated trade execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
