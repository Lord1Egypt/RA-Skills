## Description: <br>
Evaluates, improves, gates, and iterates on AI agent skills using structural scoring, LLM-assisted review, execution tests, Pareto regression checks, and trace-aware retry loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to score skill quality, generate and rank improvement candidates, run validation gates, apply or roll back accepted changes, and operate continuous improvement loops with bounded retries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify skill files and keep generated changes. <br>
Mitigation: Run it in a disposable repository or separate worktree and review diffs before retaining changes. <br>
Risk: The skill can run tests, LLM evaluations, and improvement loops that persist state. <br>
Mitigation: Use mock or dry-run modes where available and set explicit state directories plus cost and iteration limits. <br>
Risk: The skill can read session logs and send task context to LLM backends. <br>
Mitigation: Avoid sensitive skills and private session logs unless the data flow is understood and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/auto-improvement-orchestrator-skill) <br>
- [README](README.md) <br>
- [Evaluation report](EVALUATION_REPORT.md) <br>
- [Skill improvement pipeline article](docs/article-skill-improvement-pipeline.md) <br>
- [Improvement orchestrator architecture](skills/improvement-orchestrator/references/architecture.md) <br>
- [Improvement orchestrator guardrails](skills/improvement-orchestrator/references/guardrails.md) <br>
- [End-to-end demo](skills/improvement-orchestrator/references/end-to-end-demo.md) <br>
- [Task suite format](skills/improvement-evaluator/references/task-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON artifacts, and skill file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce evaluation scores, candidate rankings, gate receipts, state files, backups, and rollback guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
