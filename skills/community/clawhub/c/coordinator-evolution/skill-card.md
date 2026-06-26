## Description: <br>
Advanced AI behavior framework that transitions from a simple assistant to a task coordinator, focusing on result synthesis and atomic task scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacurtwong](https://clawhub.ai/user/jacurtwong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to guide complex AI work through synthesized execution plans, atomic task scheduling, dynamic context gathering, and verification loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage persistent changes to startup, identity, or agent-instruction files. <br>
Mitigation: Review the exact edits before allowing changes to AGENTS.md, IDENTITY.md, BOOTSTRAP.md, or equivalent startup files, and keep a clear rollback path. <br>
Risk: Persistent behavior changes may make the skill higher priority in future sessions than intended. <br>
Mitigation: Use only the planning and verification guidance when persistence is not deliberately required, and avoid installing permanent loading instructions by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacurtwong/coordinator-evolution) <br>
- [Project homepage](https://github.com/jarmuine/coordinator-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with structured plans, checklists, and inline commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file paths, line references, task states, verification steps, and configuration-change guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
