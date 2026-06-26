## Description: <br>
Retrieves recent A-share top gainers from Tonghuashun iWencai, filters out ST stocks, and returns a formatted ranking table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask for recent A-share gain rankings over a chosen time window and count. The skill helps an agent retrieve market ranking data, exclude ST stocks, renumber the results, and present the data in a readable table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags SSRF-related wording around browser navigation as suspicious. <br>
Mitigation: Review before installation and confirm the skill only accesses intended iWencai stock-query pages and does not fetch, proxy, redirect to, or expose arbitrary or internal network URLs. <br>
Risk: Stock ranking data may be time-sensitive, incomplete, or unsuitable as a sole basis for financial decisions. <br>
Mitigation: Verify results against the source platform and apply appropriate financial review before relying on the ranking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/astock-top-gainers) <br>
- [Tonghuashun iWencai stock query](https://www.iwencai.com/unifiedwap/result?w=近{N}日涨幅排名&querytype=stock) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table with summary notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes rank, stock code, stock name, current price, daily percentage change, interval gain ranking, interval percentage change, query time, data source, and a risk note.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
