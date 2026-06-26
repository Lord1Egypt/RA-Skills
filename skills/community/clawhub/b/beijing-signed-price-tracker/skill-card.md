## Description: <br>
Track configured Beijing Housing Commission new-home projects from bjjs.zjw.beijing.gov.cn project-detail URLs, read project signed-unit counts, signed area, and average price, crawl building tables including “查看更多” and paginated lists, treat both “已签约” and “网上联机备案” as signed units, estimate the implied average price per m² of newly signed rooms from changes between the previous and current project summaries, cache unsold room metadata locally, persist rows into a Feishu spreadsheet as the single source of truth, and send Feishu DM notifications after each run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronstuart](https://clawhub.ai/user/aaronstuart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to monitor configured Beijing pre-sale housing projects, sync newly signed rooms into a Feishu spreadsheet, estimate newly signed average prices, and notify a Feishu recipient after each run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a real-looking Feishu app secret and default Feishu sheet and message destination. <br>
Mitigation: Before installing or running, replace or remove the bundled Feishu configuration, use your own app ID, app secret, spreadsheet, and recipient, and rotate the exposed secret if it belongs to you. <br>
Risk: Sync operations can append rows, rewrite sorted spreadsheet ranges, and send Feishu messages. <br>
Mitigation: Test first on a non-critical or copied Feishu sheet and confirm the intended recipient before enabling routine runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronstuart/beijing-signed-price-tracker) <br>
- [Beijing Housing Commission project portal](http://bjjs.zjw.beijing.gov.cn) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON files, Feishu spreadsheet rows, Feishu notifications] <br>
**Output Format:** [Command-line text output, JSON state files, and Feishu sheet/message updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local room cache and last-sync JSON state while treating the Feishu spreadsheet as the historical ledger.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
