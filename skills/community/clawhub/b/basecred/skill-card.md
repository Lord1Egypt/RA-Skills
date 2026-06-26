## Description: <br>
Fetch onchain reputation profiles for 0x wallet addresses via the BaseCred SDK, including Ethos credibility, Talent Protocol builder and creator scores, optional Farcaster/Neynar quality, level derivation, and recency tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Callmedas69](https://clawhub.ai/user/Callmedas69) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query a wallet address and summarize onchain reputation signals from Ethos, Talent Protocol, and optionally Farcaster/Neynar. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses are queried through Ethos, Talent Protocol, and optionally Neynar. <br>
Mitigation: Install and run the skill only when those third-party service lookups are acceptable for the use case. <br>
Risk: The query script reads API keys from a workspace .env file. <br>
Mitigation: Use a dedicated workspace .env containing only TALENT_PROTOCOL_API_KEY and, when needed, NEYNAR_API_KEY. <br>
Risk: The skill depends on the locally installed basecred-sdk package. <br>
Mitigation: Pin or review the basecred-sdk version before use. <br>


## Reference(s): <br>
- [BaseCred Output Schema & Level Tables](references/output-schema.md) <br>
- [ClawHub BaseCred Skill Page](https://clawhub.ai/Callmedas69/basecred) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON profile output from the query script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a wallet address, basecred-sdk in the workspace, TALENT_PROTOCOL_API_KEY, and optionally NEYNAR_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
