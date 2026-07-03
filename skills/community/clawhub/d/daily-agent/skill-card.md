## Description: <br>
Daily Agent routes each conversation by classifying tasks, estimating complexity, matching skills, delegating execution, and running completion checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Daily Agent as an always-on orchestration layer for routing user requests, choosing execution paths, matching specialized skills, and monitoring delegated work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on task routing can affect nearly every request and may route work to background agents, cron jobs, local scripts, or repository-changing workflows. <br>
Mitigation: Install only when this orchestration behavior is intended, review the routing rules before deployment, and require explicit confirmation for spawn, cron, communication, persistence, and repository mutation actions. <br>
Risk: The skill describes writing learning or memory files, extracting user profile facts, and committing selected repository directories. <br>
Mitigation: Review or disable the profile extraction and git commit sections, and inspect generated files and commits before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with decision tables and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes work by task type and complexity, with completion checks for browser state, learning records, memory updates, generated files, and selected repository changes.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release and SKILL.md frontmatter; package.json reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
