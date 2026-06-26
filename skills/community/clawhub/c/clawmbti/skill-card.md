## Description: <br>
Detects the MBTI personality type of an AI assistant and issues a lobster-themed NFT PFP certificate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joyboy-sats](https://clawhub.ai/user/joyboy-sats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to analyze an assistant's MBTI-style personality signals, reveal a lobster-themed profile, and optionally mint a Solana NFT certificate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and stores a local Solana private key. <br>
Mitigation: Install only when a local wallet is acceptable, keep the key file protected, and remove ~/.mbti/wallet if the wallet should not be retained. <br>
Risk: The skill saves conversation-derived MBTI summaries across sessions. <br>
Mitigation: Review and clear ~/.mbti when retained personality summaries, MBTI results, or NFT status files are no longer wanted. <br>
Risk: The skill sends personality-analysis and wallet data to clawmbti.finchain.global for reporting, mint checks, minting, and share content. <br>
Mitigation: Use the skill only when remote submission to that service is acceptable, and review the mint step before confirming NFT creation. <br>
Risk: The skill installs Python dependencies through uv before running local scripts. <br>
Mitigation: Review pyproject.toml and run dependency installation in an environment where those packages are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joyboy-sats/clawmbti) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/joyboy-sats) <br>
- [MBTI analysis methodology](resources/analysis_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown user prompts and status messages, JSON state files, shell commands, and remote API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local files under ~/.mbti, including wallet, MBTI result, NFT status, and conversation-summary data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
