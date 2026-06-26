## Description: <br>
Detects the MBTI personality type of an AI assistant and issues a lobster-themed NFT PFP certificate, with user-initiated, passive threshold-based, and silent per-reply signal collection modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joyboy-sats](https://clawhub.ai/user/joyboy-sats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to classify an AI assistant's MBTI-style personality from conversation history, reveal a themed profile, and optionally mint a Solana NFT certificate. It also manages local MBTI state, conversation summaries, wallet state, and minting status for the flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs silent per-reply personality signal collection and stores conversation-derived summaries locally. <br>
Mitigation: Use only after reviewing and accepting the background profiling behavior; prefer a version that asks before collecting history. <br>
Risk: The skill creates and stores a Solana private key on the local machine. <br>
Mitigation: Install only if local wallet generation is acceptable, protect ~/.mbti, and understand that losing the private key can make the wallet unrecoverable. <br>
Risk: The skill can submit MBTI evidence, model information, agent naming data, and wallet-related data to a remote mint service. <br>
Mitigation: Review the data sent before minting or reporting results, and use only if remote submission to the configured service is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joyboy-sats/clawm-dev) <br>
- [MBTI Personality Analysis Methodology](resources/analysis_guide.md) <br>
- [MBTI type resources](resources/mbti_types.json) <br>
- [PFP prompt resources](resources/pfp_prompts.json) <br>
- [PFP image endpoint](https://pub-statics.finchain.global/clawmbit-nft/{MBTI_TYPE}.webp) <br>
- [Wallet profile endpoint](https://clawmbti-dev.myfinchain.com/wallet/[address]) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON payload examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files under ~/.mbti, generate a Solana wallet key, and submit MBTI evidence and wallet-related data to a remote mint service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
