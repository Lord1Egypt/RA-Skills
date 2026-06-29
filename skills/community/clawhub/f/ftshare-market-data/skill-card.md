## Description: <br>
FTShare-market-data routes agent requests to FTShare market-data APIs for A-share, Hong Kong, US equity, ETF, fund, index, macroeconomic, news, and financial-statement data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-oriented agents use this skill to retrieve current and historical market data, security metadata, index and ETF details, macroeconomic indicators, news, and financial statements across A-share, Hong Kong, and US markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to market.ft.tech and ftai.chat, which can expose requested symbols, date ranges, and market-data queries to those services. <br>
Mitigation: Use the skill only when external FTShare data access is acceptable, and review sensitive query terms before execution. <br>
Risk: Download commands can write market-data files into the working directory when requested. <br>
Mitigation: Use explicit output paths, review generated files before sharing them, and avoid overwriting important workspace files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-market-data) <br>
- [FTShare market data documentation](https://market.ft.tech/gateway/doc) <br>
- [FTShare market data service](https://market.ft.tech) <br>
- [FT AI Chat service](https://ftai.chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or downloaded market-data files from API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some sub-skills support pagination or all-page retrieval; download sub-skills can save market-data files when the user provides an output path.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
