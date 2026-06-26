## Description: <br>
Autonomous quality engineering swarm that forges production-ready code through continuous behavioral verification, exhaustive E2E testing, and self-healing fix loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ikennaokpala](https://clawhub.ai/user/ikennaokpala) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use Forge to run autonomous behavioral verification, E2E testing, quality gates, and fix loops across application contexts. It is aimed at projects that can tolerate an agent running local builds, tests, migrations, API seeding, code edits, commits, and persistent learning state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run builds, tests, migrations, API seeding, code edits, commits, and persistent learning workflows with broad repository authority. <br>
Mitigation: Start in verify-only mode on a clean disposable branch or worktree, confirm configuration and discovered commands, and review all diffs, commits, logs, and memory state before enabling autonomous modes. <br>
Risk: The skill is designed to use real backend APIs and seeded data, which can affect real services if pointed at production systems. <br>
Mitigation: Use only local or disposable non-production services and data, and confirm backend URLs, credentials, migration commands, and seeding endpoints before execution. <br>
Risk: Server security evidence marks the release suspicious because approval boundaries are weak for autonomous fixing behavior. <br>
Mitigation: Treat generated fixes and commits as proposals until reviewed, and require human approval before merging or deploying resulting changes. <br>


## Reference(s): <br>
- [Forge ClawHub listing](https://clawhub.ai/ikennaokpala/forge) <br>
- [Publisher profile](https://clawhub.ai/user/ikennaokpala) <br>
- [Agentic QE](https://github.com/proffesor-for-testing/agentic-qe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, JSON, and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify project files, tests, specs, commits, logs, and local memory state when used in autonomous modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and changelog, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
