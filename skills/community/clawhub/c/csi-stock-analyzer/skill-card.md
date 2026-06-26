## Description: <br>
Professional A-share stock analysis skill for market data retrieval, technical indicators, data caching, news sentiment, financial analysis, and stock-specific reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evanslin99](https://clawhub.ai/user/evanslin99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Chinese A-share stocks, combining technical indicators, financial ratios, and news sentiment into readable stock analysis reports. It is suitable for exploratory analysis workflows, not for unreviewed investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce buy, sell, rating, and confidence guidance from simulated or hard-coded market, financial, or holder data. <br>
Mitigation: Treat results as informational only unless all data sources are replaced with verified live sources and the outputs are independently reviewed before any investment decision. <br>
Risk: News search can send company or stock queries to third-party services and report generation can retain local analysis records. <br>
Mitigation: Use a dedicated Tavily API key, run in a virtual environment, and disable news search, caching, or report saving when query disclosure or local retention is not acceptable. <br>
Risk: Dependency and API behavior can change over time, affecting data quality or availability. <br>
Mitigation: Pin dependencies, review API terms and rate limits, and verify source freshness before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evanslin99/csi-stock-analyzer) <br>
- [Artifact README](artifact/README.md) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text or Markdown stock analysis reports with optional command-line usage and configuration steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local report files and cache market, financial, or news data when configured to do so.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
