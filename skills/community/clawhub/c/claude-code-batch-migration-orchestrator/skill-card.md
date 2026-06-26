## Description: <br>
Use when the user wants a large, mechanical change split into many independent units and executed in parallel with isolated workers and PRs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan broad refactors, migrations, bulk renames, or repetitive codebase-wide edits as isolated work units with validation and mergeable outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel workers could touch overlapping files or tightly coupled code paths. <br>
Mitigation: Define isolated scopes before launching workers and avoid parallel execution when work units are tightly coupled. <br>
Risk: Generated patches or PRs may introduce incorrect behavior during broad migrations. <br>
Mitigation: Require each worker to run its verification recipe and review generated patches or PRs before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wimi321/claude-code-batch-migration-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/wimi321) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with plans, verification recipes, worker instructions, and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR, patch, branch, or worktree coordination details when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
