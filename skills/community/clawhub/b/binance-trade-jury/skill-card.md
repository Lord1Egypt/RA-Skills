## Description: <br>
Use this skill when the user wants to put a Binance trade thesis on trial, review whether a long or short idea deserves risk, get an APPROVE / REVIEW / REJECT verdict, inspect the three juror opinions, receive an execution playbook, or generate a Binance Trade Jury share card link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a Binance trade idea for a verdict, juror-style review, and execution playbook before deciding whether to take risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's trade thesis, symbol, side, and optional bankroll amount to an external API. <br>
Mitigation: Do not include API keys, account identifiers, private balances, or sensitive portfolio details in the trade thesis. <br>
Risk: The returned verdict and playbook could be mistaken for trading advice. <br>
Mitigation: Treat the verdict as informational and review it independently before making any trade decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richard7463/binance-trade-jury) <br>
- [Review API endpoint](https://binance-trade-jury.vercel.app/api/trade-jury) <br>
- [Share image endpoint](https://binance-trade-jury.vercel.app/api/trade-jury/share-image) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline verdict, juror opinions, execution guidance, and optional share-card URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may call an external API with the trade symbol, side, thesis, and optional bankroll amount.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
