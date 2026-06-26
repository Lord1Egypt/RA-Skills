## Description: <br>
Screen and analyze stocks based on free cash flow and fundamentals to identify profitable companies with health scores and key metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[674067795w-wq](https://clawhub.ai/user/674067795w-wq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and financial analysis agents use this skill to screen stocks for free-cash-flow quality, compare companies, and summarize fundamental metrics. It supports single-stock analysis, multi-stock comparison, and batch-style screening prompts in English and Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols or screening requests may be sent to public financial-data APIs. <br>
Mitigation: Avoid submitting sensitive portfolio information and review the public API behavior before installation. <br>
Risk: Offline operation may return demo or mock data. <br>
Mitigation: Check whether results are based on live data or demo fallback data before using the analysis. <br>
Risk: Financial metrics and rankings can be incomplete, stale, or unsuitable for investment decisions. <br>
Mitigation: Independently verify metrics and consult appropriate financial review before acting on results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/674067795w-wq/find-profitable-stocks) <br>
- [East Money API](https://push2.eastmoney.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with health scores, grades, key metrics, and analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May indicate whether live public market data or demo/mock fallback data was used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
