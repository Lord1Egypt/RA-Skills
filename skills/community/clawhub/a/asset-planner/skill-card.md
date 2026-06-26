## Description: <br>
Asset Planner (规划虾) analyzes asset allocation screenshots and generates rebalancing strategies based on the All-Weather Portfolio and S&P Asset Quadrant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wltongxue](https://clawhub.ai/user/wltongxue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to consolidate personal asset screenshots, classify holdings, assess allocation health, and produce informational rebalancing guidance tailored to risk preference and new funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to share sensitive portfolio screenshots. <br>
Mitigation: Users should redact names, account numbers, QR codes, transaction details, and unrelated balances before uploading screenshots. <br>
Risk: The skill can name funds, trade amounts, and platform-specific buying steps. <br>
Mitigation: Treat named products and buy amounts as informational planning output and verify them independently before acting. <br>
Risk: The skill asks the agent to remember financial history without clear privacy limits. <br>
Mitigation: Only retain financial history when the user explicitly wants ongoing tracking, and avoid storing unrelated personal or account-identifying details. <br>


## Reference(s): <br>
- [AI 资产配置助手 底层知识库 & SOP](references/knowledge-base.md) <br>
- [ClawHub listing](https://clawhub.ai/wltongxue/asset-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style conversational guidance with asset summaries, health checks, and rebalancing steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses screenshots and user-provided risk preference as inputs; investment-related outputs are informational and include a disclaimer.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
