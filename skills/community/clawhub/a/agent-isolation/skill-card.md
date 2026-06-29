## Description: <br>
Agent Isolation provides boundary-rule templates and operating guidance for separating multiple AI agents' workspaces, memory, sessions, and explicit shared directories on a shared runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this prompt skill to add explicit workspace boundaries for multi-agent environments that share runtime infrastructure. It helps them define private agent workspaces, controlled shared directories, and user-directed exceptions for cross-agent actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example workspace paths or shared directories could be copied without matching the user's actual agent layout. <br>
Mitigation: Replace example paths with the real workspace and shared-directory paths before applying the rules. <br>
Risk: Overly strict boundary rules could block legitimate collaboration between agents. <br>
Mitigation: Review AGENT.md changes before use and keep explicit exception clauses for user-directed cross-agent work. <br>


## Reference(s): <br>
- [Server-resolved source import](https://github.com/Sheyuy/agent-skills/tree/main/skills/agent-isolation) <br>
- [Publisher homepage](https://www.botlearn.ai) <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/agent-isolation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with rule templates and step-by-step review instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only; produces operating rules and review guidance, not automatic actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
