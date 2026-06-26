## Description: <br>
Runs a full skill-improvement pipeline from generation through scoring, evaluation, execution, and gate review, with retries after failures and support for improving multiple skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent to coordinate end-to-end improvement runs for one or more skills, including candidate generation, reviewer scoring, optional task evaluation, controlled execution, and gate decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can modify a user-selected skill and write persistent state files. <br>
Mitigation: Run it first on a copied or backed-up target and use a disposable state directory until the proposed changes and generated artifacts have been reviewed. <br>
Risk: The orchestrator delegates authority to generator, discriminator, evaluator, executor, and gate skills. <br>
Mitigation: Review the subordinate skills before use and prefer --eval-mock for initial or CI-oriented runs. <br>
Risk: Automated proposals may introduce incorrect or misleading skill guidance. <br>
Mitigation: Review generated candidates, diffs, gate receipts, and pipeline-summary.json before promoting changes to a canonical skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/auto-improvement-orchestrator) <br>
- [Publisher Profile](https://clawhub.ai/user/lanyasheng) <br>
- [Architecture](references/architecture.md) <br>
- [Guardrails](references/guardrails.md) <br>
- [Phases](references/phases.md) <br>
- [Adapters](references/adapters.md) <br>
- [Skill Evaluator Adapter](references/skill-evaluator-adapter.md) <br>
- [End-to-End Demo](references/end-to-end-demo.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and machine-readable JSON artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes pipeline state, traces, summaries, rankings, execution records, receipts, backups, and a pipeline-summary.json file under the selected state root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
