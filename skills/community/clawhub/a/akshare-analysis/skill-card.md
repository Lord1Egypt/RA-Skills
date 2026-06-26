## Description: <br>
Analyze Hong Kong and A-share Chinese stocks by company name or ticker, producing multi-dimension BUY/HOLD/SELL signals with confidence scores using AkShare data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coxlong](https://clawhub.ai/user/coxlong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Hong Kong and A-share Chinese equities, search related news, and generate text, JSON, or HTML reports for informational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stock signals and reports could be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis only and require qualified human review before investment or trading decisions. <br>
Risk: Generated reports persist under /data/stock-reports. <br>
Mitigation: Store reports only in approved locations and remove them when they are no longer needed. <br>
Risk: HTML reports load browser script content. <br>
Mitigation: Open only reports that were intentionally generated from trusted inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coxlong/akshare-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Plain text, JSON, Markdown guidance, shell commands, and optional self-contained HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate report directories containing structured analysis data, chart data, optional AI analysis, and rendered HTML.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
