## Description: <br>
Interacts with the Bitpanda API to retrieve raw portfolio, trade, and price data without automatic aggregation, with pagination and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MattiaLaGreca](https://clawhub.ai/user/MattiaLaGreca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Bitpanda account wallets, trade history, and asset prices through the official API while keeping downstream calculations under their own control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve privacy-sensitive Bitpanda portfolio and trade data. <br>
Mitigation: Install only when that access is intended, and review requested commands before allowing the agent to fetch account data. <br>
Risk: A broad API key could allow more access than portfolio inspection requires. <br>
Mitigation: Use a dedicated read-only Bitpanda API key with the minimum required permissions, and avoid granting trading or withdrawal permissions. <br>
Risk: API keys or account outputs may be exposed through logs, backups, shared dotfiles, or shell history. <br>
Mitigation: Avoid permanent shell-profile storage on shared systems, prefer a local secrets mechanism or temporary environment variable, and keep generated outputs out of public logs. <br>


## Reference(s): <br>
- [Bitpanda Developer Portal](https://developers.bitpanda.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/MattiaLaGreca/bitpanda-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a Bitpanda API key supplied through the environment or command invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
