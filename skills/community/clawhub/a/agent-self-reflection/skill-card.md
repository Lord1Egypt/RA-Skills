## Description: <br>
Periodically analyzes recent sessions to identify what went well or wrong and writes concise, actionable insights to the appropriate workspace files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BrennerSpear](https://clawhub.ai/user/BrennerSpear) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and operators use this skill to review recent OpenClaw session history, extract new and actionable lessons, and route those lessons into durable memory, tool notes, or skill instruction files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent conversation logs, which may contain sensitive user, project, or operational information. <br>
Mitigation: Install only where session-log review is intended, keep reads bounded to recent transcript tails, and restrict readable session paths. <br>
Risk: The skill can make lasting changes to memory files, tool notes, and skill instructions, which could preserve incorrect or poisoned guidance. <br>
Mitigation: Require review of proposed diffs before persistence, avoid direct edits to skill definitions unless explicitly approved, and audit saved reflections for sensitive or misleading content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BrennerSpear/agent-self-reflection) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with optional shell commands and file-edit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed to produce a brief 2-4 sentence reflection summary after bounded session review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
