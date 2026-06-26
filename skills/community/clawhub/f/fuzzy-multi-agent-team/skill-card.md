## Description: <br>
Fuzzy Multi Agent Team helps an agent spawn and coordinate multiple AI sub-agents to work in parallel on a complex task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decompose complex work into coordinated sub-agent workflows for research, content generation, code review, data processing, and decision councils, then collect and synthesize the results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide changes to agent configuration and persistent workspaces. <br>
Mitigation: Review configuration changes before applying them and use a dedicated workspace with limited access. <br>
Risk: Persistent or long-running agents can continue using context, permissions, and compute after the initial task. <br>
Mitigation: Use one-shot mode by default, set timeouts, and enable persistent automation only when it is explicitly needed. <br>
Risk: Broad Discord permissions can expose unnecessary collaboration surfaces when Discord integration is used. <br>
Mitigation: Grant only the permissions required for the intended workflow. <br>


## Reference(s): <br>
- [Multi-Agent Team Templates](references/team-templates.md) <br>
- [ClawHub release page](https://clawhub.ai/fuzzyb33s/fuzzy-multi-agent-team) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command examples and prompt templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces orchestration guidance, sub-agent prompts, session-management commands, and synthesis patterns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
