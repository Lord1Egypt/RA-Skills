## Description: <br>
Wallet-based credit system for AI agents. Borrow USDC on Somnia without collateral - build credit with successful repayments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aroushanpurdue](https://clawhub.ai/user/aroushanpurdue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to integrate wallet-based USDC borrowing, repayment tracking, and credit-tier checks on Somnia Testnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead users or agents to grant persistent wallet permissions and perform financial blockchain transactions. <br>
Mitigation: Use only wallets and funds that can be risked, set short-lived low-limit permissions, and manually inspect every transaction before signing. <br>
Risk: Borrowing behavior depends on an API provider and contract addresses that users must trust. <br>
Mitigation: Verify the API provider, Somnia network, and contract addresses independently before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aroushanpurdue/ai-agent-lending) <br>
- [Agent docs](https://yoursite.com/agent) <br>
- [Website](https://yoursite.com) <br>
- [Leaderboard](https://yoursite.com/leaderboard) <br>
- [Somnia Shannon explorer](https://shannon-explorer.somnia.network) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, HTTP, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LENDING_API_URL and wallet review before signing transactions.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
