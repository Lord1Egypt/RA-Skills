## Description: <br>
Backtest Free helps agents support finance strategy backtesting workflows with event-driven analysis, parameter optimization, risk-control scenarios, and structured result summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, finance analysts, and automation teams use this skill to ask an agent for backtesting setup, troubleshooting, and structured analysis of trading strategies, market predictions, trading signals, and risk controls. Outputs should be treated as informational analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad command execution through the exec tool and includes installation commands. <br>
Mitigation: Run commands only in a sandbox or least-privilege environment, avoid elevated privileges, and independently verify packages before installation. <br>
Risk: The skill can produce trading signals, market predictions, and investment-style recommendations. <br>
Mitigation: Treat outputs as informational analysis only and require qualified human review before making financial decisions. <br>
Risk: Security evidence flags vague security assurances despite no overt malicious finding. <br>
Mitigation: Review and scan the skill before deployment, and provide only data and commands that the operator intentionally approves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/backtest-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Project homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON examples and inline shell or Python commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured backtest summaries, troubleshooting steps, install commands, and investment-style analysis that requires human review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
