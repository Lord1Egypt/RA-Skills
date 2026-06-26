## Description: <br>
Fund portfolio tracker with AI analysis, multi-agent debate, technical indicators (VaR/Sortino/Calmar), macro monitoring, and rebalancing alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tempest-01](https://clawhub.ai/user/tempest-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track fund portfolios, fetch market data, run technical and AI-assisted analysis, monitor macro events, and generate rebalancing or timing guidance. Outputs are for portfolio review and decision support, not a substitute for professional investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI features may send fund codes, holdings, costs, dates, notes, generated analysis, and macro context to the configured LLM provider. <br>
Mitigation: Use a dedicated low-quota API key and only configure an LLM endpoint you trust. <br>
Risk: Notification features may transmit analysis output to configured webhook, push, email, or bot endpoints. <br>
Mitigation: Configure only trusted endpoints and avoid untrusted webhook or push URLs. <br>
Risk: The skill can read local scene templates from FUND_SCENE_DIR. <br>
Mitigation: Do not point FUND_SCENE_DIR at sensitive folders or directories containing secrets. <br>
Risk: Portfolio position data can be overwritten or damaged during normal local use. <br>
Mitigation: Back up positions.json before operational use. <br>
Risk: Optional Python dependencies affect production supply-chain exposure. <br>
Mitigation: Pin and audit optional dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tempest-01/fund-ai-assistant) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [astrbot_plugin_fund_analyzer](https://github.com/2529huang/astrbot_plugin_fund_analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown, terminal text, JSON analysis payloads, generated chart files, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured LLM, market-data, macro-search, and notification endpoints; may read local position and scene-template files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
