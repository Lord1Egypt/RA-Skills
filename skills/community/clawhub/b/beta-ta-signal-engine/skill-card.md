## Description: <br>
Generate technical-analysis trade setups from OHLCV CSV using SMA/EMA/RSI/MACD/ATR with clear entry, stop, target, and position size. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading-research users use this skill to run a local OHLCV CSV through technical indicators and produce a risk-defined paper-trade setup. Outputs should be treated as analysis for planning, not financial advice or live-order instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated setup may be mistaken for financial advice or an instruction to place live orders. <br>
Mitigation: Frame outputs as technical analysis or paper-trade planning only, and require human review before any real trading decision. <br>
Risk: The bundled Python script reads user-selected local CSV files and calculations depend on the quality and sufficiency of that data. <br>
Mitigation: Run it only on CSV files the user intentionally provides, verify required OHLCV headers, and reject datasets with fewer than 60 rows. <br>


## Reference(s): <br>
- [Strategy Notes](references/strategy-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1477009639zw-blip/beta-ta-signal-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON or plain text, with agent-facing Markdown guidance when explaining results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes signal, confidence, entry, stop, target, position size, and reason; requires at least 60 OHLCV rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
