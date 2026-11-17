## Description:

Fund portfolio tracker with AI analysis, multi-agent debate, technical indicators, macro monitoring, and rebalancing alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tempest-01](https://clawhub.ai/user/tempest-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to track fund portfolios, fetch fund market data, run technical and AI-assisted analysis, compare correlations, monitor macro events, and generate rebalancing guidance. Outputs are for reference and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LLM analysis can transmit detailed fund holdings, transaction dates, prices, quantities, and notes to an external model provider.

Mitigation: Use a dedicated low-limit API key, keep sensitive notes out of positions.json, and review llm.py before running AI analysis.

Risk: This release may not honor expectations that LLM_API_BASE routes requests to a chosen third-party provider.

Mitigation: Do not configure a third-party LLM key expecting custom routing; confirm the actual LLM endpoint in llm.py before use.

Risk: Configured push, webhook, email, or bot endpoints can receive analysis output externally.

Mitigation: Configure only endpoints you control and avoid sending portfolio details to untrusted notification services.

Risk: A user-specified FUND_SCENE_DIR can cause the skill to read local Markdown scene templates.

Mitigation: Point FUND_SCENE_DIR only at a purpose-built directory and never at folders that may contain secrets or private documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tempest-01/skills/fund-ai-assistant)
- [Artifact metadata source](https://github.com/tempest-01/fund-ai-assistant)
- [astrbot_plugin_fund_analyzer](https://github.com/2529huang/astrbot_plugin_fund_analyzer)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with JSON-shaped LLM analysis, shell commands, configuration examples, and optional chart image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSON state files and PNG charts under the skill directory when analysis and chart commands are run.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
