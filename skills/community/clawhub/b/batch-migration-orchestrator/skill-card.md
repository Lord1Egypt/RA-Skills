## Description: <br>
Splits large mechanical codebase migrations into independent work units with validation steps, parallel execution boundaries, and mergeable outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wimi321](https://clawhub.ai/user/wimi321) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan broad refactors, migrations, bulk renames, or repetitive codebase-wide edits as isolated units with clear verification and PR or patch rollup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Large migrations can produce overlapping edits or unreviewed generated changes when scope boundaries are imprecise. <br>
Mitigation: Use precise migration boundaries, isolated branches or worktrees, explicit validation commands, and review generated patches or PRs before merging. <br>
Risk: Parallelizing tightly coupled work can create conflicting or incomplete changes. <br>
Mitigation: Only launch parallel workers when their write scopes do not overlap and require each unit to validate its own changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown plans, worker prompts, status summaries, and PR or patch rollups.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable payload; outputs are planning and coordination guidance for an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
