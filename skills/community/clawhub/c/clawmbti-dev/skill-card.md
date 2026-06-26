## Description: <br>
Detects the MBTI personality type of an AI assistant and issues a lobster-themed NFT PFP certificate, with active and passive triggers, local behavioral summary storage, local Solana wallet creation, and optional minting through the ClawMBTI API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joyboy-sats](https://clawhub.ai/user/joyboy-sats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to profile an AI assistant's own MBTI-style behavior, present a themed lobster PFP result, and optionally mint an NFT certificate tied to a locally managed Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background profiling can collect cross-session behavioral summaries without a just-in-time notice. <br>
Mitigation: Require explicit opt-in before background collection and provide a clear way to review and delete saved summaries under ~/.mbti. <br>
Risk: The skill can create and store a local Solana private key. <br>
Mitigation: Inform the user before wallet creation, document where the key is stored, keep owner-only permissions, and provide backup and deletion guidance. <br>
Risk: MBTI evidence and wallet information can be submitted to the ClawMBTI service. <br>
Mitigation: Ask for confirmation before each remote submission and show what categories of data will be sent. <br>
Risk: NFT minting and share-data requests can interact with a remote crypto service. <br>
Mitigation: Gate minting and share fetches behind explicit user consent and make network failures non-destructive to local results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joyboy-sats/clawmbti-dev) <br>
- [ClawMBTI wallet profile](https://clawmbti-dev.myfinchain.com/wallet/[address]) <br>
- [ClawMBTI NFT image CDN](https://pub-statics.finchain.global/clawmbti-nft/{MBTI_TYPE}.webp) <br>
- [MBTI analysis guide](resources/analysis_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversation output, JSON state files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores MBTI state, conversation summaries, wallet files, and NFT mint status under ~/.mbti.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
