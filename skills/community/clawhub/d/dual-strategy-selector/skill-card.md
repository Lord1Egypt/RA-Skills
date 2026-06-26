## Description: <br>
基于仙人指路B和老鸭头B两种技术形态筛选符合条件的A股股票，支持指定日期选股和信号检测。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and developers can use this skill to run a local CSV-based screen for A-share stocks matching the 仙人指路B and 老鸭头B technical patterns. It reports matching symbols for a target date and can save the selected results for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-selection output may be mistaken for investment advice or guaranteed performance. <br>
Mitigation: Treat results as informational screening output only; users should review signals, market context, and risk controls before making trading decisions. <br>
Risk: Incorrect, stale, or malformed CSV market data can produce misleading selections. <br>
Mitigation: Validate the required input columns and data freshness before running the selector, and review generated results before relying on them. <br>
Risk: The artifact writes a results CSV in the working directory when matching signals are found. <br>
Mitigation: Run it in an intended workspace and review generated files before sharing or importing them elsewhere. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chen6896qqwee/dual-strategy-selector) <br>
- [README.md](artifact/README.md) <br>
- [dual_strategy_selector.py](artifact/dual_strategy_selector.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, csv files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; runtime output is console text and an optional CSV file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided market data in the documented CSV schema; writes selection_YYYYMMDD.csv when matches are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
