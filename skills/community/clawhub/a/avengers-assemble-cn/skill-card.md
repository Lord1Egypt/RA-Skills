## Description: <br>
A Chinese-language Avengers-themed multi-agent coordinator that assigns work to six specialized sub-agents through sessions_spawn with round-robin dispatch and sessionKey reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenXinBest](https://clawhub.ai/user/ChenXinBest) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to coordinate complex Chinese-language agent workflows by decomposing requests, assigning sub-tasks to role-specific sub-agents, and consolidating their results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates work to multiple sub-agents, which can increase the amount of code, file, or shell activity performed for a broad request. <br>
Mitigation: Use narrow task scopes, avoid sharing secrets, and require approval checkpoints before edits, shell commands, or production-impacting actions. <br>
Risk: The themed coordinator style may make delegation decisions feel more playful than operational. <br>
Mitigation: Review the task breakdown, selected sub-agent roles, and final consolidated result before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChenXinBest/avengers-assemble-cn) <br>
- [Publisher profile](https://clawhub.ai/user/ChenXinBest) <br>
- [Marvel Avengers homepage](https://marvel.com/avengers) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown text with delegated sub-agent results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates work through sessions_spawn delegation; spawned agents may produce task-specific artifacts depending on user scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
