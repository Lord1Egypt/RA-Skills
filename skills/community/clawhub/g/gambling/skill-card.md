## Description: <br>
Gambling helps agents use Agent Casino to register, check balances, place dice, coinflip, and roulette bets, verify bets, and withdraw cryptocurrency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollhub-dev](https://clawhub.ai/user/rollhub-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Agent Casino API workflows for real-money cryptocurrency gambling, including registration, deposits, betting, bet verification, balance checks, affiliate stats, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global, subject to applicable gambling and cryptocurrency laws. <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real-money crypto gambling and does not provide safeguards before deposits, bets, or withdrawals. <br>
Mitigation: Require explicit approval for every deposit, bet, and withdrawal, set strict loss limits, and use a limited wallet. <br>
Risk: Gambling and cryptocurrency transfers may be restricted or illegal for some users or jurisdictions. <br>
Mitigation: Confirm the user's eligibility and applicable local gambling and crypto-transfer laws before using the skill. <br>
Risk: The registration example includes a referral code. <br>
Mitigation: Review the registration payload and remove or replace any referral code before creating an account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/gambling) <br>
- [Agent Casino](https://agent.rollhub.com) <br>
- [Agent Casino API Base](https://agent.rollhub.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and API request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Agent Casino API key and explicit user approval for real-money crypto actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
