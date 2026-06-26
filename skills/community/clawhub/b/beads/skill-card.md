## Description: <br>
Git-backed issue tracker for AI agents. Use when managing tasks, dependencies, or multi-step work. Triggers on task tracking, issue management, dependency graphs, ready work queues, or mentions of "beads" / "bd" CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rnijhara](https://clawhub.ai/user/rnijhara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to manage repository-backed tasks, dependencies, issue status, and handoffs with the Beads CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create or update Beads issue files in a repository. <br>
Mitigation: Review planned Beads commands before execution and inspect repository changes before committing or syncing. <br>
Risk: Beads setup and sync commands can install git hooks and sync task data through Git. <br>
Mitigation: Review bd init, bd hooks install, and bd sync behavior before allowing an agent to run them. <br>
Risk: Issue content may be pushed to a remote repository during sync. <br>
Mitigation: Avoid putting secrets or private notes into Beads issues when the repository syncs to a remote. <br>


## Reference(s): <br>
- [Beads Task Tracker on ClawHub](https://clawhub.ai/rnijhara/beads) <br>
- [rnijhara publisher profile](https://clawhub.ai/user/rnijhara) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to prefer machine-readable Beads CLI output using --json where supported.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
