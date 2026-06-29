## Description: <br>
Helps agents write, validate, and troubleshoot recurring scheduled buy (DCA) strategies on Superior Trade that add to an open pair on calendar triggers rather than price triggers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-strategy authors use this skill to draft and review Freqtrade-based DCA strategies for weekly, daily, or monthly scheduled crypto buys on Superior Trade. It supports configuration choices, callback implementation, and troubleshooting common failures such as rejected repeat entries, double-buying, and stake sizing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated DCA trading guidance can lead to real financial loss when applied with live funds, especially with futures, margin, or cross-margin settings. <br>
Mitigation: Set a maximum total budget, dry-run or backtest before live use, define exit rules up front, and use extra caution with leveraged or margin trading. <br>
Risk: Incorrect stake sizing or missing position-adjustment settings can over-allocate funds, exhaust the wallet, or prevent scheduled buys from executing as intended. <br>
Mitigation: Review stake_amount, dry_run_wallet, max_dca_multiplier, max_entry_position_adjustment, and position_adjustment_enable before deployment. <br>
Risk: A missing same-day guard can cause an unintended double buy on the initial calendar trigger. <br>
Mitigation: Keep the adjust_trade_position guard that skips an add when the latest filled entry occurred on the current candle date. <br>


## Reference(s): <br>
- [Freqtrade adjust_trade_position documentation](https://www.freqtrade.io/en/stable/strategy-callbacks/#adjust-trade-position) <br>
- [Freqtrade DigDeeperStrategy reference](https://github.com/freqtrade/freqtrade/issues/7052) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Freqtrade strategy snippets, configuration fragments, checklists, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
