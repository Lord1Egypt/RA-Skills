## Description: <br>
AI广告投手 Ad Trader helps advertising operators import CSV, Excel, or JSON ad exports, analyze campaign performance, generate optimization recommendations, detect anomalies, and produce interactive HTML reports for Tencent Ads, Ocean Engine, Baidu Ads, Meta Ads, and Google Ads data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Advertising operators, growth marketers, and analysts use this skill to normalize ad export files, inspect CTR, CVR, CPA, ROAS, ROI, budget allocation, creative fatigue, and anomalies, then generate operational reports and recommendations for campaign review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language trigger phrases may cause the assistant to apply the skill to unrelated advertising discussions. <br>
Mitigation: Use the skill only when working with intended advertising export files or explicit campaign analysis and reporting tasks. <br>
Risk: Generated HTML reports load Chart.js from a third-party CDN when opened. <br>
Mitigation: Open reports in environments where that network dependency is acceptable, or review and adapt the report before sharing in restricted environments. <br>
Risk: Reports and normalized files may contain sensitive advertising performance, spend, revenue, or campaign metrics. <br>
Mitigation: Review generated outputs before sharing and restrict distribution of reports that include sensitive business metrics. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bettermen/ad-trader) <br>
- [Advertising metrics reference](references/metrics.md) <br>
- [Advertising platform comparison](references/platforms.md) <br>
- [Advertising optimization strategies](references/strategies.md) <br>
- [Tencent Ads Marketing API](https://developers.e.qq.com/) <br>
- [Ocean Engine Open Platform](https://open.oceanengine.com/) <br>
- [Chart.js report dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, CLI commands, JSON summaries, normalized CSV or JSON files, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML reports load Chart.js from a third-party CDN when opened.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
