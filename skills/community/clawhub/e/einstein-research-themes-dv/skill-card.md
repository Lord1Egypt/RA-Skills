## Description: <br>
Detect and analyze trending market themes across sectors, including bullish and bearish narratives, sector rotation, and lifecycle maturity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate theme-level market analysis from FINVIZ industry data, ETF references, uptrend signals, and narrative checks. It helps compare hot, cold, emerging, crowded, and exhausted market themes rather than selecting individual stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key handling instructions could expose FINVIZ or FMP credentials if users echo keys in shared shells, logs, or recordings. <br>
Mitigation: Avoid echoing secrets, use a virtual environment or secret manager, prefer temporary or revocable provider keys, and review shell commands before running them. <br>
Risk: Market themes, ticker lists, and narrative queries may be sent to third-party market-data or web-search services. <br>
Mitigation: Use the skill only when sharing those queries externally is acceptable, and avoid including confidential holdings, client details, or proprietary strategy context. <br>
Risk: Public FINVIZ scraping mode is slower and limited, so reports can be incomplete or less reliable than full data runs. <br>
Mitigation: Prefer authenticated data sources for fuller coverage and independently verify market conclusions before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawdiri-ai/einstein-research-themes-dv) <br>
- [Publisher profile](https://clawhub.ai/user/clawdiri-ai) <br>
- [Cross-Sector Theme Definitions](references/cross_sector_themes.md) <br>
- [Theme Detection Methodology](references/theme_detection_methodology.md) <br>
- [Thematic ETF Catalog](references/thematic_etf_catalog.md) <br>
- [FINVIZ Industry Codes](references/finviz_industry_codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language guidance with shell commands plus generated JSON and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces theme-level market analysis and timestamped report files; does not provide individual stock picks.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
