## Description: <br>
Monitors A-share public mutual fund net values, daily changes, batches, holdings, and daily fund summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can query current fund net values and daily percentage changes, run batch checks, estimate holdings performance, and produce daily fund summaries. The skill is intended for A-share off-exchange public mutual funds and depends on network data from Eastmoney. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network calls to Eastmoney for fund data, so results may be delayed, unavailable, or affected by upstream changes. <br>
Mitigation: Treat fund data as informational, verify important values against an authoritative financial source, and expect lookup failures or rate limits. <br>
Risk: Helper scripts can publish financial summaries to a fixed Feishu document. <br>
Mitigation: Run Feishu helper scripts only when document publishing is intended and the destination document has been reviewed. <br>
Risk: Bundled Feishu credentials and document tokens should be considered exposed. <br>
Mitigation: Rotate or replace the bundled credentials before legitimate use and avoid distributing real secrets in skill artifacts. <br>


## Reference(s): <br>
- [ClawHub fund-monitor release page](https://clawhub.ai/hongjiahao371-pixel/fund-monitor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hongjiahao371-pixel) <br>
- [Eastmoney fund data endpoint](https://fund.eastmoney.com/pingzhongdata/{fund_code}.js) <br>
- [Feishu document append API](https://open.feishu.cn/open-apis/docx/v1/documents/blocks/append) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text fund reports and Markdown financial summaries, with shell commands for running bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network-dependent output may include fund prices, daily changes, holding estimates, and Feishu document update results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
