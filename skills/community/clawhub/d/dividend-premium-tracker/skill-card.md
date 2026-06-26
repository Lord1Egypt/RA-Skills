## Description: <br>
Tracks the dividend premium, calculated as dividend yield minus 10-year bond yield, for the CSI Dividend Low Volatility Index to support investment monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gykdly](https://clawhub.ai/user/gykdly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to fetch CSI dividend-yield and China 10-year bond-yield data, calculate the dividend premium, generate tracking files, and check alert conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Telegram alert path uses a user-provided bot token with a hard-coded chat ID and a shell-built curl command. <br>
Mitigation: Do not set TELEGRAM_BOT_TOKEN or enable scheduled alerts until the chat ID is changed to a verified recipient and the alert request is replaced with a safer HTTP call. <br>
Risk: The scripts write tracking files to a hard-coded local output directory. <br>
Mitigation: Change the output directory to a path controlled by the installer before running update or monitoring commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gykdly/dividend-premium-tracker) <br>
- [China Securities Index H30269 indicator XLS](https://oss-ch.csindex.com.cn/static/html/csindex/public/uploads/file/autofile/indicator/H30269indicator.xls) <br>
- [ChinaBond yield data](https://yield.chinabond.com.cn/cbweb-czb-web/czb/moreInfo?locale=cn_ZH&nameType=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown instructions with shell commands; scripts can produce CSV and XLSX tracking files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Network access is required for data downloads; optional Telegram alerts require TELEGRAM_BOT_TOKEN.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, server release metadata, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
