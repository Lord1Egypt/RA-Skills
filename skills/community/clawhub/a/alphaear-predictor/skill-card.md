## Description: <br>
Market prediction skill using Kronos for finance market time-series forecasting and news-aware forecast adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts and agent developers use this skill to generate Kronos-based market time-series forecasts and adjust them with current news context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, ticker interests, or market research context may be sent to third-party search, stock-data, model, or LLM services. <br>
Mitigation: Review provider settings before use and avoid confidential strategy terms or proprietary watchlists unless those providers are approved. <br>
Risk: Market forecasts and news-based adjustments can be wrong, stale, or misleading. <br>
Mitigation: Treat outputs as decision-support analysis, review forecasts before acting, and compare results with current market data and independent analysis. <br>
Risk: Local finance and news caches may retain research activity beyond the immediate interaction. <br>
Mitigation: Review local database paths and retention practices before deployment in sensitive environments. <br>
Risk: Custom model checkpoints can change behavior and may introduce model-loading risk. <br>
Mitigation: Use only trusted checkpoints and keep the documented checkpoint pattern and safe loading controls in place. <br>


## Reference(s): <br>
- [AlphaEar Predictor ClawHub page](https://clawhub.ai/zhouzhonglu8-png/alphaear-predictor) <br>
- [Publisher profile](https://clawhub.ai/user/zhouzhonglu8-png) <br>
- [Forecast adjustment prompts](references/PROMPTS.md) <br>
- [Kronos model reference paper](https://arxiv.org/pdf/2406.07548.pdf) <br>
- [Soft entropy reference paper](https://arxiv.org/pdf/1911.05894.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON forecasts with text or Markdown rationale and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast quality depends on available market history, selected model weights, embedding configuration, and news context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
