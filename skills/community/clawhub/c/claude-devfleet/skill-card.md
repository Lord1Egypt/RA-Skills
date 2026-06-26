## Description: <br>
Claude DevFleet helps agents plan, dispatch, monitor, and report on parallel Claude coding missions in isolated git worktrees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gensandee-na](https://clawhub.ai/user/gensandee-na) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate multiple Claude Code agents across planned coding missions, monitor progress, and read structured completion reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous DevFleet missions can launch full-tool coding agents and automatically merge code changes. <br>
Mitigation: Use version-controlled, non-production repositories first; review mission plans, diffs, reports, and test results before allowing auto-dispatch or auto-merge. <br>
Risk: The skill depends on a local DevFleet MCP service that can direct agents to modify code. <br>
Mitigation: Install only when you trust the local DevFleet service and have explicit approval, rollback procedures, and appropriate repository access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gensandee-na/claude-devfleet) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and DevFleet tool call descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate local DevFleet missions that produce structured reports and code changes in isolated worktrees.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
