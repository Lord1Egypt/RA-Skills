## Description: <br>
Professional cryptocurrency investment and strategy analysis for spot, swing, and leverage decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codeblackhole1024](https://clawhub.ai/user/codeblackhole1024) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill for practical crypto decision support, including spot investing, swing trading, leverage planning, portfolio allocation, asset comparison, and risk-controlled execution plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live market data requests disable TLS certificate and hostname verification, which can allow manipulated data to affect investment guidance. <br>
Mitigation: Restore TLS verification before relying on live-data fetches, and independently verify prices and market data before acting on the output. <br>
Risk: The skill can produce buy, sell, leverage, and allocation guidance that may be mistaken for guaranteed investment advice. <br>
Mitigation: Treat outputs as decision support only, review risk limits and assumptions, and avoid executing real trades without independent financial review. <br>
Risk: Snapshot logging can save investment notes and analysis history locally. <br>
Mitigation: Avoid logging sensitive investment notes, or review and protect local JSONL snapshot files before sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codeblackhole1024/crypto-investment-strategist) <br>
- [Publisher Profile](https://clawhub.ai/user/codeblackhole1024) <br>
- [Market Regimes](references/market-regimes.md) <br>
- [Position Planning](references/position-planning.md) <br>
- [Portfolio Construction](references/portfolio-construction.md) <br>
- [Risk Framework](references/risk-framework.md) <br>
- [Tokenomics Checklist](references/tokenomics-checklist.md) <br>
- [Asset Scoring](references/asset-scoring.md) <br>
- [Allocation Playbook](references/allocation-playbook.md) <br>
- [Review Workflow](references/review-workflow.md) <br>
- [Workflow Orchestration](references/workflow-orchestration.md) <br>
- [Numpy Migration Plan](references/numpy-migration-plan.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON-producing helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON or JSONL files when helper scripts are run with output or snapshot logging options.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
