## Description: <br>
Monitors Chinese interest-rate indicators, including LPR, government bond yields, SHIBOR, deposit benchmark rates, and mortgage-related rates, and reports detected changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial professionals, mortgage borrowers, investors, and economic researchers use this skill to check Chinese interest-rate data and receive change alerts when tracked rates change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact Yahoo Finance, SHIBOR, and ChinaMoney endpoints when checking rates. <br>
Mitigation: Run it only in environments where outbound access to those public financial-data endpoints is expected and allowed. <br>
Risk: The skill saves local rate history to support change detection. <br>
Mitigation: Review the local data path and retention expectations before scheduled or repeated execution. <br>
Risk: Broad trigger phrases may activate it for general interest-rate questions. <br>
Mitigation: Narrow trigger phrases or invoke the skill explicitly when general financial-rate discussion should not run the monitor. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanbihai/chinese-interest-rate) <br>
- [Yahoo Finance chart API for China 10-year yield](https://query1.finance.yahoo.com/v8/finance/chart/CN10Y=X) <br>
- [Shanghai Interbank Offered Rate page](https://www.shibor.org/shibor/web-htmls/shibor.html) <br>
- [ChinaMoney SHIBOR endpoint](https://www.chinamoney.com.cn/ags/ms/cm-u-bond-shibor/Shibor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown notifications with optional shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local JSON rate-history file and may stay silent when no rate changes are detected.] <br>

## Skill Version(s): <br>
3.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
