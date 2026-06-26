## Description: <br>
Orchestrates multi-agent teams with defined roles, task lifecycles, handoff protocols, review workflows, and shared artifact conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up sustained teams of two or more agents, route work through explicit lifecycle states, coordinate handoffs, and enforce review gates before shipping artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or other sensitive credentials could be exposed through prompts, shared folders, or agent handoff artifacts. <br>
Mitigation: Keep credentials out of prompts and shared directories, use environment variables or a secrets manager, and review artifacts before sharing them with additional agents. <br>
Risk: Shared workspaces can retain regulated or sensitive data beyond the intended task scope. <br>
Mitigation: Limit shared artifacts to necessary task context, avoid regulated data in shared folders, and clean or archive shared directories according to the team's data handling policy. <br>
Risk: Persistent agent instruction files can carry unsafe or stale operating rules into future tasks. <br>
Mitigation: Review role and instruction files before use, especially after handoffs, escalations, or changes to team composition. <br>
Risk: Scheduled agents can continue acting without clear oversight. <br>
Mitigation: Assign an owner for every scheduled agent, document its scope and stop procedure, and periodically review whether the schedule is still needed. <br>
Risk: Coordination guidance can produce incorrect process choices or missed quality gates if adopted without review. <br>
Mitigation: Require human or independent reviewer approval for consequential workflow changes and scan skill content before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abel-agent-team-orchestration) <br>
- [Publisher profile](https://clawhub.ai/user/abeltennyson) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Team Setup](references/team-setup.md) <br>
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown with templates, workflow checklists, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only playbook; no executable files are included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
