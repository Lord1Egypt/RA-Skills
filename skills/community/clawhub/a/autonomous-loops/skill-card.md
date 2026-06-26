## Description: <br>
Autonomous Claude Code loop patterns: sequential pipelines, persistent REPL sessions, parallel spec-driven generation, PR automation, cleanup passes, and RFC-driven DAG orchestration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to choose and run autonomous Claude Code workflows for sequential implementation, persistent sessions, parallel generation, PR automation, cleanup passes, and DAG-based multi-unit work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous repository automation can create commits, open PRs, repair CI failures, and merge changes without enough review. <br>
Mitigation: Use protected branches, dry-run or --disable-commits first, explicit max-run, cost, and duration limits, and require manual approval before merges. <br>
Risk: Session files, shared task notes, specs, directory snapshots, and captured diffs can expose secrets or sensitive customer data. <br>
Mitigation: Keep private credentials and sensitive data out of automation context files and use least-privileged GitHub credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/djc00p/autonomous-loops) <br>
- [Sequential Pipeline](references/sequential-pipeline.md) <br>
- [Persistent REPL](references/persistent-repl.md) <br>
- [Parallel Agents](references/parallel-agents.md) <br>
- [PR Automation Loop](references/pr-automation.md) <br>
- [De-Sloppify Pattern](references/de-sloppify.md) <br>
- [DAG Orchestration](references/dag-orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, configuration examples, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository automation steps that require GitHub CLI, git, Node.js, and explicit run limits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
