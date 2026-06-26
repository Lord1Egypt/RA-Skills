## Description: <br>
Financial Report helps agents analyze company financial statements, calculate profitability, growth, and financial health metrics, generate charts, and draft forecast-oriented reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[interccy-stack](https://clawhub.ai/user/interccy-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, researchers, and business users use this skill to structure public company financial statement review, calculate common ratios, visualize trends, and prepare financial analysis reports. It is not positioned for stock trading recommendations, real-time market data, or bookkeeping. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled HTML analysis tool loads Chart.js from a third-party CDN, which can expose confidential or unpublished financial data during use. <br>
Mitigation: Use the tool with public company data or approved non-confidential data, and review or locally pin the charting dependency before using sensitive financial inputs. <br>
Risk: Financial forecasts and ratio analysis can be interpreted as investment advice if presented without context. <br>
Mitigation: Present outputs as analytical support only, keep the disclaimer that reports are not investment advice, and have qualified reviewers validate assumptions before business or investment decisions. <br>
Risk: Professional-version links are external sites outside the reviewed skill package. <br>
Mitigation: Treat those links as unreviewed external destinations and evaluate them separately before relying on them in a deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/interccy-stack/financial-report) <br>
- [Publisher profile](https://clawhub.ai/user/interccy-stack) <br>
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reports, tabular financial metrics, charting guidance, and an HTML analysis tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scenario-based forecasts and local chart generation when the bundled HTML tool is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
