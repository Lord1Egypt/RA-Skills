## Description: <br>
Helps agents draft a Superior Trade breakout strategy with reference code, configuration, tuning guidance, and explicit regime-sensitivity warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading strategy developers use this skill to write or adapt a swing and intraday breakout strategy for Superior Trade, including backtest context, configuration, and tuning options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial strategy guidance can be mistaken for a profit guarantee or used without adequate testing. <br>
Mitigation: Treat the output as strategy guidance, then backtest or dry-run it before connecting any real trading account. <br>
Risk: Incorrect exchange, margin, stake, stoploss, or pair settings can create unintended financial exposure. <br>
Mitigation: Review exchange, margin, stake, stoploss, and pair settings carefully before deployment. <br>
Risk: The breakout template is regime sensitive and long-only breakouts may lose money in downtrends. <br>
Mitigation: Use regime filters or multi-pair scans where appropriate, and evaluate performance against current market conditions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/breakout) <br>
- [Freqtrade trailing stop documentation](https://www.freqtrade.io/en/stable/stoploss/#trailing-stop-loss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces strategy guidance for review; does not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
