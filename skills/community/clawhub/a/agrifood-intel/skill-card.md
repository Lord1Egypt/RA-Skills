## Description: <br>
Delivers data-driven analysis on global food prices, crop supply-demand, food security, climate impacts, agritech, trade flows, and fisheries trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, traders, policymakers, and developers use this skill to gather and structure global agrifood intelligence across food prices, crop supply-demand, hunger monitoring, climate impacts, fertilizer markets, trade flows, fisheries, and agritech. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agrifood market, food-security, weather, and policy data can become stale quickly or differ across agencies. <br>
Mitigation: Cite each source with its release date, distinguish current observations from forecasts, and call out material divergences between USDA, FAO, AMIS, IPC, WFP, and other sources. <br>
Risk: Outputs may influence commercial, policy, or humanitarian decisions where incorrect interpretation could have material consequences. <br>
Mitigation: Use the skill as decision support, verify high-impact claims against primary sources, and require expert review before acting on market, trade, or crisis-response recommendations. <br>
Risk: The release security evidence reports a clean verdict but includes operational guidance about sensitive maintenance and automation workflows. <br>
Mitigation: Install only in environments where the documented automation posture is expected, and review any generated commands or proposed actions before execution. <br>


## Reference(s): <br>
- [Agrifood Source Catalog](references/agrifood_sources.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/ai-gaoqian/agrifood-intel) <br>
- [FAO Food Price Index](https://www.fao.org/worldfoodsituation/foodpricesindex/en/) <br>
- [WFP HungerMap Live](https://hungermap.wfp.org/) <br>
- [Integrated Food Security Phase Classification](https://www.ipcinfo.org/) <br>
- [USDA WASDE](https://www.usda.gov/oce/commodity/wasde) <br>
- [World Bank Commodity Markets](https://www.worldbank.org/en/research/commodity-markets) <br>
- [NOAA Climate Prediction Center](https://www.cpc.ncep.noaa.gov/) <br>
- [FAO GIEWS](https://www.fao.org/giews/en/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with tables, cited source summaries, and structured analytical outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commodity supply-demand tables, food crisis dashboards, fertilizer affordability indices, source/date citations, and notes on divergent estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
