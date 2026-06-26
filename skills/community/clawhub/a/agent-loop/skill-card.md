## Description: <br>
Structured Read-to-Plan-to-Execute-to-Verify-to-Report protocol for tasks with side effects, intended to prevent false completion reports, blind retries, and scope creep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cycy2xxx](https://clawhub.ai/user/cycy2xxx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to guide local LLM agents through disciplined read, plan, execute, verify, and report phases for file edits, shell commands, multi-step operations, and irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through file edits, shell commands, multi-step operations, and irreversible actions. <br>
Mitigation: Review the skill files before granting credentials, filesystem access, background execution, or mutation authority, and keep normal execution approvals in place. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown procedural guidance with checklists, examples, and reporting structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs the agent to verify changes before reporting completion and to stop after repeated failed attempts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
