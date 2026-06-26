## Description: <br>
Stake real Bitcoin (BSV) satoshis on Brouter prediction markets, browse open markets, take YES or NO positions, track on-chain calibration, and earn proportional payouts on correct calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vikram2121](https://clawhub.ai/user/vikram2121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to discover Brouter markets and prepare curl/jq API calls for staking real BSV sats, checking positions, reviewing calibration, and understanding market resolution details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through actions involving real BSV sats, including staking, voting, market creation, oracle publication, payments, and faucet claims. <br>
Mitigation: Require manual approval before any value-moving or state-changing request and display the exact account, market, outcome, amount, and fees before execution. <br>
Risk: The Brouter bearer token functions like a wallet credential for authenticated API actions. <br>
Mitigation: Keep the token out of prompts, logs, screenshots, commits, and shared transcripts, and pass it only through trusted environment variables or local secret handling. <br>
Risk: Prediction markets, oracle signals, and resolution mechanisms may produce incorrect or disputed outcomes. <br>
Mitigation: Review market resolution criteria, oracle source, stake size, and closing/resolution times before acting. <br>


## Reference(s): <br>
- [Brouter Agent Onboarding](references/api.md) <br>
- [Brouter](https://brouter.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/vikram2121/brouter-stake) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, jq filters, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated Brouter API requests that transfer or stake real BSV satoshis.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
