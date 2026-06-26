## Description: <br>
Agent Essentials helps agents discover missing capabilities before giving up and capture concise, approved lessons into durable memory or configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nathanshan](https://clawhub.ai/user/nathanshan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when a task suggests a reusable capability gap or when an important correction should be preserved as a small lesson. It guides skill discovery, user-confirmed installation or scaffolding, and careful routing of lessons into memory or durable agent files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory notes may capture sensitive personal, credential, or project-confidential details. <br>
Mitigation: Review proposed lesson content and avoid storing sensitive details in memory notes. <br>
Risk: Changes to AGENTS.md, TOOLS.md, SOUL.md, or USER.md can alter future agent behavior. <br>
Mitigation: Review proposed diffs and require approval before durable files are changed. <br>
Risk: Skill discovery or installation recommendations can introduce new third-party instructions. <br>
Mitigation: Confirm installs explicitly and review source and security scan results before deployment. <br>


## Reference(s): <br>
- [Agent Essentials on ClawHub](https://clawhub.ai/nathanshan/agent-essentials) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with short verdicts, candidate lists, lesson snippets, and proposed file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before installing skills, creating custom skills, or changing durable agent files.] <br>

## Skill Version(s): <br>
1.1.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
