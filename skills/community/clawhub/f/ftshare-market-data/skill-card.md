## Description: <br>
Provides routed access to FT market-data subskills for A-share and Hong Kong stock codes, quotes, valuation, K-line data, ETF, fund, index, macroeconomic, news, and related market datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawn92](https://clawhub.ai/user/shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer market-data questions by selecting and running the appropriate FT data subskill, then returning JSON-derived summaries, tables, files, or guidance for A-share, Hong Kong, ETF, fund, index, news, and macroeconomic data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Finance-related queries and parameters are sent to FT market-data services. <br>
Mitigation: Use the skill only when sending the requested symbols, dates, keywords, and market-data parameters to those services is acceptable. <br>
Risk: Broad market-data coverage can make ambiguous macro or security questions route to the wrong subskill. <br>
Mitigation: State the desired subskill or data category explicitly when questions are ambiguous. <br>
Risk: Download handlers can overwrite files within their allowed output directory. <br>
Mitigation: Choose output filenames deliberately and avoid reusing paths that contain important local files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shawn92/ftshare-market-data) <br>
- [FT market data API base](https://market.ft.tech) <br>
- [FT AI market data endpoint](https://ftai.chat) <br>
- [FT market data app API base](https://market.ft.tech/app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown or text summaries derived from JSON API responses; selected download handlers can write PDF, XML, or XLSX files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses command-line subskill parameters and read-only HTTP GET requests; download outputs are user-directed and constrained to the working directory.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
