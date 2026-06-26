## Description: <br>
Provides multi-agent orchestration with task decomposition, parallel execution, result aggregation, and self-improving workflows for complex coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[panb-kg](https://clawhub.ai/user/panb-kg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple coding agents for code review, test generation, documentation, CI/CD configuration, and complex task decomposition. It is intended for workflows where parallel execution, result aggregation, and recoverable working state are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security scan reports suspicious memory and session-state behavior because the skill may persist sensitive session or environment context without sufficient safeguards. <br>
Mitigation: Review memory and session-state behavior before installation, and add redaction, retention limits, and strict file-permission controls before storing tokens, secrets, private paths, or detailed internal reasoning. <br>
Risk: Generated CI/CD or PR-commenting workflows can cause real repository or deployment side effects if enabled directly. <br>
Mitigation: Treat generated automation as draft output and require human review before enabling repository comments, commits, deployments, or other side effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/panb-kg/dobby-harness) <br>
- [README](artifact/README.md) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [Harness architecture](artifact/HARNESS-ARCHITECTURE.md) <br>
- [Workflow guide](artifact/WORKFLOWS.md) <br>
- [Self-improvement system](artifact/SELF-IMPROVEMENT.md) <br>
- [Security audit](artifact/SECURITY-AUDIT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JavaScript code, JSON-like reports, configuration snippets, and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may propose repository changes or automation steps; generated CI/CD and PR-commenting workflows should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
