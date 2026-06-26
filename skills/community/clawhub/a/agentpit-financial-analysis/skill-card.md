## Description: <br>
多维度股票综合分析，整合三个专业AI分析系统：日交易技术面分析、TradingAgents多智能体分析、AI对冲基金大师视角。当用户提到分析股票、买不买某股票、股票行情时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshijie24](https://clawhub.ai/user/wangshijie24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request Chinese-language stock analysis through AgentPit. The agent confirms a ticker, obtains or reuses an AgentPit consumerKey, asks which paid analysis systems to run, and summarizes technical, multi-agent, or valuation-oriented results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an AgentPit consumerKey locally for reuse. <br>
Mitigation: Use the documented 600 file permission, avoid sharing the key in conversation logs, and delete ~/.openclaw/secrets/agentpit.cpk plus unset AGENTPIT_CPK to revoke local access. <br>
Risk: Selected analysis calls are paid remote AgentPit API calls. <br>
Mitigation: Confirm the requested analysis systems before calling, watch for insufficient-balance errors, and review AgentPit billing history after use. <br>
Risk: Stock analysis may be incomplete or unsuitable as investment advice. <br>
Mitigation: Present results as reference material, preserve the skill's non-investment-advice warning, and encourage the user to review assumptions before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshijie24/agentpit-financial-analysis) <br>
- [AgentPit](https://agentpit.io) <br>
- [AgentPit settings](https://agentpit.io/settings) <br>
- [AgentPit billing](https://agentpit.io/my/billing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown conversational guidance with optional bash and JSON API-call snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AgentPit consumerKey and can trigger paid remote stock-analysis calls selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
