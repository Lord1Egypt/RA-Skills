## Description: <br>
Elite Web3 airdrop strategist with S/A/B grading, scam shields, and guided hunting workflow for checking projects, verifying links, and finding zero-cost opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Web3 users and agents use this skill to evaluate airdrop opportunities, screen suspicious airdrop links, summarize daily opportunities, and find lower-cost participation paths. Its recommendations are advisory and should be reviewed before any wallet connection, signing action, or purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically analyze broad inputs such as URLs and project names, which may make advisory output feel like an instruction to act. <br>
Mitigation: Treat all findings as advisory, require user confirmation before visiting links or connecting a wallet, and review trigger behavior before deployment. <br>
Risk: The release is tagged for crypto, wallet-related workflows, and purchase-capable contexts. <br>
Mitigation: Do not connect a wallet, sign transactions, share private keys, or spend funds based only on the skill output; verify official channels independently. <br>
Risk: Security evidence notes under-disclosed local file handling. <br>
Mitigation: Inspect the artifact before installation, run it in a restricted workspace, and prefer a release that clearly documents local file reads and writes. <br>
Risk: Airdrop recommendations can become stale or rely on malformed or future-dated data. <br>
Mitigation: Check timestamps and official sources before acting, and reject malformed or future-dated data when current-only recommendations are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bevanding/antalpha-airdrop-hunter) <br>
- [Repository](https://github.com/AntalphaAI/airdrop-hunter) <br>
- [MCP Repository](https://github.com/antalpha-com/antalpha-skills) <br>
- [Grading System](references/grading-system.md) <br>
- [Scam Detection](references/scam-detection.md) <br>
- [Trusted Sources](references/trusted-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis, JSON] <br>
**Output Format:** [Markdown guidance rendered from structured tool JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses project grades, scam warnings, next-step options, and date-aware airdrop summaries; does not provide financial advice.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
