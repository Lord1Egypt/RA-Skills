## Description: <br>
Places GTC limit orders on both bid and ask sides of selected liquid Polymarket markets to attempt to capture bid/ask spread. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or review a configurable Polymarket market-making strategy that can dry-run, place live GTC limit orders, show positions, and adjust order-selection settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live prediction-market trades when run with --live. <br>
Mitigation: Run the default dry-run mode or set TRADING_VENUE=sim before enabling live trading. <br>
Risk: The skill can cancel existing open orders in the connected account before placing new orders. <br>
Mitigation: Use it only on an account where automated order cancellation is acceptable, or isolate it from manual and other-strategy open orders. <br>
Risk: The skill requires a trading API key. <br>
Mitigation: Use a least-privilege API key when available and avoid sharing the key across unrelated strategies. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/richducat/dolph-market-maker) <br>
- [Polymarket CLOB API endpoint](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Terminal text with optional JSON automaton report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; dry run is the default unless --live is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
