## Description: <br>
Reads AI-C MD or CSV project plans, executes steps in dependency order, develops and tests changes, and reports progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sercanmetalore](https://clawhub.ai/user/sercanmetalore) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to execute AI-C project plans, create required files, apply implementation steps, run validation commands, and report Done or Blocked status for each step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad code, database, git, and path-specific changes with limited checkpoints. <br>
Mitigation: Install only in a trusted development repository, preferably on a disposable branch with backups, and review the plan and architecture files before allowing autopilot execution. <br>
Risk: Hard-coded AI-C paths and database settings may target unintended local resources. <br>
Mitigation: Confirm the paths are correct for the workspace and ensure database settings point only to local or disposable development databases before migrations or commits run. <br>
Risk: Autopilot behavior can stage files and create commits after completed steps. <br>
Mitigation: Review repository status regularly and keep secret values out of committed files, using only placeholder values in committed environment examples. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown step reports with file-change summaries, commands run, verification results, and Done or Blocked status; may also produce code and configuration file changes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can update progress state, create environment example files, run migrations or tests, and create git commits when operating in a repository.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
