## Description: <br>
Elite Web3 airdrop strategist with S/A/B grading, scam shields, and guided hunting workflow; triggers when users ask about airdrops, want to check projects, verify links, or find zero-cost opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Web3 users and agents use Airdrop Hunter to scan airdrop opportunities, check project quality, verify suspicious URLs, and find zero-cost actions before interacting with wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A third-party MCP service may receive airdrop-related URLs, project names, and query context. <br>
Mitigation: Use the skill only for Web3 and airdrop tasks, and avoid pasting private invite links, wallet secrets, session tokens, or other sensitive context. <br>
Risk: The skill registers and persists service credentials for MCP access. <br>
Mitigation: Store the generated agent_id and api_key securely, limit who can access them, and confirm how they can be revoked or rotated before broad deployment. <br>
Risk: Automatic URL and project-name triggers can send broad user input to the MCP service. <br>
Mitigation: Review the input before invocation when it may contain private or unrelated information, and invoke the skill explicitly for airdrop safety checks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/deanpeng-dotcom/airdrop-hunter) <br>
- [Skill Repository](https://github.com/AntalphaAI/airdrop-hunter) <br>
- [MCP Server Repository](https://github.com/antalpha-com/antalpha-skills) <br>
- [MCP Endpoint](https://mcp-skills.ai.antalpha.com/mcp) <br>
- [Grading System](references/grading-system.md) <br>
- [Scam Detection](references/scam-detection.md) <br>
- [Trusted Sources](references/trusted-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown briefings with tables, warnings, numbered next-step options, and concise project assessments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP-backed airdrop data, scam warnings, S/A/B/C grades, and zero-cost opportunities; not financial advice.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
