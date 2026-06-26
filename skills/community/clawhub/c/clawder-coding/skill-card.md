## Description: <br>
Production-grade AI coding agent for ZooClaw/OpenClaw following JT directives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyang1016](https://clawhub.ai/user/iyang1016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use Clawder as an autonomous coding agent for code analysis, refactoring, bug fixing, verification, and configuration work in ZooClaw/OpenClaw environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad coding-agent powers, including editing, deletion, sub-agent coordination, and persistent memory behavior. <br>
Mitigation: Run it in plan or approval mode and require explicit confirmation for deletions, pushes, dependency changes, and multi-file refactors. <br>
Risk: Automatic memory extraction may persist sensitive or unwanted project context. <br>
Mitigation: Disable memory extraction when not needed and review gotchas.md and auto-memory files before committing or sharing a workspace. <br>
Risk: Autonomous fixes and verification guidance can still produce incorrect or misleading changes. <br>
Mitigation: Inspect proposed diffs, run the project test suite, and review generated commands before relying on the result. <br>


## Reference(s): <br>
- [Clawder ClawHub Page](https://clawhub.ai/iyang1016/clawder-coding) <br>
- [Publisher Profile](https://clawhub.ai/user/iyang1016) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or perform file edits, command execution, sub-agent coordination, and memory updates depending on the hosting agent permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and agent-pack.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
