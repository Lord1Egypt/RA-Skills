## Description: <br>
Collaborative task checklist manager for AI agents with sequential, parallel, and looping execution. Features agent coordination, dependencies, deadlock prevention, and loop safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welliu](https://clawhub.ai/user/welliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to create, assign, track, and validate task checklists for multi-agent or multi-step workflows such as deployments, reviews, migrations, incident response, and onboarding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checklist entries may contain sensitive incident, deployment, migration, access, or notification details. <br>
Mitigation: Do not put secrets or sensitive incident details in checklist text, and review checklist contents before sharing or committing local state files. <br>
Risk: Dependency, deadlock, loop, and validation behavior has reliability caveats. <br>
Mitigation: Treat these checks as advisory, run validation or dry-run steps where available, and require human review before coordinating high-impact work. <br>
Risk: Checklist-driven workflows can influence production deployments, migrations, account access, or external communications. <br>
Mitigation: Require explicit human approval before acting on checklist items that affect production systems, user access, or external stakeholders. <br>


## Reference(s): <br>
- [ClawHub Checklist Skill](https://clawhub.ai/welliu/checklist) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-backed checklist state.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local checklist files under the user's home directory and bundled JSON templates; requires Bash and jq.] <br>

## Skill Version(s): <br>
1.2.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
